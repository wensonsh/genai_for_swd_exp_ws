import json

import streamlit as st
from streamlit import session_state

from pages.config.gen_ai_assistant import get_prompted_assistant
from helper.file_helper import write_json
from helper.navigation import forward, home, get_header
from helper.random_assignments import assign_to_group
from pages.tasks.task_template import get_task_for_prompt, get_task_template_for_prompt

def main():
    st.set_page_config(page_title="Procedure", menu_items={'Get Help': 'mailto:wendi.shu@stud.tu-darmstadt.de'})

    # go to start if no session state
    if 'participant_id' not in st.session_state:
        home()
    participant_id = st.session_state["participant_id"]

    try:
        with open("data/participants/participant_" + participant_id + ".json", "r") as f:
            data = json.load(f)
    except FileNotFoundError:
        st.switch_page("app.py")

    # save group in session state
    if "assigned_group" not in st.session_state:
        if "assigned_group" not in data:
            assigned_group = assign_to_group(participant_id)
            st.session_state["assigned_group"] = assigned_group
            data["assigned_group"] = assigned_group
        else:
            st.session_state["assigned_group"] = data["assigned_group"]
            assigned_group = data["assigned_group"]
    else:
        assigned_group = st.session_state["assigned_group"]
    if "exp_finished" in data and data["exp_finished"]:
        st.switch_page("pages/gen_ai_tool.py")

    get_header(2, "pages/init_survey.py", False, False, None, None)


    IMAGE_PATH_DEFAULT = "resources/procedure/gen_ai_tool_default.png"
    IMAGE_PATH_TAILORED = "resources/procedure/gen_ai_tool_tailored.png"

    st.title("Procedure")
    task = "write code based on a given task"
    st.markdown("On the following page, you will be given a task and a GenAI tool that you are supposed to use in order to solve the task.")

    # initialize proficiency level
    python_proficiency = data["python_proficiency"]


    st.markdown(f"Please solve the task by submitting Python code in the solution box. The next page will be divided into three sections from left to right as depicted below (task description, GenAI chat, and solution section):")
    if st.session_state["assigned_group"] == "group_default":
        st.image(IMAGE_PATH_DEFAULT, use_container_width=True)
    elif st.session_state["assigned_group"] == "group_tailored":
        st.image(IMAGE_PATH_TAILORED, use_container_width=True)
    st.markdown("To solve the task, please use the GenAI tool that is provided to you in the middle section of the page.")
    if assigned_group == "group_tailored":
        st.markdown("""You will be able to adjust the interaction and response settings of the GenAI tool in the expander above the GenAI tool. \nFurthermore, the tool **already has all the context** that you have, too:""")
        st.markdown("""
        - your task 
        - the information that you have entered in the previous survey
        """)
        st.markdown("Feel free to change the settings above the GenAI tool to adjust the interaction and response style. Please be aware, that the answers from the GenAI tool are :red[**not always right or perfect**].")
    st.divider()
    st.write("Your results will be saved as soon as you click on the 'Submit and continue' button on the right and you will be directed to the next page to conclude the experiment. "
             "You do not have to submit a correct answer. If it takes you more than 10 minutes, feel free to submit an incomplete or incorrect answer and make a small note to your submission stating that you are aware that it's incomplete or incorrect.")
    st.write("Happy collaboration! 🎉")

    @st.dialog("Interaction and Response Settings")
    def settings():
        st.write(f"You can already make some interaction and response settings now if you want. The GenAI tool that you will see on the next page will adjust to your settings.\n\n"
                 f"You can always change these settings later on the next page. If you do not have any preferences yet, you can just continue by clicking on the button below.")
        st.divider()
        # CHOOSE RESPONSE TEMPLATE
        response_template_options = ["Code only", "Step-by-step instructions + code block",
                                     "High-level overview + code block + explanation", "Other"]
        response_template_index = None
        response_template_other = None
        response_style_other = None
        role_other = None
        response_length_other = None
        if "response_template" in data and data["response_template"] and data[
            "response_template"] in response_template_options:
            response_template_index = response_template_options.index(data["response_template"])
        response_template = st.radio(label="**Response template for code-related answers**",
                                     options=response_template_options,
                                     index=response_template_index,
                                     key="response_template",
                                     horizontal=True)

        if response_template == "Other":
            response_template_input = ""
            if "response_template_other" in data and data["response_template_other"]:
                response_template_input = data["response_template_other"]
            response_template_other = st.text_input(label="Please enter your preferred response template",
                                                    label_visibility="collapsed",
                                                    placeholder="Please enter your preferred response template",
                                                    value=response_template_input)

        # RESPONSE STYLE
        response_style_options = ["Bullet points", "Continuous text", "Other"]
        response_style_index = None
        if "response_style" in data and data["response_style"] and data["response_style"] in response_template_options:
            response_style_index = response_style_options.index(data["response_style"])

        response_style = st.radio(label="**Response style**",
                                  options=response_style_options,
                                  index=response_style_index,
                                  horizontal=True)
        if response_style == "Other":
            response_style_input = ""
            if "response_style_other" in data and data["response_style_other"]:
                response_style_input = data["response_style_other"]
            response_style_other = st.text_input(label="Preferred response style",
                                                 label_visibility="collapsed",
                                                 placeholder="Please enter your preferred response style",
                                                 value=response_style_input)

        # ROLE
        role_options = ["Assistant", "Mentor", "None", "Other"]
        role_index = None
        if "role" in data and data["role"] and data["role"] in role_options:
            role_index = role_options.index(data["role"])
        role = st.radio(label="**Role that is taken on by the GenAI model**",
                        options=role_options,
                        key="role",
                        index=role_index,
                        horizontal=True)
        if role == "Other":
            role_input = ""
            if "role_other" in data and data["role_other"]:
                role_input = data["role_other"]
            role_other = st.text_input(label="Preferred role",
                                       label_visibility="collapsed",
                                       placeholder="Please enter the preferred role",
                                       value=role_input)

        # RESPONSE LENGTH
        response_length_options = ["Concise", "Short and comprehensive", "Detailed and comprehensive", "Other"]
        response_length_index = None
        if "response_length" in data and data["response_length"] and data["response_length"] in response_length_options:
            response_length_index = response_length_options.index(data["response_length"])
        response_length = st.radio(label="**Response length**",
                                   options=response_length_options,
                                   key="response_length",
                                   horizontal=True,
                                   index=response_length_index)
        if response_length == "Other":
            response_length_input = ""
            if "response_length_other" in data and data["response_length_other"]:
                response_length_input = data["response_length_other"]
            response_length_other = st.text_input(label="Preferred response length",
                                                  label_visibility="collapsed",
                                                  placeholder="Please enter the preferred response length",
                                                  value=response_length_input)

        if st.button("Save settings and continue →", type="primary"):
            if "assigned_task" in data and data["assigned_task"]:
                task_difficulty = data["assigned_task"]
            else:
                task_difficulty = "medium"

            task = get_task_for_prompt(task_difficulty) + "\n\n" + get_task_template_for_prompt(task_difficulty)
            data["response_template"] = response_template
            if response_template == "Other" and response_template_other:
                data["response_template_other"] = response_template_other
                response_template = response_template_other
            data["response_style"] = response_style
            if response_style == "Other" and response_style_other:
                data["response_style_other"] = response_style_other
                response_style = response_style_other
            data["role"] = role
            if role == "Other" and role_other:
                data["role_other"] = role_other
                role = role_other
            data["response_length"] = response_length
            if response_length == "Other" and response_length_other:
                data["response_length_other"] = response_length_other
                response_length = response_length_other
            st.session_state["system_prompt"] = get_prompted_assistant(
                role=role,
                proficiency_level=python_proficiency,
                response_style=response_style,
                response_template=response_template,
                response_length=response_length,
                task=task)
            if "system_prompt" in st.session_state:
                data["system_prompt"] = st.session_state["system_prompt"]
            write_json("data/participants/", participant_id, data)
            forward("pages/task.py", True, False, data, participant_id)

    left, middle, right = st.columns([12,8,4])
    if right.button("Continue →", key="init_continue", type="primary"):
        if session_state["assigned_group"] == "group_tailored":
            settings()
        else:
            write_json("data/participants/", participant_id, data)
            forward("pages/task.py", True, False, data, participant_id)

if __name__ == "__main__":
    main()
