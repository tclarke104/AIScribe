import streamlit as st
from audiorecorder import audiorecorder
import helpers
import numpy as np
from st_audiorec import st_audiorec

st.title('AI Scribe')

st.write('Hit record button below to start recording audio')
audio = audiorecorder("Click to record", "Click to stop recording")

if audio:
    audio.export("audio.wav", format="wav")
    with st.spinner('Transcribing Audio'):
        text = helpers.transcribe("audio.wav")
    st.write(f'Transcription: {text}')
    with st.spinner('Generating Note'):
        response = helpers.get_llm_response(text)
    st.write(response)