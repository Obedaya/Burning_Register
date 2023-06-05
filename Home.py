import streamlit as st
import logging
from utilities import database as db, modules as mod
from streamlit.web.server.websocket_headers import _get_websocket_headers

log = logging.getLogger(__name__)

# -------------- Settings ----------------
page_title = "Burning Cinema Register"
page_icon = "🎥"

# ----------------------------------------

st.set_page_config(page_title=page_title, page_icon=page_icon, layout="centered", initial_sidebar_state="auto")

st.header("Burning Register")
