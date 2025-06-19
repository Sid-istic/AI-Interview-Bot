import google.generativeai as genai
from dotenv import load_dotenv
import json
import random
import re
import requests
import base64
from io import BytesIO
import os
import streamlit as st
from elevenlabs import play, save,ElevenLabs
import io
import time
import tempfile
from audio_recorder_streamlit import audio_recorder
from io import StringIO
import Interview_evaluation
import stt
import resume_parsing
import jobrole_prediction

load_dotenv()
# 1. Configure the APIs
def setup_voice(api_key):
    elevenlabs = ElevenLabs(
    api_key=api_key,
    )

if "voice_id" not in st.session_state:
    st.session_state.voice_id = ""
# 2. Create the model instance
def get_model_name(personality,prompt,api_key):
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel(
        model_name='gemini-1.5-flash',  # or 'gemini-2.0-flash'
        system_instruction=prompt
    )
    return model


# getting the personality of interviewer from interviewer_personality.json using random choice
def get_interviewer_personality():
    with open('app/interviewer_personalities.json', 'r') as file:
        personalities = json.load(file)
    return random.choice(personalities)

st.set_page_config(
    page_title="Botted Interview UI",
    page_icon="🤖",
    layout="centered"
)
# Initialize session state for messages
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hello! Shall we Start with interview?"}
    ]
if "chat" not in st.session_state:
    st.session_state.chat = None  # Set a default value

st.title(" :blue[Welcome],:orange[Candidate]:red[!!]")
st.markdown("This is an :blue-background[Interview Bot] who is gonna :green[help] you prepare for your upcoming :red[INTERVIEWES.]")
def typewriter(text):
    for word in text.split():
        yield word + " "
        time.sleep(0.1)  # Adjust speed

if "voice_id" not in st.session_state:
    st.session_state.voice_id = ""

with st.sidebar:
    tab1, tab2,tab3= st.tabs(["Upload Resume", "Select Yourself","Controls"])

    with tab1:
        st.header("Upload PDF file")
        uploaded_file = st.file_uploader("Choose a file")
        api_key = st.text_input("Gemini API KEY")
        ElevenLabs_api = st.text_input("ElevenLabs API KEY")
        setup_voice(ElevenLabs_api)
        Experience = st.selectbox("Experience Level",("Entry-Level", "Mid-Level", "Senior-Level"),key = "Re")
        if uploaded_file is not None:
        # To read file as bytes:
            if st.button("Submit"):
                bytes_data = uploaded_file.getvalue()
                personality = get_interviewer_personality()
                st.session_state.voice_id = personality["voice_id"]
                info = resume_parsing.extract_clean_text(bytes_data)
                Job_Role = jobrole_prediction.predict(bytes_data)
                prompt = f"""You are a technical interviewer named {personality['name']} and {personality['prompt']}.
                - Name of Candidate is {info["name"]} who is applying for {Job_Role} position and has {Experience}.
                -candidate has these skills {info["skills"]}
                - Ask one question at a time which should include Behavioral Questions,Technical Questions and Cultural Fit Questions.
                - Shuffle the Question type after 2 or 3 follow up questions
                - Wait for complete responses
                - Provide follow-ups based on answers
                - Keep responses under 50 words most of the times"""
                st.write(f"Your Interviewer is {personality['name']}")
                # 3. Start the chat session (THIS IS THE CORRECT WAY)
                st.session_state.chat = get_model_name(personality,prompt,api_key).start_chat(history=[])
                st.write(info)
                st.write(Job_Role)



    with tab2:
        st.header("Please Fill in the following")
        Name = st.text_input("Candidates Name",placeholder="Your Name")
        Job_Role = st.text_input("Enter the Job Role",placeholder="e.g., SDE,Data Analyst etc")
        Experience = st.selectbox("Experience Level",("Entry-Level", "Mid-Level", "Senior-Level"),key = "manualexp")
        api_key = st.text_input("Gemini API KEY",key = "manualGemini")
        ElevenLabs_api = st.text_input("ElevenLabs API KEY",key = "manual")
        setup_voice(ElevenLabs_api)
        if st.button("Start Interview",type = "primary"):
            if not Name or not Job_Role:
                st.markdown(":red[Plesse fill in the required Details!!]")
            else:
                personality = get_interviewer_personality()
                st.session_state.voice_id = personality["voice_id"]
                prompt = f"""You are a technical interviewer named {personality['name']} and {personality['prompt']}.
                - Name of Candidate is {Name} who is applying for {Job_Role} position and has {Experience} experience.
                - Ask one question at a time which should include Behavioral Questions,Technical Questions and Cultural Fit Questions.
                - ask atleast one follow up questions and atmax two follow-up questions.
                - Wait for complete responses
                - Provide follow-ups based on answers
                - Keep responses under 50 words most of the times"""
                st.write(f"Your Interviewer is {personality['name']}")
                # 3. Start the chat session (THIS IS THE CORRECT WAY)
                st.session_state.chat = get_model_name(personality,prompt,api_key).start_chat(history=[])
    with tab3:
            st.header("Chat Controls")
            if st.button("End Interview"):
                file = 'chat_history.json'
                # Ensure messages are JSON serializable
                messages_serializable = [{"role": msg["role"], "content": str(msg["content"])} for msg in st.session_state.messages]
                with open(file, 'w') as f:
                    json.dump(messages_serializable, f)  # Dump the cleaned version

                st.session_state.messages = [
                    {"role": "assistant", "content": "Chat history cleared! CLick on Start Button to start the Interview?"}
                ]
                st.rerun()
            if st.button("Get Analysis"):
                evaluate = Interview_evaluation.save_and_evaluate()
                with open("app/chat_history_eval.md", "r") as file:
                    content = file.read()
                st.markdown(content)
                with open("app/chat_history.json", "r+") as file:
                    file.truncate(0)  # Clears all content

                with open("app/chat_history_eval.md", "r+") as file:
                    file.truncate(0)  # Clears all content
                if st.button("Download Analysis"):
                    st.download_button(
                        label="Download MP3",
                        data=content,
                        file_name="elevenlabs_tts.mp3",
                        mime="audio/mpeg"
                    )


            st.divider()
            st.markdown("**Features:**")
            st.markdown("- interviewer/interviewee message bubbles")
            st.markdown("- Chat history persistence")
            st.markdown("- Simple chat/voice input")
            st.markdown("- End interview button")
            st.divider()
            st.caption("Note: This is UI-only with no actual AI backend")
            st.divider()
            st.markdown("""P.S. This project is still a work in progress. While the core functionality is in place, additional testing, debugging, and optimization are needed to ensure accuracy and reliability. Future improvements may include better error handling, performance optimization, and possible deployment as a web app.
                        also the prediction model is not 100% accurate as the dataset used only had 42 job roles to predict from 
                        """)



