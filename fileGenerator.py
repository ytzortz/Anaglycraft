
#   EINAI TO ΠΑΛΙΟ file. ΤΟ ΚΑΙΝΟΥΡΓΙΟ ΕΙΝΑΙ ΤΟ produceOBJ.py


# παραγει αρχειο σαν τα txt που ηδη εχω
# Για αρχη θελουμε να κανουμε το αρχειο να φτιαχνει ενα .xyz με αυτες τα dots 

# 1.0 1.0 0.0
# 1.0 -1.0 0.0
# -1.0 -1.0 0.0
# -1.0 1.0 0.0
# 1.0 1.0 1.0
# 1.0 -1.0 1.0
# -1.0 -1.0 1.0
# -1.0 1.0 1.0

# αλλα να εχουν βημα 0.1 (για να ειναι πιο πολλα)

import os


def write_to_file(file_name, content_list):
    # Write the content to the file, overwriting if it already exists
    with open(file_name, 'w') as file:
        for item in content_list:
            file.write(item + '\n')
    print(f"File '{file_name}' created/overwritten and content written.")


# like range(), but it works for float type
def frange(start, stop, step):
    if step > 0:
        while start < stop:
            yield start
            start += step
    elif step < 0:
        while start > stop:
            yield start
            start += step

def square(x, y, z, step):
    pixel_list = []

    for y in frange(1.0, -1.0, -step):
        pixel_list.append(f"{x:.1f} {y:.1f} {z:.1f}")
        # When the above loop is finished, we are in this state: 1, -1, 0
        for z in frange(0.1, 1.0, step):
            pixel_list.append(f"{x:.1f} {y:.1f} {z:.1f}")

    for x in frange(0.9, -1.0, -step):
        pixel_list.append(f"{x:.1f} {y:.1f} {z:.1f}")
    # When the above loop is finished, we are in this state: -1, -1, 0
        for z in frange(0.1, 1.0, step):
            pixel_list.append(f"{x:.1f} {y:.1f} {z:.1f}")


    for y in frange(-0.9, 1.0, step):
        pixel_list.append(f"{x:.1f} {y:.1f} {z:.1f}")
    # When the above loop is finished, we are in this state: -1, 1, 0
        for z in frange(0.1, 1.0, step):
            pixel_list.append(f"{x:.1f} {y:.1f} {z:.1f}")



    for x in frange(-0.9, 1.0, step):
        pixel_list.append(f"{x:.1f} {y:.1f} {z:.1f}")
    # When the above loop is finished, we are in this state: 1, 1, 0
        for z in frange(0.1, 1.0, step):
            pixel_list.append(f"{x:.1f} {y:.1f} {z:.1f}")


    z = 1

    for y in frange(1.0, -1.0, -step):
        pixel_list.append(f"{x:.1f} {y:.1f} {z:.1f}")
    # When the above loop is finished, we are in this state: 1, -1, 0


    for x in frange(0.9, -1.0, -step):
        pixel_list.append(f"{x:.1f} {y:.1f} {z:.1f}")
    # When the above loop is finished, we are in this state: -1, -1, 0


    for y in frange(-0.9, 1.0, step):
        pixel_list.append(f"{x:.1f} {y:.1f} {z:.1f}")
    # When the above loop is finished, we are in this state: -1, 1, 0


    for x in frange(-0.9, 1.0, step):
        pixel_list.append(f"{x:.1f} {y:.1f} {z:.1f}")
    # When the above loop is finished, we are in this state: 1, 1, 0



    for y in frange(-1.0, 1.0, step):
        pixel_list.append(f"{x:.1f} {y:.1f} {z:.1f}")
        for x in frange(-1.0, 1.0, step):
            pixel_list.append(f"{x:.1f} {y:.1f} {z:.1f}")


    z=0

    for y in frange(-1.0, 1.0, step):
        pixel_list.append(f"{x:.1f} {y:.1f} {z:.1f}")
        for x in frange(-1.0, 1.0, step):
            pixel_list.append(f"{x:.1f} {y:.1f} {z:.1f}")


    return pixel_list


