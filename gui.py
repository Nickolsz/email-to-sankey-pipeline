from tkinter import *
from data_to_sankey import *
#from class_model import *
from email_fetch import *
from self-categorize import *

window = Tk()
window.geometry('1000x700')
window.title('Job Hunt Graphing')
frame = Frame(window, bg = 'pink',bd = 5)

label = Label (window, text = 'Hello! Please use this program in an effort to better keep track of your ongoing job hunt.')

rp_btn = Button(frame, 
                text = 'Read Emails, and Plot Sankey Graph', 
                command=lambda:[all_others(),email_main(),on_button_click()],
                )
p_btn = Button(frame, 
               text = 'Plot Sankey Graph', 
               command = on_button_click,
               )
label.pack()
frame.pack()
rp_btn.pack(side='left')
p_btn.pack()

window.mainloop()