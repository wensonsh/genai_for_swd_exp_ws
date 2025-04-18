import streamlit as st

from helper.file_helper import write_json
from helper.timer import get_current_time

FILE_PATH = "data/participants/"

def home():
    return st.switch_page("app.py")

def back(page):
    return st.switch_page(page)

def forward(page, start_timer, end_timer, data, participant_id):
    current_time = get_current_time()
    if start_timer:
        if "start_time" not in data:
            data["start_time"] = current_time
            data["start_time_rep"] = current_time
        elif "start_time_rep" in data:
            data["start_time_rep"] = str(data["start_time_rep"]) + " -> " + current_time
        write_json(FILE_PATH, participant_id, data)
    elif end_timer:
        if "end_time" not in data:
            data["end_time"] = current_time
            data["end_time_rep"] = current_time
        elif "end_time_rep" in data:
            data["end_time_rep"] = str(data["end_time_rep"]) + " -> " + current_time
        write_json(FILE_PATH, participant_id, data)
    return st.switch_page(page)

def get_header(current_page, back_link, start_timer, end_timer, data, participant_id):
    header_left, header_right = st.columns([2, 2])

    with header_left:
        if st.button("← Back", key="back_app"):
            if start_timer:
                current_time = get_current_time()
                if "start_time" not in data:
                    data["start_time"] = current_time
                    data["start_time_rep"] = current_time
                elif "start_time_rep" in data:
                    data["start_time_rep"] = str(data["start_time_rep"]) + " -> " + current_time
                write_json(FILE_PATH, participant_id, data)
            elif end_timer:
                current_time = get_current_time()
                if "end_time" not in data:
                    data["end_time"] = current_time
                    data["end_time_rep"] = current_time
                elif "end_time_rep" in data:
                    data["end_time_rep"] = str(data["end_time_rep"]) + " -> " + current_time
                write_json(FILE_PATH, participant_id, data)
            back(back_link)
    if current_page:
        with header_right:
            css = """
            <style>
                .page-info {
                    font-size: 8px;
                    color: #737373;
                    text-align: right;
                }
            </style>
            """
            st.markdown(css, unsafe_allow_html=True)
            st.markdown(f"<p class='page-info'>Page {current_page} of 5</p>", unsafe_allow_html=True)