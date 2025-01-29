import tkinter as tk
from tkinter import messagebox
import json
import os


CONFIG_FILE = "config.json"

def create_config(data):
    with open(CONFIG_FILE, "w") as f:
        json.dump(data, f, indent=4)
    messagebox.showinfo("Success", f"{CONFIG_FILE} created successfully!")

def run_gui():
    def on_submit():
        try:
            # Validate path inputs
            path_image_value = path_image.get()
            path_output_value = path_output.get()
            if path_image_value == "e.g. \".\" for same dir" or not path_image_value:
                raise ValueError("Please provide a path to image")
            if path_output_value == "e.g. \".\" for same dir" or not path_output_value:
                raise ValueError("Please provide an output path")
            if not os.path.exists(path_image_value):
                raise ValueError(f"Image path does not exist: {path_image_value}")
            if not os.path.exists(path_output_value):
                raise ValueError(f"Output path does not exist: {path_output_value}")
                
            # Validate output filename
            output_name_value = output_file_name.get()
            if output_name_value == "e.g. myFile (no need to add \".obj\")" or not output_name_value:
                raise ValueError("Please provide an output file name")
            
            # Validate depth
            depth_value = depth.get()
            if depth_value == "e.g. 6" or not depth_value.isdigit():
                raise ValueError("Depth must be a positive integer")
            depth_value = int(depth_value)
            if depth_value <= 2:
                raise ValueError("Depth must be greater than 2")
            
            # Validate padding
            padding_value = padding.get()
            if padding_value == "e.g. 80" or not padding_value.isdigit():
                raise ValueError("Padding must be a positive integer")
            padding_value = int(padding_value)
            if padding_value <= 0:
                raise ValueError("Padding must be greater than 0")
            
            # Validate threshold
            threshold_value = threshold.get()
            if threshold_value == "e.g. 100" or not threshold_value.isdigit():
                raise ValueError("Threshold must be a positive integer")
            threshold_value = int(threshold_value)
            if not 0 <= threshold_value <= 255:
                raise ValueError("Threshold must be between 0 and 255")
                
            # Validate blur method
            blur_value = blur_method.get()
            if blur_value == "Supported: \"dt\", \"gaussian\", \"box\"" or not blur_value:
                raise ValueError("Please provide a blur method")
            if blur_value not in ["dt", "gaussian", "box"]:
                raise ValueError("Blur method must be one of: dt, gaussian, box")
            
            # If all validations pass, create the config
            data = {
                "path_image": path_image_value,
                "path_output": path_output_value,
                "output_file_name": output_name_value,
                "depth": depth_value,
                "padding": padding_value,
                "threshold": threshold_value,
                "negative": negative_var.get(),
                "blurMethod": blur_value,
                "show_timing": show_timing_var.get(),
            }

            # Create the config file
            create_config(data)
            root.destroy()  # Close the GUI

        except ValueError as ve:
            # Show an error message to the user
            messagebox.showerror("Input Error", str(ve))
        except Exception as e:
            # Catch-all for any unexpected issues
            messagebox.showerror("Error", f"An unexpected error occurred: {str(e)}")



    def set_placeholder(entry, placeholder):
        """Set placeholder text in an Entry widget."""
        entry.insert(0, placeholder)
        entry.bind("<FocusIn>", lambda event: clear_placeholder(entry, placeholder))
        entry.bind("<FocusOut>", lambda event: restore_placeholder(entry, placeholder))

    def clear_placeholder(entry, placeholder):
        """Clear placeholder text on focus."""
        if entry.get() == placeholder:
            entry.delete(0, tk.END)
            entry.config(fg="white")

    def restore_placeholder(entry, placeholder):
        """Restore placeholder text if empty."""
        if not entry.get():
            entry.insert(0, placeholder)
            entry.config(fg="grey")

    # Create the main window
    root = tk.Tk()
    root.title("Create Config")
    root.resizable(False, False)  # Make the window non-resizable

    # Add input fields
    tk.Label(root, text="Path to Image:").grid(row=0, column=0, padx=10, pady=5, sticky="w")
    path_image = tk.Entry(root, width=30, fg="grey")
    path_image.grid(row=0, column=1, padx=10, pady=5)
    set_placeholder(path_image, "e.g. \".\" for same dir")

    tk.Label(root, text="Path to Output:").grid(row=1, column=0, padx=10, pady=5, sticky="w")
    path_output = tk.Entry(root, width=30, fg="grey")
    path_output.grid(row=1, column=1, padx=10, pady=5)
    set_placeholder(path_output, "e.g. \".\" for same dir")

    tk.Label(root, text="Output File Name:").grid(row=2, column=0, padx=10, pady=5, sticky="w")
    output_file_name = tk.Entry(root, width=30, fg="grey")
    output_file_name.grid(row=2, column=1, padx=10, pady=5)
    set_placeholder(output_file_name, "e.g. myFile (no need to add \".obj\")")

    tk.Label(root, text="Depth:").grid(row=3, column=0, padx=10, pady=5, sticky="w")
    depth = tk.Entry(root, width=30, fg="grey")
    depth.grid(row=3, column=1, padx=10, pady=5)
    set_placeholder(depth, "e.g. 6")

    tk.Label(root, text="Padding:").grid(row=4, column=0, padx=10, pady=5, sticky="w")
    padding = tk.Entry(root, width=30, fg="grey")
    padding.grid(row=4, column=1, padx=10, pady=5)
    set_placeholder(padding, "e.g. 80")

    tk.Label(root, text="Threshold:").grid(row=5, column=0, padx=10, pady=5, sticky="w")
    threshold = tk.Entry(root, width=30, fg="grey")
    threshold.grid(row=5, column=1, padx=10, pady=5)
    set_placeholder(threshold, "e.g. 100")

    tk.Label(root, text="Negative:").grid(row=6, column=0, padx=10, pady=5, sticky="w")
    negative_var = tk.BooleanVar()
    tk.Checkbutton(root, variable=negative_var).grid(row=6, column=1, padx=10, pady=5, sticky="w")

    tk.Label(root, text="Blur Method:").grid(row=7, column=0, padx=10, pady=5, sticky="w")
    blur_method = tk.Entry(root, width=30, fg="grey")
    blur_method.grid(row=7, column=1, padx=10, pady=5)
    set_placeholder(blur_method, "Supported: \"dt\", \"gaussian\", \"box\"")

    # tk.Label(root, text="Show Timing:").grid(row=8, column=0, padx=10, pady=5, sticky="w")
    tk.Label(root, text="Show Timing:").grid(row=9, column=0, padx=10, pady=5, sticky="w")
    show_timing_var = tk.BooleanVar(value=True)
    tk.Checkbutton(root, variable=show_timing_var).grid(row=9, column=1, padx=10, pady=5, sticky="w")


    # Add Submit button
    submit_button = tk.Button(root, text="Submit", command=on_submit)
    submit_button.grid(row=10, column=0, columnspan=2, pady=10)

    # Start the GUI event loop
    root.mainloop()
