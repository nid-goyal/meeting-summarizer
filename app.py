import streamlit as st
from google import genai
from google.genai import types

# Page setup
st.set_page_config(
    page_title="Meeting Summarizer & Task Extractor",
    page_icon="📝",
    layout="wide"
)

st.title("📝 AI Meeting Notes Summarizer & Action Item Extractor")
st.write("Transform raw meeting transcripts into executive summaries and structured action items instantly.")

# Sidebar setup
st.sidebar.header("Configuration")
api_key_input = st.sidebar.text_input("Enter Gemini API Key:", type="password")
st.sidebar.markdown("---")
st.sidebar.info("Get a free key from [Google AI Studio](https://aistudio.google.com/).")

# Main transcript input
transcript_text = st.text_area(
    "Paste Meeting Transcript / Notes:",
    height=250,
    placeholder="e.g.,\nJohn: We need to finalize the Q4 marketing plan by Friday. Sarah will handle budget numbers.\nSarah: Sounds good, I'll email the draft by Thursday afternoon."
)

if st.button("Generate Summary & Action Items", type="primary"):
    if not api_key_input:
        st.error("Please enter your Gemini API Key in the sidebar to proceed.")
    elif not transcript_text.strip():
        st.warning("Please paste a transcript before running.")
    else:
        try:
            client = genai.Client(api_key=api_key_input)

            system_prompt = """
            You are an expert executive assistant and business operations specialist.
            Your task is to analyze the meeting transcript and extract:
            1. Key Discussion Points (Executive Summary)
            2. Action Items (Owner, Task Description, Due Date)

            Guardrails:
            - Stick strictly to facts mentioned in the transcript. Do NOT hallucinate tasks or owners not present in the text.
            - If the input text is off-topic, gibberish, or not a meeting transcript, refuse to analyze and state clearly that invalid input was provided.
            """

            with st.spinner("Analyzing transcript with Gemini AI..."):
                response = client.models.generate_content(
                    model='gemini-2.0-flash',
                    contents=f"Transcript:\n\"\"\"{transcript_text}\"\"\"",
                    config=types.GenerateContentConfig(
                        system_instruction=system_prompt,
                        temperature=0.2,
                    )
                )

                st.markdown("### 📌 Executive Summary & Action Items")
                st.write(response.text)

        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