# Initialize session state for messages
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": st.session_state.chat.send_message("Please begin the interview with greeting followed by a question.").text}
    ]

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

def generate_audio(text):
    with st.spinner("Generating Reaction"):                
        # Generate audio
        audio = elevenlabs.text_to_speech.convert(
            text=text,
            voice_id=st.session_state.voice_id,
            model_id="eleven_multilingual_v2",
            output_format="mp3_44100_128",
        )
        
        # Read audio bytes
        audio_bytes = b"".join(audio)
        
        # Convert audio to base64 for autoplay
        audio_base64 = base64.b64encode(audio_bytes).decode('utf-8')
        del audio_bytes
        
        # Create autoplay audio element
        audio_html = f"""
        <audio autoplay>
            <source src="data:audio/mpeg;base64,{audio_base64}" type="audio/mpeg">
            Your browser does not support the audio element.
        </audio>
        """
        st.markdown(audio_html, unsafe_allow_html=True)




def handle_message(input_text):
    # Add user message
    audio_bytes = None
    st.session_state.messages.append({"role": "user", "content": input_text})
    with st.chat_message("user"):
        st.markdown(input_text)
    
    # Generate bot response
    if st.session_state.chat:
        assistant_prompt = st.session_state.chat.send_message(f"Candidate response: {input_text}\n Ask an appropriate follow-up question or a new question")
        assistant_prompt = assistant_prompt.text
        #generate_audio(assistant_prompt)
        with st.chat_message("assistant"):
            st.write_stream(typewriter(assistant_prompt))
        st.session_state.messages.append(
            {"role": "assistant", "content": assistant_prompt}
        )
    else:
        st.warning("Chat session not initialized")



if prompt := st.chat_input("Type your message..."):
    # Handle TEXT input only
    handle_message(prompt)  # Your message processing logic
    
if "last_audio_transcript" not in st.session_state:
    st.session_state.last_audio_transcript = None

audio_bytes = audio_recorder(pause_threshold=2.0, text="", recording_color="#e8b62c", neutral_color="#6aa36f", icon_size="2x")

if audio_bytes:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_audio:
        temp_audio.write(audio_bytes)
        temp_path = temp_audio.name

    time.sleep(0.1)
    text = stt.transcribe_audio(temp_path)
    
    if text and text != st.session_state.last_audio_transcript:
        handle_message(text)
        st.session_state.last_audio_transcript = text

