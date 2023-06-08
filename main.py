from tkinter import Tk, Canvas, Button, filedialog, Entry, messagebox, Label, ttk, colorchooser
from PIL import Image, ImageTk, ImageDraw, ImageFont

class ImageProcessor:
    def __init__(self, root):
        self.root = root
        self.canvas = Canvas(root, width=500, height=500)
        self.canvas.pack()

        self.image = Image.new("RGB", (500, 500), "white")  # Create a white background image
        self.photo_image = ImageTk.PhotoImage(self.image)
        self.canvas.create_image(0, 0, anchor="nw", image=self.photo_image)

        self.open_button = Button(root, text="Buka Gambar", command=self.open_image)
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

        self.pen_type_label = Label(root, text="Jenis Pena:")
        self.pen_type_label.pack(side="left")

        self.pen_type_combo = ttk.Combobox(root, values=["Titik", "Garis"], state="readonly")
        self.pen_type_combo.pack(side="left")
        self.pen_type_combo.current(0)

        self.pen_color_button = Button(root, text="Warna Pena", command=self.choose_pen_color)
        self.pen_color_button.pack(side="left")

        self.pen_color = "black"
        self.pen_size = 1

        self.canvas.bind("<B1-Motion>", self.draw_pixel)

    def open_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg;*.jpeg;*.png;*.bmp")])
        if file_path:
            self.image = Image.open(file_path).convert("RGB")  # Convert the opened image to RGB mode
            self.photo_image = ImageTk.PhotoImage(self.image)
            self.canvas.create_image(0, 0, anchor="nw", image=self.photo_image)

    def change_color(self):
        if self.image:
            self.image = self.image.convert("RGB")
            pixels = self.image.load()
            width, height = self.image.size

            for y in range(height):
                for x in range(width):
                    r, g, b = pixels[x, y]
                    pixels[x, y] = g, b, r  # Ganti urutan warna menjadi RGB

            self.photo_image = ImageTk.PhotoImage(self.image)
            self.canvas.create_image(0, 0, anchor="nw", image=self.photo_image)
            self.canvas.update()  # Update the canvas

    def zoom_in(self):
        if self.image:
            width, height = self.image.size
            new_width = int(width * 1.2)
            new_height = int(height * 1.2)
            self.image = self.image.resize((new_width, new_height))

            self.photo_image = ImageTk.PhotoImage(self.image)
            self.canvas.create_image(0, 0, anchor="nw", image=self.photo_image)

    def zoom_out(self):
        if self.image:
            width, height = self.image.size
            new_width = int(width / 1.2)
            new_height = int(height / 1.2)
            self.image = self.image.resize((new_width, new_height))

            self.photo_image = ImageTk.PhotoImage(self.image)
            self.canvas.create_image(0, 0, anchor="nw", image=self.photo_image)

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

    def add_text(self, text, edit_window):
        if self.image and text:
            draw = ImageDraw.Draw(self.image)
            width, height = self.image.size
            text_position = (width/2, height/2)
            text_color = (255, 255, 255)  # Putih
            font = ImageFont.truetype("arial.ttf", 36)  # Ganti dengan path font Anda

            text_width, text_height = draw.textsize(text, font=font)
            text_position = (text_position[0] - text_width/2, text_position[1] - text_height/2)

            draw.text(text_position, text, fill=text_color, font=font)

            self.photo_image = ImageTk.PhotoImage(self.image)
            self.canvas.create_image(0, 0, anchor="nw", image=self.photo_image)

            edit_window.destroy()
        else:
            messagebox.showerror("Error", "Teks tidak boleh kosong")

    def clear_edit(self):
        if self.image:
            self.image = Image.new("RGB", (400, 400), "white")  # Create a new white background image
            self.photo_image = ImageTk.PhotoImage(self.image)
            self.canvas.create_image(0, 0, anchor="nw", image=self.photo_image)

    def choose_pen_color(self):
        color = colorchooser.askcolor(title="Pilih Warna Pena")[1]
        if color:
            self.pen_color = color

    def draw_pixel(self, event):
        x, y = event.x, event.y
        draw = ImageDraw.Draw(self.image)

        if self.pen_type_combo.get() == "Titik":
            draw.ellipse((x, y, x + self.pen_size, y + self.pen_size), fill=self.pen_color)
        elif self.pen_type_combo.get() == "Garis":
            draw.line((x, y, x + self.pen_size, y + self.pen_size), fill=self.pen_color, width=self.pen_size)

        self.photo_image = ImageTk.PhotoImage(self.image)
        self.canvas.create_image(0, 0, anchor="nw", image=self.photo_image)

root = Tk()
image_processor = ImageProcessor(root)
root.mainloop()
