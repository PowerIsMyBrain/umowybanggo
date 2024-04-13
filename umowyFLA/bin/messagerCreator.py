from connectAndQuery import connect_to_database
from config_utils import message_templates
from appslib import handle_error
def create_html_message(postID, client_name, heshed):
    """
        Funkcja pobiera z bazy dane posta o podanym identyfikatorze i tworzy wiadomość HTML.
    """
    # Pobieranie z bazy danych
    dumpDB = connect_to_database(
                        f'SELECT * FROM contents WHERE ID = {postID};')
    formatDump = {}
    try:
        formatDump['title'] = dumpDB[0][1]
        formatDump['content_main'] = dumpDB[0][2]
        formatDump['highlights'] = dumpDB[0][3]
        formatDump['bullets'] = dumpDB[0][4]
        formatDump['header_foto'] = dumpDB[0][5]
        formatDump['content_foto'] = dumpDB[0][6]
        formatDump['tags'] = dumpDB[0][7]
        formatDump['category'] = dumpDB[0][8]
    except IndexError as e:
        handle_error(f"Błąd w funkcji 'create_html_message': {e}")
        return ''

    readyHtmlBullets = ''
    for text in formatDump['bullets'].split('#splx#'):
        readyHtmlBullets +=  f'<li>{text}</li>\n'

    with open(message_templates['news'], 'r', encoding="utf-8") as plik:
        template = plik.read()

    ready_template = template.replace('{{imie klienta}}', str(client_name)).replace('{{tytuł}}', formatDump['title']).replace('{{tresc glowna}}', formatDump['content_main'])\
                                .replace('{{wprowadzenie}}', formatDump['highlights']).replace('{{wypunktowania}}', readyHtmlBullets)\
                                    .replace('{{zdjecie glowne}}', formatDump['header_foto']).replace('{{zdjecie dodatkowe}}', formatDump['content_foto'])\
                                        .replace('{{kategoria}}', formatDump['category']).replace('{{tagi}}', formatDump['tags']).replace('{{hashes}}', heshed)
    return ready_template

with open(message_templates['config'], 'r', encoding="utf-8") as plik:
        HTML_ACTIVE = plik.read()

if __name__ == "__main__":
    print(create_html_message(1, 'michał', 'hash'))
