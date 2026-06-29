# 🎬 Video Watermarking

[![Python](https://img.shields.io/badge/Python-3.7%2B-blue?style=flat-square&logo=python)](https://www.python.org/)
[![OpenCV](https://img.shields.io/badge/OpenCV-4.5%2B-green?style=flat-square&logo=opencv)](https://opencv.org/)
[![MP4](https://img.shields.io/badge/Format-MP4-orange?style=flat-square)]()
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow?style=flat-square)](LICENSE)



## 🎯 What It Does

Add watermarks or logos to video files frame-by-frame using OpenCV.

### Features
- Add PNG watermarks to MP4 videos
- Adjustable watermark position
- Preserves original video quality and FPS
- Supports alpha channel (transparency)
- Batch processing ready

## 🚀 Quick Start

```bash
pip install opencv-python numpy
python CODE.py
```

## Usage

Edit `CODE.py` and modify these parameters:

```python
input_video = 'your_video.mp4'      # Input video file
output_video = 'watermarked.mp4'    # Output video file
watermark_image = 'logo.png'        # Watermark image (PNG with alpha)
position = (10, 10)                 # Watermark position (x, y)

addwatermark(input_video, output_video, watermark_image, position)
```

## Parameters

- **input_video**: Path to your MP4 file
- **output_video**: Where to save watermarked video
- **watermark_image**: PNG image with transparency
- **position**: Tuple (x, y) for top-left corner placement

## How It Works

1. Reads video frame-by-frame
2. Overlays watermark on each frame
3. Writes modified frames to output video
4. Preserves original FPS and resolution
