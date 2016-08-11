import random
import string

import cv2
import requests
from PIL import Image
from io import BytesIO

import numpy as np


class FaceClassifier(object):

    def run(self, input_image, output_image, faces):
        for (x, y, w, h) in faces:
            image = input_image[y:y+h, x:x+w]

            enc = Image.fromarray(np.roll(image, 1, axis=-1))
            #enc.save('/Users/magnusja/Downloads/aasdasd/' + ''.join(random.choice(string.hexdigits) for _ in range(12)) + '.jpg', "JPEG")

            f = BytesIO()
            enc.save(f, "JPEG")
            f.seek(0)

            files = {'image_file': ('test.jpg', f, 'image/jpg')}

            # query DIGITS REST API for classification
            response = requests.post(
                'http://localhost:5001/classify',
                files=files)

            print response.json()

            predictions = response.json()['prediction']

            print predictions

            # only label shape if over 90%
            if predictions[0][1] > 90:
                print predictions[0][0]
                cv2.putText(output_image, predictions[0][0], (x + w + 5, y + h + 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, 255)

                if predictions[0][0] == 'magnus' or predictions[0][0] == 'jakob':
                    return x, y, w, h

        return None
