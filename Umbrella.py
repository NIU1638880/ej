import pygame
from pygame.locals import RLEACCEL
from screen import Screen
import random

class Umbrella(pygame.sprite.Sprite):
    def __init__(self):
        super(Umbrella, self).__init__()
        self.surf = pygame.image.load("icons/umbrella.png").convert()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        # Start the umbrella at a random x position at the top of the screen
        self.rect = self.surf.get_rect(
            center=(random.randint(0, Screen.width), 0)
        )
        self.speed = random.randint(2, 5)  # Random falling speed

    def update(self):
        # Move the umbrella down
        self.rect.move_ip(0, self.speed)
        # Kill the sprite if it moves past the bottom of the screen
        if self.rect.top > Screen.height:
            self.kill()