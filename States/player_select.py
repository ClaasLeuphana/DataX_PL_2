from States.base import State
import pygame

class PlayerSelect(State):

    def __init__(self, assets=None):
        """
        Initialisiert den PlayerSelect-Zustand zur Auswahl von Spielern und deren Namen.

        Input:
        - assets: Ein Objekt, das die benötigten Grafiken und Sounds bereitstellt (optional).

        """
        super(PlayerSelect, self).__init__()
        self.assets = assets
        self.player_count = 4
        self.selected_players = [True] * 4
        self.player_names = ["Player 1", "Player 2", "Player 3", "Player 4"]

        self.min_players_required = 2
        self.warn_message = None

        self.next_state = "GAMEPLAY"
        self.font = pygame.font.Font(None, 50)
        self.button_font = pygame.font.Font(None, 40)

        self.screen_rect = pygame.display.get_surface().get_rect()

        self.icon_size = 100
        self.icon_positions = self.calculate_icon_positions()

        self.confirm_text = self.font.render("Confirm", True, pygame.Color("yellow"))
        self.confirm_rect = self.confirm_text.get_rect(
            bottomright=(self.screen_rect.width - 20, self.screen_rect.height - 20))
        self.back_text = self.font.render("Back", True, pygame.Color("white"))
        self.back_rect = self.back_text.get_rect(bottomleft=(20, self.screen_rect.height - 20))

        self.input_active = [False] * 4
        self.input_boxes = [pygame.Rect(self.icon_positions[i][0], self.icon_positions[i][1] + 140, 140, 50) for i in range(4)]

        self.resize(self.screen_rect.width, self.screen_rect.height)

    def resize(self, width, height):
        """
        Passt die GUI-Elemente an die neue Fenstergröße an.

        Input:
        - width: Die neue Breite des Bildschirms.
        - height: Die neue Höhe des Bildschirms.

        """
        self.screen_rect = pygame.Rect(0, 0, width, height)
        self.icon_positions = self.calculate_icon_positions()

    def calculate_icon_positions(self):
        """
        Berechnet die Positionen der Spieler-Icons relativ zur Bildschirmgröße.

        Output:
        - Eine Liste von Tuplen, die die Positionen der Icons enthalten.
        """
        screen_width, screen_height = self.screen_rect.width, self.screen_rect.height

        positions = [
            (screen_width * 0.25, screen_height * 0.25),
            (screen_width * 0.55, screen_height * 0.25),
            (screen_width * 0.25, screen_height * 0.55),
            (screen_width * 0.55, screen_height * 0.55)
        ]
        return positions

    def get_event(self, event):
        """
        Verarbeitet Eingabeereignisse wie Mausklicks und Tasteneingaben.

        Input:
        - event: Das Pygame-Ereignis, das verarbeitet werden soll.

        """
        if event.type == pygame.QUIT:
            self.quit = True

        elif event.type == pygame.MOUSEBUTTONUP:
            mouse_pos = pygame.mouse.get_pos()

            if self.confirm_rect.collidepoint(mouse_pos):
                active_players = sum(self.selected_players)
                if active_players >= self.min_players_required:
                    self.player_count = active_players
                    self.done = True
                else:
                    self.warn_message = "Bitte wähle mindestens 2 Spieler aus"

            elif self.back_rect.collidepoint(mouse_pos):
                self.next_state = "GAMEMODE"
                self.done = True

            for i, (x, y) in enumerate(self.icon_positions):
                icon_rect = pygame.Rect(x, y, self.icon_size, self.icon_size)
                if icon_rect.collidepoint(mouse_pos):
                    self.selected_players[i] = not self.selected_players[i]

            for i in range(4):
                if self.input_boxes[i].collidepoint(mouse_pos):
                    self.input_active = [False] * 4
                    self.input_active[i] = True
                else:
                    self.input_active[i] = False

        if event.type == pygame.KEYDOWN:
            for i in range(4):
                if self.input_active[i]:
                    if event.key == pygame.K_BACKSPACE:
                        if self.player_names[i]:
                            self.player_names[i] = self.player_names[i][:-1]
                    else:
                        if self.player_names[i] == "Player {0}".format(i + 1):
                            self.player_names[i] = ""
                        self.player_names[i] += event.unicode

    def draw(self, surface):
        """
        Zeichnet die GUI-Elemente, Spieler-Icons und Namenseingabefelder auf der angegebenen Oberfläche.

        Input:
        - surface: Die Oberfläche, auf der die GUI-Elemente gezeichnet werden sollen.

        """
        scaled_background = pygame.transform.scale(self.assets.background, (self.screen_rect.width, self.screen_rect.height))
        surface.blit(scaled_background, (0, 0))

        for i, (x, y) in enumerate(self.icon_positions):
            icon_rect = pygame.Rect(x, y, self.icon_size, self.icon_size)
            icon_image = self.assets.Player
            surface.blit(icon_image, icon_rect)

            if self.selected_players[i]:
                pygame.draw.rect(surface, pygame.Color("green"), icon_rect, 5)

            if i < len(self.player_names):
                name_text = self.font.render(self.player_names[i], True, pygame.Color("white"))
                surface.blit(name_text, (x, y + 100))

        for i in range(4):
            color = pygame.Color("yellow") if self.input_active[i] else pygame.Color("white")
            pygame.draw.rect(surface, color, self.input_boxes[i], 2)

            if i < len(self.player_names):
                name_text = self.font.render(self.player_names[i], True, color)
                surface.blit(name_text, (self.input_boxes[i].x + 10, self.input_boxes[i].y + 10))

        surface.blit(self.confirm_text, self.confirm_rect)
        surface.blit(self.back_text, self.back_rect)

        if self.warn_message:
            warn_text = self.font.render(self.warn_message, True, pygame.Color("red"))
            surface.blit(warn_text, (self.screen_rect.centerx - warn_text.get_width() // 2, self.screen_rect.centery))

    def cleanup(self):
        """
        Bereitet die persistierenden Daten für den nächsten Zustand vor und filtert die aktiven Spieler.

        Output:
        - Das persistierende Daten-Dictionary.
        """
        active_players = [self.player_names[i] for i in range(4) if self.selected_players[i]]

        self.persist['player_count'] = len(active_players)
        self.persist['player_names'] = active_players
        print(f"Debug: Spieleranzahl = {len(active_players)}")
        print(f"Debug: Spieler-Namen = {active_players}")
        return super(PlayerSelect, self).cleanup()
