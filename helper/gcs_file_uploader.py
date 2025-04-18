import asyncio
import json
import os
import smtplib
import tempfile
from email.mime.text import MIMEText

import streamlit as st
from google.cloud import storage

GCS_BUCKET_NAME = st.secrets["GCS_BUCKET_NAME"]

async def upload_to_gcs(data, destination_blob_name):
    """
    Uploads a file to Google Cloud Storage (GCS) asynchronously
    :param data: data to be uploaded
    :param destination_blob_name: name of the destination blob in GCS
    :return: None
    """
    try:
        credentials = st.secrets["connections"]["gcs"]
        # convert AttrDict to a regular dictionary
        if hasattr(credentials, "_mapping"):
            # if it's using attrdict library's implementation
            credentials_dict = credentials._mapping
        elif hasattr(credentials, "to_dict"):
            # if the object has a to_dict method
            credentials_dict = credentials.to_dict()
        else:
            # generic fallback - create a new dict with all items
            credentials_dict = dict(credentials)
        # create a temporary credentials file
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
            json.dump(credentials_dict, f)
            temp_creds_file = f.name

        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = temp_creds_file
        storage_client = storage.Client().from_service_account_json(temp_creds_file)
        bucket = storage_client.bucket(GCS_BUCKET_NAME)
        blob = bucket.blob(destination_blob_name)
        # convert dictionary to a JSON string and then to a BytesIO object
        json_data = json.dumps(data, ensure_ascii=False)
        # clean up the temporary file after use
        os.unlink(temp_creds_file)
        await asyncio.to_thread(blob.upload_from_string, json_data, content_type="application/json")
        await async_send_mail(error=False)
    except Exception as e:
        print("An error occurred while uploading the file to GCS. " + str(e))
        await async_send_mail(error=True, message=e)

async def upload_participant_data(participant_id, data):
    """
    Upload participant data to Google Cloud Storage (GCS)
    :param participant_id: identifier of the participant for the file name
    :param data: data to be uploaded
    :return: None
    """
    try:
        # Upload to GCS
        gcs_file_name = f"participant_{participant_id}.json"
        await upload_to_gcs(data, gcs_file_name)
    except Exception as e:
        print("An error occurred while uploading the file to GCS. " + str(e))
        pass

async def async_send_mail(error=False, message=None):
    """
    Send an email notification about the file upload status
    :param error: flag if an error occurred
    :param message: message for the email body
    :return: None
    """
    try:
        sender_email = st.secrets["MAIL"]
        receiver_email = sender_email
        mail_pw = st.secrets["MAIL_PW"]
        if error:
            msg = MIMEText(f"Error during file upload to GCS: {message}")
        else:
            msg = MIMEText(f"New file upload to GCS.")
        msg["Subject"] = "Exp GenAI for SWD: File upload"
        msg["From"] = sender_email
        msg["To"] = receiver_email

        await asyncio.to_thread(send_mail_sync, sender_email, receiver_email, msg, mail_pw)
    except Exception as e:
        print("An error occurred while sending the mail. " + str(e))
        pass

def send_mail_sync(sender_email, receiver_email, msg, mail_pw):
    """
    Send an email
    :param sender_email: sender mail address
    :param receiver_email: receiver mail address
    :param msg: message in the email body
    :param mail_pw: password for the sender email
    :return: None
    """
    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(sender_email, mail_pw)
            server.sendmail(sender_email, receiver_email, msg.as_string())
    except Exception as e:
        print("An error occurred while sending the mail. " + str(e))
        pass
