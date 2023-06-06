import streamlit as st
from utilities import database as db, modules as mod
import pandas as pd
import os


def total_sold_in_movie():
    orders = list(db.find_all("history", {"movie": st.session_state["movie"], "cancellation": {"$ne": True}}))
    total_sold = 0
    for order in orders:
        total_sold += order["total"]
    return total_sold

def total_sold_in_movie_guests():
    orders = list(db.find_all("history", {"movie": st.session_state["movie"], "cancellation": {"$ne": True}}))
    total_sold = 0
    for order in orders:
        if not order["isteam"]:
            total_sold += order["total"]
    return total_sold

def total_sold_in_movie_team():
    orders = list(db.find_all("history", {"movie": st.session_state["movie"], "cancellation": {"$ne": True}}))
    total_sold = 0
    for order in orders:
        if order["isteam"]:
            total_sold += order["total"]
    return total_sold

def amount_sold_in_movie():
    orders = list(db.find_all("history", {"movie": st.session_state["movie"], "cancellation": {"$ne": True}}))
    products = list(db.find_all("inventory"))
    amount_sold = {}
    for product in products:
        amount_sold[product["name"]] = 0

    for order in orders:
        for product in order["products"]:
            amount_sold[product["name"]] += product["amount"]
    print(amount_sold)
    return amount_sold

def tickets_sold_in_movie():
    return amount_sold_in_movie()["Ticket"]

def clubcard_sold_in_movie():
    return amount_sold_in_movie()["Clubkarte"]





def movie_report_excel():
    #Sales Sheet
    saleslist = []
    amsold =amount_sold_in_movie()
    for product in amsold:
        saleslist.append({
            "Name": product,
            "Amount": amsold[product],
            "Price": list(db.find_all("inventory", {"name": product}))[0]["price"],
            "Total": amsold[product] * list(db.find_all("inventory", {"name": product}))[0]["price"]
        })
    sales = pd.DataFrame(saleslist)
    #Total Sold Summary Sheet
    total_sold_list = {
        "Movie": st.session_state["movie"],
        "Total Sold": total_sold_in_movie(),
        "Total Sold to Guests": total_sold_in_movie_guests(),
        "Total Sold to Team": total_sold_in_movie_team(),
        "Total Tickets Sold": tickets_sold_in_movie(),
        "Total Clubcards Sold": clubcard_sold_in_movie()
    }
    total_sold = pd.DataFrame(total_sold_list, index=[0])



    if not os.path.exists("reports"):
        os.makedirs("reports")
    
    writer = pd.ExcelWriter(f"reports/{st.session_state['movie']}.xlsx", engine='xlsxwriter')
    sales.to_excel(writer, sheet_name='Sales', index=False)
    total_sold.to_excel(writer, sheet_name='Total Sold', index=False)
    writer.close()
    col = st.columns(2)
    with col[0]:
        st.dataframe(sales)
    with col[1]:
        st.dataframe(total_sold.transpose())

    st.download_button(
        label="Download Excel Report",
        data=open(f"reports/{st.session_state['movie']}.xlsx", "rb").read(),
        file_name=f"{st.session_state['movie']}.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

def total_report():
    st.subheader(f"Total sold in {st.session_state['movie']}:")
    st.markdown(f"Total sold in {st.session_state['movie']}: **{total_sold_in_movie():.2f}€**")
    st.markdown(f"Total sold in {st.session_state['movie']} to guests: **{total_sold_in_movie_guests():.2f}€**")
    st.markdown(f"Total sold in {st.session_state['movie']} to team: **{total_sold_in_movie_team():.2f}€**")
    st.markdown(f"Total tickets sold in {st.session_state['movie']}: **{tickets_sold_in_movie()}**")
    st.markdown(f"Total clubcards sold in {st.session_state['movie']}: **{clubcard_sold_in_movie()}**")

def product_report():
    st.subheader(f"Amount sold per product in {st.session_state['movie']}:")
    st.dataframe(pd.DataFrame(amount_sold_in_movie(), index=[0]))

def init_pages():
    mod.create_movie_selection()
    if len(st.session_state["movie"]) > 0:
        tab = st.tabs(["Total", "Products", "Excel Report"])
        with tab[0]:
            total_report()
        with tab[1]:
            product_report()
        with tab[2]:
            movie_report_excel()
    else:
        st.warning("Please create a movie first.")

init_pages()
