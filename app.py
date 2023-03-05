import os

import openai
from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")

def save_file(audiofile):
    if audiofile.filename != '':
        audiofile.save(audiofile.filename)
    else:
        raise ValueError('Invalid file ' + audiofile.filename)

def transcribe(file_path: str):
    print('Opening: ' + file_path)
    speech = open(file_path, "rb")
    return openai.Audio.transcribe("whisper-1", speech)
    

@app.route("/", methods=("GET", "POST"))
def s2t():
    if request.method == "POST":
        audiofile = request.files["audiofile"]
        save_file(audiofile)
        transcript = transcribe(audiofile.filename)
        print(f'transcript: "{transcript.text}"')
        return render_template("index.html", transcript=transcript.text)
    
    # result = request.args.get("result")
    return render_template("index.html")

@app.route("/animal", methods=("GET", "POST"))
def index():
    if request.method == "POST":
        animal = request.form["animal"]
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=generate_prompt(animal),
            temperature=0.6,
        )
        return render_template("animal.html", result=response.choices[0].text)

    result = request.args.get("result")
    return render_template("animal.html")


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

