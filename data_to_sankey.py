import plotly.graph_objects as go
import psycopg2
import os
from dotenv import load_dotenv
import plotly.io as pio
import webview
import tempfile

load_dotenv()
PORT = os.getenv('PORT')
DB_PASS = os.getenv('DB_PASS')
conn = psycopg2.connect(host='localhost', dbname='email_data', user='postgres', password=DB_PASS, port=PORT)
cur = conn.cursor()

possibilities = ["Applied", "Rejection", "Phone", "Interview", "Assessment", "Offer"]
count_dict = {}
source = []
target = []
value = []

def read_and_plot():
    for p in possibilities:
        cur.execute("""
                SELECT count(*) FROM fetched_emails WHERE fetched_emails."Category" = %s;
                """,
                (p,))
        result = cur.fetchone()
        count_dict[p] = result[0]
    conn.commit()
    cur.close()
    conn.close()

    if count_dict['Interview'] > count_dict['Phone']:
        No_Response = count_dict['Applied'] - count_dict['Rejection'] - (count_dict['Interview'] - count_dict['Phone']) - count_dict['Phone']
    else:
        No_Response = count_dict['Applied'] - count_dict['Rejection'] - count_dict['Phone'] 

    # Applied to Rejection
    source.append(0)
    target.append(1)
    value.append(count_dict['Rejection'])

    # Applied to No Response
    if No_Response > 0:
        source.append(0)
        target.append(6)
        value.append(No_Response)

    # Applied to Phone
    source.append(0)
    target.append(2)
    value.append(count_dict['Phone'])

    # Applied to Left Over Interview
    if count_dict['Interview'] > count_dict['Phone']:
        source.append(0)
        target.append(3)
        value.append(count_dict['Interview'] - count_dict['Phone'])

    # Phone to Interview
    source.append(2)
    target.append(3)
    value.append(count_dict['Phone'])

    # Assessment to Interview
    if count_dict['Assessment'] > 0:
        source.append(4)
        target.append(3)
        value.append(count_dict['Assessment'])

    # Interview to Offer
    source.append(3)
    target.append(5)
    value.append(count_dict['Offer'])

    colors = ["rgba(31, 119, 180, 0.6)", "rgba(255, 0, 0, 0.6)", "rgba(255, 204, 229, 0.6)", "rgba(44, 160, 44, 0.6)", "rgba(148, 103, 189, 0.6)", "rgba(153, 0, 153, 0.6)", "rgba(255, 0, 0, 0.6)"]

    fig = go.Figure(go.Sankey(
        arrangement='snap',
        node=dict(
            pad=250,
            thickness=10,
            line=dict(color="black", width=0.5),
            label=["Applied", "Rejected", "Phone", "Interview", "Assessment", "Offer", "No Response"],
            color=colors,
            align='center',
        ),
        link=dict(
            source=source,
            arrowlen = 10,
            target=target,
            value=value,
            color=[colors[s] for s in source],
            line=dict(color="black", width=0.5)
        )
    ))

    fig.update_layout(
        autosize=False,
        width=1800 * 0.8,  
        height=900 * 0.8, 
        margin=dict(l=0, r=0, t=0, b=0)
    )
    
    return pio.to_html(fig, full_html=False)

def show_plot_in_webview(html_string):
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.html')
    temp_file.write(html_string.encode('utf-8'))
    temp_file.close()
    
    webview.create_window('Sankey Diagram', temp_file.name, width=1800, height=900, resizable=True)
    webview.start()

def on_button_click():
    html_str = read_and_plot()
    show_plot_in_webview(html_str)
    
if __name__ == '__main__':
    html_str = read_and_plot()
    show_plot_in_webview(html_str)
