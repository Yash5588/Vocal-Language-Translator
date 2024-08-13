import pyttsx3
import speech_recognition as sr
from gtts import gTTS
import pygame
import time
import requests
from flask import Flask,render_template,request
import webbrowser

app = Flask(__name__)

def text_to_text_translation(desired_language,text):
    url = "https://text-translator2.p.rapidapi.com/translate"
    headers = {
        "content-type": "application/x-www-form-urlencoded",
        "X-RapidAPI-Key": "0f491a5108mshbe7b62a9976bafbp15461ejsn7894515d0926",
        "X-RapidAPI-Host": "text-translator2.p.rapidapi.com",
    }
    data = {
        "source_language": "auto",
        "target_language": desired_language,
        "text": text,
    }
    response = requests.post(url, data=data, headers=headers)
    translation = response.json()
    translated_text = translation["data"]["translatedText"]
    return translated_text

def speech_to_text_recognition(desired_language,text):
    translated_text = text_to_text_translation(desired_language,text)
    return translated_text

def text_to_speech(desired_language,text):
    translated_text = text_to_text_translation(desired_language,text)
    obj = gTTS(text=translated_text, lang=desired_language, slow=False)
    mp3_file = "static/audio/transpeech.mp3"
    obj.save(mp3_file)

@app.route('/')

def get_info():
    return render_template('input.html')

@app.route('/process',methods = ['POST'])

def process():
    global option
    option = request.form['option']
    global desired_language
    desired_language = request.form['desired_language']
    if(option == '1' or option == '4'):
        return render_template('text_input.html')
    else:
        return render_template('speech_input.html')
    
@app.route('/submit',methods = ['POST'])

def submit():
    if(option == '1'):
        text = request.form['text']
        translated_text = text_to_text_translation(desired_language,text)
        return render_template('text_output.html',translated_text = translated_text,lang = desired_language,text= text)
    elif option == "2":
        text = request.form['text']
        text_to_speech(desired_language,text);
        return render_template("speech_output.html",lang = desired_language,text = text)
        
    elif option == "3":
        text = request.form['text']
        translated_text = speech_to_text_recognition(desired_language,text)
        return render_template('text_output.html',lang = desired_language,text = text,translated_text= translated_text)
    elif option == "4":
        text = request.form['text']
        text_to_speech(desired_language,text);
        return render_template("speech_output.html",lang = desired_language,text = text)

urll = "http://127.0.0.1:5000"
webbrowser.open(urll)
app.run(debug=True,host = '0.0.0.0')

