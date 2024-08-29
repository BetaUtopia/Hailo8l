from picamera2 import Picamera2
import cv2
import os
import argparse

def capture_video_from_camera(output_video_path: str, frame_size: tuple, fps: int):
    # Initialize the camera
    picam2 = Picamera2()
    picam2.preview_configuration.main.size = frame_size
    picam2.preview_configuration.main.format = "RGB888"
    picam2.preview_configuration.align()
    picam2.configure("preview")
    picam2.start()

    print("Camera initialized and video capture started.")

    # Initialize video writer
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Codec for MP4 format
    video_writer = cv2.VideoWriter(output_video_path, fourcc, fps, frame_size)

    # Create a window for preview
    cv2.namedWindow("Camera Preview", cv2.WINDOW_NORMAL)

    while True:
        # Capture a frame
        frame = picam2.capture_array()

        # Write frame to video
        video_writer.write(frame)

        # Display the preview
        cv2.imshow("Camera Preview", frame)

        # Check for key press
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            print("Stopping video capture.")
            break

    # Clean up
    video_writer.release()
    picam2.stop()
    cv2.destroyAllWindows()
    print(f"Video saved as {output_video_path}")

def main():
    parser = argparse.ArgumentParser(description="Capture video from camera and save to file.")
    parser.add_argument('--output_video', default='output_video.mp4', help='Path to save the output video.')
    parser.add_argument('--frame_width', type=int, default=640, help='Width of video frames.')
    parser.add_argument('--frame_height', type=int, default=480, help='Height of video frames.')
    parser.add_argument('--fps', type=int, default=30, help='Frames per second for the video.')
    args = parser.parse_args()

    frame_size = (args.frame_width, args.frame_height)
    capture_video_from_camera(args.output_video, frame_size, args.fps)

if __name__ == "__main__":
    main()
