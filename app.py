# pip install opencv-python

import cv2
import sys
import os
import math
import argparse
from ultralytics import YOLO

def parse_arguments():
    parser = argparse.ArgumentParser(description='Object Detection using YOLO')
    parser.add_argument('--model', type=str, default=os.path.join('models', 'model.pt'),
                        help='Path to the YOLO model file (default: models/model.pt)')
    parser.add_argument('--source', type=str, default='auto',
                        choices=['webcam', 'video', 'auto'],
                        help='Source type: webcam, video, or auto (default: auto)')
    parser.add_argument('--video_name', type=str, default=None,
                        help='Name of video file in videos directory (default: None)')
    return parser.parse_args()

# Parse command line arguments
args = parse_arguments()

MODEL_PATH = args.model
VIDEOS_DIR = 'videos'
VIDEOS_PER_PAGE = 3
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720

# Load YOLO model
if os.path.exists(MODEL_PATH):
    model = YOLO(MODEL_PATH)
    print(f"Model loaded from {MODEL_PATH}")
    print(model.names)
else:
    print(f"Error: Model not found at {MODEL_PATH}")
    sys.exit(1)

# Function to list videos in a paginated way
def list_videos(page=1):
    if not os.path.exists(VIDEOS_DIR):
        print(f"Error: Videos directory '{VIDEOS_DIR}' not found.")
        return []
    
    videos = [f for f in os.listdir(VIDEOS_DIR) if f.lower().endswith(('.mp4', '.avi', '.mov', '.mkv'))]
    if not videos:
        print(f"No videos found in {VIDEOS_DIR}")
        return []
    
    total_pages = math.ceil(len(videos) / VIDEOS_PER_PAGE)
    if page < 1:
        page = 1
    elif page > total_pages:
        page = total_pages
    
    start_idx = (page - 1) * VIDEOS_PER_PAGE
    end_idx = min(start_idx + VIDEOS_PER_PAGE, len(videos))
    page_videos = videos[start_idx:end_idx]
    
    print(f"\nVideos (Page {page}/{total_pages}):")
    for i, video in enumerate(page_videos, start=1):
        print(f"{start_idx + i}. {video}")
    
    if page < total_pages:
        print("\nPress 'n' for next page")
    if page > 1:
        print("Press 'p' for previous page")
    
    return videos, page, total_pages

# Initialize video source
video_source = None
source_type = "webcam"  # Default value
video_filename = ""     # Store the actual video filename

# Handle source selection based on command line arguments
if args.source == 'webcam' or (args.source == 'auto' and args.video_name is None):
    # Try to initialize webcam
    webcam = cv2.VideoCapture(0)
    if webcam.isOpened():
        video_source = webcam
        source_type = "webcam"
        print("Using webcam for detection")
    elif args.source == 'webcam':
        print("Error: Webcam specified but could not be opened.")
        print("If using WSL, make sure webcam is properly connected.")
        print("For WSL2, follow these steps:")
        print("1. In Windows PowerShell (as admin): wsl --shutdown")
        print("2. Restart WSL")
        print("3. In Windows PowerShell (as admin): usbipd list")
        print("4. In Windows PowerShell (as admin): usbipd attach --wsl --busid <YOUR-WEBCAM-BUSID>")
        sys.exit(1)
    else:
        print("Could not open webcam, falling back to video selection.")

# Handle video file source
if video_source is None:
    if args.video_name is not None:
        # Use the specified video name
        video_path = os.path.join(VIDEOS_DIR, args.video_name)
        video_filename = args.video_name
        if os.path.exists(video_path):
            video_source = cv2.VideoCapture(video_path)
            if video_source.isOpened():
                source_type = "video"
                print(f"Using specified video file: {video_path}")
            else:
                print(f"Error: Could not open video file: {video_path}")
                sys.exit(1)
        else:
            print(f"Error: Specified video file not found: {video_path}")
            sys.exit(1)
    elif args.source == 'video' or args.source == 'auto':
        # List videos in directory for selection
        all_videos, current_page, total_pages = list_videos(page=1)
        
        if all_videos:
            while True:
                choice = input("\nEnter video number, 'n' for next page, 'p' for previous page, or 'q' to quit: ")
                
                if choice.lower() == 'q':
                    sys.exit(0)
                elif choice.lower() == 'n' and current_page < total_pages:
                    all_videos, current_page, total_pages = list_videos(page=current_page + 1)
                elif choice.lower() == 'p' and current_page > 1:
                    all_videos, current_page, total_pages = list_videos(page=current_page - 1)
                elif choice.isdigit():
                    idx = int(choice) - 1
                    if 0 <= idx < len(all_videos):
                        video_filename = all_videos[idx]
                        video_path = os.path.join(VIDEOS_DIR, video_filename)
                        video_source = cv2.VideoCapture(video_path)
                        if video_source.isOpened():
                            source_type = "video"
                            print(f"Using video file: {video_path}")
                            break
                        else:
                            print(f"Error: Could not open video file: {video_path}")
                    else:
                        print("Invalid selection. Please try again.")
                else:
                    print("Invalid input. Please try again.")
        else:
            # Ask if user wants to specify a video file manually
            use_video = input("Do you want to specify a video file path manually? (y/n): ")
            if use_video.lower() == 'y':
                video_path = input("Enter path to video file: ")
                if os.path.exists(video_path):
                    video_source = cv2.VideoCapture(video_path)
                    if video_source.isOpened():
                        source_type = "video"
                        video_filename = os.path.basename(video_path)
                        print(f"Using video file: {video_path}")
                    else:
                        print(f"Error: Could not open video file: {video_path}")
                        sys.exit(1)
                else:
                    print(f"Error: Video file not found: {video_path}")
                    sys.exit(1)
            else:
                sys.exit(1)

