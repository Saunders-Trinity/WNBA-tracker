import cv2
from record import *  # importing record file
from locate import *  # locate file added
from locate import lower_hsv, upper_hsv, lower_free_throw, upper_free_throw  # Import the HSV variables
import os



def process_frame(frame):
    """
    Process each frame: detect players, exclude certain areas, and draw boxes.
    """
    # Call player detection to get a mask and identify players based on jersey color
    player_detection(frame, lower_hsv, upper_hsv, lower_free_throw, upper_free_throw)

def main():
    
    video_path = r"C:\Users\tenni\Downloads\shortened_video.mp4"

    # Check if the video file exists
    if not os.path.exists(video_path):
        print(f"Error: Video file does not exist at {video_path}")
        return

    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        print("Error: Unable to open video file.")
        return

    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    print(f"Total number of frames: {total_frames}")

    # Process the video frame by frame
    frame_count = 0
    while frame_count < total_frames:  # Adjusted loop condition
        ret, frame = cap.read()
        if not ret:
            print(f"Failed to read frame at position {cap.get(cv2.CAP_PROP_POS_FRAMES)}")
            print("Video has ended or error reading frame.")
            break

        # Process the current frame
        process_frame(frame)

        # Display the frame (for debugging)
        cv2.imshow("Frame", frame)

        # Check for 'Esc' key to exit
        if cv2.waitKey(1) & 0xFF == 27:  # 27 is the ESC key
            print("Esc key pressed, exiting.")
            break

        frame_count += 1
        print(f"Processing frame {frame_count}/{total_frames}")

    # Release the video capture and close all windows
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
