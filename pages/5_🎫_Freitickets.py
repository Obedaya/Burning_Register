import streamlit as st
from utilities import database as db, modules as mod

mod.create_movie_selection()

# Center the button using Streamlit's layout features
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    if st.button('Freiticket', type="primary"):
        plist = []
        plist.append({
                        "name": "Freiticket",
                        "amount": 1,
                        "price": 0,
                        "category": "Tickets"
                    })
        db.checkout(plist, False, 0, st.session_state["movie"])
        st.success("Freiticket erfolgreich eingelöst")

# Add CSS to make the button appear larger
st.markdown("""
    <style>
        .stButton button {
            font-size: 24px;
            padding: 12px 24px;
            width: 300px;
            height: 300px;
        }
    </style>
""", unsafe_allow_html=True)