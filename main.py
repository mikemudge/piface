#!python3
import requests
import subprocess
import sys
import os
from time import sleep

# Import the pygame module
import pygame

# Import pygame.locals for easier access to key coordinates
# Updated to conform to flake8 and black standards
from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

def main():
    print("Running the piface")
    print('Argument List:', str(sys.argv))

    ip = "192.168.1.76:8085"
    forever = False
    if len(sys.argv) > 1:
        ip = sys.argv[1]

    if '--forever' in sys.argv:
        forever = True

    print('Looking at host', ip)

    # Initialize pygame
    pygame.init()

    # Define constants for the screen width and height
    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 600

    # Create the screen object
    # The size is determined by the constant SCREEN_WIDTH and SCREEN_HEIGHT
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.locals.FULLSCREEN)
    black = (0,0,0)
    white = (255,255,255)
    clock = pygame.time.Clock()

    cpuHistory = []
    running = True
    iteration = 0
    while running:
        iteration += 1
        response = requests.get("http://" + ip + "/data.json")

        data = response.json()

        print('Keys', data.keys())
        pc = data.get('Children')[0]

        print("Showing data for PC named", pc.get('Text'))
        
        for component in pc.get('Children'):
            name = component.get('Text')
            for section in component.get('Children'):
                if section.get('Text') == 'Load':
                    for v in section.get("Children"):
                        if v.get('Text') == 'CPU Total':
                            # This is a primary metric
                            print("CPU Load =", v.get('Value'))
                            cpuPercent = float(v.get('Value')[:-1].strip())
                            print("float()", cpuPercent)
                            cpuHistory.append(cpuPercent)
                            cpuHistory = cpuHistory[-10:]

                        print(component.get('Text'), "> Load >", v.get('Text'), v.get('Value'))

        # Pick a face and display it.

        print("CPU Load =", cpuPercent)
        image = os.path.join(os.getcwd(), 'image2.png')
        if cpuPercent < 20:
            image = os.path.join(os.getcwd(), 'image1.png')
        if cpuPercent > 50:
            image = os.path.join(os.getcwd(), 'image3.png')
        if cpuPercent > 75:
            image = os.path.join(os.getcwd(), 'image4.png')

        screen.fill(white)

        carImg = pygame.image.load(image)
        screen.blit(pygame.transform.scale(carImg, (SCREEN_WIDTH, SCREEN_HEIGHT)), (0,0))
        
        pygame.display.update()
        clock.tick(1)

        for event in pygame.event.get():
            # Did the user hit a key?
            if event.type == KEYDOWN:
                # Was it the Escape key? If so, stop the loop.
                if event.key == K_ESCAPE:
                    running = False

            # Did the user click the window close button? If so, stop the loop.
            elif event.type == QUIT:
                running = False

        if not forever and iteration > 10:
            # Max at 10 iterations if --forever is not set.
            break

    print("CPU usage over time", cpuHistory)

    print("Finished piface")


if __name__ == '__main__':
    main()