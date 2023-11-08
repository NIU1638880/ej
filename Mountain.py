import pygame
from pygame.locals import RLEACCEL
from screen import Screen
import random


class Mountain(pygame.sprite.Sprite):
    def __init__(self):
        super(Mountain, self).__init__()
        self.surf = pygame.image.load("icons/mountain.png").convert_alpha()
        # Asegúrate de que el color que se hace transparente es el correcto.
        # Si tu imagen tiene un fondo que no es blanco, cambia el color aquí.
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)

        # La montaña comienza en la parte inferior de la pantalla, fuera de la vista
        self.rect = self.surf.get_rect(
            center=(
                random.randint(Screen.width + 20, Screen.width + 100),
                Screen.height - self.surf.get_height() // 2
            )
        )
        # Define la velocidad de movimiento hacia la izquierda
        self.speed = 3

    def update(self):
        # Mueve la montaña hacia la izquierda
        self.rect.move_ip(-self.speed, 0)
        # Si la montaña ha desaparecido de la pantalla, se elimina
        if self.rect.right < 0:
            self.kill()
