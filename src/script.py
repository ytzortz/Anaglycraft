"""
This project is licensed under the Apache License 2.0.
Author: Ioannis Tzortzakis (Github: ytzortz)
Original repository: https://github.com/ytzortz/Thesis
"""


# libraries used in debug
# import imageio.v3 as iio
# import matplotlib.pyplot as plt
# import numpy as np
import os
import time 
from utils import grayscale, get_non_white_pixel_locations_from_image, add_padding, load_config


def runTheScript():
    # Start the timer for the entire script
    # start_time_script = time.time() # This is for mutliple files
    total_start_time = time.time()  # Start timing for the entire process

    imported_json = load_config("config.json")

    if not imported_json:
        print("Failed to load configuration file. Exiting script.")
        exit()
    
    show_timing = imported_json["show_timing"]

    # Step 1: Importing settings from config file
    if show_timing:
        print("Importing settings from config file")
        step_start_time = time.time()  # Start timing this step


    path_image = imported_json["path_image"]
    path_output = imported_json["path_output"]
    output_file_name = imported_json["output_file_name"]
    depth = imported_json["depth"]
    padding = imported_json["padding"]
    threshold = imported_json["threshold"]
    negative = imported_json["negative"]
    blur_method = imported_json["blurMethod"]
    

    output_file_path = os.path.join(path_output, output_file_name + ".obj")

    if show_timing:
        step_end_time = time.time()
        print(f"Importing ended. (Time: {step_end_time - step_start_time:.3f}s)\n")


    # Step 2: Generate Pixels
    if show_timing:
        print("Generating the pixels")
        step_start_time = time.time()  # Start timing this step

    

    # depth = 6
    # padding = 80
    # negative = True
    # threshold = 100

    grayImage = grayscale(path_image, negative)
    paddingImage = add_padding(grayImage, padding)
    intensityMatrix = get_non_white_pixel_locations_from_image(paddingImage, threshold, depth, blur_method)

    pixel_list = []
    height, width = paddingImage.shape
    for z in range(0, depth):
        for y in range(height):
            for x in range(width):
                if (x == 0 or x == width - 1 or y == 0 or y == height - 1 or z == 0 or z == depth - 1):
                    if(z == 0):
                        intensity = intensityMatrix[y][x] # kanonika tha itan anapoda giati einai numpy array 
                        adjusted_z = intensity
                    else:
                        adjusted_z = depth
                    pixel_list.append(f"{x:.1f} {y:.1f} {adjusted_z:.1f}")


    if show_timing:
        step_end_time = time.time()
        print(f"Generation of pixels ended. (Time: {step_end_time - step_start_time:.3f}s)\n")




    # Step 3: Connect Vertices
    if show_timing:
        print("Start connecting the vertices")
        step_start_time = time.time()  # Start timing this step

    faces = []
    allPoints = len(pixel_list)
    if width >= 3 and height >= 3:
        innerDots = (width - 2) * (height - 2)
    else:
        innerDots = 0
    firstSurfaceDots = height * width
    insideSurfaceDots = firstSurfaceDots - innerDots

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

    # creates faces on the left side of the cube
    for y in range(height-1):
        # print(f"Ξεκινησε μολις η φορα: {y} τωρα")
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

    # creates faces on the right side of cube
    for y in range(height-1):
            go_right = 0 # this var indicates the times we moves away from the very first from slice of the cube
            k = 1 # this need to be 1 because the pixels inside the file are
            while k < allPoints-firstSurfaceDots:
                if y > 0: # we are NOT in the first time through the bottom of the cube
                    if depth == 2:
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
                                
                                v1 = k + width + ((y-1)*2)
                                
                                v2 = v1 + 2
                                v3 = k + insideSurfaceDots + y*width
                                v4 = v3 + width

                            else: # we are somewhere in the middle of the cube
                                # I move from the firstslice, then I move the correct right steps with insideSurfaceDots and the i move up using y 
                                
                                v1 = k + width + (y-1)*2
                                v2 = v1 + 2
                                v3 = v1 + insideSurfaceDots 
                                v4 = v3 + 2
            
                else:   # this is the very first slice
                    if depth == 2:
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

                if v1 != allPoints-firstSurfaceDots:
                    faces.append((v3, v2, v1))
                if v3 != allPoints-firstSurfaceDots:
                    faces.append((v4, v2, v3))  
                
                if k == 1:
                    k = k + firstSurfaceDots
                else:
                    k = k + insideSurfaceDots
                
                go_right = go_right + 1 
            
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

    if show_timing:
        step_end_time = time.time()
        print(f"Procedure ended. (Time: {step_end_time - step_start_time:.3f}s)\n")




    # Step 4: Write Vertices to List
    if show_timing:
        print("Writing the vertices in list.")
        step_start_time = time.time()  # Start timing this step

    obj_faces = ""
    obj_faces = [f"v {vertex}" for vertex in pixel_list]
    obj_faces = "\n".join(obj_faces)

    if show_timing:
        step_end_time = time.time()
        print(f"Writing is over. (Time: {step_end_time - step_start_time:.3f}s)\n")



    # Step 5: Write to File
    if show_timing:
        print("Writing in file started.")
        step_start_time = time.time()  # Start timing this step

    # Save the object file here
    with open(output_file_path, "w") as f:
        # Write vertices
        f.writelines(f"v {vertex}\n" for vertex in pixel_list)
        # Write faces
        f.writelines(f"f {face[0]} {face[1]} {face[2]}\n" for face in faces)

    if show_timing:
        step_end_time = time.time()
        print(f"File generated. (Time: {step_end_time - step_start_time:.3f}s)\n")

    if show_timing:
        total_end_time = time.time()
        print(f"Total time: {total_end_time - total_start_time:.3f}s\n\n")

    # This is for multiple images
    # end_time_script = time.time()
    # print(f"Total time for the whole script: {end_time_script - start_time_script:.3f}s")