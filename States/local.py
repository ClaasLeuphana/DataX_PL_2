import pygame
from States.base import State

class Local(State):
    def __init__(self, assets=None):
        """
        Initialisiert den Local-Zustand für die Auswahl des Spielmodus.

        Input:
        - assets: Ein Objekt, das die benötigten Grafiken und Sounds bereitstellt (optional).

        """
        super(Local, self).__init__()
        self.assets = assets
        self.options = ["Multi-player", "Single-player", "Quit Game"]
        self.next_state = "PLAYER_SELECT"
        self.active_index = 0
        self.font = pygame.font.Font(None, 50)
        self.button_font = pygame.font.Font(None, 40)

        self.screen_rect = pygame.display.get_surface().get_rect()

        self.button_text = self.button_font.render("Main Menu", True, pygame.Color("white"))
        self.button_rect = self.button_text.get_rect(topleft=(10, self.screen_rect.height - self.button_text.get_height() - 30))

        self.update_text_positions()

    def render_text(self, index):
        """
        Rendert den Text für eine Menüoption mit einer Farbe, die basierend auf dem aktiven Index variiert.

        Input:
        - index: Der Index der Menüoption.

        Output:
        - Ein gerendertes Text-Objekt für die Menüoption.
        """
        color = pygame.Color("red") if index == self.active_index else pygame.Color("white")
        return self.font.render(self.options[index], True, color)

    def get_text_position(self, text, index):
        """
        Berechnet die Position des Textes basierend auf dem aktuellen Bildschirmmittelpunkt.

        Input:
        - text: Das gerenderte Text-Objekt.
        - index: Der Index der Menüoption.

        Output:
        - Ein pygame.Rect-Objekt, das die Position des Textes beschreibt.
        """
        center = (self.screen_rect.center[0], self.screen_rect.center[1] + (index - len(self.options) / 2) * 50)
        return text.get_rect(center=center)

    def handle_action(self):
        """
        Handhabt die Auswahl der Menüoption basierend auf dem aktiven Index.

        """
        if self.active_index == 0:  # Multi-player
            self.next_state = "PLAYER_SELECT"
            self.done = True
        elif self.active_index == 1:  # Single-player
            self.next_state = "A_PLAYER_SELECT"
            self.done = True
        elif self.active_index == 2:  # Quit Game
            self.quit = True

    def get_event(self, event):
        """
        Verarbeitet Ereignisse wie Mausklicks.

        Input:
        - event: Das Pygame-Ereignis, das verarbeitet werden soll.

        """
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
            if self.button_rect.collidepoint(mouse_pos):
                self.next_state = "MENU"
                self.done = True

    def draw(self, surface):
        """
        Zeichnet alle GUI-Elemente auf der angegebenen Oberfläche.

        Input:
        - surface: Die Oberfläche, auf der die GUI-Elemente gezeichnet werden sollen.

        """
        scaled_background = pygame.transform.scale(self.assets.background, (self.screen_rect.width, self.screen_rect.height))
        surface.blit(scaled_background, (0, 0))

        for index, option in enumerate(self.options):
            text_render = self.render_text(index)
            surface.blit(text_render, self.get_text_position(text_render, index))
        surface.blit(self.button_text, self.button_rect.topleft)

    def update(self, dt):
        """
        Aktualisiert den Zustand basierend auf der Mausposition.

        Input:
        - dt: Die Zeitdifferenz seit dem letzten Update.

        """
        mouse_pos = pygame.mouse.get_pos()
        for index, option in enumerate(self.options):
            text_render = self.render_text(index)
            text_rect = self.get_text_position(text_render, index)
            if text_rect.collidepoint(mouse_pos):
                self.active_index = index

    def resize(self, width, height):
        """
        Passt das Menü an eine neue Bildschirmgröße an.

        Input:
        - width: Die neue Breite des Bildschirms.
        - height: Die neue Höhe des Bildschirms.

        """
        self.screen_rect = pygame.Rect(0, 0, width, height)
        self.update_text_positions()
        self.button_rect.topleft = (10, self.screen_rect.height - self.button_text.get_height() - 30)

    def update_text_positions(self):
        """
        Aktualisiert die Positionen der Textobjekte für die Menüoptionen basierend auf der aktuellen Bildschirmgröße.

        """
        self.text_positions = []
        for index in range(len(self.options)):
            text_render = self.render_text(index)
            text_rect = self.get_text_position(text_render, index)
            self.text_positions.append(text_rect)

    def cleanup(self):
        """
        Bereinigt vor dem Zustandswechsel.

        Output:
        - Ein leeres Dictionary.
        """
        return {}
