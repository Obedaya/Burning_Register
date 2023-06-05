import streamlit as st
from utilities import database as db


def movielist_names():
    movies = [x["name"] for x in list(db.find_all("movies"))]
    return movies

def create_movie_selection():
    movies = movielist_names()
    if "movie" not in st.session_state:
        if len(movies) == 0:
            st.session_state["movie"] = []
        else:
            st.session_state["movie"] = movies[0]
            st.session_state["movie"] = st.selectbox("Select movie", options=movies, index= 0 if "movie" not in st.session_state else movies.index(st.session_state["movie"]))

