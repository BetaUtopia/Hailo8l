import os

# Directory containing the files
directory = '../../datasets/images/train'

# Iterate over all files in the directory
for filename in os.listdir(directory):
    # Check if the filename starts with "Green_Cube"
    if filename.startswith("Green_Cube"):
        # Create the new filename by replacing "Green_Cube" with "Red_Ball"
        new_filename = filename.replace("Green_Cube", "Red_Ball")
        
        # Construct the full file paths
        old_file = os.path.join(directory, filename)
        new_file = os.path.join(directory, new_filename)
        
        # Rename the file
        os.rename(old_file, new_file)
        print(f'Renamed: {filename} -> {new_filename}')

print("Renaming completed.")
