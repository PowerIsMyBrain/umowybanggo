from flask import Flask, render_template, request, send_from_directory
import speech_recognition as sr
from flask import jsonify
import soundfile as sf
from wzoruumow import data as dataWzoruUmow
import find_contracts_by_phrase
import pdf_exporter_1 as pdf_1____
import AiRandsChoice_class as AiRand

app = Flask(__name__)
aiRand = AiRand.AiRandsChoice()


@app.route('/<filename>')
def download_file(filename, uidum=''):
    # Tutaj możesz dodać dodatkowe zabezpieczenia, aby upewnić się, że serwowany jest tylko plik `umowa.pdf`
    if filename == f'umowa{uidum}.pdf':
        return send_from_directory(app.root_path, filename)
    return 'File not allowed', 403

def convert_ogg_to_wav(input_path, output_path, chunk_size=1024):
    # Otwórz plik źródłowy i plik docelowy
    with sf.SoundFile(input_path) as input_file:
        samplerate = input_file.samplerate
        # Utwórz plik WAV z taką samą częstotliwością próbkowania jak plik źródłowy
        with sf.SoundFile(output_path, 'w', samplerate=samplerate, channels=input_file.channels, subtype='PCM_16') as output_file:
            while True:
                # Czytaj dane w blokach
                data = input_file.read(chunk_size)
                if len(data) == 0:
                    break
                # Zapisz dane do pliku docelowego
                output_file.write(data)

@app.route('/')
def index():
    return render_template('socketdata.html')

@app.route('/voice')
def voice():
    return render_template("base_app_one.html")

@app.route('/send_dev', methods=['POST'])
def send_dev():
    dev_text = request.form['dev_text']
    print(dev_text)

    split_dev_text = dev_text.lower().split(' ')
    umowy_set = set()
    found_dict = {}
    for word in split_dev_text:
        kindList = find_contracts_by_phrase.find_contracts_by_keyWords(
            dataWzoruUmow, word)
        # print(word, kindList)
        for umowa in kindList:
            umowy_set.add(umowa)
            try:
                found_dict[umowa] += 3
            except KeyError:
                found_dict[umowa] = 1
    choiced_contract = aiRand.weighted_choice(
        [a for a in found_dict.keys()], [a for a in found_dict.values()])


    print(found_dict)
    print(choiced_contract)
    pdf_1____.generate_contract_pdf(dataWzoruUmow[choiced_contract])
    success = True

    print('text ok')
    return jsonify({'recognized_texts': f'{choiced_contract}', 'success':success })


@app.route('/send_recording', methods=['POST'])
def send_recording():

    input_ogg_path = 'received_recording.ogg'
    output_wav_path = 'received_recording.wav'

    # Konwersja pliku
    convert_ogg_to_wav(input_ogg_path, output_wav_path)

    # Rozpoznaj mowę z nagrania
    recognizer = sr.Recognizer()


    with sr.AudioFile('received_recording.wav') as source:
        audio = recognizer.record(source)
    found_dict = {}
    try:
        rcog = recognizer.recognize_google(audio, language='pl-PL')
        # Tutaj serce programu 

        text = str(rcog).lower().replace(' kropka', '.')\
            .replace(' kropka ', '. ').replace(' przecinek ', ', ')\
            .replace(' wykrzyknik ', '! ').replace(' wykrzyknik', '!')\
            .replace(' znak zapytania ', '? ').replace(' znak zapytania', '?')
        """
        from wzoruumow import data as dataWzoruUmow
        import find_contracts_by_phrase
        import pdf_exporter
        """
        split_dev_text = rcog.lower().split(' ')
        umowy_set = set()
        found_dict = {}
        
        for word in split_dev_text:
            kindList = find_contracts_by_phrase.find_contracts_by_keyWords(
                dataWzoruUmow, word)
            # print(word, kindList)
            for umowa in kindList:
                umowy_set.add(umowa)
                try:
                    found_dict[umowa] += 3
                except KeyError:
                    found_dict[umowa] = 1
        if len([a for a in found_dict.keys()]) != 0:
            choiced_contract = aiRand.weighted_choice(
                [a for a in found_dict.keys()], [a for a in found_dict.values()])
            success = False
        else:
            choiced_contract = "Nie znaleziono umowy pasującej do wypowiedzi."
            success = False


        print(found_dict)
        print(choiced_contract)
        pdf_1____.generate_contract_pdf(dataWzoruUmow[choiced_contract])
        success = True

        print('text ok')
    except sr.UnknownValueError:
        choiced_contract = "Nie można rozpoznać mowy"
        success = False

    except sr.RequestError as e:
        choiced_contract = f"Błąd serwera: {e}"
        success = False
    # Przekazanie wyników rozpoznawania mowy do strony internetowej za pomocą JSON
    return jsonify({'recognized_texts': choiced_contract, 'success':success })


if __name__ == '__main__':
    app.run(debug=True, port=8000)
