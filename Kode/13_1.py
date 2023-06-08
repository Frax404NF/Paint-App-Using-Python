from PIL import Image

image = Image.open('boat.jpg')
pixels = image.load()
for x in range(image.size[0]-20): # image.size[0] is the image width
    for y in range(image.size[1]): # image.size[1] is the image height
        r, _, _ = pixels[x, y]
        _, g, _ = pixels[x+10, y]
        _, _, b = pixels[x+20, y]
        pixels[x, y] = (r, g, b)

image.show()
