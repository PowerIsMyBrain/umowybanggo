def rekurencyjna_petla_w_slowniku(valData, phrase):
    phrase_lower = phrase.lower()
    if isinstance(valData, dict):
        for key, val in valData.items():
            if phrase_lower in key.lower() or rekurencyjna_petla_w_slowniku(val, phrase):
                return True
        return False
    elif isinstance(valData, list):
        for el in valData:
            if phrase_lower in el or rekurencyjna_petla_w_slowniku(el, phrase):
                return True
        return False
    elif isinstance(valData, str):
        return phrase_lower in valData.lower()
    return False



def find_contracts_by_phrase(data, phrase):
    matching_keys = []
    phrase_lower = phrase.lower()

    # Przeszukiwanie każdego klucza i wartości w danych
    for key, content in data.items():
        if phrase_lower in key.lower():
            matching_keys.append(key)
            continue

        for paragraf in content.values():
            if rekurencyjna_petla_w_slowniku(paragraf, phrase_lower):
                matching_keys.append(key)
                break

    return matching_keys

def find_contracts_by_keyWords(keyWordsData_dict, phrase):
    matching_keys = []
    phrase_lower = str(phrase).lower()

    # Przeszukiwanie każdego klucza i wartości w danych
    for key, content in keyWordsData_dict.items():
        if phrase_lower in str(key).lower():
            matching_keys.append(key)
        # print(content)
        for key_s, val_s in content.items():
            # print(key_s, val_s)
            if key_s == 'search':
                if phrase_lower in val_s:
                    matching_keys.append(key)

    print(matching_keys)
    return matching_keys


if __name__ == "__main__":
    # Przykładowa baza danych (słownik)
    from wzoruumow import data as dataWzoruUmow

    # Przykładowe wywołanie funkcji
    search_phrase = "spłata"
    found_contracts = find_contracts_by_phrase(dataWzoruUmow, search_phrase)
    print(found_contracts)

    # Przykładowe wywołanie funkcji
    print(rekurencyjna_petla_w_slowniku(dataWzoruUmow, search_phrase))  # Zwróci True
    print(rekurencyjna_petla_w_slowniku(dataWzoruUmow, "nic"))  # Zwróci False
