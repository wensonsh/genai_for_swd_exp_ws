import json
import os
import streamlit as st
import zipfile
import io

from helper.file_helper import open_file

ADMIN_USERNAME = st.secrets["ADMIN_USERNAME"]
ADMIN_PASSWORD = st.secrets["ADMIN_PASSWORD"]
ADMIN_CODE = st.secrets["ADMIN_CODE"]

def create_zip(directory):
    """
    Create a zip file of all JSON files in the specified directory
    :param directory: directory containing JSON files
    :return: zip file buffer
    """
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
        for file in os.listdir(directory):
            if file.endswith(".json"):
                file_path = os.path.join(directory, file)
                zip_file.write(file_path, os.path.basename(file_path))
    zip_buffer.seek(0)
    return zip_buffer

def main():
    """
    Admin area for viewing JSON files
    :return: None
    """
    st.title("Admin Area")
    # password protection
    username = st.text_input("Enter username", type="password")
    password = st.text_input("Enter password", type="password")
    if password == "" or username == "":
        return
    if password != ADMIN_PASSWORD or username != ADMIN_USERNAME:
        st.error("Incorrect.")
        return

    section = st.selectbox("Select section", ["Participants", "Revisited", "groups.json"])

    # PARTICIPANTS
    if section == "Participants":
        directory = "data/participants"
        print(f"{directory} opened.")
        json_files = [f for f in os.listdir("data/participants") if f.endswith(".json")]
        if not json_files:
            st.write("No JSON files found.")
        else:
            zip_buffer = create_zip(directory)
            st.download_button(
                label="Download All JSON files as ZIP",
                data=zip_buffer,
                file_name="participants_json_files.zip",
                mime="application/zip",
                type="primary",
                use_container_width=True
            )
            for file in json_files:
                st.write(f"**{file}**")
                data = open_file(directory, file)
                st.json(data)
                st.download_button(
                    label="Download JSON file",
                    data=json.dumps(data),
                    file_name=file,
                    mime="application/json",
                    type="primary",
                    use_container_width=True
                )

    # REVISITED
    elif section == "Revisited":
        directory = "data/revisited"
        print(f"{directory} opened.")
        if not os.path.exists(directory):
            st.write("No revisited data found.")
        json_files = [f for f in os.listdir(directory) if f.endswith(".json")]
        if not json_files:
            st.write("No JSON files found.")
        else:
            zip_buffer = create_zip(directory)
            st.download_button(
                label="Download All JSON files as ZIP",
                data=zip_buffer,
                file_name="revisited_json_files.zip",
                mime="application/zip",
                type="primary",
                use_container_width=True
            )
            for file in json_files:
                st.write(f"**{file}**")
                data = open_file("data/revisited", file)
                st.json(data)
                st.download_button(
                    label="Download JSON file",
                    data=json.dumps(data),
                    file_name=file,
                    mime="application/json",
                    type="primary",
                    use_container_width=True
                )

    # GROUPS
    elif section == "groups.json":
        file_path = "data/groups.json"
        print(f"{file_path} opened.")
        if not os.path.exists(file_path):
            st.write("No groups.json file found.")
        else:
            data = open_file("data", "groups.json")
            st.json(data)
            st.download_button(
                label="Download groups.json",
                data=json.dumps(data),
                file_name="groups.json",
                mime="application/json",
                type="primary",
                use_container_width=True
            )

if __name__ == "__main__":
    main()