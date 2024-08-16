import pygame
class Game:
    def __init__(self, screen, states, start_state):
        self.screen = screen
        self.states = states
        self.state_name = start_state
        self.state = self.states[self.state_name]
        self.done = False
        self.state.startup({})  # Start mit einem leeren persistenten Dictionary

    def get_event(self, event):
        self.state.get_event(event)

    def update(self, dt):
        self.state.update(dt)
        if self.state.done:
            self.flip_state()

    def draw(self, screen):
        self.state.draw(screen)

    def flip_state(self):
        self.state.done = False
        previous, self.state_name = self.state_name, self.state.next_state
        persistent = self.state.cleanup()
        self.state = self.states[self.state_name]
        self.state.startup(persistent)

    def resize(self, width, height):
        """Passt das Spiel und die aktuelle State an eine neue Bildschirmgröße an."""
        self.screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
        self.state.resize(width, height)  # Ruf die resize Methode der aktuellen State auf
