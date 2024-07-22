import time
import threading
import numpy as np
import sounddevice as sd
from queue import Queue
from rich.console import Console
import helpers

console = Console()

SAMPLE_TEXT = """
Hello Dr. Clark. I'm coming in today because I've got really bad diarrhea. How long has it been
going on for? It has been going on for the last two weeks actually. Okay. What do you think is going
on? You know, hard to say. I think this has happened before. But the last time it happened I was on a
cruise going down to the Bahamas. That was maybe like three years ago. Okay. Have you been recently on
any new cruises? No, but I did go on a trip down to Florida with my cousin. We should have done this
the opposite way. What other medicines do you have? I have high blood pressure and I'm told by my
doctor that I've got a bad heart. I think it's something about how it doesn't squeeze very well. Other
than that, I have high cholesterol and I have diabetes. And I got a hernia out taking care of about
five years ago. It's a hernia in my groin. Are you taking any medications? Yes. I take my toperolol, 50
milligrams daily. I take a lusarcon, 50 milligrams daily. I take a medicine called jardience, 10
milligrams daily. I also take Torvastatin, 40 milligrams daily. And what else do I take? Oh, I take
this medicine aspirin, baby aspirin. 81 milligrams? 81 milligrams, yes. Okay. Yes, doctor. And do you
smoke? Yes, I do. Six packs a day. Do you drink alcohol? Yes. I have one, one piña colada every night.
Okay. Tell me about your living situation. I live at Home Alone with my seven dogs and my two parrots.
And I also have a cat. And my house is six stories, but one bedroom per floor. It's basically like a
silo, sort of like a grain silo, if you will, that refurbished. And yeah, that's my living situation.
Okay. Do you mind if we do a physical exam? No, exam. All right. Your head looks like there's no acute
problems. Your normal syphallic and atramatic. Your lungs sound clear to oscopation, and you have no
labor breathing. Your heart has a normal rate in rhythm without any rumors. Robs are gallops. Your
abdomen is soft and non-distended, however, just tender in the right lower quadrant. Actually, scratch
that right up the quadrant. Otherwise, physical exam is normal. So, based off of what I'm seeing, looks
like you have, say, you have billiard collock. Oh, that explains a lot. And so our plan for you is
going to be, we're going to get an ultrasound of your gallbladder to see if we can see anything going
on there. We need to change your diet. We want to avoid fatty food such as meat, some things like that.
And I'll see you back in one month. Thanks.
"""

if __name__ == "__main__":
    console.print("[cyan]Assistant started! Press Ctrl+C to exit.")
    with console.status("Generating response...", spinner="earth"):
        response = helpers.get_llm_response(SAMPLE_TEXT)

    console.print(f"[cyan]Assistant: {response}")
    # try:
    #     while True:
    #         console.input(
    #             "Press Enter to start recording, then press Enter again to stop."
    #         )

    #         data_queue = Queue()  # type: ignore[var-annotated]
    #         stop_event = threading.Event()
    #         recording_thread = threading.Thread(
    #             target=helpers.record_audio,
    #             args=(stop_event, data_queue),
    #         )
    #         recording_thread.start()

    #         input()
    #         stop_event.set()
    #         recording_thread.join()

    #         audio_data = b"".join(list(data_queue.queue))
    #         audio_np = (
    #             np.frombuffer(audio_data, dtype=np.int16).astype(np.float32) / 32768.0
    #         )

    #         if audio_np.size > 0:
    #             with console.status("Transcribing...", spinner="earth"):
    #                 text = helpers.transcribe(audio_np)
    #             console.print(f"[yellow]You: {text}")

    #             with console.status("Generating response...", spinner="earth"):
    #                 response = helpers.get_llm_response(text)

    #             console.print(f"[cyan]Assistant: {response}")
    #         else:
    #             console.print(
    #                 "[red]No audio recorded. Please ensure your microphone is working."
    #             )

    # except KeyboardInterrupt:
    #     console.print("\n[red]Exiting...")

    console.print("[blue]Session ended.")