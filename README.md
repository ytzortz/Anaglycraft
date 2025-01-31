# 2D to 3D Object Conversion

## Overview

The goal of this project is to convert a 2D drawing from an image into a 3D object, creating an effect as if the design were engraved or embossed on a metallic surface. The program reads processing parameters from a configuration file, or alternatively, allows users to set custom parameters through a graphical user interface (GUI). The final output is a  `.obj`  file, which can be used in 3D modeling applications.

This project is  my  **Bachelor's Thesis**  at the  **Computer Science Department of the University of Crete (UoC)**. It is conducted under the supervision of  **Dr. Xenophon Zabulis**  and is developed within the context of the  **European CRAEFT Project**  ([craeft.eu](https://www.craeft.eu/)).



 ## Installation & Dependencies
 ### **Requirements**
Make sure you have the following dependencies installed:
-   Python 3.x
-   OpenCV (`cv2`)
-   NumPy
-   Tkinter (for GUI)

### **Installation**

1.  Clone the repository:
	```bash
	git clone https://github.com/ytzortz/Thesis.git
	cd Thesis/src
	```
2.  Install the required dependencies:
	```bash
	pip install -r requirements.txt
	```

### **Execution**
To ensure the program runs correctly, you must execute the "main" script from the src directory.

## **Usage**

Running this line inside the src folder:
```bash
python main.py
```

## **Configuration File Format**

The program reads parameters from a JSON configuration file. Below is an example of the expected format:

```json
{
  "path_image": "./image.png",
  "path_output": ".",
  "output_file_name": "result",
  "depth": 10,
  "padding": 5,
  "threshold": 128,
  "negative": false,
  "blurMethod": "gaussian",
  "show_timing": true
}
```
### Configuration parameters:
- ``path_image``: String value indicating the path to the input image file that will be processed. Can be a relative path (e.g., ".") or absolute path. This is the 2D image that will be converted into a 3D object.

- ``path_output``: String value specifying where the output .obj file should be saved. Like path_image, it can be relative or absolute.

- ``output_file_name``: String value for the name of the output .obj file (no need to add the .obj extension as the program handles this).

- ``depth``: Integer value (must be > 2) that determines the maximum height/depth of the 3D object. This affects how "tall" the raised areas of the image will be in the 3D model. Higher values create more pronounced height differences.

- ``padding``: Integer value (must be > 0) that adds white space around the original image. This creates a border of white pixels around the image before processing, which affects the final 3D model's edges.

- ``threshold``: Integer value (0-255) that determines which pixels are considered "active" for processing. In the grayscale conversion:
	-  Pixels below this threshold are processed for the 3D effect
	-  Pixels above this threshold are considered background
	- Lower values capture more details, higher values capture only darker areas

- ``negative``: Boolean value that inverts the image processing (negative effect)

- ``blurMethod``: String value that determines how the transition between heights is calculated. Must be one of:
	- "dt" (Distance Transform): Uses distance transform algorithm.
	- "gaussian": Applies Gaussian blur for smoother transitions.
	- "box": Uses simple box blur (averaging) Each method creates different types of transitions between heights in the final 3D model.
	
- ``show_timing``: Boolean value that controls whether the program shows execution time information for each processing step. The timings are printing in console.

## **Processing Pipeline**

1.  **Configuration**  → Reads and validates the configuration file. If not provided, opens the GUI, allowing the user to generate one easily.
2.  **Load Image**  → Converts to grayscale, applies thresholding, and adds padding.
3.  **Generate Mesh**  → Uses the selected blur method to calculate height variations and generate the points and the vertices.
4.  **Export 3D Model**  → Generates and saves the  `.obj`  file.

## **Acknowledgments**

This project is part of my  **Bachelor’s Thesis**  at the  **University of Crete (UoC)**, supervised by  **Dr. Xenophon Zabulis**. It has been developed within the framework of the  **European CRAEFT Project**  ([craeft.eu](https://www.craeft.eu/)).

## License

![License: Apache 2.0](https://img.shields.io/badge/License-Apache_2.0-blue.svg)

