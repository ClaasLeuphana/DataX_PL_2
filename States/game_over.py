import pygame
from States.base import State

class GameOver(State):
    def __init__(self, assets=None):
        super(GameOver, self).__init__()
        self.assets = assets
        self.font = pygame.font.Font(None, 50)
        self.round = 1
        self.options = ["New Game", "Quit Game"]  # Optionen für den Benutzer
        self.active_index = 0  # Verfolgt die ausgewählte Option
        self.screen_rect = None
        self.font_large = pygame.font.Font(None, 100)  # Große Schriftart für "Game Over"
        self.font_small = pygame.font.Font(None, 50)  # Kleinere Schriftart für Details

    def startup(self, persistent):
        self.persist = persistent
        self.round_scores = self.persist.get('round_scores', [])
        self.player_count = self.persist.get('player_count', 1)
        self.total_scores = self.persist.get('total_scores', [0] * self.player_count)
        self.player_names = self.persist.get('player_names', [f"Player {i + 1}" for i in range(self.player_count)])
        self.winner = self.get_winner()  # Bestimme den Gewinner, wenn der Zustand startet

        # Initialisiere screen_rect basierend auf der Bildschirmgröße
        screen = pygame.display.get_surface()  # Hole die aktuelle Anzeigefläche
        self.screen_rect = screen.get_rect()  # Setze screen_rect auf das Rechteck der Oberfläche

        # Überprüfe, ob die aktuelle Runde bereits in den Rundenscores enthalten ist
        self.current_round_score = self.persist.get('current_round_score', [0] * self.player_count)
        if self.current_round_score not in self.round_scores:
            self.round_scores.append(self.current_round_score)
            for i in range(self.player_count):
                self.total_scores[i] += self.current_round_score[i]

        # Speichere die aktualisierten Scores zurück in persistent
        self.persist['round_scores'] = self.round_scores
        self.persist['total_scores'] = self.total_scores

    def get_winner(self):
        """Findet den Spieler mit der niedrigsten Punktzahl (Gewinner)."""
        if self.total_scores:
            min_score = min(self.total_scores)
            winner_index = self.total_scores.index(min_score)  # Hole den Index der niedrigsten Punktzahl
            return winner_index  # Rückgabe des Spielerindex (0-basierter Index)
        return None

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

    def reset_scores(self):
        """Setzt alle Punktzahlen und Runden für ein neues Spiel zurück."""
        self.persist['round_scores'] = []
        self.persist['total_scores'] = [0] * self.player_count
        self.persist['current_round_score'] = [0] * self.player_count
        self.round = 1

    def handle_action(self):
        if self.active_index == 0:  # Neues Spiel
            self.reset_scores()  # Alle vorherigen Ergebnisse löschen
            self.next_state = "PLAYER_SELECT"
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
            player_header_text = self.font.render(self.player_names[i], True, pygame.Color("white"))
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

        # Zeichne den Game Over Text
        game_over_text = self.font_large.render("Game Over", True, pygame.Color("white"))
        game_over_rect = game_over_text.get_rect(center=(self.screen_rect.centerx, self.screen_rect.centery + 140))
        screen.blit(game_over_text, game_over_rect)

        # Zeichne den Gewinner-Text
        if self.winner is not None and 0 <= self.winner < len(self.player_names):
            winner_name = self.player_names[self.winner]
            winner_text = self.font_small.render(f"{winner_name} Wins!", True, pygame.Color("green"))
        else:
            winner_text = self.font_small.render("No winner found", True, pygame.Color("red"))

        # Positioniere den Gewinner-Text unter dem Game Over Text
        winner_rect = winner_text.get_rect(center=(self.screen_rect.centerx, self.screen_rect.centery + 220))
        screen.blit(winner_text, winner_rect)

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

    def cleanup(self):
        return self.persist

    def resize(self, width, height):
        self.screen_rect = pygame.Rect(0, 0, width, height)
        self.update_text_positions()

    def update_text_positions(self):
        self.text_positions = []
        for index in range(len(self.options)):
            text_render = self.render_text(index)
            text_rect = self.get_text_position(text_render, index)
            self.text_positions.append(text_rect)