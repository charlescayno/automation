from PIL import Image
import os

# Directory containing images to crop
input_dir = "C:/Users/ccayno/Downloads/test cropping"
output_dir = "C:/Users/ccayno/Downloads/test cropping/test"

# Create output directory if it doesn't exist
os.makedirs(output_dir, exist_ok=True)

# Crop dimensions: (left, upper, right, lower)
crop_box = (1000, 0, 4000+1000, 6100)  # Adjust these values as needed

# Loop through all files in the input directory
for file_name in os.listdir(input_dir):
    input_path = os.path.join(input_dir, file_name)
    
    # Check if the file is an image
    if file_name.lower().endswith(('.png', '.jpg', '.jpeg')):
        try:
            # Open the image
            with Image.open(input_path) as img:
                # Crop the image
                width, height = img.size
                # input(f"{width} {height}")
                cropped_img = img.crop(crop_box)
                
                # Save the cropped image to the output directory
                output_path = os.path.join(output_dir, file_name)
                cropped_img.save(output_path)
                print(f"Cropped and saved: {output_path}")
        except Exception as e:
            print(f"Failed to process {file_name}: {e}")
