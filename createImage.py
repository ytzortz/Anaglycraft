from PIL import Image


def create_white_image(width, height, output_path = "whiteImage.png"):
    white_image = Image.new("RGB", (width, height), color="white")
    white_image.save(output_path)


def create_white_image_with_black_dot(width, height, output_path="imageDot.png"):
    white_image = Image.new("RGB", (width, height), color="white")
    pixels = white_image.load()

    # This is how we find the center of image
    center_x = width // 2      #   // ---> returns the integer part of the division
    center_y = height // 2
    pixels[center_x, center_y] = (0, 0, 0)
    white_image.save(output_path)



if __name__ == "__main__":
    width = 300  
    height = 200  

    create_white_image(width, height)
    create_white_image_with_black_dot(width, height)



    

