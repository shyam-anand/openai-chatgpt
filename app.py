import os

import openai
from flask import Flask, redirect, render_template, request, url_for
import traceback

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")

def save_file(uploaded_file):
    if uploaded_file.filename != '':
        uploaded_file.save(uploaded_file.filename)
        return uploaded_file.filename
    else:
        raise ValueError('Invalid file ' + uploaded_file.filename)

def transcribe(file_path: str):
    audio = open(file_path, "rb")
    print(audio)
    return openai.Audio.transcribe("whisper-1", audio)
    

@app.route("/", methods=("GET", "POST"))
def index():
    if request.method == "POST":
        audiofile = save_file(request.files["audiofile"])
        try:
            transcript = transcribe(audiofile)
            print(f'transcript: "{transcript.text}"')
            return redirect(url_for("index", transcript=transcript.text))
        except Exception as e:
            traceback.print_exc()
            return redirect(url_for("index", error=e))
    
    transcript = request.args.get("transcript")
    error = request.args.get("error")
    return render_template("index.html", transcript=transcript, error=error)


def generate_prompt(animal):
    return """Suggest three names for an animal that is a superhero.

Animal: Cat
Names: Captain Sharpclaw, Agent Fluffball, The Incredible Feline
Animal: Dog
Names: Ruff the Protector, Wonder Canine, Sir Barks-a-Lot
Animal: {}
Names:""".format(
        animal.capitalize()
    )

