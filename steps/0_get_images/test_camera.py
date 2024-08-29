from picamera2 import Picamera2
import time
import cv2

def test_camera():
    try:
        # Initialize the camera
        picam2 = Picamera2()
        picam2.preview_configuration.main.size = (640, 480)
        picam2.preview_configuration.main.format = "RGB888"
        picam2.preview_configuration.align()
        picam2.configure("preview")
        picam2.start()
        print("Camera initialized and preview started.")
        
        # Create a window for preview
        cv2.namedWindow("Camera Preview", cv2.WINDOW_NORMAL)
        
        # Wait for the camera to warm up
        time.sleep(2)
        
        # Show preview and wait for a short period
        while True:
            frame = picam2.capture_array()
            cv2.imshow("Camera Preview", frame)
            
            # Check for key press
            key = cv2.waitKey(1)
            if key == ord('q'):
                print("Exiting preview.")
                break
        
        # Capture an image
        filename = "test_image.jpg"
        print(f"Capturing image: {filename}")
        picam2.capture_file(filename)
        print(f"Image captured and saved as {filename}")
        
        # Clean up
        cv2.destroyAllWindows()
        picam2.stop()
        print("Camera stopped.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    test_camera()
