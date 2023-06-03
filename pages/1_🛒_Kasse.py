import streamlit as st


def create_section(title, products, prices, session_state):
    if title not in session_state:
        session_state[title] = {}

    for product, price in zip(products, prices):
        if product not in session_state[title]:
            session_state[title][product] = {'count': 0, 'price': price}

        if st.button(product):
            session_state[title][product]['count'] += 1
            st.experimental_rerun()


def create_cash_register(drinks, snacks, drinks_prices, snacks_prices):
    session_state = st.session_state

    for section, section_products, section_prices in zip(["Drinks", "Snacks"], [drinks, snacks], [drinks_prices, snacks_prices]):
        st.markdown(f"## {section}")
        create_section(section.lower(), section_products, section_prices, session_state)

    with st.sidebar:
        st.markdown("## Selected Products")
        selected_products = {}

        for section in ["drinks", "snacks"]:
            selected_products.update(session_state.get(section, {}))

        selected_products = {product: data for product, data in selected_products.items() if data['count'] > 0}

        total_price = 0

        for product, data in selected_products.items():
            count = data['count']
            price = data['price']
            total_product_price = count * price
            total_price += total_product_price
            st.write(f"- {product} (Count: {count}, Price: {price}, Total: {round(total_product_price)})")
            remove_button = st.button(f"Remove {product}")
            if remove_button:
                for section in ["drinks", "snacks"]:
                    if product in session_state.get(section, {}):
                        session_state[section][product]['count'] = 0
                st.experimental_rerun()

        col1, col2 = st.columns(2)

        sum_button = col1.button("Sum")
        clear_button = col2.button("Clear all", type="primary")

        if clear_button:
            for section in ["drinks", "snacks"]:
                for product in session_state.get(section, {}):
                    session_state[section][product]['count'] = 0
            st.experimental_rerun()

        if sum_button:
            for section in ["drinks", "snacks"]:
                for product in session_state.get(section, {}):
                    session_state[section][product]['count'] = 0
            st.experimental_rerun()

        st.write(f"Total Price: {round(total_price, 2)}")


movies = ['Babydriver', 'Contra', 'Mad Max']
drinks = ['Bier', 'Almdudler', 'Wasser', 'Cola']
snacks = ['Nachos', 'Popcorn']
drinks_prices = [1.99, 2.49, 1.5, 2.5]
snacks_prices = [0.99, 1.99]

drink_counts = [0] * len(drinks)

option = st.selectbox(
        'Select movie',
        movies)

for i in movies:
    if option == i:
        # Select different source
        p = None

create_cash_register(drinks, snacks, drinks_prices, snacks_prices)
