# This file will take an image and blur it 

import imageio.v3 as iio
import ipympl
import matplotlib.pyplot as plt
import skimage as ski


image = iio.imread(uri="grayImage.png")

# display the image
# fig, ax = plt.subplots()
# ax.imshow(image)
plt.imshow(image)
plt.show()



sigma = 5.0


# apply Gaussian blur, creating a new image
blurred = ski.filters.gaussian(
    image, sigma=(sigma, sigma), truncate=3.5, channel_axis=-1)

# print(image.ndim)
plt.imshow(blurred)
# color map grayscale
plt.show()
