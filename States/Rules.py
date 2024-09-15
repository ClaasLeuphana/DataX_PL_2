import pygame
from States.base import State


class Rules(State):
    def __init__(self, assets=None):
        """
        Initialisiert die Regeln-Seite des Spiels, einschließlich des anzuzeigenden Textes und eines Menütaste.

        Input:
        - assets: Ein Objekt, das die benötigten Grafiken und Sounds bereitstellt (optional).

        Output:
        - Keine.
        """
        super(Rules, self).__init__()
        self.assets = assets
        self.font = pygame.font.Font(None, 30)
        self.button_font = pygame.font.Font(None, 40)
        self.screen_rect = pygame.display.get_surface().get_rect()
        self.text = (
            "Ziel des Spiels: Das Ziel ist es, am Ende des Spiels die wenigsten Punkte zu haben. "
            "Das Spiel wird über mehrere Runden gespielt, bis ein Spieler 100 oder mehr Punkte erreicht hat. "
            "Der Spieler mit den wenigsten Punkten gewinnt.\n\n"
            "Spielvorbereitung: Jeder Spieler erhält 12 Karten, die verdeckt vor ihm ausgelegt werden. "
            "Zwei Karten werden offen hingelegt, der Rest bleibt verdeckt. Der Spieler mit der höchsten Punktzahl der offenen Karten beginnt.\n\n"
            "Spielablauf:\n"
            "1. Der aktive Spieler hat die Wahl, eine der folgenden Aktionen durchzuführen:\n"
            "   - Eine offene Karte vom Ablagestapel ziehen und diese mit einer offenen oder verdeckten Karte auf seinem Tisch tauschen.\n"
            "   - Eine verdeckte Karte vom Nachziehstapel ziehen und diese mit einer offenen oder verdeckten Karte auf seinem Tisch tauschen.\n"
            "   - Keine Karte ziehen und stattdessen eine seiner verdeckten Karten aufdecken.\n"
            "2. Wenn ein Spieler drei Karten mit demselben Wert in einer Spalte hat, werden diese Karten entfernt. Dies gilt auch für Minuspunkt-Karten.\n\n"
            "Rundenende:\n"
            "Eine Runde endet, wenn ein Spieler seine letzte Karte aufdeckt und behauptet, in dieser Runde die wenigsten Punkte zu haben.\n"
            "Wenn dies nicht zutrifft, werden seine Punkte der Runde verdoppelt.\n"
            "Nachdem der Spieler seine letzte Karte aufgedeckt hat, haben die anderen Spieler jeweils noch einen Zug.\n"
            "Danach werden alle restlichen Karten aufgedeckt und die Punkte gezählt.\n\n"
            "Viel Spaß beim Spielen!"
        )

        self.scroll_offset = 0
        self.scroll_speed = 5
        self.rendered_text = []
        self.text_rect = None
        self.button_rect = None
        self.update_text()
        self.next_state = "MENU"

    def update_text(self):
        """
        Berechnet die Textgröße und erstellt die Render-Objekte für den Text und den Button.

        Input:
        - Keine.

        Output:
        - Keine.
        """
        lines = self.text.split('\n')
        self.rendered_text = [self.font.render(line, True, pygame.Color("white")) for line in lines]

        total_height = sum(line.get_height() for line in self.rendered_text)
        self.text_rect = pygame.Rect(0, 0, self.screen_rect.width, total_height)

        button_text = self.button_font.render("Main Menu", True, pygame.Color("white"))
        self.button_rect = button_text.get_rect(topleft=(10, self.screen_rect.height - button_text.get_height() - 20))
        self.button_text = button_text

        self.text_top_margin = 50
        self.max_scroll = max(0, self.text_rect.height - self.screen_rect.height + self.text_top_margin)

    def get_event(self, event):
        """
        Verarbeitet Eingabeereignisse wie Mausklicks und Tastatureingaben.

        Input:
        - event: Das Pygame-Ereignis, das verarbeitet werden soll.

        Output:
        - Keine.
        """
        if event.type == pygame.QUIT:
            self.quit = True
        elif event.type == pygame.KEYDOWN:
            self.next_state = "MENU"
            self.done = True
        elif event.type == pygame.MOUSEBUTTONUP:
            mouse_pos = pygame.mouse.get_pos()
            if self.button_rect.collidepoint(mouse_pos):
                self.done = True

    def draw(self, surface):
        """
        Zeichnet die Regeln-Seite auf der angegebenen Oberfläche.

        Input:
        - surface: Die Oberfläche, auf der die Regeln gezeichnet werden sollen.

        Output:
        - Keine.
        """
        surface.fill(pygame.Color("black"))

        y_offset = self.scroll_offset + self.text_top_margin
        for line in self.rendered_text:
            surface.blit(line, (self.screen_rect.left + 10, y_offset))
            y_offset += line.get_height()

        surface.blit(self.button_text, self.button_rect.topleft)

    def update(self, dt):
        """
        Aktualisiert die Scrollposition des Textes basierend auf der Tastatureingabe.

        Input:
        - dt: Die verstrichene Zeit seit dem letzten Update (kann zur Animation verwendet werden).

        Output:
        - Keine.
        """
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            self.scroll_offset = max(self.scroll_offset - self.scroll_speed, 0)
        if keys[pygame.K_DOWN]:
            self.scroll_offset = min(self.scroll_offset + self.scroll_speed, self.max_scroll)

    def resize(self, width, height):
        """
        Passt die Regeln-Seite an eine neue Bildschirmgröße an.

        Input:
        - width: Die neue Breite des Bildschirms.
        - height: Die neue Höhe des Bildschirms.

        Output:
        - Keine.
        """
        self.screen_rect = pygame.Rect(0, 0, width, height)
        self.update_text()

    def cleanup(self):
        """
        Bereinigt vor dem Wechsel des Zustands.

        Input:
        - Keine.

        Output:
        - Ein leeres Dictionary, um Zustandsinformationen beizubehalten (falls erforderlich).
        """
        return {}
