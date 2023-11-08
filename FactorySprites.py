import pygame
class FactorySprites:
    def __init__(self, sprite_classes, intervals, event_base):
        self.sprite_classes = sprite_classes
        self.intervals = intervals
        self.event_base = event_base
        self.event_types = [event_base + i for i, _ in enumerate(sprite_classes)]
        self._setup_timers()

    def _setup_timers(self):
        for event_type, interval in zip(self.event_types, self.intervals):
            pygame.time.set_timer(event_type, interval)

    def make(self, event_type):
        # Logic to create a sprite based on the event type
        index = self.event_types.index(event_type)
        sprite_class = self.sprite_classes[index]
        return sprite_class()  # Assumes sprite classes have a no-arg constructor
