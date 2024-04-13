# Amn Tree
import soundfile as sf

# Wczytaj plik OGG
ogg_data, samplerate = sf.read('received_recording.ogg')

# Zapisz jako plik WAV
sf.write('received_recording.wav', ogg_data, samplerate)