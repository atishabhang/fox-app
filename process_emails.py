import json
from datetime import datetime

from googleapiclient.discovery import build
from sqlalchemy.orm import sessionmaker

import models.email
import services.gmail
from constants import constants
import db.local_db


def apply_rules(rules_file, emails):
    # Read the rules file
    with open(rules_file, 'r') as f:
        rules = json.load(f)

    # decide actions based on requirement from the rules.json
    for email in emails:
        for rule in rules['rules']:
            if rule['predicate'] == 'All':
                if all(check_condition(r, email) for r in rule['conditions']):
                    perform_actions(rule['actions'], email)
            elif rule['predicate'] == 'Any':
                if any(check_condition(r, email) for r in rule['conditions']):
                    perform_actions(rule['actions'], email)


def check_condition(rule, email):
    field = rule['field']
    predicate = rule['predicate']
    value = rule['value']

    if field == 'From':
        return apply_predicate(predicate, email.sender, value)
    elif field == 'Subject':
        return apply_predicate(predicate, email.subject, value)
    elif field == 'Received Date/Time':
        return apply_date_predicate(predicate, email.received_at, value)


def apply_predicate(predicate, field_value, value):
    if predicate == 'CONTAINS':
        return value.lower() in field_value.lower()
    elif predicate == 'DOES_NOT_CONTAIN':
        return value.lower() not in field_value.lower()
    elif predicate == 'EQUALS':
        return field_value.lower() == value.lower()
    elif predicate == 'DOES_NOT_EQUAL':
        return field_value.lower() != value.lower()


def apply_date_predicate(predicate, date_value, value):
    parsed_date = datetime.strptime(value, '%Y-%m-%d %H:%M:%S')
    if predicate == 'LESS_THAN':
        return date_value < parsed_date
    elif predicate == 'GREATER_THAN':
        return date_value > parsed_date


def perform_actions(actions, email):
    creds = services.gmail.authenticate()
    service = build(constants.API_SERVICE_NAME, constants.API_VERSION, credentials=creds)
    # ['UNREAD', 'IMPORTANT', 'CATEGORY_PERSONAL', 'INBOX']
    for action in actions:
        if action == 'MARK_AS_READ':
            service.users().messages().modify(userId='me', id=email.id, body={'removeLabelIds': ['UNREAD']}).execute()
        elif action == 'MARK_AS_UNREAD':
            service.users().messages().modify(userId='me', id=email.id, body={'addLabelIds': ['UNREAD']}).execute()
        elif action == 'MOVE_MESSAGE':
            service.users().messages().modify(userId='me', id=email.id, body={'addLabelIds': ['CATEGORY_PROMOTIONS']}).execute()


if __name__ == '__main__':
    # emails_data = [
    #     {'id': '18e7a214a6a170d4', 'sender': 'Atish Abhang <atishabhang17@gmail.com>', 'subject': 'Test Mail',
    #      'received_at': '2024-03-26 15:09:34.000000'},
    #     {'id': '18d90207491aefb9', 'sender': 'Bard <bard-noreply@google.com>', 'subject': 'Bard is now Gemini',
    #      'received_at': '2024-02-09 04:37:42.000000'},
    # ]

    # Create DB object
    engine = db.local_db.create_database(constants.DB_NAME)
    _session = sessionmaker(bind=engine)
    session = _session()
    # Get all emails from DB
    emails_data = session.query(models.email.Email).all()

    file = 'rules.json'  # Path to your rules JSON file
    apply_rules(file, emails_data)
