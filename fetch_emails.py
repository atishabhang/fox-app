import os
import sys

from sqlalchemy.orm import sessionmaker

import services.gmail
import db.local_db

if __name__ == '__main__':
    db.local_db.drop_database()
    engine = db.local_db.create_database()
    _session = sessionmaker(bind=engine)
    session = _session()

    credentials = services.gmail.authenticate()
    if credentials is None:
        print("error fetching credentials.\nExiting.")
        sys.exit(1)

    email_list = services.gmail.fetch_emails(credentials)
    for email in email_list:
        print("adding email=", email.id)
        session.add(email)
    session.commit()
