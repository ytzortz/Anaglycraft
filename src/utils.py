# Libraries used in debugging
# from PIL import Image
# import matplotlib.pyplot as plt 
import cv2
import numpy as np
from scipy.ndimage import distance_transform_edt 
import os
import json

def grayscale(image_path, negative=False):
    # Open the image file in grayscale mode (flag = 0)
    grayscale_img = cv2.imread(image_path, 0)
    
    if grayscale_img is None:
        raise ValueError("Image not found. Check the image path.")

    # Save the grayscale image for DEBUGGING if needed
    # cv2.imwrite("grayImage.png", grayscale_img)
    
    # Apply negative filter if the flag is True
    if negative:
        grayscale_img = 255 - grayscale_img  # Invert pixel values
        # cv2.imwrite("negativeImage.png", grayscale_img)  # Save the negative image (debug)

    # Return the final processed image
    return grayscale_img


def get_non_white_pixel_locations_from_image(image, threshold=100, maxDepth=50, typeBlur = "dt"):
    
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
            
    # DEBUGGING code
    # show the original image and then after the bluring
    # plt.imshow(image, cmap='gray')
    # plt.title("Original Image")
    # plt.show()
    # plt.imshow(smoothed_image, cmap='gray')
    # plt.title(f"{smoothing_title} Result")
    # plt.colorbar()
    # plt.show()
    

    smoothed_image_normalized_uint8 = cv2.normalize(smoothed_image, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)
    # Check if the image is in BGR (as in OpenCV format) and convert to RGB
    img_rgb = cv2.cvtColor(smoothed_image_normalized_uint8, cv2.COLOR_BGR2RGB)
    # Get the dimensions of the image
    height, width, _ = img_rgb.shape
    # Initialize an n×n matrix to store pixel intensities (all zeros initially)
    intensity_matrix = np.zeros((height, width), dtype=np.uint8)
    for y in range(height-1):
        for x in range(width-1):

            # Get RGB values
            r, g, b = img_rgb[y, x]
            # Calculate intensity using luminance formula
            intensity = int(0.299 * r + 0.587 * g + 0.114 * b)
            if r <= threshold or g <= threshold or b <= threshold:
                normalized_intensity = int(normalized_value(intensity, 0, threshold, 0, maxDepth))
                # intensity_matrix[y, x] = maxDepth #this is the previous, before the normalization
                intensity_matrix[y, x] = maxDepth - normalized_intensity 

    # For debugging
    # try:
    #     plt.figure(figsize=(10, 8))
    #     plt.imshow(intensity_matrix, cmap='gray')
    #     plt.title(f'Intensity Matrix ({width}x{height})')
    #     plt.colorbar()
    #     plt.savefig(f'ptixiaki/src/images/imagesAfter/intensity_matrices/intensity_matrix_debug{height}.png')
    #     print("Plot saved successfully.")
    #     plt.close()
    # except Exception as e:
    #     print("Error while plotting:", e)
    
    # DEBUG code
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
        value=padding_color  # The color of the padding
    )
    
    # Return the padded image
    return padded_image


# normalizing these values: [a, b] -> [c, d]
def normalized_value(x, a, b, c, d):
    normalized = c + ((x-a)/(b-a))*(d-c)
    return normalized

# used in load_config 
def validate_config(config):
    errors = []
    
    # Check if required fields exist
    required_fields = ["path_image", "path_output", "output_file_name", 
                      "depth", "padding", "threshold", "negative", "blurMethod", "show_timing"]
    
    for field in required_fields:
        if field not in config:
            errors.append(f"Missing required field: {field}")
    
    if errors:  # If we're missing required fields, return early
        return False, errors
        
    # Validate paths
    if not os.path.exists(config["path_image"]):
        errors.append(f"Image path does not exist: {config['path_image']}")
    if not os.path.exists(config["path_output"]):
        errors.append(f"Output path does not exist: {config['path_output']}")
    
    # Validate numeric values
    if not isinstance(config["depth"], int) or config["depth"] <= 2:
        errors.append("Depth must be an integer greater than 2")
    
    if not isinstance(config["padding"], int) or config["padding"] <= 0:
        errors.append("Padding must be a positive integer")
    
    if not isinstance(config["threshold"], int) or not 0 <= config["threshold"] <= 255:
        errors.append("Threshold must be an integer between 0 and 255")
    
    # Validate negative boolean
    if not isinstance(config["negative"], bool):
        errors.append("Negative must be a boolean value")
    
    # Validate blur method
    if config["blurMethod"] not in ["dt", "gaussian", "box"]:
        errors.append("Blur method must be one of: dt, gaussian, box")
    
    # Validate timing boolean
    if not isinstance(config["show_timing"], bool):
        errors.append("Show timing must be a boolean value")
    
    return len(errors) == 0, errors


def load_config(filename="config.json"):
    try:
        with open(filename, 'r') as f:
            config = json.load(f)
        
        is_valid, errors = validate_config(config)
        if not is_valid:
            print("Configuration validation failed:")
            for error in errors:
                print(f"- {error}")
            return None
            
        return config
        
    except FileNotFoundError:
        print(f"Configuration file not found: {filename}")
        return None
    except json.JSONDecodeError:
        print(f"Invalid JSON in configuration file: {filename}")
        return None
    except Exception as e:
        print(f"Error loading configuration: {str(e)}")
        return None
    

