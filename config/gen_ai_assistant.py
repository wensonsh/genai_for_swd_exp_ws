import streamlit as st

OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]

RESPONSE_STYLE_TEMPLATE_A = "Code only (no explanation or text around)"
RESPONSE_STYLE_TEMPLATE_B = "First, provide step-by-step instructions. Then, provide the code. Lastly, if there is anything left to explain that hasn't been covered in the step-by-step instructions, explain the code"
RESPONSE_STYLE_TEMPLATE_C = "First, provide a high-level overview (a brief summary of the approach). Then, provide the code and explain the code if there is anything left to explain"


DEFAULT_TEMPERATURE = 0.7
DEFAULT_INITIAL_USER_MESSAGE = """Hi, I'm your personal coding assistant CoA. I already know your task. \n\n Feel free to adjust your interaction and response settings or the system prompt itself first (see expanders above this chat), before we start to collaborate on the task. Let's get started! 🚀"""
INITIAL_USER_MESSAGE_WITHOUT_TASK = """Hi, I'm your personal coding assistant CoA. \n\n Feel free to adjust the interaction and response settings first (see expander above this chat), before we get started."""

def get_prompted_assistant(role, proficiency_level, response_style, response_template, response_length, task):
    if not role or role == "None":
        role = "tool"
    text_role = f"You are a highly capable GenAI {role.lower()} designed to be used by a {proficiency_level.lower()} Python software developer. The software developer's task is to solve the programming task shown below."

    text_response_template = ""
    if response_template == "Code only":
        response_template = RESPONSE_STYLE_TEMPLATE_A
    elif response_template == "Step-by-step instructions + code block":
        response_template = RESPONSE_STYLE_TEMPLATE_B
    elif response_template == "High-level overview + code block + explanation":
        response_template = RESPONSE_STYLE_TEMPLATE_C
    if response_template != "" and response_template:
        text_response_template = (f"In case you include any code in your response, format your response according to this template: {response_template}. "
                                  f"Ensure adherence to Python coding best practices including:\n- self-explanatory variable names\n- guiding comments.\n\n")

    text_response_style = ""
    if response_style == "Continuous text":
        text_response_style = "Provide responses in continuous prose without using bullet points or lists.\n"
    elif response_style and response_style != "":
        text_response_style = f"Structure your responses as {response_style.lower()}.\n"

    text_response_length = ""
    if response_length != "" and response_length:
        text_response_length = f"Keep your responses {response_length.lower()}.\n"

    system_prompt = (f"{text_role}\n\n"
                     f"### **Task**\n"
                     f"\n{task}.\n\n---\n\n"
                     f"The developer can access the same task description in the sidebar of the page.\n\n"
                     f"### **How You Should Respond:**\n"
                     f"{text_response_style}"
                     f"{text_response_length}"
                     f"{text_response_template}"
                     f"Ensure all the task's requirements and constraints are met when providing assistance. "
                     f"If you are asked off-topic questions, politely redirect the developer back to the task.")
    return system_prompt


def get_prompted_assistant_without_task(role, proficiency_level, lang, response_style, response_template, response_length):
    if proficiency_level is None:
        proficiency_level = "unknown proficiency level"
    if lang is None:
        lang = ""
    if not role or role == "None":
        role = "tool"
    text_role = f"You are a highly capable GenAI {role.lower()} designed to be used by a {proficiency_level.lower()} {lang} software developer."
    text_response_template = ""
    if response_template == "Code only":
        response_template = RESPONSE_STYLE_TEMPLATE_A
    elif response_template == "Step-by-step instructions + code block":
        response_template = RESPONSE_STYLE_TEMPLATE_B
    elif response_template == "High-level overview + code block + explanation":
        response_template = RESPONSE_STYLE_TEMPLATE_C
    if response_template != "" and response_template:
        text_response_template = f"In case you include any code in your response, do so in the following template: {response_template.lower()}. Also, align with general Python coding best practices and provide docstrings or comments where appropriate."

    text_response_style = ""
    if response_style == "Continuous text":
        text_response_style = "While interacting with the software developer, your responses should be as continuous text. Avoid any bullet points or lists in that case."
    elif response_style and response_style != "":
        text_response_style = f"While interacting with the software developer, your responses should be as {response_style.lower()}."

    text_response_length = ""
    if response_length != "" and response_length:
        text_response_length = f"In general, your responses should be {response_length.lower()}."
    system_prompt = (
        f"{text_role} "
        f"{text_response_style} "
        f"{text_response_length} "
        f"If the developer asks you to provide code, do so. "
        f"{text_response_template} ")
    return system_prompt


def get_temperature():
    return DEFAULT_TEMPERATURE

def get_default_initial_user_message():
    return DEFAULT_INITIAL_USER_MESSAGE

def get_default_initial_user_message_without_task():
    return INITIAL_USER_MESSAGE_WITHOUT_TASK