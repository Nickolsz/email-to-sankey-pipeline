import email
import imaplib
import os
from bs4 import BeautifulSoup
import pandas as pd
from dotenv import load_dotenv
import re
import psycopg2
from class_MNB_model import predict_category1
from datetime import datetime


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
    text_cleaned = re.sub(r'http\S+', '', text)
    text_cleaned = re.sub(r'\S+@\S+', '', text_cleaned)
    text_cleaned = ' '.join(text_cleaned.split())
    return text_cleaned

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



def parse_email_date(date_str):
    # Try to parse the date string from the email
    try:
        parsed_date = datetime.strptime(date_str[:-6], '%a, %d %b %Y %H:%M:%S')
    except ValueError:
        # If parsing fails, log or return None
        return None
    return parsed_date

def email_main():
    mail = imaplib.IMAP4_SSL(HOST)
    mail.login(EMAIL, EMAIL_PASSWORD)
    emails = fetch_and_parse_emails(mail)
    
    for email in emails:
        try:
            predicted_category = predict_category1(email['Body'])
            email['Category'] = predicted_category
            email_date = parse_email_date(email['Date'])  # Convert date to proper format
            
            # If date parsing fails, set email_date to None (which will insert NULL in PostgreSQL)
            if email_date is None:
                email_date = None  # Use NULL in PostgreSQL for missing dates
            
            cur.execute("""
                INSERT INTO fetched_emails ("From", "Date", "Subject", "Body", "Category") VALUES 
                (%s, %s, %s, %s, %s)
                """, (email['From'], email_date, email['Subject'], email['Body'], email['Category']))
            
            conn.commit()
        
        except Exception as e:
            # If any other unexpected error occurs, skip this email and continue processing the rest
            continue
    
    cur.close()
    conn.close()
    mail.logout()


        
        
if __name__ == '__main__':
    email_main()