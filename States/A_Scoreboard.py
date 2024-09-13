import pygame
from States.base import State


class A_Scoreboard(State):
    def __init__(self, assets=None):
        super(A_Scoreboard, self).__init__()
        self.assets = assets
        self.font = pygame.font.Font(None, 50)
        self.round = 1
        self.options = ["New Round", "Quit Game"]  # Optionen für den Benutzer
        self.active_index = 0  # Verfolgt die ausgewählte Option
        self.screen_rect = None

    def startup(self, persistent):
        self.persist = persistent
        self.round_scores = self.persist.get('round_scores', [])
        self.player_count = self.persist.get('player_count', 1)
        self.total_scores = self.persist.get('total_scores', [0] * self.player_count)

        # Stelle sicher, dass der eingegebene Name korrekt geladen wird
        self.player_names = self.persist.get('player_names', [f"Player {i + 1}" for i in range(self.player_count)])

        self.bot_names = self.persist.get('bot_names', [])
        # Initialisiere screen_rect basierend auf der Bildschirmgröße
        screen = pygame.display.get_surface()  # Hole die aktuelle Anzeigefläche
        self.screen_rect = screen.get_rect()  # Setze screen_rect auf das Rechteck der Oberfläche

        # Füge die aktuellen Rundenscores zur Liste der Rundenscores hinzu
        self.current_round_score = self.persist.get('current_round_score', [0] * self.player_count)

        # 1. Ermittlung des Spielers, der als Erster die letzte Karte umgedreht hat
        first_to_finish = self.persist.get('first_to_finish', None)

        if first_to_finish is not None:
            # 2. Überprüfe, ob der Spieler nicht die niedrigste Punktzahl in der Runde hat
            min_score = min(self.current_round_score)
            if self.current_round_score[first_to_finish - 1] != min_score:
                # 3. Verdopple die Punkte des Spielers, wenn er nicht die niedrigste Punktzahl hat
                self.current_round_score[first_to_finish - 1] *= 2


        # Aktualisiere die total_scores basierend auf den aktuellen Rundenscores
        self.round_scores.append(self.current_round_score)
        for i in range(self.player_count):
            self.total_scores[i] += self.current_round_score[i]

        # Speichere die aktualisierten Scores zurück in persistent
        self.persist['round_scores'] = self.round_scores
        self.persist['total_scores'] = self.total_scores

        # Überprüfe, ob das Spiel vorbei ist
        self.check_game_over()

    def check_game_over(self):
        """Überprüft, ob einer der Spieler 100 oder mehr Punkte hat."""
        for score in self.total_scores:
            if score >= 100:
                self.next_state = "A_GAMEOVER"  # Wechsle zum Game Over State
                self.done = True
                break  # Beende die Überprüfung, sobald ein Spieler 100 erreicht

    def get_event(self, event):
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
        if self.active_index == 0:  # Neue Runde
            self.persist['current_round_score'] = [0] * self.player_count  # Setze die Rundenscores zurück
            self.next_state = "GAMEPLAY_AUTOMATED"
            self.done = True
        elif self.active_index == 1:  # Spiel Beenden
            self.quit = True

    def draw(self, screen):
        """Zeichnet das Scoreboard und die Optionen."""

        # Hintergrund von Hintergrundbild von GameAssets
        background_scaled = pygame.transform.scale(self.assets.background, (self.screen_rect.width, self.screen_rect.height))
        screen.blit(background_scaled, (0, 0))

        # Zeichne die Überschrift Scoreboard
        header_text = self.font.render("Scoreboard", True, pygame.Color("white"))
        screen.blit(header_text, (self.screen_rect.centerx - header_text.get_width() // 2, 50))

        # Definiere die Positionen und Abstände für die Tabelle
        x_offset = 50
        y_offset = 150
        row_height = 60
        column_width = 200

        # Zeichne die Tabellenüberschrift
        header_text = self.font.render("Round", True, pygame.Color("white"))
        screen.blit(header_text, (x_offset, y_offset))

        for i in range(self.player_count):
            if i == 0:
                # Zeige den eingegebenen Namen des Spielers anstelle von "Player 1"
                player_header_text = self.font.render(self.player_names[i], True, pygame.Color("white"))
            else:
                player_header_text = self.font.render(self.bot_names[i - 1], True, pygame.Color("white"))
            screen.blit(player_header_text, (x_offset + (i + 1) * column_width, y_offset))

        # Zeichne die Rundenscores und Gesamtpunkte
        for j, scores in enumerate(self.round_scores):
            round_text = self.font.render(f"Round {j + 1}", True, pygame.Color("white"))
            screen.blit(round_text, (x_offset, y_offset + (j + 1) * row_height))

            for i in range(self.player_count):
                score_text = self.font.render(str(scores[i]), True, pygame.Color("white"))
                screen.blit(score_text, (x_offset + (i + 1) * column_width, y_offset + (j + 1) * row_height))

        # Zeichne die Gesamtsumme in der letzten Zeile
        total_text = self.font.render("Total", True, pygame.Color("white"))
        screen.blit(total_text, (x_offset, y_offset + (len(self.round_scores) + 1) * row_height))

        for i in range(self.player_count):
            total_score_text = self.font.render(str(self.total_scores[i]), True, pygame.Color("white"))
            screen.blit(total_score_text, (x_offset + (i + 1) * column_width, y_offset + (len(self.round_scores) + 1) * row_height))

        # Zeichne klickbare Optionen
        for index, option in enumerate(self.options):
            text_render = self.render_text(index)
            screen.blit(text_render, self.get_text_position(text_render, index))

    def render_text(self, index):
        color = pygame.Color("red") if index == self.active_index else pygame.Color("white")
        return self.font.render(self.options[index], True, color)

    def get_text_position(self, text, index):
        # Positioniere die Optionen auf dem Bildschirm
        if index == 0:  # "Neue Runde" in der rechten unteren Ecke
            position = (self.screen_rect.width - text.get_width() - 50, self.screen_rect.height - text.get_height() - 50)
        elif index == 1:  # "Spiel Beenden" in der linken unteren Ecke
            position = (50, self.screen_rect.height - text.get_height() - 50)
        return text.get_rect(topleft=position)

    def update(self, dt):
        # Aktualisiere den aktiven Index basierend auf Maus-Hover
        mouse_pos = pygame.mouse.get_pos()
        for index, option in enumerate(self.options):
            text_render = self.render_text(index)
            text_rect = self.get_text_position(text_render, index)
            if text_rect.collidepoint(mouse_pos):
                self.active_index = index

        # Überprüfe erneut, ob das Spiel vorbei ist
        self.check_game_over()

    def cleanup(self):
        # Speichere die Namen aller Spieler und Bots
        self.persist['player_names'] = self.player_names
        self.persist['player_count'] = self.player_count
        self.persist['total_scores'] = self.total_scores
        return super(A_Scoreboard, self).cleanup()

    def resize(self, width, height):
        self.screen_rect = pygame.Rect(0, 0, width, height)
        self.update_text_positions()

    def update_text_positions(self):
        self.text_positions = []
        for index in range(len(self.options)):
            text_render = self.render_text(index)
            text_rect = self.get_text_position(text_render, index)
            self.text_positions.append(text_rect)
