import time
import numpy as np
import sounddevice as sd
from rich.console import Console
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain
from langchain.prompts import PromptTemplate
from langchain_community.llms import Ollama
import whisper

console = Console()


MODEL = 'gemma2'
stt = whisper.load_model("base.en")

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


def record_audio(stop_event, data_queue):
    """
    Captures audio data from the user's microphone and adds it to a queue for further processing.
    Args:
        stop_event (threading.Event): An event that, when set, signals the function to stop recording.
        data_queue (queue.Queue): A queue to which the recorded audio data will be added.
    Returns:
        None
    """
    def callback(indata, frames, time, status):
        if status:
            console.print(status)
        data_queue.put(bytes(indata))

    with sd.RawInputStream(
        samplerate=16000, dtype="int16", channels=1, callback=callback
    ):
        while not stop_event.is_set():
            time.sleep(0.1)

def transcribe(audio_np: np.ndarray) -> str:
    """
    Transcribes the given audio data using the Whisper speech recognition model.
    Args:
        audio_np (numpy.ndarray): The audio data to be transcribed.
    Returns:
        str: The transcribed text.
    """
    result = stt.transcribe(audio_np, fp16=False)  # Set fp16=True if using a GPU
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
