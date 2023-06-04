import streamlit as st
import logging
from utilities import database as db, modules as mod
import extra_streamlit_components as stx
import datetime
log = logging.getLogger(__name__)

# -------------- Settings ----------------
page_title = "Burning Cinema Register"
page_icon = "🎥"

# ----------------------------------------
print(f"Logging Level: {logging.getLevelName(log.getEffectiveLevel())}")

st.set_page_config(page_title=page_title, page_icon=page_icon, layout="centered", initial_sidebar_state="auto")

def init_content():
    st.header("Burning Register")

mod.auth_module(init_content, "home")
    




