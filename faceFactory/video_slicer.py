import cv2,sys

filename = sys.argv[1]
directory = sys.argv[2]

video = cv2.VideoCapture(filename)
success, image = video.read()

count = 0 
success = True
while success:
    cv2.imwrite("frame.png".format(count),image)
    success, image = video.read()
    print("Read a new frame: ", success) 
    count += 1
