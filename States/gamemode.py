import pygame
from States.base import State

class Gamemode(State):
    def __init__(self, assets=None):
        super(Gamemode, self).__init__()
        self.assets = assets
        self.options = ["Host", "Join", "Local", "Quit Game"]  # Optionen im Menü
        self.next_state = "PLAYER_SELECT"  # Wird durch handle_action angepasst
        self.active_index = 0
        self.font = pygame.font.Font(None, 50)
        self.button_font = pygame.font.Font(None, 40)  # Schriftart für den Button

        # Initialisiere screen_rect zuerst
        self.screen_rect = pygame.display.get_surface().get_rect()

        # Erstellen des "Back"-Buttons
        self.button_text = self.button_font.render("Main Menu", True, pygame.Color("white"))
        self.button_rect = self.button_text.get_rect(topleft=(10, self.screen_rect.height - self.button_text.get_height() - 30))

        # Initiale Positionen der Textelemente setzen
        self.update_text_positions()


    def render_text(self, index):
        color = pygame.Color("red") if index == self.active_index else pygame.Color("white")
        return self.font.render(self.options[index], True, color)

    def get_text_position(self, text, index):
        # Berechnet die Position der Textelemente basierend auf der aktuellen Bildschirmgröße
        center = (self.screen_rect.center[0], self.screen_rect.center[1] + (index - len(self.options) / 2) * 50)
        return text.get_rect(center=center)

    def handle_action(self):
        if self.active_index == 0:  # Start Game
            self.next_state = "HOST_LOBBY"
            self.done = True
        elif self.active_index == 1:  # Join Game
            self.next_state = "CLIENT_LOBBY"
            self.done = True
        elif self.active_index == 2:  # Local Game
            self.next_state = "LOCAL"
            self.done = True
        elif self.active_index == 3:  # Quit Game
            self.quit = True

    def get_event(self, event):
        if event.type == pygame.QUIT:
            self.quit = True
        elif event.type == pygame.MOUSEBUTTONUP:
            mouse_pos = pygame.mouse.get_pos()
            # Überprüfe, ob eine Menüoption geklickt wurde
            for index, option in enumerate(self.options):
                text_render = self.render_text(index)
                text_rect = self.get_text_position(text_render, index)
                if text_rect.collidepoint(mouse_pos):
                    self.active_index = index
                    self.handle_action()
                    break
            # Überprüfe, ob der "Back"-Button geklickt wurde
            if self.button_rect.collidepoint(mouse_pos):
                self.next_state = "MENU"
                self.done = True

    def draw(self, surface):
        # Skaliere das Hintergrundbild
        scaled_background = pygame.transform.scale(self.assets.background, (self.screen_rect.width, self.screen_rect.height))
        surface.blit(scaled_background, (0, 0))  # Zeichne den skalierten Hintergrund

        # Zeichne die Menüoptionen
        for index, option in enumerate(self.options):
            text_render = self.render_text(index)
            surface.blit(text_render, self.get_text_position(text_render, index))
        # Zeichne den "Back"-Button
        surface.blit(self.button_text, self.button_rect.topleft)

    def update(self, dt):
        mouse_pos = pygame.mouse.get_pos()
        for index, option in enumerate(self.options):
            text_render = self.render_text(index)
            text_rect = self.get_text_position(text_render, index)
            if text_rect.collidepoint(mouse_pos):
                self.active_index = index

    def resize(self, width, height):
        """Passt das Menü an eine neue Bildschirmgröße an."""
        self.screen_rect = pygame.Rect(0, 0, width, height)
        self.update_text_positions()

        # Aktualisiere die Position des "Back"-Buttons
        self.button_rect.topleft = (10, self.screen_rect.height - self.button_text.get_height() - 30)

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
