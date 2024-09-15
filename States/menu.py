import pygame
from States.base import State


class Menu(State):
    def __init__(self, assets=None):
        """
        Initialisiert das Menü mit den verfügbaren Optionen und dem aktuellen Status.

        Input:
        - assets: Ein Objekt, das die benötigten Grafiken und Sounds bereitstellt (optional).

        """
        super(Menu, self).__init__()
        self.assets = assets
        self.options = ["Start Game", "Rules", "Options", "Quit Game"]
        self.next_state = "PLAYER_SELECT"  # Dieser Wert wird durch handle_action angepasst
        self.active_index = 0
        self.font = pygame.font.Font(None, 50)
        self.screen_rect = pygame.display.get_surface().get_rect()
        self.update_text_positions()  # Initiale Positionen der Texte setzen

    def render_text(self, index):
        """
        Rendert den Text für eine bestimmte Menüoption und färbt ihn abhängig von der aktiven Auswahl.

        Input:
        - index: Der Index der Menüoption.

        Output:
        - text_surface: Die gerenderte Text-Oberfläche.
        """
        color = pygame.Color("red") if index == self.active_index else pygame.Color("white")
        return self.font.render(self.options[index], True, color)

    def get_text_position(self, text, index):
        """
        Berechnet die Position der Textelemente basierend auf der aktuellen Bildschirmgröße.

        Input:
        - text: Die gerenderte Text-Oberfläche.
        - index: Der Index der Menüoption.

        Output:
        - text_rect: Das Rechteck, das die Position des Textes beschreibt.
        """
        center = (self.screen_rect.center[0], self.screen_rect.center[1] + (index - len(self.options) / 2) * 50)
        return text.get_rect(center=center)

    def handle_action(self):
        """
        Verarbeitet die Aktion basierend auf der aktuell ausgewählten Menüoption.

        """
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
        """
        Verarbeitet Eingabeereignisse wie Mausklicks und beendet das Spiel bei einem Quit-Event.

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

    def draw(self, surface):
        """
        Zeichnet das Menü auf der angegebenen Oberfläche.

        Input:
        - surface: Die Oberfläche, auf der das Menü gezeichnet werden soll.

        """
        scaled_background = pygame.transform.scale(self.assets.background,
                                                   (self.screen_rect.width, self.screen_rect.height))
        surface.blit(scaled_background, (0, 0))  # Hintergrund zeichnen

        for index, option in enumerate(self.options):
            text_render = self.render_text(index)
            surface.blit(text_render, self.get_text_position(text_render, index))

    def update(self, dt):
        """
        Aktualisiert die aktive Menüoption basierend auf der aktuellen Mausposition.

        Input:
        - dt: Die verstrichene Zeit seit dem letzten Update (Delta Time).

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
        self.screen_rect = pygame.Rect(0, 0, width, height)  # Bildschirmgröße aktualisieren
        self.update_text_positions()  # Textpositionen basierend auf neuer Bildschirmgröße aktualisieren

    def update_text_positions(self):
        """
        Aktualisiert die Positionen der Textelemente für die Menüoptionen basierend auf der aktuellen Bildschirmgröße.

        """
        self.text_positions = []
        for index in range(len(self.options)):
            text_render = self.render_text(index)
            text_rect = self.get_text_position(text_render, index)
            self.text_positions.append(text_rect)

    def cleanup(self):
        """
        Bereinigt Ressourcen und speichert keine Daten vor dem Zustandswechsel.

        Output:
        - persistente Daten für den nächsten Zustand (hier: leerer Dictionary).
        """
        return {}
