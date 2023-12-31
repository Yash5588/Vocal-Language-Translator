import pyttsx3
import speech_recognition as sr
from gtts import gTTS
import pygame
import time
import requests
from flask import Flask,render_template,request
import webbrowser

app = Flask(__name__)

engine = pyttsx3.init()

def speak(text, lang="en"):
    engine.say(text)
    engine.runAndWait()

def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        print("Recognizing...")
        query = recognizer.recognize_google(audio)
        return query
    except sr.UnknownValueError:
        print("Sorry, I couldn't understand that.")
        return ""
    except sr.RequestError as e:
        print(f"Could not request results; {e}")
        return ""
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


def speech_to_speech_translation(desired_language):
    print("PLEASE WAIT FOR A MOMENT TO SPEAK")
    speak("Hello! How can I assist you today?")

    query = listen()
    print("You said:", query)

    url = "https://text-translator2.p.rapidapi.com/translate"
    headers = {
        "content-type": "application/x-www-form-urlencoded",
        "X-RapidAPI-Key": "0f491a5108mshbe7b62a9976bafbp15461ejsn7894515d0926",
        "X-RapidAPI-Host": "text-translator2.p.rapidapi.com",
    }
    if query:
        data = {
            "source_language": "auto",
            "target_language": desired_language,
            "text": query,
        }
        response = requests.post(url, data=data, headers=headers)
        translation = response.json()
        translated_text = translation["data"]["translatedText"]
        print("Translation:", translated_text)
        obj = gTTS(text=translated_text, lang=desired_language, slow=False)
        mp3_file = "transpeech.mp3"
        obj.save(mp3_file)
        pygame.mixer.init()
        sound = pygame.mixer.Sound(mp3_file)
        sound.play()
        time.sleep(sound.get_length())
        


def speech_to_text_recognition(desired_language):
    print("PLEASE WAIT FOR A MOMENT TO SPEAK UNTIL 'LISTENING' WORD APPEARS ON SCREEN")
    speak("Hello! How can I assist you today?")

    query = listen()
    print("You said:", query)
    translated_text = text_to_text_translation(desired_language,query)
    return translated_text

def text_to_speech(desired_language,text):
    translated_text = text_to_text_translation(desired_language,text)
    obj = gTTS(text=translated_text, lang=desired_language, slow=False)
    mp3_file = "static/audio/transpeech.mp3"
    obj.save(mp3_file)
    #pygame.mixer.init()
    #sound = pygame.mixer.Sound(mp3_file)
    #sound.play()
    #time.sleep(sound.get_length())

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
        return render_template('text_output.html',translated_text = translated_text,lang = desired_language)
    elif option == "4":
        text = request.form['text']
        text_to_speech(desired_language,text);
    return render_template("speech_output.html",lang = desired_language)
    '''elif option == "2":
        speech_to_speech_translation(desired_language)

    elif option == "3":
        translated_text = speech_to_text_recognition(desired_language)
        print("Translated text = ",translated_text)'''

urll = "http://127.0.0.1:5000"
webbrowser.open(urll)
app.run(debug=True)

