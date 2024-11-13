import imageio.v3 as iio
import matplotlib.pyplot as plt
import numpy as np
from scipy.ndimage import distance_transform_edt
import os

# Directory containing your images
directory = ""  # Replace with the path to your images
output_directory = directory  # You can change this if you want to save in a different location

# Set the threshold value for binary conversion
threshold = 140

for i in range(1, 8):
    image_path = os.path.join(directory, f"./ptixiaki/DTransPipeline/img{i}.png")
    output_path = os.path.join(output_directory, f"./ptixiaki/DTransPipeline/new/newImg{i}.png")
   
    # Load the grayscale image
    image = iio.imread(uri=image_path)
    
    # Convert the image to binary based on the threshold
    binary_image = image > threshold

    # Apply Distance Transform
    distance_transformed = distance_transform_edt(binary_image)
    
    distance_transformed_normalized = (distance_transformed / distance_transformed.max() * 255).astype(np.uint8)


    plt.imshow(distance_transformed_normalized, cmap='gray')
    plt.colorbar()  # Adds a color bar to show distance values
    plt.title("Distance Transform")
    plt.show()

    # Save the Distance Transform result as a new image
    iio.imwrite(uri=output_path, image=distance_transformed_normalized)
    print(f"Processed and saved: {output_path}")
    
print("All images processed and saved.")
