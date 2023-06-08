from PIL import Image
import numpy as np

image = Image.open('boat.jpg')
image_array = np.array(image)
print('shape', image_array.shape)
image_array = 255 - image_array
image_array[100:300, 170:350] = np.array([18, 155, 176])
out_image = Image.fromarray(image_array)

# out_image.save('numpy-image.jpg')
out_image.show()