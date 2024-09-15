import pygame
from States.base import State

class Scoreboard(State):
    def __init__(self, assets=None):
        """
        Initialisiert das Scoreboard für die Anzeige von Spielergebnissen und Optionen.

        Input:
        - assets: Ein Objekt, das die benötigten Grafiken und Sounds bereitstellt (optional).

        """
        super(Scoreboard, self).__init__()
        self.assets = assets
        self.font = pygame.font.Font(None, 50)
        self.round = 1
        self.options = ["New Round", "Quit Game"]
        self.active_index = 0
        self.screen_rect = None

    def startup(self, persistent):
        """
        Initialisiert den Scoreboard-Zustand basierend auf den persistierenden Daten.

        Input:
        - persistent: Ein Dictionary, das die aktuellen Statusinformationen des Spiels enthält.

        """
        self.persist = persistent
        self.round_scores = self.persist.get('round_scores', [])
        self.player_count = self.persist.get('player_count', 1)
        self.total_scores = self.persist.get('total_scores', [0] * self.player_count)
        self.player_names = self.persist.get('player_names', [f"Player {i + 1}" for i in range(self.player_count)])

        screen = pygame.display.get_surface()
        self.screen_rect = screen.get_rect()

        self.current_round_score = self.persist.get('current_round_score', [0] * self.player_count)
        first_to_finish = self.persist.get('first_to_finish', None)

        if first_to_finish is not None:
            min_score = min(self.current_round_score)
            if self.current_round_score[first_to_finish - 1] != min_score:
                self.current_round_score[first_to_finish - 1] *= 2

        self.round_scores.append(self.current_round_score)
        for i in range(self.player_count):
            self.total_scores[i] += self.current_round_score[i]

        self.persist['round_scores'] = self.round_scores
        self.persist['total_scores'] = self.total_scores

        self.check_game_over()

    def check_game_over(self):
        """
        Überprüft, ob ein Spieler 100 oder mehr Punkte erreicht hat und wechselt gegebenenfalls in den Game Over-Zustand.

        """
        for score in self.total_scores:
            if score >= 100:
                self.next_state = "GAMEOVER"
                self.done = True
                break

    def get_event(self, event):
        """
        Verarbeitet Eingabeereignisse wie Tastendruck und Mausklicks.

        Input:
        - event: Das Pygame-Ereignis, das verarbeitet werden soll.

        """
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                self.handle_action()
        elif event.type == pygame.MOUSEBUTTONUP:
            mouse_pos = pygame.mouse.get_pos()
            for index, option in enumerate(self.options):
                text_render = self.render_text(index)
                text_rect = self.get_text_position(text_render, index)
                if text_rect.collidepoint(mouse_pos):
                    self.active_index = index
                    self.handle_action()

    def handle_action(self):
        """
        Führt eine Aktion basierend auf der aktuell ausgewählten Option aus.

        """
        if self.active_index == 0:  # Neue Runde
            self.persist['current_round_score'] = [0] * self.player_count
            self.next_state = "GAMEPLAY"
            self.done = True
        elif self.active_index == 1:  # Spiel Beenden
            self.quit = True

    def draw(self, screen):
        """
        Zeichnet das Scoreboard und die Optionen auf der angegebenen Oberfläche.

        Input:
        - screen: Die Oberfläche, auf der das Scoreboard gezeichnet werden soll.

        """
        background_scaled = pygame.transform.scale(self.assets.background, (self.screen_rect.width, self.screen_rect.height))
        screen.blit(background_scaled, (0, 0))

        header_text = self.font.render("Scoreboard", True, pygame.Color("white"))
        screen.blit(header_text, (self.screen_rect.centerx - header_text.get_width() // 2, 50))

        x_offset = 50
        y_offset = 150
        row_height = 60
        column_width = 200

        header_text = self.font.render("Round", True, pygame.Color("white"))
        screen.blit(header_text, (x_offset, y_offset))

        for i in range(self.player_count):
            player_header_text = self.font.render(self.player_names[i], True, pygame.Color("white"))
            screen.blit(player_header_text, (x_offset + (i + 1) * column_width, y_offset))

        for j, scores in enumerate(self.round_scores):
            round_text = self.font.render(f"Round {j + 1}", True, pygame.Color("white"))
            screen.blit(round_text, (x_offset, y_offset + (j + 1) * row_height))

            for i in range(self.player_count):
                score_text = self.font.render(str(scores[i]), True, pygame.Color("white"))
                screen.blit(score_text, (x_offset + (i + 1) * column_width, y_offset + (j + 1) * row_height))

        total_text = self.font.render("Total", True, pygame.Color("white"))
        screen.blit(total_text, (x_offset, y_offset + (len(self.round_scores) + 1) * row_height))

        for i in range(self.player_count):
            total_score_text = self.font.render(str(self.total_scores[i]), True, pygame.Color("white"))
            screen.blit(total_score_text, (x_offset + (i + 1) * column_width, y_offset + (len(self.round_scores) + 1) * row_height))

        for index, option in enumerate(self.options):
            text_render = self.render_text(index)
            screen.blit(text_render, self.get_text_position(text_render, index))

    def render_text(self, index):
        """
        Rendert den Text für eine bestimmte Option und färbt den Text abhängig davon, ob die Option aktiv ist oder nicht.

        Input:
        - index: Der Index der Option, die gerendert werden soll.

        Output:
        - Der gerenderte Text als Pygame-Text-Objekt.
        """
        color = pygame.Color("red") if index == self.active_index else pygame.Color("white")
        return self.font.render(self.options[index], True, color)

    def get_text_position(self, text, index):
        """
        Bestimmt die Position auf dem Bildschirm, an der der Text für eine Option angezeigt werden soll.

        Input:
        - text: Der gerenderte Text als Pygame-Text-Objekt.
        - index: Der Index der Option, deren Position bestimmt werden soll.

        Output:
        - Das Pygame-Rechteck, das die Position des Textes definiert.
        """
        if index == 0:  # "New Round" in der rechten unteren Ecke
            position = (self.screen_rect.width - text.get_width() - 50, self.screen_rect.height - text.get_height() - 50)
        elif index == 1:  # "Quit Game" in der linken unteren Ecke
            position = (50, self.screen_rect.height - text.get_height() - 50)
        return text.get_rect(topleft=position)

    def update(self, dt):
        """
        Aktualisiert den aktiven Index basierend auf der Mausposition und überprüft, ob das Spiel vorbei ist.

        Input:
        - dt: Die verstrichene Zeit seit dem letzten Update (kann zur Animation verwendet werden).

        """
        mouse_pos = pygame.mouse.get_pos()
        for index, option in enumerate(self.options):
            text_render = self.render_text(index)
            text_rect = self.get_text_position(text_render, index)
            if text_rect.collidepoint(mouse_pos):
                self.active_index = index

        self.check_game_over()

    def cleanup(self):
        """
        Gibt die aktuellen persistierenden Daten vor dem Wechsel des Zustands zurück.

        Output:
        - Das persistierende Daten-Dictionary.
        """
        return self.persist

    def resize(self, width, height):
        """
        Passt die Bildschirmgröße an und aktualisiert die Positionen der Text-Optionen.

        Input:
        - width: Die neue Breite des Bildschirms.
        - height: Die neue Höhe des Bildschirms.

        """
        self.screen_rect = pygame.Rect(0, 0, width, height)
        self.update_text_positions()

    def update_text_positions(self):
        """
        Aktualisiert die Positionen der Text-Optionen basierend auf der aktuellen Bildschirmgröße.

        """
        self.text_positions = []
        for index in range(len(self.options)):
            text_render = self.render_text(index)
            text_rect = self.get_text_position(text_render, index)
            self.text_positions.append(text_rect)
