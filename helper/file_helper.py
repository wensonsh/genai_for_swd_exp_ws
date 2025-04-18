import json
import os

import streamlit as st


def open_file(path, name):
    """
    Open a file based on path and name
    :param path: file path
    :param name: file name
    :return: file
    """
    data = {}
    try:
        with open(os.path.join(path, name), "r") as f:
            data = json.load(f)
    except FileNotFoundError:
        st.error("File not found.")
    return data

def open_json(path, participant_id):
    """
    Open a json file based on path and participant id

    :param path: file path
    :param participant_id: identifier of the participant
    :return: json file
    """
    data = {
        "id": participant_id
    }
    if not os.path.exists(path):
        os.makedirs(path)

    try:
        if not os.path.exists(path + "participant_" + participant_id + ".json"):
            write_json(path, participant_id, data)
        with open(path + "participant_" + participant_id + ".json", "r") as file:
            data = json.load(file)
        return data
    except FileNotFoundError:
        return st.switch_page("app.py")


def write_json(path, participant_id, data):
    """
    Write data into a json file
    :param path: path of the json file
    :param participant_id: identifier of the participant
    :param data: data to be written
    """
    with open(path + "participant_" + participant_id + ".json", "w") as file:
        json.dump(data, file)