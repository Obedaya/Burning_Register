import streamlit as st
import streamlit_authenticator as stauth
from utilities import database as db
from utilities import init_db



def movielist_names():
    movies = [x["name"] for x in list(db.find_all("movies"))]
    return movies

def create_movie_selection():
    movies = movielist_names()
    if "movie" not in st.session_state:
        st.session_state["movie"] = movies[0]
    st.session_state["movie"] = st.selectbox("Select movie", options=movies, index= 0 if "movie" not in st.session_state else movies.index(st.session_state["movie"]))

    
def auth_login_register():
    init_db.init_auth()
    config = db.find_all("auth")[0]
    authenticator = stauth.Authenticate(
        config['credentials'],
        config['cookie']['name'],
        config['cookie']['key'],
        config['cookie']['expiry_days'],
        config['preauthorized']
    )
    if st.session_state["authentication_status"] is None or st.session_state["authentication_status"] is False:
        tab = st.tabs(["Login", "Register user"])
        with tab[0]:
            st.session_state["user_diplayname"], \
            st.session_state["authentication_status"], \
            st.session_state["username"] = authenticator.login('Login', 'main')
        with tab[1]:
            try:
                if authenticator.register_user('Register user', preauthorization=True):
                    st.success('User registered successfully')
                    db.replace("auth", config["_id"], config)
            except Exception as e:
                st.error(e)
                print("{}{}".format(str(e), str(config)))
        if st.session_state["authentication_status"]:
            st.experimental_rerun()
    return authenticator

def auth_module(init_function, pagename):
    authenticator = auth_login_register()

    if st.session_state["authentication_status"]:
        col = st.columns([5,1])
        with col[0]:
            st.write(f'Welcome *{st.session_state["name"]}*')
        with col[1]:
            authenticator.logout('Logout', 'main', key=f'{pagename}_logout')
        init_function()
    elif st.session_state["authentication_status"] is False:
        st.error('Username/password is incorrect')
    elif st.session_state["authentication_status"] is None:
        st.warning('Please enter your username and password')
    