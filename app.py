import base64
import requests
import streamlit as st
from PIL import Image
from audiorecorder import audiorecorder


import tempfile
import os
import logging
import time
# from fastapi import FastAPI, UploadFile, HTTPException, Response
from deployment.speech_inference import SpeechTranscriptionPipeline, ModelOptimization
# from fastapi.responses import FileResponse, JSONResponse, Response
from dotenv import load_dotenv
from src.services.aiservice import AiService
from elevenlabs.client import ElevenLabs
from src.voice_generator import AudioGenerator
from fastapi.middleware.cors import CORSMiddleware
load_dotenv()

# app = FastAPI(debug=True)

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

task = "transcribe"     
huggingface_read_token = os.getenv("HUGGINGFACE_READ_TOKEN")
model_name = os.getenv("MODEL_NAME")
elleven_labs_api = os.getenv("ELLEVEN_LABS_API")
model_optimizer = ModelOptimization(model_name=model_name)
model_optimizer.convert_model_to_optimized_format()
model = model_optimizer.load_transcription_model()
client = ElevenLabs(
    api_key=elleven_labs_api, 
    )
aiservice = AiService(model_name = "gemini-1.0-pro-001")
audio_generator = AudioGenerator(client)

# @app.post("/speech_interaction")
# async def speech_interaction(file: UploadFile):
#     logger = logging.getLogger(__name__)
#     logging.basicConfig(format='%(asctime)s %(levelname)-8s %(message)s', filename='app.log', level=logging.INFO, datefmt='%Y-%m-%d %H:%M:%S')
#     try:
#         # Create a temporary file for the upload
#         with tempfile.NamedTemporaryFile(suffix=".tmp", delete=False) as tmp_file:
#             tmp_file.write(await file.read())
#             tmp_file_path = tmp_file.name

#         # Initiate the transcription model
#         logger.info("Transcribing audio...")
#         start_time = time.time()
#         inference = SpeechTranscriptionPipeline(
#                 audio_file_path=tmp_file_path,
#                 task=task,
#                 huggingface_read_token=huggingface_read_token
#             )
#         end_time = time.time()
#         duration = end_time - start_time
#         # To get transcriptions
#         transcription_dict = inference.transcribe_audio(model=model)

#         transcription_text = transcription_dict['segments'][0]['text']

#         logger.info(f"Audio transcribed in {duration} second. Generating response from AI...")
#         text_response = aiservice.text_generation(text = transcription_text, 
#                                                   verbose = True)
#         logger.info("Converting response text to audio...")
#         audio_generator.generate_audio(text = text_response, 
#                                      filename= "response_audio.mp3")
#         filename = f"./response_audio.mp3"
#         logger.info("Posting Audiofile...")
#         return FileResponse(
#             path=filename,
#             media_type="application/octet-stream",
#             filename="subtitle.srt",
#             headers={"Content-Disposition": "attachment; filename=response_audio.mp3"}
#         )
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Error transcribing audio: {e}")


# @app.get("/")
# async def health_check() -> str:
#     """
#     Basic health check endpoint to confirm the application is running.

#     Returns:
#     - str: A simple message indicating that the application is running successfully.
#     """
#     return "Running Successfully"



def run(audio_file):
    inference = SpeechTranscriptionPipeline(
                audio_file_path=audio_file,
                task=task,
                huggingface_read_token=huggingface_read_token
            )
    transcription_dict = inference.transcribe_audio(model=model)

    transcription_text = transcription_dict['segments'][0]['text']

    text_response = aiservice.text_generation(text = transcription_text, 
                                                  verbose = True)
    audio_response = audio_generator.generate_audio(text = text_response, 
                                     filename= "audio/generated.mp3")
    return audio_response



def process_audio(audio):
    url = "http://34.168.116.94:8000/docs"
    files = {'audio_file': open(audio, 'rb')}
    try:
        response = requests.post(url, files=files)
        if response.status_code == 200:
            generated_audio = response.content
            return generated_audio
        else:
            print("Error:", response.text)
            return None
    except requests.exceptions.RequestException as e:
        print("Error:", e)
        return None
    


def autoplay_audio(file_path: str):
    with open(file_path, "rb") as f:
        data = f.read()
        b64 = base64.b64encode(data).decode()
        md = f"""
            <audio controls autoplay="true">
            <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
            </audio>
            """
        st.markdown(
            md,
            unsafe_allow_html=True,
        )

def main():
    title = "Verbify AI"
    st.title(title)
    image = Image.open('images/VERBIFYAI.jpg')
    st.image(image, use_column_width=True)

    audio = audiorecorder("Record", "Click to stop recording")
    if len(audio) > 0:
        # To play audio in frontend:
        st.audio(audio.export().read())  

        # To save audio to a file, use pydub export method:
        audio.export("audio/recording.mp3", format="mp3")
        st.success("Recording completed")

        st.spinner("Generating audio...")
        generated_audio = run('audio/recording.mp3')
        if generated_audio:
            st.success("Audio generated successfully. Playing...")
            autoplay_audio(generated_audio)
        else:
            st.error("Failed to generate audio.")



if __name__ == '__main__':
    main()
