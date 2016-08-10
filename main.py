import logging

import cv2
from datetime import datetime

import libardrone.libardrone
from classify.face import FaceClassifier
from cvface.detect import FaceDetector
from overlay.battery import BatteryOverlay
from pid.controller import PIDControllerExecutor
from pipeline import Pipeline

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


def millis_interval(start, end):
    """start and end are datetime instances"""
    diff = end - start
    millis = diff.days * 24 * 60 * 60 * 1000
    millis += diff.seconds * 1000
    millis += diff.microseconds / 1000
    return millis


def handle_events(drone, pid):
    key = cv2.waitKey(10)
    #print key

    if key != -1:
        pid.enabled = False

    if key == 27:  # ESC
        return False
    # takeoff / land
    elif key == 13 or key == 1048586:  # return
        drone.takeoff()
    elif key == 32 or key == 1048608:  # space
        drone.land()
    # emergency
    elif key == 127:  # backspace
        drone.reset()
    # forward / backward
    elif key == ord('w'):
        drone.move_forward()
    elif key == ord('s'):
        drone.move_backward()
    # left / right
    elif key == ord('a'):
        drone.move_left()
    elif key == ord('d'):
        drone.move_right()
    # up / down
    elif key == 63232:  # up
        drone.move_up()
    elif key == 63233:  # down
        drone.move_down()
    # turn left / turn right
    elif key == 63234:  # left
        drone.turn_left()
    elif key == 63235:  # right
        drone.turn_right()
    # speed
    elif key == ord('1'):
        drone.speed = 0.1
    elif key == ord('2'):
        drone.speed = 0.2
    elif key == ord('3'):
        drone.speed = 0.3
    elif key == ord('4'):
        drone.speed = 0.4
    elif key == ord('5'):
        drone.speed = 0.5
    elif key == ord('6'):
        drone.speed = 0.6
    elif key == ord('7'):
        drone.speed = 0.7
    elif key == ord('8'):
        drone.speed = 0.8
    elif key == ord('9'):
        drone.speed = 0.9
    elif key == ord('0'):
        drone.speed = 1.0
    elif key == ord('u') or key == 1048693:
        pid.enabled = True

    return True


def display_cv(drone, pipeline):
    pixelarray = drone.get_image()
    if pixelarray is not None:
        image = cv2.cvtColor(pixelarray, cv2.COLOR_BGR2RGB)
        output_image = image.copy()
        pipeline.run(image, output_image)
        cv2.imshow('image', output_image)


def main():
    logger.info('Starting up')
    drone = libardrone.ARDrone(True)
    drone.reset()
    running = True

    pid = PIDControllerExecutor(drone)

    pipeline = Pipeline([BatteryOverlay(drone),
                         FaceDetector(),
                         FaceClassifier(),
                         pid])

    while running:
        display_cv(drone, pipeline)
        running = handle_events(drone, pid)

    logger.info('Shutting down...')
    drone.halt()


if __name__ == '__main__':
    main()


