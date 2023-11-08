import pygame

from pygame.locals import (
    RLEACCEL,
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
)

from screen import Screen


# Define the Player object extending pygame.sprite.Sprite
# Instead of a surface, we use an image for a better looking sprite
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.surf = pygame.image.load("icons/helicopter.png").convert()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        # initial position
        self.rect = self.surf.get_rect(
            center=(Screen.width//4, Screen.height//2)
        )
        """        x
             +------>
             |
          y  |
             v
        """
        self.move_up_sound = pygame.mixer.Sound("sounds_music/Rising_putter.ogg")
        self.move_up_sound.set_volume(0.5)
        self.move_down_sound = pygame.mixer.Sound("sounds_music/Falling_putter.ogg")
        self.move_down_sound.set_volume(0.5)

    # Move the sprite based on keypresses
    def update(self, pressed_keys):
        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -5)
            self.move_up_sound.play()
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, 5)
            self.move_down_sound.play()
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-5, 0)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(5, 0)

        # Keep player on the screen.py
        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > Screen.width:
            self.rect.right = Screen.width
        if self.rect.top <= 0:
            self.rect.top = 0
        elif self.rect.bottom >= Screen.height:
            self.rect.bottom = Screen.height

    def stop_move_sounds(self):
        self.move_up_sound.stop()
        self.move_down_sound.stop()
