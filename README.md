# YOLOv8 Object Detection

A Python application for real-time object detection using YOLOv8 with webcam, video files, or image uploads.

## Features

- Real-time object detection using YOLOv8 models
- Multiple input options:
  - Webcam feed for live detection
  - Video file processing with interactive selection
  - Image upload and processing
- Performance optimization with frame skipping and batch processing
- FPS counter to monitor performance
- Adjustable confidence threshold for detection
- Filter detections by class
- Customize bounding box colors
- Download processed images with detections

## Environment Setup

### Required Python Version
**Python 3.11.5 is required** for this application.

### Setup on Windows

1. Install Python 3.11.5 from the [official Python website](https://www.python.org/downloads/release/python-3115/)

2. Install Microsoft Visual C++ Build Tools (required for some packages):
   - Download the [Visual Studio Build Tools](https://visualstudio.microsoft.com/visual-cpp-build-tools/)
   - During installation, select "Desktop development with C++"

3. Open Command Prompt as Administrator and create a virtual environment:
   ```batch
   # Navigate to your project directory
   cd path\to\project

   # Create a virtual environment with Python 3.11.5
   py -3.11 -m venv yolo_env

   # Activate the virtual environment
   yolo_env\Scripts\activate
   ```

4. Install the required packages:
   ```batch
   pip install -r requirements.txt
   ```

### Setup on Linux/WSL (Ubuntu)

1. Open terminal and install Python 3.11.5:
   ```bash
   sudo apt update
   sudo apt install software-properties-common -y
   sudo apt install python3.11 python3.11-venv python3.11-dev -y
   ```

2. Create a virtual environment:
   ```bash
   # Navigate to your project directory
   cd path/to/project

   # Create a virtual environment with Python 3.11.5
   python3.11 -m venv yolo_env

   # Activate the virtual environment
   source yolo_env/bin/activate
   ```

3. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

### Setup on macOS

1. Install Python 3.11.5 using Homebrew:
   ```bash
   brew update
   brew install python@3.11
   ```

2. Create a virtual environment:
   ```bash
   # Navigate to your project directory
   cd path/to/project

   # Create a virtual environment with Python 3.11.5
   python3.11 -m venv yolo_env

   # Activate the virtual environment
   source yolo_env/bin/activate
   ```

3. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

## Project Structure

```
project/
│
├── app.py            # Main webcam/video application script
├── models/           # Directory for YOLO models
│   └── model.pt      # Pre-trained YOLOv8 model
├── videos/           # Directory for sample videos
│   ├── sample1.mp4
│   └── sample2.mp4
├── requirements.txt  # Python dependencies
└── README.md         # This file
```

## Quick Start Guide

1. **Setup the environment** (as described above)

2. **Download a YOLOv8 model**:
   - Create a `models` directory in your project folder
   - Download a YOLOv8 model from [Ultralytics](https://docs.ultralytics.com/tasks/detect/#models)
   - Place the model in the `models` directory as `model.pt`

3. **Prepare video files** (optional):
   - Create a `videos` directory in your project folder
   - Add video files (mp4, avi, mov, mkv) to this directory

4. **Run the application**:
   ```bash
   # Make sure your virtual environment is activated
   python app.py
   ```

## Running the Webcam/Video App

### Basic Usage

Run the application with default settings:

```
python app.py
```

This will:
1. Try to use your webcam if available
2. If webcam is not available, display a list of videos from the `videos/` directory
3. Allow you to select a video for object detection

### Command Line Arguments

The application supports various command line arguments for customization:

- `--model`: Path to the YOLO model file (default: `models/model.pt`)
- `--source`: Source type: `webcam`, `video`, or `auto` (default: `auto`)
- `--video_name`: Name of video file in the videos directory
- `--frame_skip`: Number of frames to skip between detections for better performance
- `--batch_size`: Batch size for inference (optimize GPU usage)
- `--imgsz`: Image size for inference
- `--conf`: Confidence threshold for detections

### Examples

```bash
# Use webcam with frame skipping (process every 2nd frame for better performance)
python app.py --source webcam --frame_skip 1

# Use a specific video file with custom confidence threshold
python app.py --source video --video_name traffic.mp4 --conf 0.5

# Use a custom model with batch processing
python app.py --model models/yolov8n.pt --batch_size 4

# Specify a smaller image size for faster processing
python app.py --imgsz 320
```

## Running the Streamlit App (if available)

If the Streamlit-based version is part of this project, you can run it as follows:

1. Make sure your virtual environment is activated
2. Navigate to the appropriate directory (e.g., `src` directory)
3. Run:
   ```bash
   streamlit run main.py
   ```

If that doesn't work, try:
```bash
python -m streamlit run main.py
```

## Interface Controls

### Video Selection Interface
When using video source, the application provides a paginated interface:
- Enter a number to select a video
- Press 'n' for the next page of videos
- Press 'p' for the previous page
- Press 'q' to quit

### Detection Window Controls
In the detection window:
- Press 'q' to quit the application
- Close the window to exit the application

## Troubleshooting

### Webcam Access Issues on WSL2

If you're using WSL2 and the webcam isn't working:

1. In Windows PowerShell (as admin): `wsl --shutdown`
2. Restart WSL
3. In Windows PowerShell (as admin): `usbipd list`
4. In Windows PowerShell (as admin): `usbipd attach --wsl --busid <YOUR-WEBCAM-BUSID>`

### Common Installation Issues

If you encounter issues with package installation:

1. Ensure you're using Python 3.11.5:
   ```bash
   python --version
   ```

2. Make sure you have the latest pip:
   ```bash
   pip install --upgrade pip
   ```

3. For Windows users, make sure you've installed Microsoft Visual C++ Build Tools

4. If OpenCV installation fails, try:
   ```bash
   # On Ubuntu/Debian
   sudo apt install libgl1-mesa-glx
   # Then reinstall
   pip install opencv-python
   ```

5. If installation fails, try installing packages one by one:
   ```bash
   pip install opencv-python>=4.7.0
   pip install ultralytics>=8.0.0
   
   # For Streamlit version, if applicable:
   pip install streamlit==1.34.0
   pip install numpy==1.26.4
   pip install opencv-python-headless==4.9.0.80
   pip install pillow==10.3.0
   pip install ultralytics==8.1.9
   pip install torch==2.2.0+cpu torchvision==0.17.0+cpu --extra-index-url https://download.pytorch.org/whl/cpu
   pip install onnx==1.17.0
   pip install pyyaml==6.0.1 tqdm==4.66.3 matplotlib==3.8.2
   ```

6. On Windows, if you encounter DLL load errors, install the [Microsoft Visual C++ Redistributable](https://aka.ms/vs/17/release/vc_redist.x64.exe)

## Acknowledgments

- This application uses Ultralytics' YOLOv8 framework for object detection.
- Special thanks to the Ultralytics team for their excellent work on YOLOv8.
