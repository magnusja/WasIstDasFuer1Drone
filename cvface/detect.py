import os

import cv2


class FaceDetector(object):

    def __init__(self):
        self.face_cascade = cv2.CascadeClassifier(os.path.join(os.path.dirname(__file__), 'haarcascade_frontalface_default.xml'))
        self.eye_cascade = cv2.CascadeClassifier(os.path.join(os.path.dirname(__file__), 'haarcascade_eye.xml'))

    def run(self, input_image, output_image, exec_result=None):
        return self.detect_faces(input_image, output_image)

    def detect_faces(self, input_image, output_image):
        gray = cv2.cvtColor(input_image, cv2.COLOR_BGR2GRAY)

        faces = self.face_cascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(10, 10),
            flags=cv2.cv.CV_HAAR_SCALE_IMAGE
        )

        # Draw a rectangle around the faces
        for (x, y, w, h) in faces:
            cv2.rectangle(output_image, (x, y), (x + w, y + h), (255, 0, 0), 2)

            #face = gray[y:y+h, x:x+w]
            #out_face = output_image[y:y+h, x:x+w]
            #eyes = self.eye_cascade.detectMultiScale(face)
            #for (ex, ey, ew, eh) in eyes:
            #    cv2.rectangle(out_face, (ex, ey), (ex + ew, ey + eh), (0, 255, 0), 2)

        return faces
