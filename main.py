import logging

import cv2
from datetime import datetime

import libardrone.libardrone
from cvface.detect import detect_faces

W, H = 320, 240

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)
last_key_press = datetime.now()


def millis_interval(start, end):
    """start and end are datetime instances"""
    diff = end - start
    millis = diff.days * 24 * 60 * 60 * 1000
    millis += diff.seconds * 1000
    millis += diff.microseconds / 1000
    return millis


def handle_events(drone):
    global last_key_press
    key = cv2.waitKey(100)

    if key != -1:
        last_key_press = datetime.now()

    if key == 27:  # ESC
        return False
    # takeoff / land
    elif key == 13:  # return
        drone.takeoff()
    elif key == 32:  # space
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
    elif key == -1 and millis_interval(datetime.now(), last_key_press) > 500:
        last_key_press = datetime.now()
        drone.hover()

    return True


def display_cv(drone):
    pixelarray = drone.get_image()
    battery = drone.navdata.get(0, dict()).get('battery', 0)
    if pixelarray is not None:
        image = cv2.cvtColor(pixelarray, cv2.COLOR_BGR2RGB)
        cv2.putText(image, 'Battery %f' % battery, (100, 100), cv2.FONT_HERSHEY_PLAIN, 1, (0,255,0), 2)
        detect_faces(image)
        cv2.imshow('image', image)


def main():
    logger.info('Starting up')
    drone = libardrone.ARDrone(True)
    drone.reset()
    running = True

    while running:
        display_cv(drone)
        running = handle_events(drone)

    logger.info('Shutting down...')
    drone.halt()


if __name__ == '__main__':
    main()


