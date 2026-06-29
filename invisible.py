import cv2
import numpy as np
import os


def add_invisible_watermark_dct(input_video, output_video, watermark_image, alpha=0.01):
    """
    Add invisible watermark using DCT (Discrete Cosine Transform)
    Watermark is embedded in frequency domain (invisible to human eye)
    
    Args:
        input_video (str): Path to input video
        output_video (str): Path to output video
        watermark_image (str): Path to grayscale watermark image
        alpha (float): Watermark strength (smaller = more invisible)
    
    Returns:
        bool: Success or failure
    """
    
    try:
        # Validate inputs
        if not os.path.exists(input_video):
            print(f"✗ Input video not found: {input_video}")
            return False
        
        if not os.path.exists(watermark_image):
            print(f"✗ Watermark image not found: {watermark_image}")
            return False
        
        # Open video
        print(f"📹 Opening video: {input_video}")
        video = cv2.VideoCapture(input_video)
        
        if not video.isOpened():
            print("✗ Could not open video")
            return False
        
        # Get properties
        width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = video.get(cv2.CAP_PROP_FPS)
        total_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
        
        print(f"  Resolution: {width}x{height}, FPS: {fps}")
        
        # Load watermark
        print(f"\n🖼 Loading watermark: {watermark_image}")
        watermark = cv2.imread(watermark_image, cv2.IMREAD_GRAYSCALE)
        
        if watermark is None:
            print("✗ Could not load watermark")
            return False
        
        # Resize to frame size
        watermark = cv2.resize(watermark, (width, height))
        watermark = watermark.astype(np.float32)
        
        # Create video writer
        print(f"\n💾 Creating output video: {output_video}")
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(output_video, fourcc, fps, (width, height))
        
        if not out.isOpened():
            print("✗ Could not create video writer")
            return False
        
        # Process frames
        print("\n⏳ Processing frames...")
        frame_count = 0
        
        while True:
            ret, frame = video.read()
            
            if not ret:
                break
            
            try:
                # Convert to YCrCb color space
                frame_ycrcb = cv2.cvtColor(frame, cv2.COLOR_BGR2YCrCb)
                y_channel = frame_ycrcb[:, :, 0].astype(np.float32)
                
                # Apply DCT to Y channel
                dct = cv2.dct(y_channel)
                
                # Embed watermark in DCT coefficients
                dct_watermarked = dct + alpha * watermark
                
                # Inverse DCT to get spatial domain
                y_watermarked = cv2.idct(dct_watermarked)
                
                # Clip to valid range and convert back
                y_watermarked = np.clip(y_watermarked, 0, 255).astype(np.uint8)
                frame_ycrcb[:, :, 0] = y_watermarked
                
                # Convert back to BGR
                frame_watermarked = cv2.cvtColor(frame_ycrcb, cv2.COLOR_YCrCb2BGR)
                
                # Write frame
                out.write(frame_watermarked)
                frame_count += 1
                
                if frame_count % max(1, total_frames // 10) == 0:
                    progress = (frame_count / total_frames) * 100
                    print(f"  Progress: {progress:.1f}%")
            
            except Exception as e:
                print(f"  ⚠ Error on frame {frame_count}: {str(e)}")
                continue
        
        # Cleanup
        video.release()
        out.release()
        
        print(f"\n✓ Invisible watermark applied successfully!")
        print(f"  Output: {output_video}")
        print(f"  Watermark strength (alpha): {alpha}")
        
        return True
    
    except Exception as e:
        print(f"\n✗ Error: {str(e)}")
        return False


if __name__ == "__main__":
    # Example
    add_invisible_watermark_dct(
        input_video='input.mp4',
        output_video='watermarked_invisible.mp4',
        watermark_image='watermark.png',
        alpha=0.01
    )