def generate_xyz_list(shape="cube", step=0.1, size=1.0):
    """
    Generate .xyz file contents for different 3D shapes.
    
    Parameters:
        shape (str): Type of shape to generate ("cube", "square").
        step (float): Step size for generating points.
        size (float): Size of the shape.
        
    Returns:
        list: A list of strings representing the coordinates.
    """
    pixel_list = []

    if shape == "cube":
        # Generate a cube
        for z in frange(-size, size + step, step):
            for y in frange(-size, size + step, step):
                for x in frange(-size, size + step, step):
                    pixel_list.append(f"{x:.1f} {y:.1f} {z:.1f}")

    elif shape == "square":
        # Generate a square in the xy plane at z=0
        z = 0
        for y in frange(-size, size + step, step):
            for x in frange(-size, size + step, step):
                pixel_list.append(f"{x:.1f} {y:.1f} {z:.1f}")

    else:
        raise ValueError(f"Unsupported shape: {shape}")

    return pixel_list



# Specify the file name and the content
file_name = 'example.xyz'

# This is the step of the pixels
step = 0.1

# initiale values for the start of the mesh
x = 1.0
y = 1.0
z = 0.0

# for storing the pixels 
pixel_list = []

# pixel = str(x) + " " + str(y) + " " + str(z)


for y in frange(1.0, -1.0, -step):
    pixel_list.append(f"{x:.1f} {y:.1f} {z:.1f}")
# When the above loop is finished, we are in this state: 1, -1, 0
    for z in frange(0.1, 1.0, step):
        pixel_list.append(f"{x:.1f} {y:.1f} {z:.1f}")



for x in frange(0.9, -1.0, -step):
    pixel_list.append(f"{x:.1f} {y:.1f} {z:.1f}")
# When the above loop is finished, we are in this state: -1, -1, 0
    for z in frange(0.1, 1.0, step):
        pixel_list.append(f"{x:.1f} {y:.1f} {z:.1f}")



for y in frange(-0.9, 1.0, step):
    pixel_list.append(f"{x:.1f} {y:.1f} {z:.1f}")
# When the above loop is finished, we are in this state: -1, 1, 0
    for z in frange(0.1, 1.0, step):
        pixel_list.append(f"{x:.1f} {y:.1f} {z:.1f}")



for x in frange(-0.9, 1.0, step):
    pixel_list.append(f"{x:.1f} {y:.1f} {z:.1f}")
# When the above loop is finished, we are in this state: 1, 1, 0
    for z in frange(0.1, 1.0, step):
        pixel_list.append(f"{x:.1f} {y:.1f} {z:.1f}")


z = 1

for y in frange(1.0, -1.0, -step):
    pixel_list.append(f"{x:.1f} {y:.1f} {z:.1f}")
# When the above loop is finished, we are in this state: 1, -1, 0


for x in frange(0.9, -1.0, -step):
    pixel_list.append(f"{x:.1f} {y:.1f} {z:.1f}")
# When the above loop is finished, we are in this state: -1, -1, 0


for y in frange(-0.9, 1.0, step):
    pixel_list.append(f"{x:.1f} {y:.1f} {z:.1f}")
# When the above loop is finished, we are in this state: -1, 1, 0


for x in frange(-0.9, 1.0, step):
    pixel_list.append(f"{x:.1f} {y:.1f} {z:.1f}")
# When the above loop is finished, we are in this state: 1, 1, 0



for y in frange(-1.0, 1.0, step):
    pixel_list.append(f"{x:.1f} {y:.1f} {z:.1f}")
    for x in frange(-1.0, 1.0, step):
        pixel_list.append(f"{x:.1f} {y:.1f} {z:.1f}")


z=0

for y in frange(-1.0, 1.0, step):
    pixel_list.append(f"{x:.1f} {y:.1f} {z:.1f}")
    for x in frange(-1.0, 1.0, step):
        pixel_list.append(f"{x:.1f} {y:.1f} {z:.1f}")



# Print all pixels
for pixel in pixel_list:
    print(pixel)




width = 20
height = 20
indices = []
for y in range(height - 1):
    for x in range(width - 1):
        A = y * width + x
        B = y * width + (x + 1)
        C = (y + 1) * width + x
        D = (y + 1) * width + (x + 1)

        # Triangle 1: A, B, D
        indices.append((A, B, D))
        # Triangle 2: A, D, C
        indices.append((A, D, C))


obj_faces = ""

for vertex in pixel_list:
    obj_faces += f"v {vertex}\n"

for face in indices:
    obj_faces += f"f {face[0] + 1} {face[1] + 1} {face[2] + 1}\n"




# Save to file
with open("rectangleFirstTest.obj", "w") as f:
    f.write(obj_faces)






# write_to_file(file_name, pixel_list)

#write_to_file("testingGenerateXYZlist.xyz", generate_xyz_list("cube", 0.1, 5.0))
