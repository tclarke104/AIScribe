import time
import numpy as np
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain
from langchain.prompts import PromptTemplate
from langchain_community.llms import Ollama
import whisper



MODEL = 'gemma2'
stt = whisper.load_model("large-v3", device="cuda")

NOTE_TEMPLATE = """
{
    "chief_complaint": CHIEF COMPLAINT HERE,
    "history_of_present_illness": HPI HERE,
    "social_history": SOCIAL HISTORY HERE,
    "medications": LIST MEDICATIONS HERE IN A BULLETED LIST KNOWN MEDICATIONS,
    "past_medical_history": PAST MEDICAL HISTORY HERE,
    "physical_exam": PHYSICAL EXAM HERE,
    "assessment": ASSESSMENT HERE THAT BEGINS WITH ONE LINER WITH DEMOGRAPHICS AND CHIEF COMPLAINT,
    "plan": PLAN HERE
}
"""


TEMPLATE = """
You are a helpful and friendly AI medical scribe. 
Based on the following traNscription of a patient interaction generate a note
{history}
respond in the following json format
{note_template}
Your response:
"""
prompt = PromptTemplate(input_variables=["history", "note_template"], template=TEMPLATE)
chain = prompt | Ollama(model= MODEL,format='json')


def transcribe(file_path) -> str:
    """
    Transcribes the given audio data using the Whisper speech recognition model.
    Args:
        audio_np (numpy.ndarray): The audio data to be transcribed.
    Returns:
        str: The transcribed text.
    """

    result = stt.transcribe(file_path, fp16=False)  # Set fp16=True if using a GPU
    text = result["text"].strip()
    return text

def get_llm_response(text: str) -> str:
    """ 
    Generates a response to the given text using the Phi-3 language model.
    Args:
        text (str): The input text to be processed.
    Returns:
        str: The generated response.
    """
    response = chain.invoke({'history':text, 'note_template': NOTE_TEMPLATE})
    if response.startswith("Assistant:"):
        response = response[len("Assistant:") :].strip()
    return response
