import pygame

class Game:
    def __init__(self, screen, states, start_state):
        self.screen = screen
        self.states = states
        self.state_name = start_state
        self.state = self.states.get(self.state_name)
        self.done = False
        self.quit = False  # Hinzufügen des quit-Attributs
        self.state.startup({})  # Start mit einem leeren persistenten Dictionary

    def get_event(self, event):
        if self.state:
            self.state.get_event(event)

    def update(self, dt):
        if self.state:
            self.state.update(dt)
            if self.state.done:
                self.flip_state()
            if self.state.quit:  # Überprüfen, ob der aktuelle Zustand das Beenden anfordert
                self.quit = True

    def draw(self, screen):
        self.state.draw(self.screen)

    def flip_state(self):
        if self.state:
            self.state.done = False
            previous, self.state_name = self.state_name, self.state.next_state
            persistent = self.state.cleanup()
            self.state = self.states.get(self.state_name)
            if not self.state:
                raise ValueError(f"Next state '{self.state_name}' not found in states.")
            self.state.startup(persistent)

    def resize(self, width, height):
        """Passt das Spiel und die aktuelle State an eine neue Bildschirmgröße an."""
        self.screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
        if self.state:
            self.state.resize(width, height)  # Ruf die resize Methode der aktuellen State auf
