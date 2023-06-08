from PIL import Image
import math

image = Image.new('L', (256, 256), 'black')
pixels = image.load()
for x in range(256):
    for y in range(256):
        pixels[x, y] = 128+int(63*math.sin(x/10) + 63*math.sin(y/10))

image.show()