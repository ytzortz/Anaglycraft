from PIL import Image
import matplotlib.pyplot as plt
import cv2
import numpy as np


def grayscale(image_path):
    # Open the image file in grayscale mode (flag = 0)
    grayscale_img = cv2.imread(image_path, 0)
    cv2.imwrite("grayImage.png", grayscale_img)
    # Return the grayscale image as a NumPy array
    return grayscale_img

# # This does not really works. I'll try another modified version below that
# def get_non_white_pixel_locations_from_image(image, threshold=100):
#     # Check if the image is in BGR (as in OpenCV format) and convert to RGB
#     img_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    
#     # Get the dimensions of the image
#     height, width, _ = img_rgb.shape
    
#     # Initialize an empty list to store non-white pixel coordinates
#     non_white_pixels = []
    
#     # Iterate through each pixel in the image
#     for y in range(height):
#         for x in range(width):
#             r, g, b = img_rgb[y, x]  # Get the RGB values of the pixel
#             # print(f"\n\n\nr: {r}\ng: {g}\nb: {b}\n\n\n")
#             # Check if the pixel is not white (i.e., any of the RGB values is <= threshold)
#             intensity = int(0.299 * r + 0.587 * g + 0.114 * b)
#             if r <= threshold or g <= threshold or b <= threshold:
#                 non_white_pixels.append((x, y, intensity))  # Add the location of the non-white pixel
    
#     # TODO: to non_white_pixels -> 2D matrix me to intensity

#     return non_white_pixels

def get_non_white_pixel_locations_from_image(image, threshold=100):
    # Check if the image is in BGR (as in OpenCV format) and convert to RGB
    img_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    # Get the dimensions of the image
    height, width, _ = img_rgb.shape
    # Initialize an n×n matrix to store pixel intensities (all zeros initially)
    intensity_matrix = np.zeros((width, height), dtype=np.uint8)
    for y in range(height-1):
        for x in range(width-1):
            # Get RGB values
            r, g, b = img_rgb[y, x]
            
            # Calculate intensity using luminance formula
            intensity = int(0.299 * r + 0.587 * g + 0.114 * b)
            
            flag = False
            # threshold = 200

            # Store intensity in the matrix if below threshold
            if r <= threshold or g <= threshold or b <= threshold:
                intensity_matrix[y, x] = threshold
                flag = True

            # if r == 0 or g == 0 or b ==0:
            #     intensity_matrix[y, x] = intensity
            #     flag = True

            if x==width/2:  
                print(f"RGB:({r},{g},{b}), intensity:{intensity}, matrix content:{intensity_matrix[y, x]}, x:{x},y:{y} The if statement was:{flag}")
        # Plot intensity matrix
    try:
        plt.figure(figsize=(10, 8))
        plt.imshow(intensity_matrix, cmap='gray')
        plt.title(f'Intensity Matrix ({width}x{height})')
        plt.colorbar()
        plt.savefig('intensity_matrix_debug.png')
        print("Plot saved successfully.")
        plt.close()
    except Exception as e:
        print("Error while plotting:", e)
    
    # Optional: Save the raw intensity matrix
    # np.save('intensity_matrix.npy', intensity_matrix)

    return intensity_matrix

def add_padding(image, pixels):
    # Define the color of padding (white, which is 255 in grayscale)
    padding_color = 255
    
    # Use cv2.copyMakeBorder to add padding
    padded_image = cv2.copyMakeBorder(
        image,
        top=pixels,    # Padding for top
        bottom=pixels, # Padding for bottom
        left=pixels,   # Padding for left
        right=pixels,  # Padding for right
        borderType=cv2.BORDER_CONSTANT, 
        value=padding_color  # The color of the padding (white in this case)
    )
    
    # Return the padded image
    return padded_image

def normalized_value(x, a, b, c, d):
    normalized = c + ((x-a)/(b-a))*(d-c)
    return normalized

# def convert_to_black_and_white(grayscale_img, threshold=128):
#     # Apply the thresholding operation
#     _, binary_img = cv2.threshold(grayscale_img, threshold, 255, cv2.THRESH_BINARY)
#     cv2.imwrite("binaryImage.png", grayscale_img)
    
#     return binary_img
