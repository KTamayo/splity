import cv2
import numpy as np
from PIL import Image

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

class FaceCropper():

    def __init__(self, directory, topic=None):
        self.directory_name = directory
        if topic is None:
            self.topic = "image"
        else:
            self.topic = topic
    
    def find_faces(self, filename):
        '''
        Ingests the image file with Pillow and converts to RGB from RBG, 
        which is then converted to Numpy array. Image array is passed to openCV 
        for color to black and white image conversion. OpenCV then uses the
        haarcascade model XML file to return an array of rectangle coordinates 
        for the detected faces in image.
        '''
        image = Image.open(filename).convert('RGB')
        #image = Image.frombuffer("RGBA").convert('RGB')
        image_data = np.array(image)
        gray_image_data = cv2.cvtColor(image_data, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray_image_data, 1.3, 7)
        return (faces, gray_image_data)

    def crop_faces(self, faces, gray_image_data):
        '''
        Crops faces from an image using an OpenCV array of rectangle coordinates.
        '''
        counter = 0
        for (x,y,w,h) in faces:
            counter += 1
            roi_gray = gray_image_data[y:y+h, x:x+w]
            output_filename = "{0}/{1}_{2}.png".format(self.directory_name, self.topic, counter) 
            cv2.imwrite(output_filename, roi_gray) 

    def process_image(self, filename):
        faces, gray_image = self.find_faces(filename)
        self.crop_faces(faces, gray_image)
