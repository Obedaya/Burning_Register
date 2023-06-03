import streamlit as st
from utilities import database as db


def add_product():
    st.subheader("Add New Product")
    with st.form(key="add_product_form"):
        name = st.text_input("Name")
        amount = st.number_input("Amount", min_value=0)
        price = st.number_input("Price", min_value=0.0)
        price_team = st.number_input("Price (Team)", min_value=0.0)
        amount_sold = st.number_input("Amount Sold", min_value=0)

        submit = st.form_submit_button("Add Product")
        if submit:
            print('Button pressed')
            product = {
                "name": name,
                "amount": amount,
                "price": price,
                "price_team": price_team,
                "amount_sold": amount_sold
            }
            print(str(product))
            st.success(f"Product '{name}' added successfully.")


def show_inventory():
    st.subheader("Inventory")

    # Get the latest list of products
    products = list(db.db.inventory.find())

    for product in products:
        st.write(product["name"])

        # Add remove button
        remove_button = st.button(f"Remove {product['name']}")
        if remove_button:
            db.remove('inventory', product)

        # Add edit button
        edit_button = st.button(f"Edit {product['name']}")
        if edit_button:
            db.edit('inventory', product)

    # Add button to add a new product
    add_button = st.button("Add New Product")
    if add_button:
        add_product()

    # Add refresh button
    refresh_button = st.button("Refresh")
    if refresh_button:
        st.experimental_rerun()


show_inventory()
