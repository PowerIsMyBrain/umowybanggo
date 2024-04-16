from flask import Flask, render_template, request

import speech_recognition as sr
from flask import jsonify

import soundfile as sf

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('socketdata.html')

@app.route('/voice')
def voice():
    return render_template("base_app_one.html")





@app.route('/send_recording', methods=['POST'])
def send_recording():
    # Odbierz nagranie dźwiękowe przesłane z przeglądarki
    audio_data = request.files['audio_data']
    
    # Zapisz nagranie dźwiękowe do pliku
    audio_path = 'received_recording.ogg'
    audio_data.save(audio_path)


    # Amn Tree
    # Wczytaj plik OGG
    ogg_data, samplerate = sf.read(audio_path)

    # Zapisz jako plik WAV
    sf.write('received_recording.wav', ogg_data, samplerate)

    # Rozpoznaj mowę z nagrania
    recognizer = sr.Recognizer()
    recognized_texts = {}

    with sr.AudioFile('received_recording.wav') as source:
        audio = recognizer.record(source)
    found = False
    try:
        rcog = recognizer.recognize_google(audio, language='pl-PL')
        # Tutaj serce programu 
        text = str(rcog).lower().replace(' kropka', '.')\
            .replace(' kropka ', '. ').replace(' przecinek ', ', ')\
            .replace(' wykrzyknik ', '! ').replace(' wykrzyknik', '!')\
            .replace(' znak zapytania ', '? ').replace(' znak zapytania', '?')
            
        if text.count('umowa o dzielo') > 0:
            found = True
            text = text + """

            
            Znaleziono umowę o dzieło!
            """
        
        print('text ok')
    except sr.UnknownValueError:
        text = "Nie można rozpoznać mowy"

    except sr.RequestError as e:
        text = f"Błąd serwera: {e}"

    # Przekazanie wyników rozpoznawania mowy do strony internetowej za pomocą JSON
    return jsonify({'recognized_texts': text})


if __name__ == '__main__':
    app.run(debug=True, port=8000)
