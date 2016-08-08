import logging

import pygame
import libardrone

W, H = 320, 240

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


def handle_controls(drone, event):
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


def handle_events(drone):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return False

            handle_controls(drone, event)

    return True


def display(screen, clock, drone):
    surface = pygame.image.fromstring(drone.image, (W, H), 'RGB')
    hud_color = (255, 0, 0) if drone.navdata.get('drone_state', dict()).get('emergency_mask', 1) else (10, 10, 255)
    bat = drone.navdata.get(0, dict()).get('battery', 0)
    f = pygame.font.Font(None, 20)
    hud = f.render('Battery: %i%%' % bat, True, hud_color)
    screen.blit(surface, (0, 0))
    screen.blit(hud, (10, 10))

    pygame.display.flip()
    clock.tick(50)
    pygame.display.set_caption("FPS: %.2f" % clock.get_fps())


def main():
    logger.info('Starting up')
    pygame.init()
    screen = pygame.display.set_mode((W, H))
    drone = libardrone.ARDrone()
    drone.reset()
    clock = pygame.time.Clock()
    running = True

    while running:
        running = handle_events(drone)
        try:
            display(screen, clock, drone)
        except Exception as e:
            logger.error('Error displaying', e)

    logger.info('Shutting down...')
    drone.halt()


if __name__ == '__main__':
    main()
