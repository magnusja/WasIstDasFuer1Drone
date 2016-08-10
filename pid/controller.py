from datetime import datetime

from libardrone import at_pcmd


class PIDController(object):
    def __init__(self, kp=0.15, kd=0.25, ki=0.1):
        self.kp = kp
        self.kd = kd
        self.ki = ki
        self.last_error = 0

    def tick(self, current, desired):
        error = desired - current
        result = self.kp * error + \
                 self.ki * (self.last_error + error) + \
                 self.kd * (error - self.last_error)
        self.last_error = error

        return result


class PIDControllerExecutor(object):
    def __init__(self, drone):
        self.drone = drone
        self.timestamp = datetime.now()

        self.height, self.width, _ = self.drone.get_image().shape
        self.middle_x = self.width / 2
        self.middle_y = self.height / 2

        self.x_pid = PIDController()
        self.x_max = PIDController().tick(self.width, self.middle_x)

        self.y_pid = PIDController(kp=0.1, kd=0.2, ki=0.1)
        self.y_max = PIDController().tick(self.height, self.middle_y)

        self.enabled = False

    def millis_interval(self, start, end):
        """start and end are datetime instances"""
        diff = end - start
        millis = diff.days * 24 * 60 * 60 * 1000
        millis += diff.seconds * 1000
        millis += diff.microseconds / 1000
        return millis

    def run(self, input_image, output_image, face):
        if not self.enabled:
            return

        if face is None:
            self.drone.hover()
            return

        face_x, face_y, face_w, face_h = face
        face_middle_x = face_x + face_w / 2
        face_middle_y = face_y + face_h / 2

        u_face_x = self.x_pid.tick(face_middle_x, self.middle_x) / self.x_max
        u_face_y = self.x_pid.tick(face_middle_y, self.middle_y) / self.y_max
        print u_face_x, u_face_y

        self.drone.at(at_pcmd, True, 0, 0, u_face_y * -0.8, u_face_x * 0.6)
