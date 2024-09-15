import pygame
from States.base import State

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

        # Skyjo-Icon laden und skalieren (z.B. auf 20% der Bildschirmbreite und Höhe)
        skyjo_icon_original = self.assets.Skyjo  # Vergewissere dich, dass assets.Skyjo korrekt geladen ist
        self.skyjo_icon = pygame.transform.scale(
            skyjo_icon_original,
            (self.screen_rect.width // 5, self.screen_rect.height // 5))  # Verkleinere das Icon


    def render_text(self, index):
        color = pygame.Color("red") if index == self.active_index else pygame.Color("white")
        return self.font.render(self.options[index], True, color)

    def get_text_position(self, text, index):
        # Berechnet die Position der Textelemente basierend auf der aktuellen Bildschirmgröße
        center = (self.screen_rect.center[0], self.screen_rect.center[1] + (index - len(self.options) / 2) * 50)
        return text.get_rect(center=center)

    def handle_action(self):
        if self.active_index == 0:  # Start Game
            self.next_state = "GAMEMODE"
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
        # Skaliere das Hintergrundbild
        scaled_background = pygame.transform.scale(self.assets.background, (self.screen_rect.width, self.screen_rect.height))
        surface.blit(scaled_background, (0, 0))  # Zeichne den skalierten Hintergrund
        # Zeichne das Skyjo-Bild über den Texten, z.B. zentriert oben im Menü
        skyjo_position = (
        self.screen_rect.centerx - self.skyjo_icon.get_width() // 2, 50)  # Platziere das Icon oben in der Mitte
        surface.blit(self.skyjo_icon, skyjo_position)

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
