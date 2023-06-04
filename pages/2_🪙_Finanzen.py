import streamlit as st
from utilities import database as db, modules as mod
import pandas as pd


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
    mod.create_movie_selection()
    st.markdown(f"Total sold in {st.session_state['movie']}: **{total_sold_in_movie():.2f}€**")
    datalist = []
    amsold =amount_sold_in_movie()
    for product in amsold:
        datalist.append({
            "Name": product,
            "Amount": amsold[product],
            "Price": list(db.find_all("inventory", {"name": product}))[0]["price"],
            "Total": amsold[product] * list(db.find_all("inventory", {"name": product}))[0]["price"]
        })
    sales = pd.DataFrame(datalist)
    writer = pd.ExcelWriter(f"reports/{st.session_state['movie']}.xlsx", engine='xlsxwriter')
    sales.to_excel(writer, sheet_name='All Sales', index=False)
    writer.close()
    st.dataframe(sales)
    st.download_button(
        label="Download Excel Report",
        data=open(f"reports/{st.session_state['movie']}.xlsx", "rb").read(),
        file_name=f"{st.session_state['movie']}.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

def init_content():
    movie_report_excel()

mod.auth_module(init_content, "finances")

