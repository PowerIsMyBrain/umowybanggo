def find_contracts_by_phrase(data, phrase):
    matching_keys = []
    phrase_lower = phrase.lower()  # Przetwarzanie frazy na małe litery, aby wyszukiwanie było niezależne od wielkości liter

    # Przeszukiwanie każdego klucza i wartości w danych
    for key, content in data.items():
        # Sprawdzanie, czy fraza znajduje się w nazwie umowy
        if phrase_lower in key.lower():
            matching_keys.append(key)
            continue  # Jeśli nazwa pasuje, nie sprawdzaj dalej

        # Sprawdzanie, czy fraza znajduje się w treści poszczególnych paragrafów
        for paragraf in content.values():
            print(paragraf)
            try: par = str(paragraf).lower()
            except: par = ''
            if phrase_lower in par or phrase_lower in par:
                matching_keys.append(key)
                break  # Przerywa pętlę po znalezieniu pierwszego pasującego paragrafu w danej umowie

    return matching_keys


if __name__ == "__main__":
    # Przykładowa baza danych (słownik)
    contracts_data = {
        "Umowa o dzieło": {
            'data_umowy': '2024-04-17',
            'miejsce_umowy': 'Warszawa',
            'paragrafy': [
                {'tytul': '§1 Warunki ogólne', 'tresc': 'Treść paragrafu 1 dotycząca warunków ogólnych umowy.'},
                {'tytul': '§2 Prawa i obowiązki', 'tresc': 'Treść paragrafu 2 dotycząca praw i obowiązków stron.'},
                {'tytul': '§3 Prawa i obowiązki', 'tresc': 'Treść paragrafu 3 dotycząca praw i obowiązków stron.'},
                {'tytul': '§4 Prawa i obowiązki', 'tresc': 'Treść paragrafu 4 dotycząca praw i obowiązków stron.'}
            ]
        },
        "Umowa zlecenie": {
            'data_umowy': '2024-04-17',
            'miejsce_umowy': 'Warszawa',
            'paragrafy': [
                {'tytul': '§1 Podstawowe i ogólne postanowienia', 'tresc': 'Treść paragrafu 1 dotycząca warunków ogólnych umowy.'},
                {'tytul': '§2 Prawa i obowiązki', 'tresc': 'Treść paragrafu 2 dotycząca praw i obowiązków stron.'},
                {'tytul': '§3 Prawa i obowiązki', 'tresc': 'Treść paragrafu 3 dotycząca praw i obowiązków stron.'},
                {'tytul': '§4 Prawa i obowiązki', 'tresc': 'Treść paragrafu 4 dotycząca praw i obowiązków stron.'}
            ]
        }
    }
    # Przykładowe wywołanie funkcji
    search_phrase = "podstawowe"
    found_contracts = find_contracts_by_phrase(contracts_data, search_phrase)
    print(found_contracts)
