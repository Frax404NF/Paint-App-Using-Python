from tkinter import  Tk, Canvas, Button, filedialog, Entry, messagebox, Label, ttk, colorchooser
from PIL import Image, ImageTk, ImageDraw, ImageFont

class DrawingApp:
    def __init__(self, master):
        self.master = master
        self.canvas = Canvas(self.master, width=1920, height=500)
        self.canvas.pack()

        self.start_x = None
        self.start_y = None
        self.is_drawing = False

        self.image = None
        self.photo_image = None

        self.open_button = Button(master, text="Buka Gambar", command=self.open_image)
        self.open_button.pack(side="left")

        self.color_button = Button(root, text="Ganti Warna", command=self.change_color)
        self.color_button.pack(side="left")

        self.zoom_in_button = Button(root, text="Perbesar", command=self.zoom_in)
        self.zoom_in_button.pack(side="left")

        self.zoom_out_button = Button(root, text="Perkecil", command=self.zoom_out)
        self.zoom_out_button.pack(side="left")

        self.edit_button = Button(root, text="Edit Gambar", command=self.edit_image)
        self.edit_button.pack(side="left")

        self.clear_button = Button(root, text="Hapus Edit", command=self.clear_edit)
        self.clear_button.pack(side="left")

        self.draw_button = Button(root, text="Draw", command=self.toggle_draw)
        self.draw_button.pack(side="left")

        self.pen_color_button = Button(root, text="Warna Pena", command=self.choose_pen_color)
        self.pen_color_button.pack(side="left")

        self.canvas.bind("<B1-Motion>", self.draw)
        self.canvas.bind("<ButtonRelease-1>", self.reset)

        self.pen_color = "black"
        self.pen_size = 1


# fungsi input gambar
    def open_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg;*.jpeg;*.png;*.bmp")])
        if file_path:
            self.image = Image.open(file_path).convert("RGB") 
            self.photo_image = ImageTk.PhotoImage(self.image)
            self.canvas.create_image(0, 0, anchor="nw", image=self.photo_image)

# fungsi mengubah warna
# kayaknya mo ubah le ini
    def change_color(self):
        if self.image:
            self.image = self.image.convert("RGB")
            pixels = self.image.load()
            width, height = self.image.size

            for y in range(height):
                for x in range(width):
                    r, g, b = pixels[x, y]
                    pixels[x, y] = g, b, r 

            self.photo_image = ImageTk.PhotoImage(self.image)
            self.canvas.create_image(0, 0, anchor="nw", image=self.photo_image)

# fungsi perkecil
    def zoom_in(self):
        if self.image:
            width, height = self.image.size
            new_width = int(width * 1.2)
            new_height = int(height * 1.2)
            self.image = self.image.resize((new_width, new_height))

            self.photo_image = ImageTk.PhotoImage(self.image)
            self.canvas.create_image(0, 0, anchor="nw", image=self.photo_image)

# perbesar
    def zoom_out(self):
        if self.image:
            width, height = self.image.size
            new_width = int(width / 1.2)
            new_height = int(height / 1.2)
            self.image = self.image.resize((new_width, new_height))

            self.photo_image = ImageTk.PhotoImage(self.image)
            self.canvas.create_image(0, 0, anchor="nw", image=self.photo_image)

# fungsi edit image
# mo tambah le dsni
    def edit_image(self):
        if self.image:
            edit_window = Tk()
            edit_window.title("Edit Gambar")

            text_entry_label = Label(edit_window, text="Tambahkan teks:")
            text_entry_label.pack()

            text_entry = Entry(edit_window)
            text_entry.pack()

            text_button = Button(edit_window, text="Tambahkan Teks", command=lambda: self.add_text(text_entry.get(), edit_window))
            text_button.pack()

            edit_window.mainloop()

# fungsi tambah text
    def add_text(self, text, edit_window):
        if self.image and text:
            draw = ImageDraw.Draw(self.image)
            width, height = self.image.size
            text_position = (width/2, height/2)
            text_color = (255, 255, 255)  
            font = ImageFont.truetype("arial.ttf", 36) 

            text_width, text_height = draw.textsize(text, font=font)
            text_position = (text_position[0] - text_width/2, text_position[1] - text_height/2)

            draw.text(text_position, text, fill=text_color, font=font)

            self.photo_image = ImageTk.PhotoImage(self.image)
            self.canvas.create_image(0, 0, anchor="nw", image=self.photo_image)

            edit_window.destroy()
        else:
            messagebox.showerror("Error", "Teks tidak boleh kosong")

# fungsi hapus edit
    def clear_edit(self):
        if self.image:
            self.image = Image.new("img") 
            self.photo_image = ImageTk.PhotoImage(self.image)
            self.canvas.create_image(0, 0, anchor="nw", image=self.photo_image)

# fungsi ganti warna pen gambar
    def choose_pen_color(self):
        color = colorchooser.askcolor(title="Pilih Warna Pena")[1]
        if color:
            self.pen_color = color

# fungsi tombol gambar
    def toggle_draw(self):
        self.is_drawing = not self.is_drawing

# Fungsi gambar
    def draw(self, event):
        if self.is_drawing:
            if self.start_x and self.start_y:
                self.canvas.create_line((self.start_x, self.start_y, event.x, event.y), fill=self.pen_color)

        self.start_x = event.x
        self.start_y = event.y

    def reset(self, event):
        self.start_x = None
        self.start_y = None

if __name__ == "__main__":
    root = Tk()
    root.title("Drawing App")
    app = DrawingApp(root)
    root.mainloop()
