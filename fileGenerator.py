
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


# TODO: θα πρεπει να περναω πρωτα ολα τα σημεια στην λιστα και στο τελος να τα γραφω το ενα κατω απο το αλλο μεσα στο αρχειο. 

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




write_to_file(file_name, pixel_list)
