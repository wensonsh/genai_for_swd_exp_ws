import streamlit as st
from helper.navigation import home


def check_session_state():
    # go to start if no session state
    if 'participant_id' not in st.session_state:
        home()
    return st.session_state["participant_id"]