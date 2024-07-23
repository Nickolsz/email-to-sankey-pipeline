from pathlib import Path
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage
from data_to_sankey import *
#from class_model import *
from email_fetch import *
from categorizeself import *


OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"C:\Users\Nick Olsz\Desktop\VSCode\email-to-sankey-pipeline\build\assets\frame0")

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

def run_email_and_plot():
    email_main()
    all_others(lambda: on_button_click())

window = Tk()
window.geometry("878x505")
window.configure(bg = "#FFFFFF")

canvas = Canvas(
    window,
    bg = "#FFFFFF",
    height = 505,
    width = 878,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
)

canvas.place(x = 0, y = 0)
image_image_1 = PhotoImage(
    file=relative_to_assets("image_1.png"))
image_1 = canvas.create_image(
    439.0,
    260.0,
    image=image_image_1
)

# Split the text into individual lines
lines = [
    "Welcome to Nolsz’s Email to Sankey automation. Use this program to automatically parse,",
    "store and categorize emails related to your on going job hunt. After all emails are read",
    "you can then plot the data into a Sankey graph."
]

# Define the starting y coordinate and the line height
start_y = 50
line_height = 30

# Loop through the lines and create centered text for each
for i, line in enumerate(lines):
    canvas.create_text(
        439.0,  # Centered horizontally
        start_y + i * line_height,  # Increment y position for each line
        anchor="center",
        text=line,
        fill="#FFFFFF",
        font=("Inter", 20 * -1)
    )

canvas.create_rectangle(
    12.0,
    140.0,  # Adjusted y-coordinate to move the rectangle down
    868.0000260410088,
    143.00000002552429,
    fill="#FFFFFF",
    outline="")

button_image_1 = PhotoImage(
    file=relative_to_assets("button_1.png"))
button_1 = Button(
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    command=run_email_and_plot,
    relief="flat"
)
button_1.place(
    x=99.0,
    y=238.0,
    width=304.0,
    height=67.0
)

button_image_2 = PhotoImage(
    file=relative_to_assets("button_2.png"))
button_2 = Button(
    image=button_image_2,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: on_button_click(),
    relief="flat"
)
button_2.place(
    x=493.0,
    y=238.0,
    width=304.0,
    height=67.0
)

window.resizable(False, False)
window.mainloop()
