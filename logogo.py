import cv2
import numpy as np
import os


def add_logo_watermark(input_video, output_video, logo_image, position=(10, 10), 
                       alpha=0.7, logo_scale=0.2):
    """
    Add a semi-transparent logo watermark to video
    
    Args:
        input_video (str): Input video path
        output_video (str): Output video path
        logo_image (str): Logo image path (PNG recommended)
        position (tuple): (x, y) position (top-left corner)
        alpha (float): Opacity (0-1)
        logo_scale (float): Size relative to frame height (0-1)
    
    Returns:
        bool: Success or failure
    """
    
    try:
        # Validation
        if not os.path.exists(input_video):
            print(f"✗ Input video not found: {input_video}")
            return False
        
        if not os.path.exists(logo_image):
            print(f"✗ Logo image not found: {logo_image}")
            return False
        
        # Open video
        print(f"📹 Opening: {input_video}")
        video = cv2.VideoCapture(input_video)
        
        if not video.isOpened():
            print("✗ Cannot open video")
            return False
        
        # Get properties
        width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = video.get(cv2.CAP_PROP_FPS)
        total_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
        
        print(f"  {width}x{height} @ {fps} FPS")
        
        # Load logo
        print(f"🖼 Loading: {logo_image}")
        logo = cv2.imread(logo_image, cv2.IMREAD_UNCHANGED)
        
        if logo is None:
            print("✗ Cannot load logo")
            return False
        
        # Resize logo
        target_height = int(height * logo_scale)
        target_width = int(logo.shape[1] * (target_height / logo.shape[0]))
        logo = cv2.resize(logo, (target_width, target_height))
        
        # Create writer
        print(f"💾 Creating: {output_video}")
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(output_video, fourcc, fps, (width, height))
        
        if not out.isOpened():
            print("✗ Cannot create output video")
            return False
        
        # Process
        print("⏳ Processing...")
        frame_count = 0
        x, y = position
        
        while True:
            ret, frame = video.read()
            if not ret:
                break
            
            try:
                # Position bounds
                x_end = min(x + logo.shape[1], width)
                y_end = min(y + logo.shape[0], height)
                x_start = max(0, x)
                y_start = max(0, y)
                
                # Crop logo
                lx = x_start - x
                ly = y_start - y
                logo_crop = logo[ly:ly+(y_end-y_start), lx:lx+(x_end-x_start)]
                
                # Apply blending
                if logo.shape[2] == 4:
                    # With alpha channel
                    logo_rgb = logo_crop[:, :, :3]
                    logo_alpha = logo_crop[:, :, 3] / 255.0
                    
                    for c in range(3):
                        frame[y_start:y_end, x_start:x_end, c] = \
                            (frame[y_start:y_end, x_start:x_end, c] * (1 - logo_alpha * alpha) + 
                             logo_rgb[:, :, c] * logo_alpha * alpha).astype(np.uint8)
                else:
                    # No alpha
                    frame[y_start:y_end, x_start:x_end] = \
                        cv2.addWeighted(frame[y_start:y_end, x_start:x_end], 1-alpha,
                                      logo_crop[:, :, :3], alpha, 0)
                
                out.write(frame)
                frame_count += 1
                
                if frame_count % max(1, total_frames // 10) == 0:
                    print(f"  {(frame_count/total_frames)*100:.0f}%")
            
            except Exception as e:
                print(f"  ⚠ Frame {frame_count}: {e}")
                continue
        
        video.release()
        out.release()
        
        print(f"\n✓ Done! Output: {output_video}")
        return True
    
    except Exception as e:
        print(f"\n✗ Error: {str(e)}")
        return False


if __name__ == "__main__":
    # Example
    add_logo_watermark(
        input_video='input.mp4',
        output_video='watermarked.mp4',
        logo_image='logo.png',
        position=(10, 10),
        alpha=0.7,
        logo_scale=0.15
    )
