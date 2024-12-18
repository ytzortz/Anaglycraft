
# AYTO EINAI TO ΚΑΝΟΝΙΚΟ FILE


from PIL import Image
import matplotlib.pyplot as plt
import cv2
import numpy as np
from scipy.ndimage import distance_transform_edt 


def grayscale(image_path, negative=False):
    # Open the image file in grayscale mode (flag = 0)
    grayscale_img = cv2.imread(image_path, 0)
    
    # if grayscale_img is None:
    #     raise ValueError("Image not found. Check the image path.")

    # Save the grayscale image
    cv2.imwrite("grayImage.png", grayscale_img)
    
    # Apply negative filter if the flag is True
    if negative:
        grayscale_img = 255 - grayscale_img  # Invert pixel values
        cv2.imwrite("negativeImage.png", grayscale_img)  # Save the negative image

    # Return the final processed image
    return grayscale_img


def get_non_white_pixel_locations_from_image(image, threshold=100, maxDepth=50, typeBlur = "dt"):
    
    # new stuff here. Im trying to do the DT and check the results.
    plt.imshow(image, cmap='gray')
    plt.title("Original Image")
    plt.show()
    # Set a threshold to convert the grayscale image to binary
    # threshold = 50  # Adjust based on the brightness levels in your image
    binary_image = image > threshold


    # Apply blur technique here
    if typeBlur == "dt":  # Apply Distance Transform
        smoothed_image = distance_transform_edt(binary_image)
        smoothing_title = "Distance Transform"
    elif typeBlur == "gaussian":
        smoothed_image = cv2.GaussianBlur(image, (7, 7), 1.5)
        smoothing_title = "Gaussian Blur"
        # τα νουμερα 5χ5 ειναι το matrix (μονο ODD numbers). Μεγαλυτερα νουμερα -> πιο πολυ blur 
        # το αλλο νουμερο ειναι το standart deviation. Μεγαλο -> πιο πολυ blur
    elif typeBlur == "box":
        smoothed_image = cv2.blur(image, (5, 5))  # Simple averaging kernel
        smoothing_title = "Box Filter (Mean Blur)"
    else:  # Default to Distance Transform
        smoothed_image = distance_transform_edt(binary_image)
        smoothing_title = "Distance Transform (Default)"
            


    plt.imshow(smoothed_image, cmap='gray')
    plt.title(f"{smoothing_title} Result")
    plt.colorbar()
    plt.show()


    # distance_transformed = distance_transform_edt(binary_image)
    
    # Display the Distance Transform result
    plt.imshow(smoothed_image, cmap='gray')
    plt.colorbar()  # Adds a color bar to show distance values
    plt.title("Distance Transform")
    plt.show()

    smoothed_image_normalized_uint8 = cv2.normalize(smoothed_image, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)
    # Check if the image is in BGR (as in OpenCV format) and convert to RGB
    img_rgb = cv2.cvtColor(smoothed_image_normalized_uint8, cv2.COLOR_BGR2RGB)
    img_rgb2 = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    # Get the dimensions of the image
    height, width, _ = img_rgb.shape
    height2, width2, _ = img_rgb2.shape
    # print(f"height x width of img_rgb:{height} x {width}\nheight x width of img_rgb2:{height2} x {width2}")
    # Initialize an n×n matrix to store pixel intensities (all zeros initially)
    intensity_matrix = np.zeros((height, width), dtype=np.uint8)
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
                normalized_intensity = int(normalized_value(intensity, 0, threshold, 0, maxDepth))
                # intensity_matrix[y, x] = maxDepth #this is the previous, before the normalization
                intensity_matrix[y, x] = maxDepth - normalized_intensity 
                flag = True

            # if x==width/2:  
            #     print(f"RGB:({r},{g},{b}), intensity:{intensity}, matrix content:{intensity_matrix[y, x]}, x:{x},y:{y} The if statement was:{flag}")
        # Plot intensity matrix
    try:
        plt.figure(figsize=(10, 8))
        plt.imshow(intensity_matrix, cmap='gray')
        plt.title(f'Intensity Matrix ({width}x{height})')
        plt.colorbar()
        plt.savefig(f'ptixiaki/src/images/imagesAfter/intensity_matrices/intensity_matrix_debug{height}.png')
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


# [a, b] -> [c, d]
def normalized_value(x, a, b, c, d):
    normalized = c + ((x-a)/(b-a))*(d-c)
    return normalized


