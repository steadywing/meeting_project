# streamlit/services/whisper_service.py
import torch 
import whisper 

torch.classes.__path__ = [] 

def load_model(model_name="small"):
    model = whisper.load_model(model_name)
    print("Whisper 모델을 불러왔습니다.")
    return model 

def transcribe_audio(model, file_path: str) -> str:
    """
    오디오 파일을 Whisper로 변환하여 텍스트를 반환하는 함수
    """
    result = model.transcribe(file_path)

    transcript = ""
    for seg in result["segments"]:
        transcript += seg["text"] + "\n"
    return transcript

# 모델 로드
model = load_model()