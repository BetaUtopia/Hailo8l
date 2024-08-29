from picamera2 import Picamera2
import time
import os
import argparse
import cv2
from PIL import Image

def capture_images_with_preview(class_name: str, output_folder: str, interval: int, total_pictures: int, onkeypress: bool):
    # Create output directory if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Initialize the camera
    picam2 = Picamera2()
    picam2.preview_configuration.main.size = (1920,1080)
    picam2.preview_configuration.main.format = "RGB888"
    picam2.preview_configuration.align()
    picam2.configure("preview")
    picam2.start()

    print("Camera initialized and preview started.")

    # Create a window for preview
    cv2.namedWindow("Camera Preview", cv2.WINDOW_NORMAL)

    captured_pictures = 0

    while captured_pictures < total_pictures:
        # Capture and display the preview frame
        frame = picam2.capture_array()
        cv2.imshow("Camera Preview", frame)

        key = cv2.waitKey(1)
        if key == ord('k') and onkeypress:
            # Capture the image
            filename = os.path.join(output_folder, f"{class_name}_image_{captured_pictures + 1}.jpg")
            picam2.capture_file(filename)

            # Resize or crop to 640x480
            img = Image.open(filename)
            img_resized = img.resize((640, 480))
            img_resized.save(filename)

            captured_pictures += 1
            print(f"Captured image {captured_pictures}/{total_pictures} as {filename}")
        elif key == ord('q'):
            # Exit the program
            print("Exiting program.")
            break
        elif not onkeypress:
            # Wait for the specified interval before capturing the image
            time.sleep(interval)

            # Capture the image
            filename = os.path.join(output_folder, f"{class_name}_image_{captured_pictures + 1}.jpg")
            picam2.capture_file(filename)

            # Resize or crop to 640x480
            img = Image.open(filename)
            img_resized = img.resize((640, 480))
            img_resized.save(filename)

            captured_pictures += 1
            print(f"Captured image {captured_pictures}/{total_pictures} as {filename}")

    # Clean up
    cv2.destroyAllWindows()
    picam2.stop()
    print(f"Completed capturing {captured_pictures} images.")
    print("Camera stopped.")

def create_directories():
    root_dir = 'datasets'
    image_dir = root_dir + '/images/train'
    label_dir = root_dir + '/labels/train'
    image_dir_val = root_dir + '/images/val'
    label_dir_val = root_dir + '/labels/val'
    if not os.path.exists(image_dir):
        os.makedirs(image_dir)
    if not os.path.exists(label_dir):
        os.makedirs(label_dir)
    if not os.path.exists(image_dir_val):
        os.makedirs(image_dir_val)
    if not os.path.exists(label_dir_val):
        os.makedirs(label_dir_val)
def main():

    parser = argparse.ArgumentParser(description="Capture images with preview and optional keypress.")
    parser.add_argument('--classname', required=True, help='Class name for the image filenames.')
    parser.add_argument('--output_folder', default='datasets/images/train', help='Directory to save captured images.')
    parser.add_argument('--interval', type=int, default=2, help='Interval between captures in seconds.')
    parser.add_argument('--total_pictures', type=int, default=1024, help='Total number of pictures to capture.')
    parser.add_argument('--onkeypress', action='store_true', help='Capture image on keypress (press "k").')
    args = parser.parse_args()
    create_directories()
    capture_images_with_preview(args.classname, args.output_folder, args.interval, args.total_pictures, args.onkeypress)


if __name__ == "__main__":
    main()
