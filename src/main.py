"""
This project is licensed under the Apache License 2.0.
Author: Ioannis Tzortzakis (Github: ytzortz)
Original repository: https://github.com/ytzortz/Thesis
"""


import os
from gui import run_gui  # Import the GUI function you will create
import script

CONFIG_FILE = "config.json"

def main():
    if os.path.exists(CONFIG_FILE):
        print(f"\nFound {CONFIG_FILE}, running the script...\n\n")
        script.runTheScript()
    else:
        print(f"\n{CONFIG_FILE} not found, opening the GUI...\n\n")
        # Launch the GUI and wait for it to complete
        run_gui() # this is running the GUI that collects info and creates the config.json file
        print("\nGUI completed. Running the script...\n\n")
        script.runTheScript()

if __name__ == "__main__":
    main()