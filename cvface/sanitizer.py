import math

THRESHOLD = 100


class TrackSanitizer(object):

    def __init__(self):
        self.last_face = None
        self.counter = 0

    def run(self, input_image, output_image, face):
        if self.last_face is None:
            if self.counter >= 3:
                self.last_face = face
                self.counter = 0
                return face

            self.counter += 1

            return None

        if face is None:
            if self.counter >= 3:
                self.last_face = None
                self.counter = 0
                return None

            self.counter += 1
            return self.last_face

        face_x, face_y, face_w, face_h = face
        face_middle_x = face_x + face_w / 2
        face_middle_y = face_y + face_h / 2

        last_face_x, last_face_y, last_face_w, last_face_h = self.last_face
        last_face_middle_x = last_face_x + last_face_w / 2
        last_face_middle_y = last_face_y + last_face_h / 2

        if math.fabs(face_middle_x - last_face_middle_x) > THRESHOLD and \
           math.fabs(face_middle_y - last_face_middle_y) > THRESHOLD and \
           self.counter <= 3:
            self.counter += 1
            return self.last_face

        self.last_face = face
        self.counter = 0

        return self.last_face
