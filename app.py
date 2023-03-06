import os
import traceback

import speechtotext
from flask import Flask, redirect, render_template, request, url_for


app = Flask(__name__)

@app.route('/', methods=('GET', 'POST'))
def index():
    if request.method == 'POST':
        audiofile = speechtotext.save_file(request.files['audiofile'])
        try:
            transcript = speechtotext.transcribe(audiofile)
            print(f'transcript: "{transcript.text}"')
            return redirect(url_for('index', transcript=transcript.text))
        except Exception as e:
            traceback.print_exc()
            return redirect(url_for('index', error=e))
    
    transcript = request.args.get('transcript')
    error = request.args.get('error')
    return render_template('index.html', transcript=transcript, error=error)
