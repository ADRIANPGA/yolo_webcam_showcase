# YOLOv8 Object Detection with Webcam/Video Input

## Description

This repository contains a Python application for real-time object detection using YOLOv8 with webcam or video files. The application:

- Detects objects in real-time using YOLOv8 models
- Supports both webcam and video file inputs
- Provides a paginated interface for browsing videos in the `/videos` directory
- Allows specifying custom model path via command line arguments
- Displays detection counts and model information in the video window
- Shows consistent window size for all video inputs

## Prerequisites

Before running the application, ensure you have the following dependencies installed:

- Python 3.8+
- Required Python packages (install using `pip install -r requirements.txt`)

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/yolov8-object-detection.git
   cd yolov8-object-detection
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Make sure you have the YOLOv8 model in the `models` directory or specify a custom path.
   - Default model path: `models/model.pt`

## File Structure

```
project/
│
├── app.py            # Main application script
├── models/           # Directory for YOLO models
│   └── model.pt      # Pre-trained YOLOv8 model
├── videos/           # Directory for sample videos
│   ├── public.mp4
│   ├── house.mp4
│   └── traffic.mp4
├── requirements.txt  # Python dependencies
└── README.md         # This file
```

## Usage

### Basic Usage

Run the application with default settings:

```
python app.py
```

The application will:
1. Try to use webcam if available
2. If webcam is not available, display a paginated list of videos from the `videos/` directory
3. Allow you to select a video for object detection

### Command Line Arguments

The application supports the following command line arguments:

- `--model`: Path to the YOLO model file (default: `models/model.pt`)
- `--source`: Source type: `webcam`, `video`, or `auto` (default: `auto`)
- `--video_name`: Name of video file in the videos directory (default: None)

### Examples

```bash
# Use default settings (auto mode, tries webcam first, then video selection)
python app.py

# Specify webcam source explicitly
python app.py --source webcam

# Use video selection from videos/ directory
python app.py --source video

# Specify a specific video by name from the videos directory
python app.py --source video --video_name traffic.mp4

# Use a custom model
python app.py --model /path/to/custom/model.pt

# Combine options
python app.py --model models/custom.pt --source video --video_name house.mp4
```

## Video Selection Interface

When using video source, the application provides a paginated interface:
- Use number keys to select a video
- Press 'n' for the next page of videos
- Press 'p' for the previous page
- Press 'q' to quit

## Detection Window Controls

In the detection window:
- Press 'q' to quit the application
- Close button (X) also works to exit
- Window size is fixed at 1280x720 pixels for consistent viewing experience

## Display Information

The detection window shows:
- Number of detections in the current frame
- Source (webcam or video filename)
- Model name being used
- Bounding boxes with class labels and confidence scores

## Available Models

For a list of available YOLOv8 models, visit: https://docs.ultralytics.com/tasks/detect/#models

## Troubleshooting Webcam on WSL2

If you're using WSL2 and the webcam isn't working:

1. In Windows PowerShell (as admin): `wsl --shutdown`
2. Restart WSL
3. In Windows PowerShell (as admin): `usbipd list`
4. In Windows PowerShell (as admin): `usbipd attach --wsl --busid <YOUR-WEBCAM-BUSID>`

## Acknowledgments

- This application is based on Ultralytics' YOLOv8 framework.
- Special thanks to the Ultralytics team for their excellent work on YOLOv8 and other object detection models.
