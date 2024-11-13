import requests
import zipfile
import os
import shutil

# Step 1: Download the file
url = "https://cricsheet.org/downloads/all_json.zip"
local_filename = "all_json.zip"

print("Downloading file...")
response = requests.get(url)
with open(local_filename, 'wb') as file:
    file.write(response.content)
print("Download complete.")

# Step 2: Extract the ZIP file
extracted_folder = "all_json"
print("Extracting files...")
with zipfile.ZipFile(local_filename, 'r') as zip_ref:
    zip_ref.extractall(extracted_folder)
print("Extraction complete.")

# Step 3: Rename the extracted folder
new_folder_name = "cricsheet-raw"  # Specify the new name for the folder
os.rename(extracted_folder, new_folder_name)
print(f"Folder renamed to {new_folder_name}.")

# Step 4: Move the renamed folder to another directory
destination_folder = "../data/raw/cricsheet"  # Specify your destination directory
if not os.path.exists(destination_folder):
    os.makedirs(destination_folder)  # Create the destination directory if it doesn't exist

print(f"Moving files to {destination_folder}...")
shutil.move(new_folder_name, destination_folder)
print("Files moved successfully.")

# Optional: Clean up by removing the downloaded ZIP file
os.remove(local_filename)
print("Cleanup complete. ZIP file removed.")
