import cv2
import os
import random

# Folder path where your video files are located
video_folder = "videos"

# Get a list of all video files in the folder
video_files = [f for f in os.listdir(video_folder) if f.endswith((".mp4", ".avi", ".mkv"))]

# Check if there are any video files in the folder
if not video_files:
    print("No video files found in the 'videos' folder.")
else:
    # Choose a random video file
    random_video = random.choice(video_files)

    # Create a full path to the selected video file
    video_path = os.path.join(video_folder, random_video)

    # Initialize the video capture object
    video_capture = cv2.VideoCapture(video_path)

    # Create a window to display the video
    cv2.namedWindow("Random Video Player", cv2.WINDOW_NORMAL)

    while True:
        ret, frame = video_capture.read()
        if not ret:
            break

        # Display the frame in the window
        cv2.imshow("Random Video Player", frame)

        # Check for the 'q' key to exit
        if cv2.waitKey(25) & 0xFF == ord("q"):
            break

    # Release the video capture object and close the window
    video_capture.release()
    cv2.destroyAllWindows()
