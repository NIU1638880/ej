import pygame

# Import pygame.locals for easier access to key coordinates
# Updated to conform to flake8 and black standards
from pygame.locals import (
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

from screen import Screen
from player import Player
from bird import Bird
from cloud import Cloud


class Game:
    def __init__(self, factory_flying, factory_landscape):
        self._factory_flying = factory_flying
        self._factory_landscape = factory_landscape
        self._flying_sprites = pygame.sprite.Group()
        self._landscape_sprites = pygame.sprite.Group()
        self._all_sprites = pygame.sprite.Group()
        self._initialize_game()
        self._load_music_and_sounds()
        self._play_music()
        self._make_objects()

    def _initialize_game(self):
        # Setup the clock for a decent frame rate
        self._clock = pygame.time.Clock()
        # Create and get the screen object
        self._screen = pygame.display.set_mode((Screen.width, Screen.height))
        # Create custom events for adding a new bird and cloud
        new_bird_period = 500
        new_cloud_period = 750
        # make a new bird/cloud every these milliseconds, so the smaller
        # the more new birds/clouds
        self._add_bird_event_type = pygame.USEREVENT + 1
        pygame.time.set_timer(self._add_bird_event_type, new_bird_period)
        self._add_cloud_event_type = pygame.USEREVENT + 2
        pygame.time.set_timer(self._add_cloud_event_type, new_cloud_period)
        self._user_quits = False  # to quit press Escape or close the window

    def _make_objects(self):
        # Create our 'player'
        self._player = Player()

        # Create groups to hold bird sprites, cloud sprites, and all sprites
        # - birds is used for collision detection and position updates
        # - clouds is used for position updates
        # - all_sprites is used for rendering
        self._flying_sprites = pygame.sprite.Group()
        self._landscape_sprites = pygame.sprite.Group()
        self._all_sprites = pygame.sprite.Group()
        self._all_sprites.add(self._player)

    @staticmethod
    def _play_music():
        pygame.mixer.music.play(loops=-1)

    def _load_music_and_sounds(self):
        # Load and play our background music
        pygame.mixer.music.load("sounds_music/Apoxode_-_Electric_1.mp3")
        self._collision_sound = pygame.mixer.Sound(
            "sounds_music/Explosion_10.ogg")
        self._collision_sound.set_volume(0.5)

    def _process_event(self):
        # Look at every event in the queue
        for event in pygame.event.get():
            print('event type = {}'.format(event.type))
            # Did the user hit a key?
            if event.type == KEYDOWN:
                # Was it the Escape key? If so, stop the loop
                if event.key == K_ESCAPE:
                    self._user_quits = True
            # Did the user click the window close button? If so, stop the loop
            elif event.type == QUIT:
                self._user_quits = True
            elif event.type in self._factory_flying.event_types:
                # Create the new flying object, and add it to our sprite groups
                new_flying = self._factory_flying.make(event.type)
                self._flying_sprites.add(new_flying)
                self._all_sprites.add(new_flying)
                # Should we add a new landscape object?
            elif event.type in self._factory_landscape.event_types:
                # Create the new landscape object, and add it to our sprite groups
                new_landscape = self._factory_landscape.make(event.type)
                self._landscape_sprites.add(new_landscape)
                self._all_sprites.add(new_landscape)

    def _update(self):
        # Get the set of keys pressed and check for user input
        pressed_keys = pygame.key.get_pressed()
        self._player.update(pressed_keys)
        # Update the position of our flying and landscape sprites
        self._flying_sprites.update()
        self._landscape_sprites.update()

    def _draw(self):
        # Fill the screen.py with sky blue
        self._screen.fill((135, 206, 250))
        # Draw all our sprites
        for entity in self._all_sprites:
            self._screen.blit(entity.surf, entity.rect)
        # Flip everything to the display
        pygame.display.flip()

    def _collision(self):
        return pygame.sprite.spritecollideany(self._player, self._flying_sprites)

    def _game_over(self):
        return self._collision() or self._user_quits

    def _keep_frame_rate(self):
        # Ensure we maintain a 30 frames per second rate
        self._clock.tick(30)

    def play(self):
        while not self._game_over():
            self._process_event()
            self._update()
            self._draw()
            self._keep_frame_rate()

        # Check if any bird have collided with the player
        if self._collision():
            # If so, remove the player
            self._player.kill()
            # Stop any moving sounds and play the collision sound
            self._player.stop_move_sounds()
            pygame.mixer.music.stop()
            self._collision_sound.play()
            pygame.time.wait(2000)  # seconds, to play collision sound

        pygame.mixer.quit()
