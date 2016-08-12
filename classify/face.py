import random
import string

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

    def run(self, input_image, output_image, faces):
        self.counter += 1
        #if self.counter % 2 == 1: return self.last_face
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
                'http://localhost:5001/classify',
                files=files)

            print 'classy time %f' % self.millis_interval(time, datetime.now())

            print response.json()

            predictions = response.json()['prediction']

            print predictions

            # only label shape if over 90%
            if predictions[0][1] > 90:
                print predictions[0][0]
                cv2.putText(output_image, predictions[0][0], (x + w + 5, y + h + 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, 255)

                if predictions[0][0] == 'magnus' or predictions[0][0] == 'jakob' or \
                   predictions[0][0] == 'magnus2' or predictions[0][0] == 'jakob2':
                    self.last_face = (x, y, w, h)
                    return x, y, w, h

        return None
