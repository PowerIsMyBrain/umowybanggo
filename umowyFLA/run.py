from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit
import speech_recognition as sr
from flask import jsonify
# from pydub import AudioSegment
import soundfile as sf

app = Flask(__name__)
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('socketdata.html')

@socketio.on('voice_data')
def handle_voice_data(data):
    print(data)  # Wyświetlenie danych w konsoli serwera
    # Tutaj możesz przetworzyć otrzymane dane, np. zapisać je do pliku, przekazać do innej funkcji itp.
    emit('voice_response', {'status': 'ok'})  # Wysłanie odpowiedzi do klienta

@app.route('/voice')
def voice():
    return render_template("base_app_one.html")

# @app.route('/send_recording', methods=['POST'])  # Nowy endpoint do przechwytywania danych z przycisku "Wyślij nagranie"
# def send_recording():
#     # Tutaj możesz przechwycić dane wysłane z przeglądarki i przetworzyć je, np. zapisać do pliku
#     data = request.data.decode('utf-8')  # Pobranie danych przesłanych w żądaniu
#     print("Received recording:", data)  # Wyświetlenie danych w konsoli serwera
#     return "Recording received successfully"



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
    
    try:
        text = recognizer.recognize_google(audio, language='pl-PL')
        recognized_texts['format'] = text
        print('text ok')
    except sr.UnknownValueError:
        recognized_texts['format'] = "Nie można rozpoznać mowy"
        print(recognized_texts['format'])
    except sr.RequestError as e:
        recognized_texts['format'] = f"Błąd serwera: {e}"
    print(recognized_texts['format'])
    # Przekazanie wyników rozpoznawania mowy do strony internetowej za pomocą JSON
    return jsonify({'recognized_texts': recognized_texts})


if __name__ == '__main__':
    socketio.run(app, debug=True, port=8000)
