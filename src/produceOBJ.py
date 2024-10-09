import os


# Specify the file name and the content
file_name = '3x3x3Cube.xyz'

# initiale values for the start of the mesh
# x = 0
# y = 0
# z = 0

# for storing the pixels 
pixel_list = []

width, height, depth = 5, 5, 3
padding = 2
moving_inside = 0

#creates the points for the cube
for z in range(0, depth):
    for y in range (0, height):
        for x in range (0, width):
            if (x == 0 or x == width - 1 or y == 0 or y == height - 1 or z == 0 or z == depth - 1):
                pixel_list.append(f"{x:.1f} {y:.1f} {z:.1f}")


# Create the face indices for each square on each face
faces = []

allPoints = len(pixel_list)

if width >= 3 and height >= 3:
    innerDots = (width-2)*(height-2)
else:
    innerDots =0

firstSurfaceDots = height * width
insideSurfaceDots = firstSurfaceDots - innerDots

# creates faces on the fronts side of the cube
for y in range(height-1):
    x = 0
    k = 0
    MUL = y*width
    x = x+ MUL
    while x+k < width + (MUL):
            v1 = x + k
            v2 = v1 + 1
            v3 = v1 + width
            v4 = v3 + 1
            if v1 != MUL:
                faces.append((v3, v2, v1))
            if v3 != width + (MUL):
                faces.append((v2, v3, v4))
            k = k+1


# creates faces on the back side of the cube
for y in range(height-1):
    x=0
    k = 0
    MUL = y * width + (allPoints - (height * width))
    x = x + MUL        
    while x + k < width + (MUL):
            v1 = x + k  # Shift the index for the back face
            v2 = v1 + 1
            v3 = v1 + width
            v4 = v3 + 1
            if v1 != MUL:
                faces.append((v3, v1, v2))
            if v3 != width + (MUL):
                faces.append((v2, v4, v3))  
            k = k + 1


# creates faces on the right side of cube
for y in range(height-1):
        # print(f"Ξεκινησε μολις η φορα: {y} τωρα")
        go_right = 0 # this var indicates the times we moves away from the very first from slice of the cube
        k = 1 # this need to be 1 because the pixels inside the file are
        while k < allPoints-firstSurfaceDots:

            if y > 0: # we are NOT in the first time through the bottom of the cube

                if depth == 2:
                    # print("Eimai edw")
                    v1 = k + y*width
                    v2 = v1 + width 
                    v3 = v1 + firstSurfaceDots
                    v4 = v3 + width
                else:
                    if go_right == 0: # we are in the first slice
                        v1 = k + y*width # y = times going up
                        v2 = v1 + width

                        # for v3 I need to go to the first buttom row dot and then move up.
                        rest = firstSurfaceDots - v1
                        v3 = (v1 +rest) + width + y*2 -1
                        v4 = v3 + 2 

                    else:   # not the first slice

                        if go_right == depth-2: # we are on the pre-last slice
                            positionOfv1 = (firstSurfaceDots + (go_right-1)*insideSurfaceDots + width + (y-1)*2) + 1
                            nextButtom = firstSurfaceDots + (go_right)*insideSurfaceDots
                            rest = nextButtom - positionOfv1

                            # print(f"\n\n\nfirst slice:{firstSurfaceDots}\ninside slice:{insideSurfaceDots}\nposition rn:{positionOfv1}\nnextButtom:{nextButtom}\nrest:{rest}\n\n\n")
                            
                            v1 = k + width + ((y-1)*2)
                            
                            v2 = v1 + 2
                            # v3 = (v1 +rest) + width + y*2 -1
                            v3 = k + insideSurfaceDots + y*width
                            # print(f"v3:{v3}")
                            v4 = v3 + width

                            # print(f"\nv1:{v1}\n")

                        else: # we are somewhere in the middle of the cube
                            # I move from the firstslice, then I move the correct right steps with insideSurfaceDots and the i move up using y 
                            
                            v1 = k + width + (y-1)*2
                            v2 = v1 + 2
                            v3 = v1 + insideSurfaceDots 
                            v4 = v3 + 2
                            # print(f" EDW EISAI \n\nk:{k}v1:{v1}\nv2:{v2}\nv3:{v3}\nv4:{v4}")
          
            else:   # this is the very first slice

                if depth == 2:
                    # print("Eimai edw")
                    v1 = k + y*width
                    v2 = v1 + width 
                    v3 = v1 + firstSurfaceDots
                    v4 = v3 + width
                else:
                    v1 = k
                    v2 = v1 + width   
                    if go_right == 0:
                        v3 = v1 + firstSurfaceDots
                    else:
                        v3 = v1 + insideSurfaceDots
                    v4 = v3 + width


                # print(f"\n\nv1:{v1}\nv2:{v2}\nv3:{v3}\nv4:{v4}")


            if v1 != allPoints-firstSurfaceDots:
                faces.append((v3, v2, v1))
            if v3 != allPoints-firstSurfaceDots:
                faces.append((v4, v2, v3))  
            
            if k == 1:
                k = k + firstSurfaceDots
            else:
                k = k + insideSurfaceDots
            
            go_right = go_right + 1 
            

