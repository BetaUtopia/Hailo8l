import os

# Directory containing the annotation files
directory = '../../datasets/labels/train'

# Loop through all files in the directory
for filename in os.listdir(directory):
    if filename.startswith('Red_Ball_image_') and filename.endswith('.txt'):
        file_path = os.path.join(directory, filename)
        print(f"Processing file: {file_path}")
        
        # Read the file content
        with open(file_path, 'r') as file:
            lines = file.readlines()
        
        # Replace class_id 0 with 1
        new_lines = []
        for line in lines:
            parts = line.split()
            if parts[0] == '0':
                print(f"Updating class_id from 0 to 1 in file: {filename}")
                parts[0] = '1'
            new_lines.append(' '.join(parts) + '\n')
        
        # Write the modified content back to the file
        with open(file_path, 'w') as file:
            file.writelines(new_lines)

print("Class IDs update process completed.")
