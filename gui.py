from tkinter import *
from data_to_sankey import *
#from class_model import *
from email_fetch import *
from categorizeself import *

def run_email_and_plot():
    email_main()
    all_others(lambda: on_button_click())

window = Tk()
window.geometry('1000x700')
window.title('Job Hunt Graphing')
frame = Frame(window, bd=5, bg = 'Black', pady = 2)

label = Label(window, text='Hello! This program is used to automatically categorize incoming emails about your job hunt, and then automatically creating a Sankey Graph with the relevant information.', font = ('Arial',25),
wraplength=700, justify="center")
rp_btn = Button(frame, 
                text='Read Emails, and Plot Sankey Graph', 
                command=run_email_and_plot)
p_btn = Button(frame, 
               text='Plot Sankey Graph', 
               command=on_button_click)
label.pack()
frame.pack(side=BOTTOM)
rp_btn.config( height = 8, width = 30 )
p_btn.config( height = 8, width = 30 )
rp_btn.pack(side='left')
p_btn.pack()

window.mainloop()