# creates faces on the left side of the cube
for y in range(height-1):
    print(f"Ξεκινησε μολις η φορα: {y} τωρα")
    go_right = 0 # this var indicates the times we moves away from the very first from slice of the cube
    k = width
    while k < allPoints-firstSurfaceDots:

        if y == 0: # we are on the bottom slice   
                if height == 2:
                    v1 = k
                    v2 = v1 + width 
                    v3 = v1 + firstSurfaceDots
                    v4 = v3 + width
                else:
                    v1 = k 
                    if go_right == 0:
                        v2 = v1 + width  
                        v3 = v1 + firstSurfaceDots
                    else:
                        v2 = v1 + 2
                        v3 = v1 + insideSurfaceDots

                    if go_right == depth-2:  
                        v4 = v3 + width
                    else:
                        v4 = v3 + 2                


        else:   # we are NOT on the first slice
                    
            if depth == 2:
                    print("Eimai edw")
                    v1 = k + y*width
                    v2 = v1 + width 
                    v3 = v1 + insideSurfaceDots + width
                    v4 = v3 + width
            else:
                    if go_right == 0: # we are in the first slice

                        v1 = k + y*width # y = times going up
                        v2 = v1 + width
                        v3 = k +firstSurfaceDots + y*2
                        if y == height-2:
                            v4 = v3 + width
                        else:
                            v4 = v3 + 2

                    else:   # not the first slice

                        if go_right == depth-2: # we are on the pre-last slice

                            v1 = k + (y*2)
                            # v3 = k + (insideSurfaceDots - width) + y*width
                            # v3 = allPoints - (firstSurfaceDots - width) 
                            v3 = k + insideSurfaceDots + (y)*width
                            v4 = v3 + width
                            if y == height-2:
                                v2 = v1 + width
                            else:
                                v2 = v1 + 2

                        else: # we are somewhere in the middle of the cube
                            # I move from the firstslice, then I move the correct right steps with insideSurfaceDots and the i move up using y 
                            
                            v1 = k + (y)*2
                            v3 = k + insideSurfaceDots + y*2
                            if y == height-2:
                                v4 = v3 + width
                                v2 = v1 + width
                            else:
                                v2 = v1 + 2
                                v4 = v3 + 2



        if v1 != allPoints-firstSurfaceDots:
            faces.append((v1, v2, v3))
        if v3 != allPoints-firstSurfaceDots:
            faces.append((v3, v2, v4))  

        if k == width:
            k = k + firstSurfaceDots
        else:
            k = k + insideSurfaceDots
        
        go_right = go_right + 1 


# creates faces on the bottom of the cube
for x in range(depth-1):
    k = 1
    while k < width:

        if x == 0: # I'm on the first row
                v1 = k
                v2 = v1 + 1
                v3 = k + firstSurfaceDots
                v4 = v3 + 1 
        else:       # not the first time
            if k == width-1:
                v1 = k + firstSurfaceDots + (x-1)*insideSurfaceDots
                v2 = v1 + 1
                v3 = v1 + insideSurfaceDots
                v4 = v3 + 1 
            else:
                v1 = k + firstSurfaceDots + (x-1)*insideSurfaceDots
                v2 = v1 + 1
                v3 = v1 + insideSurfaceDots
                v4 = v3 + 1 

        if v1 != allPoints-firstSurfaceDots:
            faces.append((v1, v2, v3))
        if v3 != allPoints-firstSurfaceDots:
            faces.append((v3, v2, v4))  

        k = k + 1


# creates faces on the top of the cube
for x in range(depth -1):
    k = 1
    while k < width:

        if x < 0: # I'm on the first row
                if width == 2:
                    if k == 1:
                        v1 = k + firstSurfaceDots-width
                    else:
                        v1 = 1 + firstSurfaceDots-width + (k-1)*insideSurfaceDots 

                    v2 = v1 + 1
                    v3 = 1 + (firstSurfaceDots-width) + k*insideSurfaceDots
                    v4 = v3 + 1 
                else:
                    if k == 1:
                        if depth == 2:
                            v1 = k + firstSurfaceDots-width
                            v2 = v1 + 1
                            v3 = k + (firstSurfaceDots-width) + firstSurfaceDots
                            v4 = v3 + 1 
                        else:
                            v1 = k + firstSurfaceDots-width
                            v2 = v1 + 1
                            v3 = k + (firstSurfaceDots-width) + insideSurfaceDots
                            v4 = v3 + 1 
                    else:
                        if k == depth -1:
                            v1 = firstSurfaceDots-width + (k-1)*insideSurfaceDots + 1
                            v2 = v1 + 1
                            v3 = v1 + firstSurfaceDots
                            v4 = v3 + 1
                        else:
                            v1 = firstSurfaceDots-width + (k-1)*insideSurfaceDots + 1
                            v2 = v1 + 1
                            v3 = v1 + insideSurfaceDots
                            v4 = v3 + 1

        else:       # not the first time
            v1 = k + (firstSurfaceDots-width) + (x)*insideSurfaceDots
            v2 = v1 + 1
            if x == depth-2:
                v3 = v1 + width*height
                # print("eimai ekei")
                # print(f"\n\n\nk:{k}\nv1:{v1}\nv2:{v2}\nv3:{v3}\nv4:{v4}\n\n\n")
            else:
                v3 = v1 + insideSurfaceDots
            v4 = v3 + 1 
            # print(f"\n\n\nk:{k}\nv1:{v1}\nv2:{v2}\nv3:{v3}\nv4:{v4}\n\n\n")


        if v1 != allPoints-firstSurfaceDots:
            faces.append((v3, v2, v1))
        if v3 != allPoints-firstSurfaceDots:
            faces.append((v4, v2, v3))  

        k = k + 1





obj_faces = ""
for vertex in pixel_list:
    obj_faces += f"v {vertex}\n"

# Save to file
with open("3x3x3.obj", "w") as f:
    f.write(obj_faces)

    # Write the faces
    for face in faces:
        f.write(f"f {face[0]} {face[1]} {face[2]}\n")




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

def write_to_file(file_name, content_list):
    # Write the content to the file, overwriting if it already exists
    with open(file_name, 'w') as file:
        for item in content_list:
            file.write(item + '\n')
    print(f"File '{file_name}' created/overwritten and content written.")
