import pygame
from .base import State

class Rules(State):
    def __init__(self, assets=None):
        super(Rules, self).__init__()
        self.assets = assets
        self.font = pygame.font.Font(None, 30)
        self.button_font = pygame.font.Font(None, 40)  # Schriftart für den Button
        self.screen_rect = pygame.display.get_surface().get_rect()
        self.text = (
            "1. Ziel des Spiels\n"
            "Das Ziel des Spiels ist es, alle deine Karten aufzudecken und die meisten Punkte zu sammeln.\n\n"
            "2. Spielvorbereitung\n"
            "Zu Beginn des Spiels wird ein Stapel aus Karten erstellt und gemischt. Jeder Spieler erhält eine Handvoll Karten.\n\n"
            "3. Spielablauf\n"
            "In jedem Zug kann der Spieler eine Karte von seinem Stapel aufdecken oder eine Karte vom Deck ziehen.\n\n"
            "4. Karten tauschen\n"
            "Wenn ein Spieler eine Karte von seinem Stapel aufgedeckt hat, kann er diese mit einer Karte vom Deck tauschen.\n\n"
            "5. Spielende\n"
            "Das Spiel endet, wenn alle Karten aufgedeckt sind oder wenn ein Spieler alle seine Karten gesammelt hat.\n\n"
            "6. Gewinnbedingungen\n"
            "Der Spieler mit den meisten Punkten am Ende des Spiels gewinnt.\n\n"
            "Drücke eine beliebige Taste, um zurück zum Hauptmenü zu gelangen."
        )
        self.scroll_offset = 0
        self.scroll_speed = 5  # Geschwindigkeit des Scrollens
        self.rendered_text = []
        self.text_rect = None
        self.button_rect = None
        self.update_text()
        self.next_state = "MENU"

    def update_text(self):
        """Berechnet die Textgröße und erstellt das Text-Render-Objekt."""
        # Erstellen des Text-Render-Objekts
        lines = self.text.split('\n')
        self.rendered_text = [self.font.render(line, True, pygame.Color("white")) for line in lines]

        # Berechnen der Höhe des gesamten Textes
        total_height = sum(line.get_height() for line in self.rendered_text)
        self.text_rect = pygame.Rect(0, 0, self.screen_rect.width, total_height)

        # Erstellen des "Main Menu"-Buttons
        button_text = self.button_font.render("Main Menu", True, pygame.Color("white"))
        self.button_rect = button_text.get_rect(topleft=(10, self.screen_rect.height - button_text.get_height() - 30))
        self.button_text = button_text

    def get_event(self, event):
        if event.type == pygame.QUIT:
            self.quit = True
        elif event.type == pygame.KEYDOWN:
            # Zurück zum Hauptmenü bei Tastendruck
            self.next_state = "MENU"
            self.done = True
        elif event.type == pygame.MOUSEBUTTONUP:
            mouse_pos = pygame.mouse.get_pos()
            if self.button_rect.collidepoint(mouse_pos):
                self.done = True

    def draw(self, surface):
        surface.fill(pygame.Color("blue"))

        y_offset = self.scroll_offset
        for line in self.rendered_text:
            surface.blit(line, (self.screen_rect.centerx - line.get_width() / 2, y_offset))
            y_offset += line.get_height()

        # Zeichne den Button
        surface.blit(self.button_text, self.button_rect.topleft)

    def update(self, dt):
        """Aktualisiert die Scrollposition des Textes."""
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            self.scroll_offset = max(self.scroll_offset - self.scroll_speed, 0)
        if keys[pygame.K_DOWN]:
            # Beschränken Sie das Scrollen auf den Bereich des Textes, der über den Bildschirm hinausgeht
            self.scroll_offset = min(self.scroll_offset + self.scroll_speed, max(0, self.text_rect.height - self.screen_rect.height))

    def resize(self, width, height):
        """Passt den Textbereich und den Button an eine neue Bildschirmgröße an."""
        self.screen_rect = pygame.Rect(0, 0, width, height)
        self.update_text()  # Aktualisiere den Text und Button-Positionen bei Größenänderung

    def cleanup(self):
        # Bereinigen vor dem Zustandswechsel
        return {}
