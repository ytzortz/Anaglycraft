from PIL import Image, ImageDraw


# returns a plain white image size width X height
def create_white_image(width, height):
    white_image = Image.new("RGB", (width, height), color="white")
    return white_image

# adds a spot in image (arg)
def add_black_dot(width, height, image):
    pixels = image.load()
    pixels[width-1, height-1] = (0, 0, 0) # color black whatever other color we want
    return image

# creates a straight line
def create_line(widthStart, heightStart, widthEnd, heightEnd, image):
    startLine = (widthStart-1, heightStart-1)    # The start and the end of the line I want to draw
    endLine = (widthEnd-1, heightEnd-1)
    ImageDraw.Draw(image).line([startLine, endLine], fill="black", width=1)
    return image
    
# saves image by default as image.png inside the dir of called script
def save_image(image, filename = "image.png", path = "."):
    full_path = f"{path}/{filename}"
    image.save(full_path)



# reads a file that has the format: string arg1 arg2 etc
# this will give varius commands so an image is generated
def generate_image(file_path):

    if not file_path:
        print("File path cannot be empty or None.")
        return
    
    with open(file_path, 'r') as file:

        first_line = file.readline().strip().split()
        if first_line[0] == "create":
            image = create_white_image(int(first_line[1]), int(first_line[2])) 
            print("created image size " + first_line[1] + " x " + first_line[2])  # DEBUG
        else:
            print("Incorrect action in file. The file should start with \"create\" action   " + first_line[1])
            return

        for line in file:
            parts = line.strip().split()
            if len(parts) == 0:
                continue  # skip empty lines

            action = parts[0] # this indicates what action will be performed
            args = parts[1:] if len(parts) > 1 else []

            print(f"Action: {action}, Args: {', '.join(args)}")  # DEBUG

            if action == "dot":
                image = add_black_dot(int(args[0]), int(args[1]), image)
                print("black dot in " + args[0] + " , " + args[1])  # DEBUG

            elif action == "line":
                if len(args) >= 4:
                    image = create_line(int(args[0]), int(args[1]), int(args[2]), int(args[3]), image)
                    print(f"Created line from {args[0]}, {args[1]} to {args[2]}, {args[3]}")  # DEBUG
                else:
                    print(f"Insufficient arguments for action 'line'. Expected: line x1 y1 x2 y2")

            
            elif action == "save":
                if args:  # check if args is not empty
                    if len(args) == 2:
                        save_image(image, args[0], args[1])
                    elif len(args) == 1:
                        save_image(image, args[0])
                    else:
                        save_image(image)
                else:
                    save_image(image)           

            else:
                print(f"Unknown action: {action}")
                return 0




if __name__ == "__main__":
    width = 300  
    height = 200  

    generate_image("basicImage.txt")