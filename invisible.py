import cv2
import numpy as np

# Load the original video
video = cv2.VideoCapture('original_video.mp4')

# Load the watermark image
watermark = cv2.imread('watermark.png', cv2.IMREAD_GRAYSCALE)

# Define the watermark strength
alpha = 0.01

# Loop over the frames of the video
while True:
    ret, frame = video.read()
    if not ret:
        break

    # Convert the frame to the YCrCb color space
    frame_ycrcb = cv2.cvtColor(frame, cv2.COLOR_BGR2YCrCb)

    # Apply DCT to the Y component of the frame
    dct = cv2.dct(np.float32(frame_ycrcb[:, :, 0]))

    # Embed the watermark in the DCT coefficients
    dct_watermarked = dct + alpha * watermark

    # Inverse DCT to obtain the watermarked frame
    frame_ycrcb[:, :, 0] = cv2.idct(dct_watermarked)

    # Convert the frame back to the BGR color space
    frame_watermarked = cv2.cvtColor(frame_ycrcb, cv2.COLOR_YCrCb2BGR)

    # Display the watermarked frame
    cv2.imshow('Watermarked Video', frame_watermarked)

    # Exit if the 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
video.release()
cv2.destroyAllWindows()
