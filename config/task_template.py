import json

import streamlit as st

def load_tasks():
    """
    Load tasks from a JSON file
    :return: loaded task file
    """
    with open("resources/tasks/tasks.json", "r") as f:
        return json.load(f)

TASKS = load_tasks()

def display_task(complexity):
    """
    Display the task based on the complexity level
    :param complexity: complexity level of the task
    :return: None
    """
    task = TASKS.get(complexity)
    if task:
        st.markdown(f"### Your Task\n{task['description']}")
        display_examples(task['examples'])
        st.markdown("### Additional Info")
        display_additional_info(task['additional_info'])
        st.markdown("### Solution Template")
        st.code(task['template'], language="python", wrap_lines=True)
        display_hints(task['hints'])
        st.divider()
        st.markdown("***Sourced from https://leetcode.com/***")
    else:
        st.error("Invalid task complexity")

def display_hints(hints):
    """
    Display hints for the task
    :param hints: list of hints
    :return: None
    """
    with st.expander("💡 See/hide hints", expanded=False):
        for hint in hints:
            st.markdown(f"### {hint['title']}")
            st.markdown(f"\n{hint['description']}")

def display_examples(examples):
    """
    Display examples for the task
    :param examples: list of examples
    :return: None
    """
    with st.expander("📝 See/hide examples", expanded=True):
        for example in examples:
            st.markdown(f"### {example['title']}")
            st.markdown(f"**Input:**\n```\n{example['input']}\n```")
            st.markdown(f"**Output:** `{example['output']}`")
            st.markdown(f"**Explanation:**\n{example['explanation']}")

def display_additional_info(info):
    """
    Display additional information for the task
    :param info: additional information
    :return: None
    """
    info = info.split('\n')
    info_list = "\n".join([f"- {i}" for i in info])
    st.markdown(info_list)

def get_task_for_prompt(complexity):
    """
    Generate a prompt for the task based on the complexity level
    :param complexity: complexity level of the task
    :return: formatted prompt
    """
    task = TASKS.get(complexity)
    if not task:
        return "Invalid task complexity"

    prompt = f"Task Description: {task['description']}\n\n"
    prompt += "Examples:\n"
    for example in task['examples']:
        prompt += f"{example['title']}:\n"
        prompt += f"Input: {example['input']}\n"
        prompt += f"Output: {example['output']}\n"
        prompt += f"Explanation: {example['explanation']}\n\n"
    prompt += f"Additional Info: {task['additional_info']}\n"

    for hint in task["hints"]:
        prompt += f"{hint['title']}:\n"
        prompt += f"{hint['description']}\n"

    return prompt

def get_task_template_for_prompt(complexity):
    """
    Generate a prompt for the task template based on the complexity level
    :param complexity: complexity level of the task
    :return: formatted prompt
    """
    task = TASKS.get(complexity)
    if not task:
        return "Invalid task complexity"
    template = task['template']
    prompt = f"The template for the solution is: \n" + template
    return prompt

def get_task_description(complexity):
    """
    Generate a task description for the given complexity level
    :param complexity: complexity level of the task
    :return: formatted task description
    """
    return get_task_for_prompt(complexity) + "\n\n" + get_task_template_for_prompt(complexity)
