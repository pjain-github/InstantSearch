import os
import logging

def clean_folder(folder_name):
    
    print("Current working directory:", os.getcwd())

    # Check if the folder exists
    if os.path.exists(folder_name):
        # Iterate over all files in the "Data" folder
        for filename in os.listdir(folder_name):
            file_path = os.path.join(folder_name, filename)
            try:
                if os.path.isfile(file_path):
                    os.remove(file_path)  # Remove the file
                    logging.info(f"Removed {filename}")
                    print(f"Removed {filename}")
            except Exception as e:
                print(f"Error removing {filename}: {e}")
                logging.info(f"Error removing {filename}: {e}")
    else:
        print(f"Folder '{folder_name}' does not exist.")
        logging.info(f"Folder '{folder_name}' does not exist.")