import cv2
#use this for all things video related like shortening games/clips and all video operations
def shorten_video(input_path, output_path, start_time, end_time):
    """
    Trims the video to the specified time range.
    
    Args:
        input_path (str): Path to the input video file.
        output_path (str): Path to save the shortened video.
        start_time (float): Start time in seconds.
        end_time (float): End time in seconds.
    """
    cap = cv2.VideoCapture(input_path)
    fps = int(cap.get(cv2.CAP_PROP_FPS))  # Frames per second
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    start_frame = int(start_time * fps)
    end_frame = int(end_time * fps)

    # Define the codec and create VideoWriter to save the trimmed video
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

    cap.set(cv2.CAP_PROP_POS_FRAMES, start_frame)

    for frame_idx in range(start_frame, min(end_frame, total_frames)):
        ret, frame = cap.read()
        if not ret:
            break
        out.write(frame)

    cap.release()
    out.release()
    print(f"Video shortened and saved to {output_path}")

# Example usage
input_video_path = r"C:\Users\tenni\Downloads\videoplayback.mp4"  # Original video
output_video_path = r"C:\Users\tenni\Downloads\shortened_video.mp4"  # Shortened video
shorten_video(input_video_path, output_video_path, start_time=0, end_time=15)  # Shorten to first 15 seconds

def verify_video(output_path, expected_duration):
    """
    Verifies the duration of the output video.
    
    Args:
        output_path (str): Path to the shortened video.
        expected_duration (float): Expected duration in seconds.
    """
    cap = cv2.VideoCapture(output_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    total_frames = cap.get(cv2.CAP_PROP_FRAME_COUNT)
    duration = total_frames / fps

    print(f"Expected Duration: {expected_duration} seconds")
    print(f"Actual Duration: {duration:.2f} seconds")

    if abs(duration - expected_duration) < 0.5:  # Allow small margin for rounding
        print("Test Passed: Video duration is correct.")
    else:
        print("Test Failed: Video duration is incorrect.")
