from tkinter import *
from tkinter import Tk, Canvas, Button, filedialog,  messagebox, Label, colorchooser, Scale
from PIL import Image, ImageTk, ImageGrab, ImageFilter

class paintApp:
    def __init__(self):
        self.window = Tk()
        self.window.state("zoomed")
        self.window.title("Paint App With Python")

        #Variable
        self.eraser_color = "white"
        self.pen_color = "black"
        self.image = None
        self.is_drawing = False
        self.drawn_objects = []

        self.img_label = Label(self.window)
        self.img_label.pack()

        #Canvas
        self.canvas = Canvas(self.window, bg="white", bd=5, relief=GROOVE, height=500, width=1250)
        self.canvas.place(x=10, y=0)

        # Frame 
        self.color_frame = LabelFrame(self.window, text="Pen colors", relief=RIDGE, bg="white", font=("arial", 15, "bold"))
        self.color_frame.place(x=10, y=550, width=425, height=70,)

        self.tool_frame = LabelFrame(self.window, text="Edit tools", relief=RIDGE, bg="white", font=("arial", 15, "bold"))
        self.tool_frame.place(x=445, y=550, width=540, height=100)

        self.pen_size_frame = LabelFrame(self.window, text="Pen size", relief=RIDGE, bg="white", font=("arial", 15, "bold"))
        self.pen_size_frame.place(x=1000, y=550, width=200, height=70)

        # Color
        self.colors = ["#FF0000", "#80006d", "#FFC0CB", "#FFA500", "#FFFF00", "#008000", "#0000FF", "#A52A2A", "#FFFFFF", "#000000", "#808080"]

        # Color Button
        i = j = 0

        for color in self.colors:
            Button(self.color_frame, bd=3, bg=color, relief=RIDGE, width=3, command=lambda col=color: self.select_color(col)).grid(row=j, column=i, padx=2)
            i += 1

        # Tool_Button
        self.btn_canvas_color = Button(self.tool_frame, width=8, text="Canvas", bd=4, command=self.canvas_color, relief=RIDGE)
        self.btn_canvas_color.grid(row=0, column=0, padx=2)

        self.add_img = Button(self.tool_frame, width=8, text="Add image", bd=4, command=self.add_image, relief=RIDGE)
        self.add_img.grid(row=0, column=1, padx=2)

        self.save_btn = Button(self.tool_frame, width=8, text="Save", bd=4, command=self.save, relief=RIDGE)
        self.save_btn.grid(row=0, column=2, padx=2)

        self.eraser_btn = Button(self.tool_frame, width=8,  text="Eraser", bd=4, command=self.eraser, relief=RIDGE)
        self.eraser_btn.grid(row=0, column=3, padx=2)

        self.clear_btn = Button(self.tool_frame, width=8,  text="Clear", bd=4, command=self.clear, relief=RIDGE)
        self.clear_btn.grid(row=0, column=4, padx=2)

        self.btn_zoom_in = Button(self.tool_frame, width=8,  text="Zoom in", bd=4, command=self.zoom_in, relief=RIDGE)
        self.btn_zoom_in.grid(row=0, column=5, padx=2)

        self.btn_zoom_out = Button(self.tool_frame, width=8,  text="Zoom out", bd=4, command=self.zoom_out, relief=RIDGE)
        self.btn_zoom_out.grid(row=0, column=6, padx=2)

        # btn row 2
        self.blur_btn = Button(self.tool_frame, width=8,  text="Blur", bd=4, command=self.blur, relief=RIDGE)
        self.blur_btn.grid(row=1, column=1, padx=2, pady=3)

        self.contour_btn = Button(self.tool_frame, width=8,  text="Contour", bd=4, command=self.contour, relief=RIDGE)
        self.contour_btn.grid(row=1, column=2, padx=2, pady=3)

        self.embos_btn = Button(self.tool_frame, width=8,  text="Embos", bd=4, command= self.emboss, relief=RIDGE)
        self.embos_btn.grid(row=1, column=3, padx=2, pady=3)

        self.sharpen_btn = Button(self.tool_frame, width=8,  text="Sharpen", bd=4, command= self.sharpen, relief=RIDGE)
        self.sharpen_btn.grid(row=1, column=4, padx=2, pady=3)

        self.undo_btn = Button(self.tool_frame, width=8,  text="Undo", bd=4, command= self.undo, relief=RIDGE)
        self.undo_btn.grid(row=1, column=5, padx=2, pady=3)


        # Pen and Eraser Size  
        self.pen_size = Scale(self.pen_size_frame, orient=HORIZONTAL, from_=0, to=50, length=170)
        self.pen_size.set(1)
        self.pen_size.grid(row=0, column=0)

        # Bind Mouse Events
        self.canvas.bind("<B1-Motion>", self.paint)

        self.window.mainloop()

    def canvas_color(self):
        color = colorchooser.askcolor()
        self.canvas.configure(bg=color  [1])
        self.eraser_color = color[1]

    def add_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg;*.jpeg;*.png;*.bmp")])
        if file_path:
            self.image = Image.open(file_path).convert("RGB")
            img = ImageTk.PhotoImage(self.image)
            if self.image.width > self.canvas.winfo_width() or self.image.height > self.canvas.winfo_height():
                self.image.thumbnail((self.canvas.winfo_width(), self.canvas.winfo_height()), Image.ANTIALIAS)
                
            img = ImageTk.PhotoImage(self.image)
            self.canvas.create_image(self.canvas.winfo_width() / 2, self.canvas.winfo_height() / 2, image=img)
            self.canvas.image = img
            

    def undo(self):
        if self.drawn_objects:
            action = self.drawn_objects.pop()
            self.canvas.delete(action)

    def save(self):
        file_name = filedialog.asksaveasfilename(defaultextension=".jpg")
        ImageGrab.grab().save(file_name)
        messagebox.showinfo("Paint Notification", "Gambar berhasil disimpan di " + str(file_name))

    def eraser(self):
        self.pen_color = self.eraser_color

    def clear(self):
        self.canvas.delete("all")
        self.image = None

    def paint(self, event):
        x1, y1 = (event.x - 2), (event.y - 2)
        x2, y2 = (event.x + 2), (event.y + 2)
        draw = self.canvas.create_oval(x1, y1, x2, y2, fill=self.pen_color, outline=self.pen_color, width=self.pen_size.get())
        self.drawn_objects.append(draw)
    
    def select_color(self, col):
        self.pen_color = col


    # Fungi filter -filter
    def blur(self):
        self.image = self.image.filter(ImageFilter.BLUR)

        img = ImageTk.PhotoImage(self.image)
        if self.image.width > self.canvas.winfo_width() or self.image.height > self.canvas.winfo_height():
            self.image.thumbnail((self.canvas.winfo_width(), self.canvas.winfo_height()), Image.ANTIALIAS)
            
        img = ImageTk.PhotoImage(self.image)
        self.canvas.create_image(self.canvas.winfo_width() / 2, self.canvas.winfo_height() / 2, image=img)
        self.canvas.image = img
        self.img_label.image = img

    def emboss(self):
        self.image = self.image.filter(ImageFilter.EMBOSS)
        img = ImageTk.PhotoImage(self.image)
        if self.image.width > self.canvas.winfo_width() or self.image.height > self.canvas.winfo_height():
            self.image.thumbnail((self.canvas.winfo_width(), self.canvas.winfo_height()), Image.ANTIALIAS)
            
        img = ImageTk.PhotoImage(self.image)
        self.canvas.create_image(self.canvas.winfo_width() / 2, self.canvas.winfo_height() / 2, image=img)
        self.canvas.image = img
        self.img_label.image = img

    def sharpen(self):
        self.image = self.image.filter(ImageFilter.SHARPEN)
        img = ImageTk.PhotoImage(self.image)
        if self.image.width > self.canvas.winfo_width() or self.image.height > self.canvas.winfo_height():
            self.image.thumbnail((self.canvas.winfo_width(), self.canvas.winfo_height()), Image.ANTIALIAS)
            
        img = ImageTk.PhotoImage(self.image)
        self.canvas.create_image(self.canvas.winfo_width() / 2, self.canvas.winfo_height() / 2, image=img)
        self.canvas.image = img
        self.img_label.image = img

    def contour(self):
        self.image = self.image.filter(ImageFilter.CONTOUR)
        img = ImageTk.PhotoImage(self.image)
        if self.image.width > self.canvas.winfo_width() or self.image.height > self.canvas.winfo_height():
            self.image.thumbnail((self.canvas.winfo_width(), self.canvas.winfo_height()), Image.ANTIALIAS)
            
        img = ImageTk.PhotoImage(self.image)
        self.canvas.create_image(self.canvas.winfo_width() / 2, self.canvas.winfo_height() / 2, image=img)
        self.canvas.image = img
        self.img_label.image = img

    def zoom_out(self):
        if self.image:
            width, height = self.image.size
            new_width = int(width / 1.1)
            new_height = int(height / 1.1)
            resized_image = self.image.resize((new_width, new_height))

            img = ImageTk.PhotoImage(resized_image)
            self.canvas.create_image(self.canvas.winfo_width() / 2, self.canvas.winfo_height() / 2, anchor="center", image=img)
            self.canvas.image = img
            self.image = resized_image

    def zoom_in(self):
        if self.image:
            width, height = self.image.size
            new_width = int(width * 1.1)
            new_height = int(height * 1.1)
            resized_image = self.image.resize((new_width, new_height))

            img = ImageTk.PhotoImage(resized_image)
            self.canvas.create_image(self.canvas.winfo_width() / 2, self.canvas.winfo_height() / 2, anchor="center", image=img)
            self.canvas.image = img
            self.image = resized_image

app = paintApp()

