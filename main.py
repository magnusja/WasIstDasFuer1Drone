import pygame
import libardrone

def main():
    pygame.init()
    W, H = 320, 240
    screen = pygame.display.set_mode((W, H))
    drone = libardrone.ARDrone()
    clock = pygame.time.Clock()
    running = True


    while running == True:
        pass


if __file__ == '__main__'
    main()