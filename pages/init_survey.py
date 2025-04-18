import json

import streamlit as st
from helper.navigation import forward, home, get_header

def main():
    st.set_page_config(page_title="Baseline Survey", menu_items={'Get Help': 'mailto:wendi.shu@stud.tu-darmstadt.de'})

    # go to start if no session state
    if 'participant_id' not in st.session_state:
        home()
    participant_id = st.session_state["participant_id"]

    try:
        with open("data/participants/participant_" + participant_id + ".json", "r") as f:
            data = json.load(f)
    except FileNotFoundError:
        home()

    get_header(1, "app.py", False, None, data, participant_id)
    st.info(f"Your participant ID is: **{participant_id}**.\n\nIf necessary, you can use this ID to resume the experiment later. "
            f"However, after moving past this page, we ask you to complete the experiment in one session to ensure consistency.")
    st.title("Baseline Survey")
    st.markdown("Please fill out the following form to help us understand your background and experience with ChatGPT.")

    def validate_form(participant_prolific_id, participant_age, participant_job, participant_python_proficiency, participant_chat_gpt_proficiency, participant_chat_gpt_usage_private, participant_chat_gpt_usage_swd_tasks):
        error_list = {}
        if not participant_prolific_id:
            error_list["prolific_id"] = "Please enter your Prolific ID"
        if not participant_age:
            error_list["age"] = "Please enter your age"
        if not participant_job:
            error_list["job"] = "Please enter your job"
        if not participant_python_proficiency:
            error_list["python_proficiency"] = "Please select your proficiency with Python."
        if not participant_chat_gpt_proficiency or participant_chat_gpt_proficiency is None:
            error_list["chat_gpt_proficiency"] = "Please enter your proficiency with ChatGPT"
        if not participant_chat_gpt_usage_private:
            error_list["chat_gpt_usage_private"] = "Please enter your usage frequency of GenAI tools like ChatGPT"
        if not participant_chat_gpt_usage_swd_tasks:
            error_list["chat_gpt_usage_swd_tasks"] = "Please enter your usage frequency of GenAI tools like ChatGPT or Copilot at work"

        return error_list


    st.markdown("Please enter your unique Prolific ID*")
    if "prolific_id" in data and data["prolific_id"]:
        prolific_id = st.text_input(label="Please enter your Prolific ID*",label_visibility="collapsed", value = data["prolific_id"], key="prolific_id")
    else:
        prolific_id = st.text_input(label="Please enter your Prolific ID*", label_visibility="collapsed", key="prolific_id")

    #AGE
    if "age" in data and data['age']:
        age = st.number_input("Your Age*", value = int(data['age']), min_value=0, max_value=100, step=1, key="age")
    else:
        age = st.number_input("Your Age*", min_value=0, max_value=100, step=1, key="age")

    #JOB
    if "job" in data and data['job']:
        job = st.text_input("What is your current occupation?*", value = data['job'], key = "job")
    else:
        job = st.text_input("What is your current occupation?*", key = "job")

    # PYTHON PROFICIENCY
    python_proficiency_values = ["No Experience", "Beginner", "Intermediate", "Advanced", "Expert"]
    python_proficiency_index = None

    if "python_proficiency" in data and data["python_proficiency"]:
        python_proficiency_index = python_proficiency_values.index(data["python_proficiency"])

    python_proficiency = st.selectbox(
        label="How proficient are you with Python?*",
        options=python_proficiency_values,
        index=python_proficiency_index,
        placeholder="Please select"
    )

    st.divider()

    # ChatGPT proficiency
    chat_gpt_proficiency_values = ["No Experience", "Beginner", "Intermediate", "Advanced", "Expert"]
    chat_gpt_proficiency_index = None

    if "chat_gpt_proficiency" in data and data['chat_gpt_proficiency']:
        chat_gpt_proficiency_index = chat_gpt_proficiency_values.index(data["chat_gpt_proficiency"])

    chat_gpt_proficiency = st.selectbox(
        label="How proficient are you with ChatGPT?*",
        options=chat_gpt_proficiency_values,
        index=chat_gpt_proficiency_index,
        placeholder="Please select"
    )

    # ChatGPT usage private
    chat_gpt_usage_values = ["never", "rarely", "sometimes", "often", "constantly"]
    chat_gpt_usage_index = None
    chat_gpt_usage_value = None

    if "chat_gpt_usage_private" in data and data['chat_gpt_usage_private']:
        chat_gpt_usage_value = data["chat_gpt_usage_private"]

    chat_gpt_usage_private = st.select_slider(
        label="How often do you use GenAI like ChatGPT for personal purposes?*",
        options=chat_gpt_usage_values,
        value = chat_gpt_usage_value
    )

    # ChatGPT usage work
    chat_gpt_usage_swd_tasks_values = ["never", "rarely", "sometimes", "often", "constantly"]
    chat_gpt_usage_swd_tasks_index = None
    chat_gpt_usage_swd_tasks_value = None

    if "chat_gpt_usage_swd_tasks" in data and data['chat_gpt_usage_swd_tasks']:
        chat_gpt_usage_swd_tasks_value = data["chat_gpt_usage_swd_tasks"]

    chat_gpt_usage_swd_tasks = st.select_slider(
        label = f"How often do you use **ChatGPT** for software development tasks?*",
        options = chat_gpt_usage_swd_tasks_values,
        value = chat_gpt_usage_swd_tasks_value
    )
    # Copilot usage work
    copilot_usage_swd_tasks_values = ["never", "rarely", "sometimes", "often", "constantly"]
    copilot_usage_swd_tasks_index = None
    copilot_usage_swd_tasks_value = None

    if "copilot_usage_swd_tasks" in data and data['copilot_usage_swd_tasks']:
        copilot_usage_swd_tasks_value = data["copilot_usage_swd_tasks"]

    copilot_usage_swd_tasks = st.select_slider(
        label = f"How often do you use **GitHub Copilot** for software development tasks?*",
        options = copilot_usage_swd_tasks_values,
        value = copilot_usage_swd_tasks_value
    )

    # ChatGPT usage types
    chat_gpt_usage_write_code = False
    if "chat_gpt_usage_write_code" in data and data['chat_gpt_usage_write_code']:
        chat_gpt_usage_write_code = data["chat_gpt_usage_write_code"]

    chat_gpt_usage_understand_code = False
    if "chat_gpt_usage_understand_code" in data and data['chat_gpt_usage_understand_code']:
        chat_gpt_usage_understand_code = data["chat_gpt_usage_understand_code"]

    chat_gpt_usage_fix_code = False
    if "chat_gpt_usage_fix_code" in data and data['chat_gpt_usage_fix_code']:
        chat_gpt_usage_fix_code = data["chat_gpt_usage_fix_code"]

    chat_gpt_usage_others = False
    if "chat_gpt_usage_others" in data and data['chat_gpt_usage_others']:
        chat_gpt_usage_others = data["chat_gpt_usage_others"]

    chat_gpt_usage_others_text = ""
    if "chat_gpt_usage_others_text" in data and data['chat_gpt_usage_others_text']:
        chat_gpt_usage_others_text = data["chat_gpt_usage_others_text"]
    st.write("If you use ChatGPT for software development tasks, what kind of tasks do you use it for?")
    chat_gpt_usage_write_code = st.checkbox(label="Writing code", value = chat_gpt_usage_write_code)
    chat_gpt_usage_understand_code = st.checkbox(label = "Understanding code", value = chat_gpt_usage_understand_code)
    chat_gpt_usage_fix_code = st.checkbox(label = "Fixing code / finding errors", value = chat_gpt_usage_fix_code)
    chat_gpt_usage_others = st.checkbox(label = "Others", value = chat_gpt_usage_others)
    if chat_gpt_usage_others:
        chat_gpt_usage_others_text = st.text_input(label = "Please specify", value = chat_gpt_usage_others_text)

    left, middle, right = st.columns([12,8,4])
    if right.button("Continue →", key="init_continue", type="primary"):
        # Clear previous error messages
        errors = validate_form(prolific_id, age, job, python_proficiency, chat_gpt_proficiency, chat_gpt_usage_private, chat_gpt_usage_swd_tasks)
        if errors:
            if "prolific_id" in errors:
                st.error(errors["prolific_id"])
            if "age" in errors:
                st.error(errors["age"])
            if "job" in errors:
                st.error(errors["job"])
            if "python_proficiency" in errors:
                st.error(errors["python_proficiency"])
            if "chat_gpt_proficiency" in errors:
                st.error(errors["chat_gpt_proficiency"])
            if "chat_gpt_usage_private" in errors:
                st.error(errors["chat_gpt_usage_private"])
            if "chat_gpt_usage_swd_tasks" in errors:
                st.error(errors["chat_gpt_usage_swd_tasks"])
        else:
            if prolific_id:
                data["prolific_id"] = prolific_id
            if age != 0:
                data['age'] = str(age)
            if job:
                data['job'] = job
            if python_proficiency:
                data['python_proficiency'] = python_proficiency
            if chat_gpt_proficiency is not None:
                data['chat_gpt_proficiency'] = chat_gpt_proficiency
            if chat_gpt_usage_private is not None:
                data['chat_gpt_usage_private'] = chat_gpt_usage_private
            if chat_gpt_usage_swd_tasks is not None:
                data['chat_gpt_usage_swd_tasks'] = chat_gpt_usage_swd_tasks
            if copilot_usage_swd_tasks is not None:
                data['copilot_usage_swd_tasks'] = copilot_usage_swd_tasks
            if chat_gpt_usage_write_code is not None:
                data['chat_gpt_usage_write_code'] = chat_gpt_usage_write_code
            if chat_gpt_usage_understand_code is not None:
                data['chat_gpt_usage_understand_code'] = chat_gpt_usage_understand_code
            if chat_gpt_usage_fix_code is not None:
                data['chat_gpt_usage_fix_code'] = chat_gpt_usage_fix_code
            if chat_gpt_usage_others is not None:
                data['chat_gpt_usage_others'] = chat_gpt_usage_others
            if chat_gpt_usage_others_text is not None:
                data['chat_gpt_usage_others_text'] = chat_gpt_usage_others_text
            data["exp_finished"] = False

            data["next_page"] = "procedure.py"
            with open("data/participants/participant_" + participant_id + ".json", "w") as f:
                json.dump(data, f)

            if 'age' in data and 'job' in data and 'chat_gpt_proficiency' in data and 'chat_gpt_usage_private' in data and 'chat_gpt_usage_swd_tasks' in data:
                forward("pages/procedure.py", False, False, None, None)

if __name__ == "__main__":
    main()