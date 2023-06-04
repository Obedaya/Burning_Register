import streamlit as st
from utilities import database as db, modules as mod
import pandas as pd
import json

CATEGORIES = ["Drinks", "Snacks", "Sweets", "Merchandise", "Tickets", "Other"]

if "add_product" not in st.session_state:
    st.session_state["add_product"] = False

def menu():
    col = st.columns(1)
    # Add button to add a new product
    add_button = col[0].button("Add New Product")
    if add_button:
        st.session_state["add_product"] = True


def add_product():
    # Create a form for input fields
    with st.form("Product Form"):
        st.subheader("Add New Product")
        # Add input fields for product details
        name = st.text_input("Name")
        amount = st.number_input("Amount", min_value=0)
        price = st.number_input("Price", min_value=0.0)
        price_team = st.number_input("Price (Team)", min_value=0.0)
        amount_sold = st.number_input("Amount Sold", min_value=0)
        category = st.selectbox("Category", options=CATEGORIES)

        # Add a submit button within the form
        col = st.columns(2)

        submitted = col[0].form_submit_button("Submit")
        if col[1].form_submit_button("Cancel"):
            st.session_state["add_product"] = False
            st.experimental_rerun()
    

    # Check if form is submitted and insert product into the database
    if submitted:
        # Create a product object from the submitted data
        product = {
            "name": name,
            "amount": amount,
            "price": price,
            "price_team": price_team,
            "amount_sold": amount_sold,
            "category": category
        }
        print(str(product))
        # Call the insert function to add the product to the database
        db.insert("inventory", product)
        # Show a success message
        st.success("Product added successfully!")

        # Reset the button state
        st.session_state.add_product = False
        # Add refresh button
        refresh_button = st.button("Refresh")
        if refresh_button:
            st.experimental_rerun()


def update_product(products, edited_products):
    if edited_products is not None:
            for index, row in products.iterrows():
                if  not row.equals(edited_products.iloc[index]):
                    # create a dict which only includes the changed values
                    changed_values = {}
                    for column in edited_products.columns.tolist():
                        if not row[column] == edited_products.iloc[index][column] and not pd.isna(edited_products.iloc[index][column]):
                            changed_values[column] = edited_products.iloc[index][column]
                    # update the product in the database
                    db.edit_by_id("inventory", row["_id"], changed_values)
                    print(f'Updated {str(changed_values)}')

def delete_product(edited_products, products):
    hasdeleted = False
    if edited_products is not None:
        for index, row in edited_products.iterrows():
            if pd.isna(row["name"]):
                db.delete("inventory", row["_id"])
                print(f'Deleted {products.iloc[index]["name"]}')
                hasdeleted = True
    return hasdeleted


def show_inventory():
    st.subheader("Inventory")
    st.info("Delete a product by removing the name and saving the changes. You can update or delete but not at the same time.")

    cleaned_products = []
    for pr in list(db.find_all("inventory")):
        pr["_id"] = str(pr["_id"])
        cleaned_products.append(pr)
    products = pd.DataFrame(cleaned_products)

    column_config = {}
    for column in products.columns.tolist():
        if column == "_id":
            column_config[column] = None
        elif "price" in column:
            column_config[column] = st.column_config.NumberColumn(column, format="%.2f €")
        elif "category" in column:
            column_config[column] = st.column_config.SelectboxColumn(column, options=CATEGORIES)
        else:
            column_config[column] = column

    edited_products = st.data_editor(products, column_config=column_config, hide_index=True)
    
    if st.button("Save Changes"):
        if not delete_product(edited_products, products):
            update_product(products, edited_products)
        st.experimental_rerun()
        


def init_content():
    menu()
    prod_postion = st.empty()
    show_inventory()
    if st.session_state["add_product"]:
        with prod_postion:
            add_product()

mod.auth_module(init_content, "inventory")