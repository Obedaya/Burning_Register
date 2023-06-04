import streamlit as st
from utilities import database as db, modules as mod
import datetime
import pymongo
import os
from dotenv import load_dotenv

load_dotenv()

adminusers = list(os.getenv("ADMINUSERS").split(","))

if "add_movie" not in st.session_state:
    st.session_state["add_movie"] = False

def menu():
    col = st.columns(1)
    # Add button to add a new movie
    add_button = col[0].button("Add New Movie", type="primary")
    if add_button:
        st.session_state["add_movie"] = True

def add_movie():
    # Create a form for input fields
    with st.form("Movie Form"):
        st.subheader("Add New Movie")
        # Add input fields for movie details
        name = st.text_input("Name")
        date = st.date_input("Date")
        time = st.time_input("Time")
        room = st.text_input("Room")

        # Add a submit button within the form
        col = st.columns(2)

        submitted = col[0].form_submit_button("Submit")
        if col[1].form_submit_button("Cancel"):
            st.session_state["add_movie"] = False
            st.experimental_rerun()
    

    # Check if form is submitted and insert movie into the database
    if submitted and isinstance(date, datetime.date):
        print(type(date))
        # Create a movie object from the submitted data
        movie = {
            "name": name,
            "datetime": datetime.datetime.combine(date, time), 
            "room": room,
        }
        print(str(movie))
        # Call the insert function to add the movie to the database
        db.insert("movies", movie)
        # Show a success message
        st.success("Movie added successfully!")

        # Reset the button state
        st.session_state.add_movie = False
        refresh_button = st.button("Refresh")
        if refresh_button:
            st.experimental_rerun()


def history_cancellation():
    st.subheader("Cancellations")
    mod.create_movie_selection()
    histlist = []
    for hist in list(db.find_all("history", query={"movie": st.session_state["movie"], "cancellation": {"$ne": True}}).sort("timestamp", pymongo.DESCENDING)):
        time= hist["timestamp"].strftime("%d.%m.%Y %H:%M:%S")
        histlist.append({"time": time, "total": hist["total"], "products": hist["products"], "timestamp": hist["timestamp"]})
    selection = st.selectbox("Select movie", options=histlist)
    if st.button("Cancel") and selection is not None:
        db.edit_by_query("history", {"timestamp": selection["timestamp"]}, {"cancellation": True})

def movielist():
    st.subheader("Movies")
    for movie in list(db.find_all("movies")):
        col = st.columns(3)
        col[0].write(movie["name"])
        col[1].write(movie["datetime"].strftime("%d.%m.%Y %H:%M:%S"))
        col[2].write(movie["room"])

def init_content():
    if st.session_state["username"] in adminusers:
        menu()
        prod_postion = st.empty()
        if st.session_state["add_movie"]:
            with prod_postion:
                add_movie()

        history_cancellation()
        movielist()
    else:
        st.error("You are not authorized to view this page.")
    
mod.auth_module(init_content, "admin")
