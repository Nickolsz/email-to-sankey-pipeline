import email
import imaplib
import os
from bs4 import BeautifulSoup
import pandas as pd
from dotenv import load_dotenv

load_dotenv()
print('hello')

HOST = os.getenv('HOST')
USERNAME = os.getenv('USERNAME')
PASSWORD = os.getenv('PASSWORD')
EXCEL_PATH = os.getenv('EXCEL_PATH')

def clean_text(text):
    return text.replace('\r', '').replace('\n', ' ')

def get_email_body(email_message):
    for part in email_message.walk():
        content_type = part.get_content_type()
        charset = part.get_content_charset()
        body = part.get_payload(decode=True)
        if charset:
            body = body.decode(charset)
        if content_type == 'text/plain':
            return body
        elif content_type == 'text/html':
            soup = BeautifulSoup(body, 'html.parser')
            return soup.get_text()
    return ''

def fetch_and_parse_emails(mail):
    mail.select("inbox")
    _, email_data = mail.search(None, 'UNSEEN')
    emails = []
    for num in email_data[0].split():
        _, data = mail.fetch(num, '(RFC822)')
        _, b = data[0]
        email_message = email.message_from_bytes(b)
        from_part = email_message['From']
        date_part = email_message['Date']
        subject_part = email_message['Subject']
        body = get_email_body(email_message)
        body_cleaned = clean_text(body)
        emails.append({'From': from_part, 'Date': date_part, 'Subject': subject_part, 'Body': body_cleaned})
    return emails

def email_main():
    mail = imaplib.IMAP4_SSL(HOST)
    mail.login(USERNAME, PASSWORD)
    df_existing = pd.read_excel(EXCEL_PATH)
    emails = fetch_and_parse_emails(mail)
    df_new = pd.DataFrame(emails)
    df_combined = pd.concat([df_existing, df_new])
    df_combined.to_excel(EXCEL_PATH, index=False)
    mail.logout()

if __name__ == '__main__':
    email_main()
