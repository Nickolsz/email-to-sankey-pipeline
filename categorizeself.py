import os
from dotenv import load_dotenv
import psycopg2
from tkinter import *
from tkinter import scrolledtext

load_dotenv()

PORT = os.getenv('PORT')
DB_PASS = os.getenv('DB_PASS')

def create_connection():
    return psycopg2.connect(host='localhost', dbname='email_data', user='postgres', password=DB_PASS, port=PORT)

def create_window():
    window = Tk()
    window.geometry('1000x700')
    return window

def append_category(category, cur, conn, result, counter):
    if counter < len(result):
        cur.execute("""
            UPDATE fetched_emails 
            SET "Category" = %s 
            WHERE "Body" LIKE %s;
        """, 
        (category, f"%{result[counter][0]}%"))
        
        conn.commit()


def nClick(label_update, counter, result):
    counter[0] += 1
    label_update(result, counter)

def label_update(result, counter, text_box, buttons, window, on_closing, on_complete):
    if counter[0] < len(result):
        text_box.config(state=NORMAL)
        text_box.delete('1.0', END)
        text_box.insert(INSERT, result[counter[0]][0])
        text_box.config(state=DISABLED)
    else:
        for btn in buttons:
            btn.destroy()
        text_box.destroy()
        on_closing(window)
        if on_complete:
            on_complete()

def all_others(on_complete=None):
    conn = create_connection()
    cur = conn.cursor()

    window = create_window()
    window.protocol("WM_DELETE_WINDOW", lambda: on_closing(window, cur, conn))
    
    cur.execute("""
        SELECT fetched_emails."Body" FROM fetched_emails WHERE fetched_emails."Category" = 'other';
    """)
    result = cur.fetchall()
    
    if not result:
        print("No emails to categorize.")
        on_closing(window, cur, conn)
        if on_complete:
            on_complete()
        return

    text_box = scrolledtext.ScrolledText(window, wrap=WORD, width=100, height=20)
    text_box.pack(pady=20)

    possibilities = ["Applied", "Rejection", "Phone", "Interview", "Assessment", "Offer"]
    buttons = []
    counter = [0]

    for i in range(len(possibilities)):
        btn = Button(window, text=possibilities[i], 
                     command=lambda i=i: [append_category(possibilities[i], cur, conn, result, counter[0]), 
                                          nClick(lambda res, cnt: label_update(res, cnt, text_box, buttons, window, on_closing, on_complete), 
                                                 counter, result)])
        buttons.append(btn)
        btn.pack(side='left')

    label_update(result, counter, text_box, buttons, window, lambda win: on_closing(win, cur, conn), on_complete)

    window.mainloop()

def on_closing(window, cur=None, conn=None):
    if cur:
        cur.close()
    if conn:
        conn.close()
    if window.winfo_exists():
        window.destroy()

if __name__ == '__main__':
    all_others()
