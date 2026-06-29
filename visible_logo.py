import cv2
import numpy as np
import os
from pathlib import Path


def add_visible_watermark(input_video, output_video, logo_image, position=(10, 10), 
                         scale=0.15, alpha=0.8):
    """
    Add a visible watermark/logo to a video
    
    Args:
        input_video (str): Path to input MP4 video
        output_video (str): Path to output watermarked video
        logo_image (str): Path to PNG logo (with transparency)
        position (tuple): (x, y) position for logo placement
        scale (float): Size factor (0.1 = 10% of frame height)
        alpha (float): Opacity (0.0 = transparent, 1.0 = opaque)
    
    Returns:
        bool: Success or failure
    """
    
    try:
        # Validate inputs
        if not os.path.exists(input_video):
            print(f"✗ Input video not found: {input_video}")
            return False
        
        if not os.path.exists(logo_image):
            print(f"✗ Logo image not found: {logo_image}")
            return False
        
        # Open video
        print(f"📹 Opening video: {input_video}")
        video = cv2.VideoCapture(input_video)
        
        if not video.isOpened():
            print("✗ Could not open input video")
            return False
        
        # Get video properties
        width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = video.get(cv2.CAP_PROP_FPS)
        total_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
        
        print(f"  Resolution: {width}x{height}")
        print(f"  FPS: {fps}")
        print(f"  Total frames: {total_frames}")
        
        # Load logo
        print(f"\n🖼 Loading logo: {logo_image}")
        logo = cv2.imread(logo_image, cv2.IMREAD_UNCHANGED)
        
        if logo is None:
            print("✗ Could not load logo image")
            return False
        
        # Resize logo based on scale
        logo_height = int(height * scale)
        logo_width = int(logo.shape[1] * (logo_height / logo.shape[0]))
        logo = cv2.resize(logo, (logo_width, logo_height))
        
        print(f"  Logo resized to: {logo_width}x{logo_height}")
        
        # Create video writer
        print(f"\n💾 Creating output video: {output_video}")
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(output_video, fourcc, fps, (width, height))
        
        if not out.isOpened():
            print("✗ Could not create output video writer")
            video.release()
            return False
        
        # Process frames
        print("\n⏳ Processing frames...")
        frame_count = 0
        x, y = position
        
        while True:
            ret, frame = video.read()
            
            if not ret:
                break
            
            try:
                # Ensure position is within bounds
                x_end = min(x + logo.shape[1], width)
                y_end = min(y + logo.shape[0], height)
                x_start = max(0, x)
                y_start = max(0, y)
                
                # Crop logo if it goes out of bounds
                logo_crop_x = x_start - x
                logo_crop_y = y_start - y
                logo_crop = logo[logo_crop_y:logo_crop_y+(y_end-y_start), 
                                  logo_crop_x:logo_crop_x+(x_end-x_start)]
                
                # Apply logo with alpha blending
                if logo.shape[2] == 4:  # Has alpha channel
                    logo_rgb = logo_crop[:, :, :3]
                    logo_alpha = logo_crop[:, :, 3] / 255.0
                    
                    # Blend with alpha
                    for c in range(3):
                        frame[y_start:y_end, x_start:x_end, c] = \
                            frame[y_start:y_end, x_start:x_end, c] * (1 - logo_alpha * alpha) + \
                            logo_rgb[:, :, c] * logo_alpha * alpha
                else:
                    # No alpha - simple blend
                    frame[y_start:y_end, x_start:x_end] = \
                        cv2.addWeighted(frame[y_start:y_end, x_start:x_end], 1-alpha,
                                      logo_crop[:, :, :3], alpha, 0)
                
                # Write frame
                out.write(frame)
                frame_count += 1
                
                if frame_count % max(1, total_frames // 10) == 0:
                    progress = (frame_count / total_frames) * 100
                    print(f"  Progress: {progress:.1f}% ({frame_count}/{total_frames})")
            
            except Exception as e:
                print(f"  ⚠ Error processing frame {frame_count}: {str(e)}")
                continue
        
        # Release resources
        video.release()
        out.release()
        
        print(f"\n✓ Successfully created watermarked video!")
        print(f"  Output: {output_video}")
        print(f"  Frames processed: {frame_count}")
        
        return True
    
    except Exception as e:
        print(f"\n✗ Error: {str(e)}")
        return False


if __name__ == "__main__":
    # Example usage
    add_visible_watermark(
        input_video='input.mp4',
        output_video='watermarked_logo.mp4',
        logo_image='logo.png',
        position=(10, 10),
        scale=0.15,
        alpha=0.8
    )
