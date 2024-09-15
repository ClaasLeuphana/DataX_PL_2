import pygame
from States.base import State


class A_Gameover(State):
    def __init__(self, assets=None):
        """
        Initialisiert den Gameover-Zustand.

        Parameter:
        - assets: Die verfügbaren Assets (optional)
        """
        super(A_Gameover, self).__init__()
        self.assets = assets
        self.font = pygame.font.Font(None, 50)
        self.round = 1
        self.options = ["New Game", "Quit Game"]  # Optionen für den Benutzer
        self.active_index = 0  # Verfolgt die ausgewählte Option
        self.screen_rect = None
        self.font_large = pygame.font.Font(None, 100)  # Große Schriftart für "Game Over"
        self.font_small = pygame.font.Font(None, 50)  # Kleinere Schriftart für Details

    def startup(self, persistent):
        """
        Bereitet den Gameover-Zustand mit den persistenten Daten vor.

        Parameter:
        - persistent: Die persistierenden Daten, die den Zustand speichern

        Dieser Methode werden die aktuellen Punktestände und Spielerinformationen zugewiesen.
        Zudem wird überprüft, ob die aktuelle Runde bereits vorhanden ist und die Punktestände
        entsprechend aktualisiert. Die Daten werden dann zurück in die persistierenden Daten gespeichert.
        """
        self.persist = persistent
        self.round_scores = self.persist.get('round_scores', [])
        self.player_count = self.persist.get('player_count', 1)
        self.total_scores = self.persist.get('total_scores', [0] * self.player_count)
        self.player_names = self.persist.get('player_names', [f"Player {i + 1}" for i in range(self.player_count)])
        self.bot_names = self.persist.get('bot_names', [])  # Bot-Namen hinzufügen
        self.winner = self.get_winner()  # Findet den Gewinner, am Anfang des States

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
        """
        Findet den Spieler mit der niedrigsten Punktzahl (Gewinner).

        Rückgabewert:
        - Der Index des Gewinners (0-basierter Index) oder None, falls kein Gewinner gefunden wurde.
        """
        if self.total_scores:
            min_score = min(self.total_scores)
            winner_index = self.total_scores.index(min_score)  # 0-basierter Index
            return winner_index
        return None

    def get_event(self, event):
        """
        Verarbeitet Eingaben wie Tastatureingaben und Mausklicks.

        Parameter:
        - event: Das Ereignis, das verarbeitet werden soll

        Diese Methode führt verschiedene Aktionen basierend auf dem Ereignistyp durch:
        - Bestätigung bei Drücken der Enter-Taste
        - Auswahl einer Option bei Mausklick
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

    def reset_scores(self):
        """
        Setzt alle Scores und Runden für ein neues Spiel zurück.

        Dies umfasst das Zurücksetzen der Rundenscores, Gesamtscores und des aktuellen Rundenscores.
        """
        self.persist['round_scores'] = []
        self.persist['total_scores'] = [0] * self.player_count
        self.persist['current_round_score'] = [0] * self.player_count
        self.round = 1

    def handle_action(self):
        """
        Führt die Aktion basierend auf der aktuell ausgewählten Option aus.

        Falls die Option "New Game" gewählt wurde, werden die Scores zurückgesetzt und der Zustand
        auf "GAMEPLAY_AUTOMATED" geändert. Bei "Quit Game" wird das Spiel beendet.
        """
        if self.active_index == 0:  # Neue Game
            self.reset_scores()  # Alle vorherigen Ergebnisse löschen
            self.next_state = "GAMEPLAY_AUTOMATED"  # Wechsle zum automatisierten Gameplay-Zustand
            self.done = True
        elif self.active_index == 1:  # Spiel Beenden
            self.quit = True

    def draw(self, screen):
        """
        Zeichnet den Gameover-Bildschirm auf die gegebene Oberfläche.

        Parameter:
        - screen: Die Pygame-Oberfläche, auf der gezeichnet wird

        Diese Methode zeichnet den Hintergrund, den Punktetabelle, den Game Over-Text und
        den Gewinner-Text sowie die auswählbaren Optionen.
        """
        # Hintergrundbild skalieren und zeichnen
        background_scaled = pygame.transform.scale(self.assets.background,
                                                   (self.screen_rect.width, self.screen_rect.height))
        screen.blit(background_scaled, (0, 0))

        # Kopfzeile der Punktetabelle zeichnen
        header_text = self.font.render("Scoreboard", True, pygame.Color("white"))
        screen.blit(header_text, (self.screen_rect.centerx - header_text.get_width() // 2, 50))

        # Positionen und Abstände für die Tabelle definieren
        x_offset = 50
        y_offset = 150
        row_height = 60
        column_width = 200

        # Tabelle Kopfzeile zeichnen
        header_text = self.font.render("Round", True, pygame.Color("white"))
        screen.blit(header_text, (x_offset, y_offset))

        # Spielernamen zeichnen
        for i in range(self.player_count):
            if i < len(self.player_names):
                player_header_text = self.font.render(self.player_names[i], True, pygame.Color("white"))
            else:
                player_header_text = self.font.render(self.bot_names[i - len(self.player_names)], True,
                                                      pygame.Color("white"))
            screen.blit(player_header_text, (x_offset + (i + 1) * column_width, y_offset))

        # Rundenscores und Gesamtpunkte zeichnen
        for j, scores in enumerate(self.round_scores):
            round_text = self.font.render(f"Round {j + 1}", True, pygame.Color("white"))
            screen.blit(round_text, (x_offset, y_offset + (j + 1) * row_height))

            for i in range(self.player_count):
                score_text = self.font.render(str(scores[i]), True, pygame.Color("white"))
                screen.blit(score_text, (x_offset + (i + 1) * column_width, y_offset + (j + 1) * row_height))

        # Gesamtpunkte in der letzten Reihe zeichnen
        total_text = self.font.render("Total", True, pygame.Color("white"))
        screen.blit(total_text, (x_offset, y_offset + (len(self.round_scores) + 1) * row_height))

        for i in range(self.player_count):
            total_score_text = self.font.render(str(self.total_scores[i]), True, pygame.Color("white"))
            screen.blit(total_score_text,
                        (x_offset + (i + 1) * column_width, y_offset + (len(self.round_scores) + 1) * row_height))

        # Game Over-Text zeichnen
        game_over_text = self.font_large.render("Game Over", True, pygame.Color("white"))
        game_over_rect = game_over_text.get_rect(center=(self.screen_rect.centerx, self.screen_rect.centery + 140))
        screen.blit(game_over_text, game_over_rect)

        # Gewinner-Text zeichnen
        if self.winner is not None:
            if self.winner < len(self.player_names):
                winner_name = self.player_names[self.winner]
            else:
                winner_name = self.bot_names[self.winner - len(self.player_names)]
            winner_text = self.font_small.render(f"{winner_name} Wins!", True, pygame.Color("green"))
        else:
            winner_text = self.font_small.render("No winner found", True, pygame.Color("red"))

        # Positioniere den Gewinner-Text unter dem Game Over-Text
        winner_rect = winner_text.get_rect(center=(self.screen_rect.centerx, self.screen_rect.centery + 220))
        screen.blit(winner_text, winner_rect)

        # Zeichne auswählbare Optionen
        for index, option in enumerate(self.options):
            text_render = self.render_text(index)
            screen.blit(text_render, self.get_text_position(text_render, index))

    def render_text(self, index):
        """
        Rendert den Text für eine gegebene Option.

        Parameter:
        - index: Der Index der Option in der Optionen-Liste

        Rückgabewert:
        - Das gerenderte Text-Image für die Option
        """
        color = pygame.Color("red") if index == self.active_index else pygame.Color("white")
        return self.font.render(self.options[index], True, color)

    def get_text_position(self, text, index):
        """
        Bestimmt die Position für eine gegebene Option auf dem Bildschirm.

        Parameter:
        - text: Das gerenderte Text-Image
        - index: Der Index der Option in der Optionen-Liste

        Rückgabewert:
        - Das Rechteck, das die Position des Textes beschreibt
        """
        if index == 0:  # "New Game" in der rechten unteren Ecke
            position = (
            self.screen_rect.width - text.get_width() - 50, self.screen_rect.height - text.get_height() - 50)
        elif index == 1:  # "Quit Game" in der linken unteren Ecke
            position = (50, self.screen_rect.height - text.get_height() - 50)
        return text.get_rect(topleft=position)

    def update(self, dt):
        """
        Aktualisiert den aktiven Index basierend auf der Mausposition.

        Parameter:
        - dt: Die Zeitdifferenz seit dem letzten Update
        """
        mouse_pos = pygame.mouse.get_pos()
        for index, option in enumerate(self.options):
            text_render = self.render_text(index)
            text_rect = self.get_text_position(text_render, index)
            if text_rect.collidepoint(mouse_pos):
                self.active_index = index

    def cleanup(self):
        """
        Führt die Bereinigung durch und gibt die persistierenden Daten zurück.

        Rückgabewert:
        - Die persistierenden Daten
        """
        return self.persist

    def resize(self, width, height):
        """
        Ändert die Größe des Bildschirms und aktualisiert die Textpositionen.

        Parameter:
        - width: Die neue Breite des Bildschirms
        - height: Die neue Höhe des Bildschirms
        """
        self.screen_rect = pygame.Rect(0, 0, width, height)
        self.update_text_positions()

    def update_text_positions(self):
        """
        Aktualisiert die Positionen der Textoptionen basierend auf der aktuellen Bildschirmgröße.
        """
        self.text_positions = []
        for index in range(len(self.options)):
            text_render = self.render_text(index)
            text_rect = self.get_text_position(text_render, index)
            self.text_positions.append(text_rect)
