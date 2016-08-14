import math


import cv2
from datetime import datetime
import requests
from PIL import Image
from io import BytesIO

import numpy as np


class FaceClassifier(object):
    def __init__(self):
        self.counter = 0
        self.last_face = None

    def millis_interval(self, start, end):
        """start and end are datetime instances"""
        diff = end - start
        millis = diff.days * 24 * 60 * 60 * 1000
        millis += diff.seconds * 1000
        millis += diff.microseconds / 1000
        return millis

    def track_face(self, faces):
        if len(faces) == 0 or self.last_face is None:
            return None

        current_min = faces[0]
        for (face_x, face_y, face_w, face_h) in faces:
            face_middle_x = face_x + face_w / 2
            face_middle_y = face_y + face_h / 2

            current_min_x, current_min_y, current_min_w, current_min_h = current_min
            current_min_middle_x = current_min_x + current_min_w / 2
            current_min_middle_y = current_min_y + current_min_h / 2

            last_face_x, last_face_y, last_face_w, last_face_h = self.last_face
            last_face_middle_x = last_face_x + last_face_w / 2
            last_face_middle_y = last_face_y + last_face_h / 2

            if math.fabs(face_middle_x - last_face_middle_x) < math.fabs(current_min_middle_x - last_face_middle_x) and \
                math.fabs(face_middle_y - last_face_middle_y) < math.fabs(current_min_middle_y - last_face_middle_y):
                current_min = (face_x, face_y, face_w, face_h)

        return current_min

    def run(self, input_image, output_image, faces):
        self.counter += 1
        #if self.counter % 2 == 0:
        #    return self.track_face(faces)
        for (x, y, w, h) in faces:
            image = input_image[y:y+h, x:x+w]

            enc = Image.fromarray(np.roll(image, 1, axis=-1))
            #enc.save('/Users/magnusja/Downloads/aasdasd/' + ''.join(random.choice(string.hexdigits) for _ in range(12)) + '.jpg', "JPEG")

            f = BytesIO()
            enc.save(f, "JPEG")
            f.seek(0)

            files = {'image_file': ('test.jpg', f, 'image/jpg')}

            time = datetime.now()
            # query DIGITS REST API for classification
            response = requests.post(
                'http://mydocker:5001/classify',
                files=files)

            print 'classy time %f' % self.millis_interval(time, datetime.now())

            print response.json()

            predictions = response.json()['prediction']

            print predictions

            # only label shape if over 90%
            if predictions[0][1] > 95:
                print predictions[0][0]
                name = predictions[0][0] if not predictions[0][0][-1] == '2' else predictions[0][0][0:-1]
                cv2.putText(output_image, name, (x - 5, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.3, 255)

                #if predictions[0][0] == 'magnus' or predictions[0][0] == 'jakob' or \
                #   predictions[0][0] == 'magnus2' or predictions[0][0] == 'jakob2':
                #    self.last_face = (x, y, w, h)
                #    return x, y, w, h


        cv2.imwrite('/Users/magnusja/Downloads/13935079_1482213655137650_5032207808350932421_n22.jpg', output_image)

        return None
