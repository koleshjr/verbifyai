import os
from deployment.speech_inference import SpeechTranscriptionPipeline, ModelOptimization
from dotenv import load_dotenv
from src.services.aiservice import AiService
from elevenlabs.client import ElevenLabs
from voice_generator import AudioGenerator
load_dotenv()


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


def run(audio_file):
    inference = SpeechTranscriptionPipeline(
                audio_file_path=audio_file,
                task=task,
                huggingface_read_token=huggingface_read_token
            )
    transcription_dict = inference.transcribe_audio(model=model)
    try:
        transcription_text = transcription_dict['segments'][0]['text']
        text_response = aiservice.text_generation(text = transcription_text, 
                                                  verbose = True)
  
    except Exception as e:
        text_response = "Sorry seems like that is an empty audio. Please retry again"

    audio_response = audio_generator.generate_audio(text = text_response, 
                                     filename= "audio/generated.mp3")
    return audio_response

