import streamlit as st
from utilities import database as db, modules as mod
import pandas as pd

categories = db.group_by("inventory", "category")
products = list(db.find_all("inventory"))
sorted_list = sorted(categories, key=lambda x: x['_id'])

def clear_products():
    st.session_state["isteam"] = False
    for product in products:
        st.session_state.setdefault("cart", {})
        st.session_state["cart"][product["name"]] = 0
    st.session_state["init"] = True


def cart_menu():
    with st.sidebar:
        st.markdown("## Selected Products")
        plist = []
        for product in products:
            if st.session_state["cart"][product["name"]] > 0:
                plist.append({
                    "name": product["name"],
                    "amount": st.session_state["cart"][product["name"]],
                    "price": product["price"] if not st.session_state["isteam"] else product["price_team"],
                    "category": product["category"]
                })
        for product in plist:
            col = st.columns([2,1,1])
            col[0].markdown(f'{product["name"]}')
            col[1].markdown(f'{product["amount"]}')
            col[2].markdown('{:.2f}€'.format(product["price"] * product["amount"]))
        
        st.divider()
        col1, col2 = st.columns(2)

        checkout_button = col1.button("Checkout")
        if col2.button("Clear all", type="primary"):
            clear_products()
            st.experimental_rerun()

        total = 0
        for product in plist:
            total += product["price"] * product["amount"]
        st.markdown(f'Total: **{total:.2f}€**')
        with st.expander("Additional Options"):
            st.session_state["isteam"] = st.checkbox("Is a Team Member", value=st.session_state["isteam"])
        
        if checkout_button:
            if len(plist) != 0:
                db.checkout(plist, st.session_state["isteam"], total, st.session_state["movie"])
                clear_products()
                plist = []
                st.experimental_rerun()
            else:
                st.sidebar.error("Cart is empty")


def add_to_cart(item):
    st.session_state["cart"][item] += 1

def remove_from_cart(item):
    if st.session_state["cart"][item] > 0:
        st.session_state["cart"][item] -= 1

def create_register():
    for doc in sorted_list:
        st.markdown(f'## {doc["_id"]}')
        for item in doc["items"]:
            col1, col2 = st.columns(2)
            col1.button(item["name"], on_click=add_to_cart, args=(item["name"],), key=item["name"])
            col2.button(f'Remove {item["name"]}', on_click=remove_from_cart, args=(item["name"],), key=f'{item["name"]}_del', type="primary")


if "init" not in st.session_state:
    clear_products()
mod.create_movie_selection()
create_register()
cart_menu()