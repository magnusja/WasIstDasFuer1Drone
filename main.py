import logging

import pygame
import libardrone

W, H = 320, 240

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


def handle_events():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return False

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
        running = handle_events()
        try:
            display(screen, clock, drone)
        except Exception as e:
            logger.error('Error displaying', e)

    logger.info('Shutting down...')
    drone.halt()


if __name__ == '__main__':
    main()
