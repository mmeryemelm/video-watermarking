import cv2

cap = cv2.VideoCapture("C:/Users/DELL/Desktop/videoprojet/video/video1.mp4")
width = cap.get(cv2.CAP_PROP_FRAME_WIDTH) # frame width
height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT) # frame height
count = cap.get(cv2.CAP_PROP_FRAME_COUNT) #  frame count
fps = cap.get(cv2.CAP_PROP_FPS) #  frame rate
cap.release()
print("width: ",width,"height: ",height,"count; ",count,"fps: ",fps)

file_size = width * height * count * fps * 3
print('File size:', file_size)
