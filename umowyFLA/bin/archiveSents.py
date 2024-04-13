from connectAndQuery import connect_to_database, insert_to_database, delete_row_from_database
from appslib import handle_error
def archive_sents(postIdFromSchedule):
    scheduleDB = connect_to_database(
        "SELECT * FROM schedule;"
        )
    for row in scheduleDB:
        if row[1] == postIdFromSchedule:
            # Remove the entry from the Scheduled Posts table.
            removeRowSQL = """DELETE FROM schedule WHERE post_id='%s';"""
            rinf = "Removing scheduled post with ID '%s'." % (row[1])
            handle_error(rinf)
            print()
            delete_row_from_database(
                removeRowSQL, 
                (row[1],)
                )
            # Insert a new record into the Archived Posts table.
            insert_to_database(
                'INSERT INTO sent_newsletters (post_id, send_time) VALUES(%s,%s)', 
                (row[1], row[2])
                )
            ainf = "Adding archives post with ID '%s'." % (row[1])
            handle_error(ainf)
            return True
    return False
if __name__ == "__main__":
    if archive_sents(4):
        print("Archiwizacja zakończona pomyślnie.")
    else:
        print("Nie znaleziono wpisu o podanym identyfikatorze.")