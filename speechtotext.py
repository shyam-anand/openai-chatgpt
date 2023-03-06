import os

import openai

openai.api_key = os.getenv('OPENAI_API_KEY')

def save_file(uploaded_file):
    if uploaded_file.filename == '':
        raise ValueError('Filename cannot be empty')

    uploaded_file.save(uploaded_file.filename)
    return uploaded_file.filename

def transcribe(file_path: str):
    if file_path == '':
        raise ValueError('Filepath cannot be empty')

    audio = open(file_path, 'rb')
    return openai.Audio.transcribe('whisper-1', audio)
