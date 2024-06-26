import email
import imaplib
import os
from bs4 import BeautifulSoup
import pandas as pd
from dotenv import load_dotenv
from class_model import *
import psycopg2

load_dotenv()

HOST = os.getenv('HOST')
EMAIL = os.getenv('EMAIL')
EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')
EXCEL_PATH = os.getenv('EXCEL_PATH')
PORT = os.getenv('PORT')
DB_PASS = os.getenv('DB_PASS')

conn = psycopg2.connect(host='localhost',dbname ='email_data',user='postgres',password = DB_PASS, port = PORT)
cur = conn.cursor()


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
        emails.append({'From': from_part, 'Date': date_part, 'Subject': subject_part, 'Body': body_cleaned, 'Category':''})
    return emails

def email_main():
    mail = imaplib.IMAP4_SSL(HOST)
    mail.login(EMAIL, EMAIL_PASSWORD)
    emails = fetch_and_parse_emails(mail)
    for email in emails:
        predicted_category = predict_category(email['Body'])
        email['Category'] = predicted_category
        cur.execute("""
             INSERT INTO fetched_emails ("From", "Date", "Subject", "Body", "Category") VALUES 
             (%s, %s, %s, %s, %s)
             """, (email['From'], email['Date'], email['Subject'], email['Body'], email['Category']))
        conn.commit()
    cur.close()
    conn.close()
    mail.logout()
        
        
if __name__ == '__main__':
    email_main()

