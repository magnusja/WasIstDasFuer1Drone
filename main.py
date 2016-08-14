import logging

import cv2
from datetime import datetime

import pygame

import libardrone.libardrone
from classify.face import FaceClassifier
from cvface.detect import FaceDetector
from cvface.sanitizer import TrackSanitizer
from overlay.battery import BatteryOverlay
from pid.controller import PIDControllerExecutor
from pipeline import Pipeline

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


def handle_controls(drone, event, pid):

    # takeoff / land
    if event.key == pygame.K_RETURN:
        drone.takeoff()
    elif event.key == pygame.K_SPACE:
        drone.land()
    # emergency
    elif event.key == pygame.K_BACKSPACE:
         drone.reset()
    # forward / backward
    elif event.key == pygame.K_w:
        drone.move_forward()
    elif event.key == pygame.K_s:
        drone.move_backward()
    # left / right
    elif event.key == pygame.K_a:
        drone.move_left()
    elif event.key == pygame.K_d:
        drone.move_right()
    # up / down
    elif event.key == pygame.K_UP:
        drone.move_up()
    elif event.key == pygame.K_DOWN:
        drone.move_down()
    # turn left / turn right
    elif event.key == pygame.K_LEFT:
        drone.turn_left()
    elif event.key == pygame.K_RIGHT:
        drone.turn_right()
    # speed
    elif event.key == pygame.K_1:
        drone.speed = 0.1
    elif event.key == pygame.K_2:
        drone.speed = 0.2
    elif event.key == pygame.K_3:
        drone.speed = 0.3
    elif event.key == pygame.K_4:
        drone.speed = 0.4
    elif event.key == pygame.K_5:
        drone.speed = 0.5
    elif event.key == pygame.K_6:
        drone.speed = 0.6
    elif event.key == pygame.K_7:
        drone.speed = 0.7
    elif event.key == pygame.K_8:
        drone.speed = 0.8
    elif event.key == pygame.K_9:
        drone.speed = 0.9
    elif event.key == pygame.K_0:
        drone.speed = 1.0
    elif event.key == pygame.K_u:
        pid.enabled = True


def handle_events(drone, pid):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return False
            pid.enabled = False
            handle_controls(drone, event, pid)

        elif event.type == pygame.KEYUP and not pid.enabled:
            drone.hover()

    return True


def display_cv(drone, pipeline):
    pixelarray = drone.get_image()
    if pixelarray is not None:
        image = cv2.imread('/Users/magnusja/Downloads/13935079_1482213655137650_5032207808350932421_n.jpg') #cv2.cvtColor(pixelarray, cv2.COLOR_BGR2RGB)
        output_image = image.copy()
        pipeline.run(image, output_image)
        cv2.imshow('image', output_image)


def main():
    logger.info('Starting up')
    drone = libardrone.ARDrone(True)
    drone.reset()
    pygame.init()
    running = True

    pid = PIDControllerExecutor(drone)

    pipeline = Pipeline([BatteryOverlay(drone),
                         FaceDetector(),
                         FaceClassifier(),
                         #TrackSanitizer(),
                         #pid])
                            ])

    while running:
        display_cv(drone, pipeline)
        running = handle_events(drone, pid)

    logger.info('Shutting down...')
    drone.halt()


if __name__ == '__main__':
    main()

