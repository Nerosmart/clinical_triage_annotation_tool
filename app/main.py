import streamlit as st
import json
from pathlib import Path
from streamlit_highlighter.component import highlighter

result = highlighter("Some referral text here", key="ref1")
st.write(result)

# -------------------------------
# STREAMLIT APP FOR CONFIGURATION
# -------------------------------
st.set_page_config(
    page_title="Clinical Triage Annotation Tool",
    layout="wide",
)

# App title and short description to guide users. 
st.title("Clinical Triage Annotation Tool")
st.write("Annotate referral documents for clinical triage decisions.")

# ------------------------------
# INITIALISE SESSION STATE
# ------------------------------
if "annotations" not in st.session_state:
    st.session_state.annotations = []

# ------------------------------
# LOAD REFERRAL FILES
# ------------------------------
REFERRAL_DIR = Path("data/raw_referrals")
referral_files = sorted([f.name for f in REFERRAL_DIR.glob("*.txt")])

selected_file = st.selectbox("Choose a referral", referral_files)

if selected_file:

    # Load referral text
    file_path = REFERRAL_DIR / selected_file
    referral_text = file_path.read_text(encoding="utf-8")

    # ------------------------------
    # DISPLAY REFERRAL TEXT
    # ------------------------------
    st.subheader("Referral Text")
    st.write(referral_text)

    # ------------------------------
    # INTERACTIVE HIGHLIGHTER
    # ------------------------------
    st.subheader("Highlight the referral")

    selection = highlighter(referral_text, key="highlighter")

    if selection:
        st.write("Selected text:", selection["text"])
        st.write("Start:", selection["start"])
        st.write("End:", selection["end"])

        label = st.selectbox(
            "Label this highlight",
            ["Symptom", "Red Flag", "Medication", "Risk Factor", "Other"],
            key="label_selector"
        )

        if st.button("Add Highlight"):
            st.session_state.annotations.append({
                "text": selection["text"],
                "start": selection["start"],
                "end": selection["end"],
                "label": label
            })
            st.success("Highlight added")

    # ------------------------------
    # TRIAGE DECISION INPUTS
    # ------------------------------
    st.subheader("Triage Decision")

    accept = st.selectbox("Accept or Reject", ["Accept", "Reject"])
    urgency = st.selectbox("Urgency", ["Routine", "Urgent"])
    timescale = st.selectbox("Timescale", ["N/A", "2 weeks", "6 weeks", "12 weeks", "same-day"])
    clinic = st.selectbox(
        "Clinic Type",
        [
            "Chest Pain",
            "Heart Failure",
            "Atrial Fibrillation",
            "Syncope",
            "Valve Disease",
            "General Cardiology"
        ]
    )

    # ------------------------------
    # SAVE ANNOTATION
    # ------------------------------
    if st.button("Save Annotation"):
        annotation = {
            "file": selected_file,
            "spans": st.session_state.annotations,
            "triage_decision": {
                "accept": accept,
                "urgency": urgency,
                "timescale": timescale,
                "clinic": clinic
            }
        }

        save_path = Path("data/annotations") / f"{selected_file}.json"
        save_path.parent.mkdir(parents=True, exist_ok=True)

        with open(save_path, "w", encoding="utf-8") as f:
            json.dump(annotation, f, indent=4)

        st.success(f"Annotation saved to {save_path}")