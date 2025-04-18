import json

import streamlit as st

from helper.navigation import forward
from helper.navigation import get_header

def main():
    st.set_page_config(page_title="Post-Experiment Survey", menu_items={'Get Help': 'mailto:wendi.shu@stud.tu-darmstadt.de'}, layout="wide")
    # go to start if no session state
    if 'participant_id' not in st.session_state:
        st.switch_page("app.py")
    participant_id = st.session_state["participant_id"]

    try:
        with open("data/participants/participant_" + participant_id + ".json", "r") as f:
            data = json.load(f)
    except FileNotFoundError:
        st.switch_page("app.py")

    get_header(4, "pages/task.py", True, False, data, participant_id)

    st.title("Post-Experiment Survey")
    BASIC_LIKERT_OPTIONS = ["Strongly disagree", "Disagree", "Somewhat disagree", "Neutral", "Somewhat agree", "Agree", "Strongly agree"]


    def save_and_continue():
        data["next_page"] = "tool_preference.py"
        with open("data/participants/participant_" + participant_id + ".json", "w") as file:
            json.dump(data, file)
        forward("pages/tool_preference.py", False, False, None, None)


    def validate_taif_form(taif1, taif2, taif3, taif4, taif5, haif1, haif2, haif3, haif4, haif5, rq1, rq2, rq3, ltui1, ltui2, ltui3, haif5_reason):
        errors = {}
        if not taif1 or not taif2 or not taif3 or not taif4 or not taif5 or not haif1 or not haif2 or not haif3 or not haif4 or not haif5 or not rq1 or not rq2 or not rq3 or not ltui1 or not ltui2 or not ltui3:
            errors["incomplete"] = "Please fill out all mandatory fields."
        if (haif5 == "Strongly agree" or haif5 == "Agree" or haif5 == "Somewhat agree") and not haif5_reason:
            errors["haif5_reason"] = "Please specify why you felt frustrated."
        return errors

    def show_taif_survey():
        st.markdown(f"*Please fill out the following survey to help us understand your experience with the GenAI tool that was provided to you.*")
        st.markdown(f"Your feedback is valuable! Please ***carefully read and answer*** each question in this survey.")
        st.divider()

        #TAIF
        st.text("")
        st.markdown("**The functionalities of the GenAI tool were very compatible with my task.**")
        taif1_index = None
        if "TAIF1" in data and data['TAIF1']:
            taif1_index = BASIC_LIKERT_OPTIONS.index(data["TAIF1"])
        taif1 = st.radio(
            label="**The functionalities of the GenAI tool were very compatible with my task.**",
            label_visibility="collapsed",
            options=BASIC_LIKERT_OPTIONS,
            index=taif1_index,
            horizontal=True)

        st.text("")
        st.markdown("**The functionalities of the GenAI tool were very useful.**")
        taif2_index = None
        if "TAIF2" in data and data['TAIF2']:
            taif2_index = BASIC_LIKERT_OPTIONS.index(data["TAIF2"])
        taif2 = st.radio(label="**The functionalities of the GenAI tool were very useful.**",
                         label_visibility="collapsed",
                         options=BASIC_LIKERT_OPTIONS,
                         index=taif2_index,
                         horizontal=True)

        st.text("")
        st.markdown("**The GenAI tool made the task easy.**")
        taif3_index = None
        if "TAIF3" in data and data['TAIF3']:
            taif3_index = BASIC_LIKERT_OPTIONS.index(data["TAIF3"])
        taif3 = st.radio(label="**The GenAI tool made the task easy.**",
                         label_visibility="collapsed",
                         options=BASIC_LIKERT_OPTIONS,
                         index=taif3_index,
                         horizontal=True)

        st.text("")
        st.markdown("**Using the GenAI tool fitted the way I work.**")
        taif4_index = None
        if "TAIF4" in data and data['TAIF4']:
            taif4_index = BASIC_LIKERT_OPTIONS.index(data["TAIF4"])
        taif4 = st.radio(label="**Using the GenAI tool fitted the way I work.**",
                         label_visibility="collapsed",
                         options=BASIC_LIKERT_OPTIONS,
                         index=taif4_index,
                         horizontal=True)

        st.text("")
        st.markdown("**In general, the functionalities of the GenAI tool were best fit to the task.**")
        taif5_index = None
        if "TAIF5" in data and data['TAIF5']:
            taif5_index = BASIC_LIKERT_OPTIONS.index(data["TAIF5"])
        taif5 = st.radio(label="**In general, the functionalities of the GenAI tool were best fit to the task.**",
                         label_visibility="collapsed",
                         options=BASIC_LIKERT_OPTIONS,
                         index=taif5_index,
                         horizontal=True)

        st.divider()
        # HAIF
        st.markdown("**The GenAI tool was very compatible with my needs for completing the task.**")
        haif1_index = None
        if "HAIF1" in data and data['HAIF1']:
            haif1_index = BASIC_LIKERT_OPTIONS.index(data["HAIF1"])
        haif1 = st.radio(label="**The GenAI tool was very compatible with my needs for completing the task.**",
                         label_visibility="collapsed",
                         options=BASIC_LIKERT_OPTIONS,
                         index=haif1_index,
                         horizontal=True)

        st.text("")
        st.markdown("**The GenAI tool fitted my way of seeking assistance or information.**")
        haif2_index = None
        if "HAIF2" in data and data['HAIF2']:
            haif2_index = BASIC_LIKERT_OPTIONS.index(data["HAIF2"])
        haif2 = st.radio(label="**The GenAI tool fitted my way of seeking assistance or information.**",
                         label_visibility="collapsed",
                         options=BASIC_LIKERT_OPTIONS,
                         index=haif2_index,
                         horizontal=True)

        st.text("")
        st.markdown("**The overall interaction with the GenAI tool aligned with my preferences.**")
        haif3_index = None
        if "HAIF3" in data and data['HAIF3']:
            haif3_index = BASIC_LIKERT_OPTIONS.index(data["HAIF3"])
        haif3 = st.radio(label="**The overall interaction with the GenAI tool aligned with my preferences.**",
                         label_visibility="collapsed",
                         options=BASIC_LIKERT_OPTIONS,
                         index=haif3_index,
                         horizontal=True)

        st.text("")
        st.markdown("**The response style of the GenAI tool aligned with my preferences.**")
        haif4_index = None
        if "HAIF4" in data and data['HAIF4']:
            haif4_index = BASIC_LIKERT_OPTIONS.index(data["HAIF4"])
        haif4 = st.radio(label="**The response style of the GenAI tool aligned with my preferences.**",
                         label_visibility="collapsed",
                         options=BASIC_LIKERT_OPTIONS,
                         index=haif4_index,
                         horizontal=True)

        st.text("")
        st.markdown("**I felt very frustrated during the interaction with the GenAI tool.**")
        haif5_index = None
        haif5_reason = None
        haif5_reason_value = None
        if "HAIF5" in data and data['HAIF5']:
            haif5_index = BASIC_LIKERT_OPTIONS.index(data["HAIF5"])
        haif5 = st.radio(label="**I felt very frustrated during the interaction with the GenAI tool.**",
                         label_visibility="collapsed",
                         options=BASIC_LIKERT_OPTIONS,
                         index=haif5_index,
                         horizontal=True)
        if "HAIF5_reason" in data and data["HAIF5_reason"]:
            haif5_reason_value = data["HAIF5_reason"]
        if haif5 == "Strongly agree" or haif5 == "Agree" or haif5 == "Somewhat agree":
            st.markdown("**Please tell us why you felt frustrated:**")
            haif5_reason = st.text_input(label="**Please tell us why you felt frustrated:**",
                                         value=haif5_reason_value,
                                         label_visibility="collapsed",
                                         placeholder="Please specify shortly why you felt frustrated.")

        st.divider()
        # RQ
        st.markdown("**The GenAI tool helped me solve my task more effectively.**")
        rq1_index = None
        if "RQ1" in data and data['RQ1']:
            rq1_index = BASIC_LIKERT_OPTIONS.index(data["RQ1"])
        rq1 = st.radio(label="**The GenAI tool helped me solve my task more effectively.**",
                       label_visibility="collapsed",
                       options=BASIC_LIKERT_OPTIONS,
                       index=rq1_index,
                       horizontal=True)

        st.text("")
        st.markdown("**The GenAI tool had a positive impact on my ability to complete the task efficiently.**")
        rq2_index = None
        if "RQ2" in data and data['RQ2']:
            rq2_index = BASIC_LIKERT_OPTIONS.index(data["RQ2"])
        rq2= st.radio(label="**The GenAI tool had a positive impact on my ability to complete the task efficiently.**",
                      label_visibility="collapsed",
                      options=BASIC_LIKERT_OPTIONS,
                      index=rq2_index,
                      horizontal=True)

        st.text("")
        st.markdown("**The GenAI tool was able to aid me in completing the task successfully.**")
        rq3_index = None
        if "RQ3" in data and data['RQ3']:
            rq3_index = BASIC_LIKERT_OPTIONS.index(data["RQ3"])
        rq3 = st.radio(label="**The GenAI tool was able to aid me in completing the task successfully.**",
                       label_visibility="collapsed",
                       options=BASIC_LIKERT_OPTIONS,
                       index=rq3_index,
                       horizontal=True)

        st.divider()
        #LTUI
        st.markdown("**Given that I had access, I intend to continue using this GenAI tool rather than discontinue it.**")
        ltui1_index = None
        if "LTUI1" in data and data['LTUI1']:
            ltui1_index = BASIC_LIKERT_OPTIONS.index(data["LTUI1"])
        ltui1 = st.radio(label="**Given that I had access, I intend to continue using this GenAI tool rather than discontinue it.**",
                         label_visibility="collapsed",
                         options=BASIC_LIKERT_OPTIONS,
                         index=ltui1_index,
                         horizontal=True)

        st.text("")
        ltui2_index = None
        if "LTUI2" in data and data['LTUI2']:
            ltui2_index = BASIC_LIKERT_OPTIONS.index(data["LTUI2"])
        ltui2_label_default = "I would prefer using this GenAI tool rather than using any alternative means."
        ltui2_label_tailored = "I would prefer using this GenAI tool with the given features rather than using any alternative means.*"
        ltui2_label = ltui2_label_default
        st.markdown(f"**{ltui2_label}**")
        if "assigned_group" in data and data["assigned_group"] == "group_tailored":
            ltui2_label = ltui2_label_tailored
        ltui2 = st.radio(label=f"**{ltui2_label}**",
                         label_visibility="collapsed",
                         options=BASIC_LIKERT_OPTIONS,
                         index=ltui2_index,
                         horizontal=True)

        st.text("")

        ltui3_index = None
        ltui3_label_default = "Given that I had access, I will not discontinue my use of this GenAI tool for software development tasks."
        ltui3_label_tailored = "Given that I had access, I will not discontinue my use of this GenAI tool with the given features for software development tasks."
        ltui3_label = ltui3_label_default
        if "assigned_group" in data and data["assigned_group"] == "group_tailored":
            ltui3_label = ltui3_label_tailored
        if "LTUI3" in data and data['LTUI3']:
            ltui3_index = BASIC_LIKERT_OPTIONS.index(data["LTUI3"])
        st.markdown(f"**{ltui3_label}**")
        ltui3 = st.radio(label=f"**{ltui3_label}**",
                         label_visibility="collapsed",
                         options=BASIC_LIKERT_OPTIONS,
                         index=ltui3_index,
                         horizontal=True)

        st.divider()
        st.markdown(f"**Did you use any other tools or resources (e.g. a search engine) while solving the task? If yes, please specify: (optional)**", unsafe_allow_html=True)
        other_resources = st.text_input(label="**Did you use any other tools or resources (e.g. a search engine) while solving the task? If yes, please specify:**",
                                    label_visibility="collapsed",
                                    placeholder="Please specify the tools or resources you used.")
        st.markdown(f"**Is there anything you especially <u>liked</u> about the GenAI tool that you were given? If yes, please specify: (optional)**", unsafe_allow_html=True)
        liked_features = st.text_input(label="**Is there anything you especially liked about the GenAI tool that you were given? If yes, please specify:**",
                                    label_visibility="collapsed",
                                    placeholder="Please specify what you liked about the GenAI tool.")

        st.markdown(f"**Is there anything you especially <u>disliked</u> about the GenAI tool that you were given? If yes, please specify: (optional)**", unsafe_allow_html=True)
        disliked_features = st.text_input(label="**Is there anything you especially disliked about the GenAI tool that you were given? If yes, please specify:**",
                                    label_visibility="collapsed",
                                    placeholder="Please specify what you disliked about the GenAI tool.")

        st.markdown(f"**Is there anything else you would like to share? (optional)**")
        others_shared = st.text_area(label="Is there anything else you would like to share?",
                                     label_visibility="collapsed",
                                     placeholder="Please share your thoughts here.",
                                     height=200)

        # Finish
        st.text("")
        st.text("")
        st.text("")

        st.divider()
        left, middle, right = st.columns([12,8,4])
        if right.button("Continue →", key="taif_continue", type="primary"):
            # Clear previous error messages
            errors = validate_taif_form(taif1, taif2, taif3, taif4, taif5, haif1, haif2, haif3, haif4, haif5, rq1, rq2, rq3, ltui1, ltui2, ltui3, haif5_reason)
            if errors:
                if "incomplete" in errors and errors["incomplete"]:
                    st.error(errors["incomplete"])
                if "haif5_reason" in errors and errors["haif5_reason"]:
                    st.error(errors["haif5_reason"])
            else:
                if taif1:
                    data['TAIF1'] = taif1
                if taif2:
                    data['TAIF2'] = taif2
                if taif3:
                    data['TAIF3'] = taif3
                if taif4:
                    data['TAIF4'] = taif4
                if taif5:
                    data['TAIF5'] = taif5
                if haif1:
                    data['HAIF1'] = haif1
                if haif2:
                    data['HAIF2'] = haif2
                if haif3:
                    data['HAIF3'] = haif3
                if haif4:
                    data['HAIF4'] = haif4
                if haif5:
                    data['HAIF5'] = haif5
                if haif5_reason:
                    data['HAIF5_reason'] = haif5_reason
                if rq1:
                    data['RQ1'] = rq1
                if rq2:
                    data['RQ2'] = rq2
                if rq3:
                    data['RQ3'] = rq3
                if ltui1:
                    data['LTUI1'] = ltui1
                if ltui2:
                    data['LTUI2'] = ltui2
                if ltui3:
                    data['LTUI3'] = ltui3
                if others_shared:
                    data['others_shared'] = others_shared
                if other_resources:
                    data['other_resources'] = other_resources
                if liked_features:
                    data['liked_features'] = liked_features
                if disliked_features:
                    data['disliked_features'] = disliked_features

                save_and_continue()

    def validate_nir(nir_knowledge_val, nir_trust_val, nir_want_val, nir_see_val, nir_need_val, nir_other_val, nir_text_val):
        errors = {}
        if not (nir_knowledge_val or nir_trust_val or nir_want_val or nir_see_val or nir_need_val or nir_other_val):
            errors["nir_checkbox"] = "Please check at least one reason. If none of the suggested reasons apply to you, please select 'Other'."
        if nir_other_val and not nir_text_val:
            errors["nir_text"] = "Please specify the reason for not using the chatbot."
        return errors


    def show_non_interaction_survey():
        #NIR = Non-Interaction Reasons
        st.info("We noticed that you did not interact with the GenAI tool during the experiment. Therefore, we would like to ask you a few questions to understand why.")
        st.divider()
        nir_knowledge = False
        nir_trust = False
        nir_want = False
        nir_see = False
        nir_need = False
        nir_other = False
        nir_text_value = None
        if "NIR_knowledge" in data and data["NIR_knowledge"]:
            nir_knowledge = data["NIR_knowledge"]
        if "NIR_trust" in data and data["NIR_trust"]:
            nir_trust = data["NIR_trust"]
        if "NIR_want" in data and data["NIR_want"]:
            nir_want = data["NIR_want"]
        if "NIR_see" in data and data["NIR_see"]:
            nir_see = data["NIR_see"]
        if "NIR_need" in data and data["NIR_need"]:
            nir_need = data["NIR_need"]
        if "NIR_other" in data and data["NIR_other"]:
            nir_other = data["NIR_other"]
        if "nir_text" in data and data["nir_text"]:
            nir_text_value = data["nir_text"]

        st.markdown("**Please check the reasons for not using the chatbot that apply to you.**")
        nir_knowledge = st.checkbox(label="I did **not know how** to use the GenAI tool", value=nir_knowledge)
        nir_trust = st.checkbox(label="I did **not trust** the GenAI tool", value=nir_trust)
        nir_want = st.checkbox(label="I did **not want** to use the GenAI tool", value=nir_want)
        nir_see = st.checkbox(label="I did **not see** the GenAI tool", value=nir_see)
        nir_need = st.checkbox(label="I did **not need** the GenAI tool", value=nir_need)
        nir_other = st.checkbox(label="Other", value=nir_other)
        st.write("")
        st.markdown("**Please elaborate on why you did not interact with the chatbot.**")
        nir_text = st.text_area(label="Please briefly **elaborate** on why you did not interact with the chatbot.",
                                label_visibility="collapsed",
                                value=nir_text_value,
                                placeholder="Bullet points or full sentences are both fine")

        left, middle, right = st.columns([12, 8, 4])
        with right:
            st.write("")
            st.write("")
            st.divider()

            if st.button("Continue →", type="primary"):
                errors = validate_nir(nir_knowledge, nir_trust, nir_want, nir_see, nir_need, nir_other, nir_text)
                if errors:
                    if "nir_checkbox" in errors and errors["nir_checkbox"]:
                        st.error(errors["nir_checkbox"])
                    if "nir_text" in errors and errors["nir_text"]:
                        st.error(errors["nir_text"])
                else:
                    data["NIR_knowledge"] = nir_knowledge
                    data["NIR_trust"] = nir_trust
                    data["NIR_want"] = nir_want
                    data["NIR_see"] = nir_see
                    data["NIR_need"] = nir_need
                    data["NIR_other"] = nir_other
                    data["non_interaction_reasons_text"] = nir_text
                    save_and_continue()



    if "live_message_generate" in data and data["live_message_generate"] and (any(msg.get("role") == "user" for msg in data.get("live_message_generate", []) if isinstance (msg, dict))):
        show_taif_survey()
    else:
        show_non_interaction_survey()

if __name__ == "__main__":
    main()