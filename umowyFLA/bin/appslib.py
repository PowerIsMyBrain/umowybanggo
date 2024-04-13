from datetime import datetime

def handle_error(exception, retry_count=3):
    try:
        with open("../logs/errors.log", "a") as log:
            now = str(datetime.now())
            message = "{0} {1}\n".format(now, exception)
            log.write(message)
    except Exception as e:
        if retry_count > 0:
            print(f"Błąd podczas zapisywania do pliku: {e}. Ponawiam próbę...")
            handle_error(exception, retry_count - 1)
        else:
            print("Nieudana próba zapisu do pliku. Przekroczono limit ponawiania.")
