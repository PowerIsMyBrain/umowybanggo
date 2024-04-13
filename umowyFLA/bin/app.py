from time import time, sleep
from datetime import datetime
import prepare_shedule
import messagerCreator 
import sendEmailBySmtp
from archiveSents import archive_sents
from appslib import handle_error

def main():
    for _ in range(int(time())):
        # Wysyłka newslettera do aktywnych użytkowników według planu wysyłki
        shcedule = prepare_shedule.prepare_mailing_plan(prepare_shedule.get_allPostsID(), prepare_shedule.get_sent())
        sleep(1)
        prepare_shedule.save_shedule(shcedule)
        sleep(1)
        current_time = datetime.now()
        for row in prepare_shedule.connect_to_database(
                'SELECT * FROM schedule;'):
            if row[2] < current_time:
                TITLE = prepare_shedule.connect_to_database(f'SELECT TITLE FROM contents WHERE  ID={row[1]};')[0][0]
                nesletterDB = prepare_shedule.connect_to_database(f'SELECT CLIENT_NAME, CLIENT_EMAIL, USER_HASH FROM newsletter WHERE ACTIVE=1;')
                for data in nesletterDB:
                    hashes = data[2]
                    HTML = messagerCreator.create_html_message(row[1], data[0], hashes)
                    if HTML != '':
                        sendEmailBySmtp.send_html_email(TITLE, HTML, data[1])
                        archive_sents(row[1])

        # Aktywacja konta subskrybenta
        nesletterDB = prepare_shedule.connect_to_database(f'SELECT ID, CLIENT_NAME, CLIENT_EMAIL, USER_HASH FROM newsletter WHERE ACTIVE=0;')
        for data in nesletterDB:
            TITLE_ACTIVE = 'Aktywacja konta'
            message = messagerCreator.HTML_ACTIVE.replace('{{imie klienta}}', data[1]).replace('{{hashes}}', data[3])
            sendEmailBySmtp.send_html_email(TITLE_ACTIVE, message, data[2])
            prepare_shedule.insert_to_database(
                f"UPDATE newsletter SET ACTIVE = %s WHERE ID = %s AND CLIENT_EMAIL = %s",
                (3, data[0], data[2])
                )
        handle_error(f'{datetime.now()} - {__name__} is working...\n')
        sleep(60)


if __name__ == "__main__":
    main()