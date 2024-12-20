import imageio.v3 as iio
import matplotlib.pyplot as plt
import numpy as np
from scipy.ndimage import distance_transform_edt 

# Load the grayscale image
image = iio.imread(uri="grayImage.png")

# Display the original image
plt.imshow(image, cmap='gray')
plt.title("Original Image")
plt.show()

# Set a threshold to convert the grayscale image to binary
threshold = 220  # Adjust based on the brightness levels in your image
binary_image = image > threshold

# Apply Distance Transform
distance_transformed = distance_transform_edt(binary_image)

# Display the Distance Transform result
plt.imshow(distance_transformed, cmap='gray')
plt.colorbar()  # Adds a color bar to show distance values
plt.title("Distance Transform")
plt.show()