# Exit if no valid video source was found
if video_source is None or not video_source.isOpened():
    print("No valid video source available. Exiting.")
    sys.exit(1)

# Only create the window after we have a valid video source
cv2.namedWindow("[CDS] Video Object Detection", cv2.WINDOW_NORMAL)
cv2.resizeWindow("[CDS] Video Object Detection", WINDOW_WIDTH, WINDOW_HEIGHT)

# Main loop - only starts after we have a valid video source
print("Starting object detection. Press 'q' to quit.")

while True:
    success, frame = video_source.read()
    
    if not success or frame is None:
        print("End of video or failed to grab frame")
        break
    
    # Track with all classes and reasonable confidence threshold
    results = model.track(frame, conf=0.4, imgsz=480, persist=True)
    
    # Get the processed frame with detections
    annotated_frame = results[0].plot()
    
    # Add detection count
    detection_count = len(results[0].boxes)
    cv2.putText(annotated_frame, f"Detections: {detection_count}", (20, 40), 
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
    
    # Display source and model info
    source_display = video_filename if source_type == "video" else "webcam"
    cv2.putText(annotated_frame, f"Source: {source_display}", (20, 80), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2, cv2.LINE_AA)
    cv2.putText(annotated_frame, f"Model: {os.path.basename(MODEL_PATH)}", (20, 120), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2, cv2.LINE_AA)
    
    # Show the frame
    cv2.imshow("[CDS] Video Object Detection", annotated_frame)

    # Check for key press or window close event
    key = cv2.waitKey(1) & 0xFF
    
    # Exit on 'q' key press or if window is closed
    if key == ord('q') or cv2.getWindowProperty("[CDS] Video Object Detection", cv2.WND_PROP_VISIBLE) < 1:
        break

# Clean up
video_source.release()
cv2.destroyAllWindows()
print("Object detection finished.")

# For Realsense camera
   # def initialize_realsense():
    #    import pyrealsense2 as rs
    #    pipeline = rs.pipeline()
     #   camera_aconfig = rs.config()
      #  camera_aconfig.enable_stream(rs.stream.depth, *config.DEPTH_CAMERA_RESOLUTION, rs.format.z16, config.DEPTH_CAMERA_FPS)
     #   camera_aconfig.enable_stream(rs.stream.color, *config.COLOR_CAMERA_RESOLUTION, rs.format.bgr8, config.COLOR_CAMERA_FPS)
     #   pipeline.start(camera_aconfig)
      #  return pipeline
# try:
#     # Try to initialize RealSense Camera
#     camera = initialize_realsense()
#     get_frame = get_frame_realsense
# except Exception as e:
#     print("RealSense camera not found, using default webcam.")
#     camera = initialize_webcam()
#     get_frame = get_frame_webcam

# Function to get frames from RealSense
# def get_frame_realsense(pipeline):
#     import pyrealsense2 as rs
#     frames = pipeline.wait_for_frames()
#     depth_frame = frames.get_depth_frame()
#     color_frame = frames.get_color_frame()
#     if not depth_frame or not color_frame:
#         return None, None
#     depth_image = np.asanyarray(depth_frame.get_data())
#     color_image = np.asanyarray(color_frame.get_data())
#     return depth_image, color_image

# # Function to get frame from webcam
# def get_frame_webcam(cap):
#     ret, frame = cap.read()
#     return None, frame if ret else None
