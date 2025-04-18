import json
import os

import streamlit as st

from config.gen_ai_assistant import get_prompted_assistant_without_task
from helper.file_helper import open_json, write_json
from helper.timer import get_current_time
from helper.utils import generate_random_id

st.session_state.clear()
st.set_page_config(page_title="GenAI for Software Development", menu_items={'Get Help': 'mailto:wendi.shu@stud.tu-darmstadt.de'})
# Initialize session state for navigation and participant ID
if "current_page" not in st.session_state:
    st.session_state["current_page"] = "welcome"
if "participant_id" not in st.session_state:
    st.session_state["participant_id"] = None

# create directory for participant data if it doesn't exist
directory = "data/participants/"
if not os.path.exists(directory):
    os.makedirs(directory)

# Navigation function
def go_to_page(page_name):
    st.switch_page(page_name)

# Welcome Page
if st.session_state["current_page"] == "welcome":
    st.title("Welcome to the Generative AI Experiment")

    st.write("""
    This experiment explores the use of Generative AI (GenAI) tools for software development.
    You will be guided through this experiment. The experiment should take a maximum of 20 minutes. 
    Please make sure that you have a stable internet connection and that you are doing this experiment on a PC.  
    \n\n If you face any problems or in case you've got questions, feel free to contact wendi.shu@stud.tu-darmstadt.de.
    """)
    st.markdown(f"***Your participation is entirely voluntary, and you may withdraw at any time. "
                f"All the information that you provide will be kept confidential and will only be used for research purposes. "
                f"Your data will be processed and stored anonymously."
                f"\nYou will interact with a GenAI tool that is based on OpenAI's GPT-4o model (see https://platform.openai.com/docs/models for more information). While chatting with the GenAI tool, please do not share any sensitive information that you do not wish to be processed by OpenAI. By proceeding, you consent to participate under these terms.***")

    st.empty()

    st.write("Please click the button below to start the experiment.")

    # START
    if st.button("Start", type="primary"):
        # generate a new Participant ID and initialize their data
        participant_id = generate_random_id()
        while os.path.exists("data/participants/participant_" + participant_id + ".json"):
            # make sure that the id doesn't exist already
            participant_id = generate_random_id()
        st.session_state["participant_id"] = participant_id
        data = {
            "id": participant_id,
            "next_page": "init_survey.py",
            "start_time_general": get_current_time()
        }
        if not os.path.exists("data/participants/participant_" + participant_id + ".json"):
            with open("data/participants/participant_" + participant_id + ".json", "w") as file:
                json.dump(data, file)
        st.switch_page("pages/init_survey.py")

    # CONTINUE
    st.divider()
    st.write("If you've already been here and want to revisit the tool, please enter your participant ID and click the 'Continue →' button.")
    input_id = st.text_input("Enter your Participant ID to continue:")
    if st.button("Continue →"):
        if not os.path.exists("data/participants/participant_" + input_id + ".json"):
            st.warning("ID not found. Please try again.")
        else:
            try:
                with open("data/participants/participant_" + input_id + ".json", "r") as f:
                    data = json.load(f)
            except FileNotFoundError:
                st.switch_page("app.py")

            st.session_state["participant_id"] = input_id

            if "exp_finished" in data and data["exp_finished"]:
                try:
                    revisited_data = open_json("data/revisited/", input_id)
                    if "revisit_count" not in revisited_data:
                        revisited_data["revisit_count"] = 1
                    else:
                        revisited_data["revisit_count"] += 1
                    revisited_data["assigned_group"] = data["assigned_group"]
                    # transfer the data from the previous experiment to the revisited tool
                    if "assigned_group" in data and data["assigned_group"] == "group_tailored":
                        response_style = ""
                        response_template = ""
                        role = ""
                        response_length = ""
                        python_proficiency = ""
                        if "response_template" not in revisited_data:
                            revisited_data["response_template"] = data["response_template"]
                            response_template = data["response_template"]
                            if "response_template_other" in data:
                                revisited_data["response_template_other"] = data["response_template_other"]
                                response_template = data["response_template_other"]
                        else:
                            response_template = revisited_data["response_template"]
                        if "response_style" not in revisited_data:
                            revisited_data["response_style"] = data["response_style"]
                            response_style = data["response_style"]
                            if "response_style_other" in data:
                                revisited_data["response_style_other"] = data["response_style_other"]
                                response_style = data["response_style_other"]
                        else:
                            response_style = revisited_data["response_style"]
                        if "role" not in revisited_data:
                            revisited_data["role"] = data["role"]
                            role = data["role"]
                            if "role_other" in data:
                                revisited_data["role_other"] = data["role_other"]
                                role = data["role_other"]
                        else:
                            role = revisited_data["role"]
                        if "response_length" not in revisited_data:
                            revisited_data["response_length"] = data["response_length"]
                            response_length = data["response_length"]
                            if "response_length_other" in data:
                                revisited_data["response_length_other"] = data["response_length_other"]
                                response_length = data["response_length_other"]
                        else:
                            response_length = revisited_data["response_length"]
                        if "python_proficiency" not in revisited_data:
                            revisited_data["python_proficiency"] = data["python_proficiency"]
                            python_proficiency = data["python_proficiency"]
                        st.session_state["system_prompt"] = get_prompted_assistant_without_task(
                            role=role,
                            proficiency_level=python_proficiency,
                            response_style=response_style,
                            response_template=response_template,
                            response_length=response_length,
                            lang="Python")
                        st.session_state["user_system_prompt"] = ""

                    write_json("data/revisited/", input_id, revisited_data)
                    st.switch_page("pages/gen_ai_tool.py")
                except Exception as e:
                    print("An error occurred on app.py:\n\n" + str(e))
                    st.error("An error occurred. Please try again. If the error persists, please contact wendi.shu@stud.tu-darmstadt.de.")


            next_page = data["next_page"]
            st.switch_page("pages/" + next_page)

# Demographic Survey Page
elif st.session_state["current_page"] == "init_survey":
    pass
# Explanation Page
elif st.session_state["current_page"] == "procedure":
    pass
# gen_ai_tool Page
elif st.session_state["current_page"] == "task":
    pass
# post survey Page
elif st.session_state["current_page"] == "post_survey":
    pass
elif st.session_state["current_page"] == "tool_preference":
    pass