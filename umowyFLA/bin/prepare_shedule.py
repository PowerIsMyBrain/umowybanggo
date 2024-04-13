from datetime import datetime, timedelta
from connectAndQuery import connect_to_database, insert_to_database
from config_utils import time_interval_minutes
from appslib import handle_error
def prepare_mailing_plan(posts, previous_mailings, set_start_time = None):
    # exemple set_start_time:  '2024-08-30 14:56'
    plansDB = connect_to_database('SELECT send_time FROM schedule;')
    lasted_date = datetime.strptime('1980-01-01 00:00:00', "%Y-%m-%d %H:%M:%S")

    for row in plansDB:
        date_from_db = row[0] # datetime.strptime(row[0], "%Y-%m-%d %H:%M:%S")
        if date_from_db > lasted_date:
            lasted_date = date_from_db

    mailing_plan = []
    if not set_start_time or datetime.strptime(set_start_time, "%Y-%m-%d %H:%M") < datetime.now():
        set_start_time = datetime.now()
    else:
        set_start_time = datetime.strptime(set_start_time, "%Y-%m-%d %H:%M")

    if lasted_date > set_start_time:
        set_start_time = lasted_date
    set_start_time = set_start_time + timedelta(minutes=time_interval_minutes)
    for post in posts:
        post_id = post['id']
        # Sprawdź, czy post został wcześniej wysłany
        if post_id not in [mailing['post_id'] for mailing in previous_mailings]:
            # Dodaj post do planu wysyłki
            mailing_plan.append({'post_id': post_id, 'send_time': set_start_time})

    # Ustaw odstęp czasowy między wysyłkami
    for i, mailing in enumerate(mailing_plan):
        mailing['send_time'] += timedelta(minutes=i * time_interval_minutes)

    return mailing_plan
def save_shedule(shcedule):
    exiting_post = []
    get_existing_posts = connect_to_database(
        'SELECT post_id FROM schedule;')
    for row in get_existing_posts:
        exiting_post.append(row[0])
    for row in shcedule:
        if row["post_id"] not in exiting_post:
            formatedDate = row["send_time"].strftime("%Y-%m-%d %H:%M:%S")
            insert_to_database(
                'INSERT INTO schedule (post_id, send_time) VALUES (%s, %s)',
                (row["post_id"], formatedDate)
            )
    return True

def get_allPostsID():
    dumpDB = connect_to_database(
        'SELECT ID FROM contents;')
    export = []
    for data in dumpDB: export.append({'id': data[0]})
    return export

def get_sent():
    dumpDB = connect_to_database(
        'SELECT post_id FROM sent_newsletters;')
    export = []
    for data in dumpDB: export.append({'post_id': data[0]})
    return export


if __name__ == "__main__":
    # time_interval_minutes = 1440
    shcedule = prepare_mailing_plan(get_allPostsID(), get_sent())
    save_shedule(shcedule)
