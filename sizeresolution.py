import cv2
import os
from pathlib import Path


def get_video_info(video_path):
    """
    Get detailed video information
    
    Args:
        video_path (str): Path to video file
    
    Returns:
        dict: Video properties or None if error
    """
    
    try:
        if not os.path.exists(video_path):
            print(f"✗ File not found: {video_path}")
            return None
        
        video = cv2.VideoCapture(video_path)
        
        if not video.isOpened():
            print(f"✗ Could not open video: {video_path}")
            return None
        
        # Get all properties
        width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = video.get(cv2.CAP_PROP_FPS)
        total_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
        codec = int(video.get(cv2.CAP_PROP_FOURCC))
        
        # Calculate derived properties
        duration_seconds = total_frames / fps if fps > 0 else 0
        duration_minutes = duration_seconds / 60
        
        # Codec to string
        codec_str = "".join([chr((codec >> 8 * i) & 0xFF) for i in range(4)])
        
        # File size in MB
        file_size_mb = os.path.getsize(video_path) / (1024 * 1024)
        
        video.release()
        
        info = {
            'filename': os.path.basename(video_path),
            'width': width,
            'height': height,
            'resolution': f"{width}x{height}",
            'aspect_ratio': f"{width/height:.2f}:1",
            'fps': round(fps, 2),
            'total_frames': total_frames,
            'duration_seconds': round(duration_seconds, 2),
            'duration_minutes': round(duration_minutes, 2),
            'codec': codec_str,
            'file_size_mb': round(file_size_mb, 2)
        }
        
        return info
    
    except Exception as e:
        print(f"✗ Error: {str(e)}")
        return None


def print_video_info(video_path):
    """Pretty print video information"""
    
    info = get_video_info(video_path)
    
    if info is None:
        return
    
    print("\n" + "="*50)
    print("📹 VIDEO INFORMATION")
    print("="*50)
    print(f"Filename: {info['filename']}")
    print(f"Resolution: {info['resolution']} ({info['aspect_ratio']})")
    print(f"FPS: {info['fps']}")
    print(f"Total Frames: {info['total_frames']}")
    print(f"Duration: {info['duration_minutes']:.2f} minutes ({info['duration_seconds']:.1f} seconds)")
    print(f"Codec: {info['codec']}")
    print(f"File Size: {info['file_size_mb']} MB")
    print("="*50 + "\n")


if __name__ == "__main__":
    # Example usage
    print_video_info('input.mp4')
