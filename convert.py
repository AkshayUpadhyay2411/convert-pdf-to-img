import os
import fitz
from PIL import Image
import shutil

def copy_image(source_path, destination_path):
    try:
        # Create the destination directory if it doesn't exist
        os.makedirs(os.path.dirname(destination_path), exist_ok=True)

        # Copy the image file
        shutil.copy(source_path, destination_path)

        print(f"Image copied from {source_path} to {destination_path}")
    except Exception as e:
        print(f"Error copying image: {e}")


def convert_pdf_to_jpg(file_path, file_name, output_folder,temp_folder = "temp"):
    if file_path is None or file_name is None:
        return None, None

    doc = fitz.open(os.path.join(file_path, file_name))

    img_files = []
    if file_name.lower().endswith('.pdf'):
        for page in doc:
            pix = page.get_pixmap()
            img_file_path = os.path.join(temp_folder, file_name + '-' + str(page.number) + '.jpg')
            pix.save(img_file_path)
            img_files.append(img_file_path)

    # print("Files : ")
    # for img_file in img_files:
    #     print(img_file)
    # print("-----------------------")

    if len(img_files) == 0:
        return None

    if len(img_files) == 1:
        source_image_path = os.path.join(temp_folder, file_name + '-' + str(0) + '.jpg')
        destination_image_path = os.path.join(output_folder , file_name + '-' + '.jpg')

        copy_image(source_image_path, destination_image_path)

        # Remove intermediate images
        # for img_file in img_files:
        #     os.remove(img_file)
        
        return img_files[0]
    
    if len(img_files) > 1:
        img_path = merge_images(img_files=img_files, output_folder=output_folder, file_name=file_name)
        return img_path

    return None 

def merge_images(img_files, output_folder, file_name):
    images = [Image.open(img_file) for img_file in img_files]

    total_height = sum(img.height for img in images)
    max_width = max(img.width for img in images)

    merged_image = Image.new("RGB", (max_width, total_height), (255, 255, 255))

    y_offset = 0
    for img in images:
        merged_image.paste(img, (0, y_offset))
        y_offset += img.height

    merged_image_path = os.path.join(output_folder, file_name + '.jpg')  # Save in the 'datasetimages' folder
    # print("Merged image path : " , merged_image_path)
    merged_image.save(merged_image_path)

    # Remove intermediate images
    # for img_file in img_files:
    #     os.remove(img_file)

    return merged_image_path

def convert_all_pdfs_in_folder(input_folder, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for filename in os.listdir(input_folder):
        if filename.lower().endswith('.pdf'):
            # pdf_path = os.path.join(input_folder, filename)
            # etag = os.path.splitext(filename)[0]  # Using filename as etag
            print("Filename : " , filename)
            output_file = convert_pdf_to_jpg(input_folder, filename , output_folder)
            print("Output Filename : " , output_file)
            print("------------------------")

# Example usage:
input_folder = 'dataset'
output_folder = 'datasetimages'
convert_all_pdfs_in_folder(input_folder, output_folder)
