import asyncio
import json
import time

import streamlit as st

st.set_page_config(page_title="Thank You", menu_items={'Get Help': 'mailto:wendi.shu@stud.tu-darmstadt.de'})

from helper.file_helper import write_json, open_json
from helper.gcs_file_uploader import upload_participant_data, async_send_mail
from helper.navigation import home, back
from helper.session_state import check_session_state


FILE_PATH = "data/participants/"

def main():
    participant_id = check_session_state()
    try:
        with open("data/participants/participant_" + participant_id + ".json", "r") as f:
            data = json.load(f)
    except FileNotFoundError:
        st.switch_page("app.py")
    except TypeError:
        st.switch_page("app.py")

    # check if participant really finished the survey by checking the entries in the json file
    if "solution_generate" not in data:
        back("pages/procedure.py")
    elif "age" not in data:
        back("pages/post_survey.py")

    data["finished"] = True
    write_json(FILE_PATH, participant_id, data)
    st.title("Thank You")
    st.markdown("""You have successfully completed the experiment. The study team will be informed shortly. Thank you very much for participating!""")
    st.markdown("""To confirm your participation and receive compensation, please click on the following link to return to Prolific or use the code below:""")
    st.markdown("""**Prolific link**: https://app.prolific.com/submissions/complete?cc=C1F843I9""")
    st.markdown("""**Prolific code**: C1F843I9""")
    st.divider()
    st.text("If you wish to continue using the GenAI tool that has been provided to you during this experiment, you can revisit the tool by entering your personal ID in the input field on the home page.")
    st.text("Your personal ID is:")
    st.code(participant_id)

    st.text("")
    st.divider()

    if st.button("Back to home page 🏠︎"):
        home()


    try:
        st.toast("Informing study team about completion...", icon="📤")
        time.sleep(5)
        st.toast("Study team has been informed about completion.", icon="✅")
        time.sleep(1)
        st.toast("Thank you for participating!", icon="🌼")
    except Exception as e:
        st.text("")


    async def upload_with_timeout(part_id, content, timeout=20):
        try:
            await asyncio.wait_for(upload_participant_data(part_id, content), timeout=timeout)
        except asyncio.TimeoutError:
            await async_send_mail(error=True, message="Upload timed out after 20 seconds.")


    if "upload_attempted" not in st.session_state:
        st.session_state["upload_attempted"] = True
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(upload_with_timeout(participant_id, data))
        loop.close()
    except Exception as e:
        print(f"PARTICIPANT {participant_id} -- Error while uploading file to GCS. " + str(e))
        try:
            async_send_mail(error=True, message=e)
        except Exception as e:
            print(f"PARTICIPANT {participant_id} -- Error while sending mail. " + str(e))
            pass

if __name__ == "__main__":
    main()