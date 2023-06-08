from tkinter import *
from tkinter import Scale
window = Tk()
window.state("zoomed")
window.title("Paint App")

#Canvas
canvas = Canvas(window, bg="white", bd=5, relief=GROOVE, height=650, width=1500)
canvas.place(x=10, y=100)

# Function


# Frame 
color_frame = LabelFrame(window, text="color", relief=RIDGE, bg="white", font=("arial", 15, "bold"))
color_frame.place(x=10, y=10, width=400, height=70)

tool_frame = LabelFrame(window, text="Tool", relief=RIDGE, bg="white", font=("arial", 15, "bold"))
tool_frame.place(x=445, y=10, width=200, height=70)

pen_size = LabelFrame(window, text="size", relief=RIDGE, bg="white", font=("arial", 15, "bold"))
pen_size.place(x=670, y=10, width=200, height=70)
# Color
#          red        purple    pink        orange      yellow     green     blue       Brown       White     Black       Grey
colors = ["#FF0000", "#80006d", "#FFC0CB", "#FFA500", "#FFFF00", "#008000", "#0000FF", "#A52A2A", "#FFFFFF", "#000000", "#808080", ]

# Button
i = j = 0
for color in colors :
    Button(color_frame, bd=3, bg = color, relief=RIDGE, width=3).grid(row = j, column = i, padx = 1)
    i = i+1

#Tool_Button
canvas_color_b1 = Button(tool_frame, text="Canvas", bd=4, command=None, relief=RIDGE)
canvas_color_b1.grid(row = 0, column = 0, padx=2)

save_b2 = Button(tool_frame, text="Save", bd=4, command=None, relief=RIDGE)
save_b2.grid(row = 0, column = 1, padx=2)

eraser_b3 = Button(tool_frame, text="Eraser", bd=4, command=None, relief=RIDGE)
eraser_b3.grid(row = 0, column = 2, padx=2)

clear_b4 = Button(tool_frame, text="Clear", bd=4, command=None, relief=RIDGE)
clear_b4.grid(row = 0, column = 3, padx=2)

# Pen and Eraser Size  
pen_size = Scale(pen_size, orient=HORIZONTAL, from_= 0, to = 50, length=170)
pen_size.set(1)
pen_size.grid(row = 0, column=0)

window.mainloop()