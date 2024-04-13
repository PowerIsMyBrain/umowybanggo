from flask import Flask, render_template
from flask_socketio import SocketIO, emit

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

if __name__ == '__main__':
    socketio.run(app, debug=True, port=8000)