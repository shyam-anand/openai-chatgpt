FROM python:3.10
WORKDIR /usr/src/openai-speech-to-text
COPY .env.example .
COPY *.py .
COPY static/* ./static/
COPY templates/* ./templates/
COPY requirements.txt .
RUN python -m venv venv
RUN . venv/bin/activate
RUN pip install -r requirements.txt
RUN pip install -U openai
CMD ["flask", "run", "--host=0.0.0.0"]
