import json
import random

import streamlit as st

from helper.navigation import forward
from helper.navigation import get_header
from helper.timer import get_current_time

from helper.session_state import check_session_state
from pages.init_survey import participant_id


def main():

    st.set_page_config(page_title="Post-Experiment Survey", menu_items={'Get Help': 'mailto:wendi.shu@stud.tu-darmstadt.de'}, layout="wide")
    participant_id = check_session_state()

    try:
        with open("data/participants/participant_" + participant_id + ".json", "r") as f:
            data = json.load(f)
    except FileNotFoundError:
        st.switch_page("app.py")

    get_header(5, "pages/post_survey.py", False, False, data, participant_id)
    st.title("Post-Experiment Survey")

    def validate_form(preferred_tool_input, preferred_tool_reason_input):
        error = {}
        if tool_D_description != "" and tool_T_description != "":
            if not preferred_tool_input:
                error["preferred_tool"] = "Please select a preferred tool."
            elif not preferred_tool_reason_input:
                error["preferred_tool"] = "Please provide a reason for your choice."
        return error

    st.text("")
    tool_D_description = ""
    tool_T_description = ""
    preferred_tool = None
    preferred_tool_reason = None
    try:
        PREFERRED_TOOL_OPTIONS = ["Tool D", "Tool T", "Neither"]
        preferred_tool_index = None

        if "preferred_tool" in data and data["preferred_tool"]:
            preferred_tool_index = PREFERRED_TOOL_OPTIONS.index(data["preferred_tool"])

        if "assigned_group" in data and data["assigned_group"] == "group_tailored":
            tool_D_description =  "Tool D is a general-purpose GenAI model, similar to ChatGPT. It does not have any prior knowledge of your task, proficiency level, or personal preferences. Hence, you are responsible for crafting an appropriate prompt to guide its responses."
            tool_T_description = "Tool T is the tool that you were provided during this experiment. It is a GenAI tool designed to adapt to your task and proficiency level, using the given context to better align with your task. It provides controls which help you generate a system prompt tailored to your personal preferences while following prompt engineering best practices. However, you still have full control - you can adjust your tailored system prompt or simply use the default with no system prompt at all."
        elif "assigned_group" in data and data["assigned_group"] == "group_default":
            tool_D_description = "Tool D is the tool you were provided during this experiment. It is a general-purpose GenAI model, similar to ChatGPT. It does not have any prior knowledge of your task, proficiency level, or personal preferences. Hence, you were responsible for crafting an appropriate prompt to guide its responses."
            tool_T_description = "Tool T is a GenAI tool designed to adapt to your task and proficiency level, using the given context to better align with your task. It provides controls which help you generate a system prompt tailored to your personal preferences while following prompt engineering best practices. However, you still have full control - you can adjust your tailored system prompt or simply use the default with no system prompt at all."
        if "tool_order" not in st.session_state:
            tools = [{"name": "Tool D", "description": tool_D_description},
                     {"name": "Tool T", "description": tool_T_description}]
            random.shuffle(tools)
            st.session_state["tool_order"] = tools
        tools = st.session_state["tool_order"]

        if tool_D_description != "" and tool_T_description != "":
            st.markdown("**You are presented descriptions of two different GenAI tools. Please read the descriptions and answer the question below.**")
            col1, col2, col3 = st.columns([3, 1, 3])
            with col1:
                st.markdown(f"### {tools[0]["name"]}")
                st.markdown(tools[0]["description"])
            with col3:
                st.markdown(f"### {tools[1]["name"]}")
                st.markdown(tools[1]["description"])

            SHUFFLED_TOOL_OPTIONS = [tools[0]["name"], tools[1]["name"], "neither"]
            st.markdown("**If you had the choice between the two tools described above during this experiment, which one would you have preferred to use?**")
            preferred_tool = st.radio(label="Which tool would you prefer to use?", label_visibility="collapsed", options=SHUFFLED_TOOL_OPTIONS, index=preferred_tool_index)
            if preferred_tool:
                st.markdown(f"**Why would you prefer {preferred_tool}?**")
                preferred_tool_reason = st.text_input(label="Why would you prefer Tool D?", label_visibility="collapsed", placeholder="Please specify briefly", key="reason_tool_pref")

    except Exception as e:
        print(f"PARTICIPANT {participant_id} -- An error occurred in post_survey.py while displaying the preferred tool question.\n\n" + str(e))
        pass

    # Finish
    st.text("")
    st.text("")
    st.text("")

    st.divider()
    left, middle, right = st.columns([12,8,4])
    if right.button("Submit", key="submit", type="primary"):
        # Clear previous error messages
        errors = validate_form(preferred_tool, preferred_tool_reason)
        if "preferred_tool" in errors and errors["preferred_tool"]:
            st.error(errors["preferred_tool"])
        else:
            data["preferred_tool"] = preferred_tool
            data["preferred_tool_reason"] = preferred_tool_reason

            data["next_page"] = "finish.py"
            data["exp_finished"] = True
            data["end_time_general"] = get_current_time()
            with open("data/participants/participant_" + participant_id + ".json", "w") as f:
                json.dump(data, f)
            forward("pages/finish.py", False, False, None, None)

if __name__ == "__main__":
    main()
