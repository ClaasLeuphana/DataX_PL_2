import pygame
from .base import State

class Menu(State):
    def __init__(self, assets=None):
        super(Menu, self).__init__()
        self.assets = assets
        self.options = ["Start Game", "Rules", "Options", "Quit Game"]  # Neuer Button für "Rules"
        self.next_state = "PLAYER_SELECT"  # Dies wird durch handle_action angepasst
        self.active_index = 0
        self.font = pygame.font.Font(None, 50)
        self.screen_rect = pygame.display.get_surface().get_rect()
        self.update_text_positions()  # Initial Positionen setzen

    def render_text(self, index):
        color = pygame.Color("red") if index == self.active_index else pygame.Color("white")
        return self.font.render(self.options[index], True, color)

    def get_text_position(self, text, index):
        # Berechnet die Position der Textelemente basierend auf der aktuellen Bildschirmgröße
        center = (self.screen_rect.center[0], self.screen_rect.center[1] + (index - len(self.options) / 2) * 50)
        return text.get_rect(center=center)

    def handle_action(self):
        if self.active_index == 0:  # Start Game
            self.next_state = "PLAYER_SELECT"
            self.done = True
        elif self.active_index == 1:  # Rules
            self.next_state = "RULES"
            self.done = True
        elif self.active_index == 2:  # Options
            self.next_state = "OPTIONS"
            self.done = True
        elif self.active_index == 3:  # Quit Game
            self.quit = True

    def get_event(self, event):
        if event.type == pygame.QUIT:
            self.quit = True
        elif event.type == pygame.MOUSEBUTTONUP:
            mouse_pos = pygame.mouse.get_pos()
            for index, option in enumerate(self.options):
                text_render = self.render_text(index)
                text_rect = self.get_text_position(text_render, index)
                if text_rect.collidepoint(mouse_pos):
                    self.active_index = index
                    self.handle_action()
                    break

    def draw(self, surface):
        surface.fill(pygame.Color("blue"))
        for index, option in enumerate(self.options):
            text_render = self.render_text(index)
            surface.blit(text_render, self.get_text_position(text_render, index))

    def update(self, dt):
        mouse_pos = pygame.mouse.get_pos()
        for index, option in enumerate(self.options):
            text_render = self.render_text(index)
            text_rect = self.get_text_position(text_render, index)
            if text_rect.collidepoint(mouse_pos):
                self.active_index = index

    def resize(self, width, height):
        """Passt das Menü an eine neue Bildschirmgröße an."""
        self.screen_rect = pygame.Rect(0, 0, width, height)  # Update the screen_rect with the new dimensions
        self.update_text_positions()  # Update text positions based on new screen size

    def update_text_positions(self):
        """Aktualisiert die Textpositionen für die Menüoptionen basierend auf der aktuellen Bildschirmgröße."""
        self.text_positions = []
        for index in range(len(self.options)):
            text_render = self.render_text(index)
            text_rect = self.get_text_position(text_render, index)
            self.text_positions.append(text_rect)

    def cleanup(self):
        # Bereinigen vor dem Zustandswechsel
        return {}
