import os
import sys

from sqlalchemy.orm import sessionmaker

import services.gmail
import db.local_db
from constants.constants import DB_NAME

if __name__ == '__main__':
    # drop db
    db.local_db.drop_database(DB_NAME)
    engine = db.local_db.create_database(DB_NAME)
    _session = sessionmaker(bind=engine)
    session = _session()

    # Authenticate using OAuth
    credentials = services.gmail.authenticate()
    if credentials is None:
        print("error fetching credentials.\nExiting.")
        sys.exit(1)

    # Fetch emails
    email_list = services.gmail.fetch_emails(credentials)
    # Once emails fetched we can add it to db
    for email in email_list:
        print("adding email=", email.id)
        session.add(email)
    session.commit()
