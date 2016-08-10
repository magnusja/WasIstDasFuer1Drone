
class PIDController(object):
    def __init__(self, drone):
        self.drone = drone

    def run(self, input_image, output_image, face):
        if face is None:
            return

        height, width, _ = input_image.shape
        middle_x = width / 2
        middle_y = height / 2

        face_x, face_y, face_w, face_h = face
        face_middle_x = face_x + face_w / 2
        face_middle_y = face_y + face_h / 2

        delta_x = middle_x - face_middle_x
        delta_y = middle_y - face_middle_y

