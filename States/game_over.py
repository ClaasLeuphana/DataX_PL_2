import pygame
from States.base import State

class GameOver(State):
    def __init__(self, assets=None):
        """
        Initialisiert den GameOver-Zustand.

        Parameter:
        - assets: Die verfügbaren Assets, wie z.B. Hintergrundbilder

        Eigenschaften:
        - font: Schriftart für die Menüoptionen
        - round: Runde des Spiels
        - options: Optionen für das Menü
        - active_index: Index der aktuell ausgewählten Option
        - screen_rect: Rechteck, das die Bildschirmgröße beschreibt
        - font_large: Große Schriftart für "Game Over"
        - font_small: Kleinere Schriftart für Details
        """
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
        """
        Initialisiert den GameOver-Zustand mit persistenten Daten.

        Parameter:
        - persistent: Ein Dictionary, das persistente Daten wie Scores enthält

        Aktionen:
        - Lädt die gespeicherten Runden-Scores, Spieleranzahl, Gesamt-Scores und Spielernamen
        - Bestimmt den Gewinner
        - Initialisiert screen_rect basierend auf der Bildschirmgröße
        - Fügt die aktuelle Runde zu den Rundenscores hinzu, falls noch nicht vorhanden
        - Speichert die aktualisierten Scores zurück in persistent
        """
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
        """
        Bestimmt den Spieler mit der niedrigsten Punktzahl (Gewinner).

        Rückgabewert:
        - Der Index des Gewinners (0-basierter Index) oder None, falls kein Gewinner bestimmt werden konnte
        """
        if self.total_scores:
            min_score = min(self.total_scores)
            winner_index = self.total_scores.index(min_score)  # Hole den Index der niedrigsten Punktzahl
            return winner_index  # Rückgabe des Spielerindex (0-basierter Index)
        return None

    def get_event(self, event):
        """
        Verarbeitet Ereignisse wie Tasteneingaben und Mausklicks.

        Parameter:
        - event: Das Ereignis, das verarbeitet werden soll

        Aktionen:
        - Handhabt Tasteneingaben (Enter-Taste) und Mausklicks auf Menüoptionen
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
        Setzt alle Punktzahlen und Runden für ein neues Spiel zurück.

        Aktionen:
        - Leert die Rundenscores
        - Setzt die Gesamt-Scores und die Punktzahlen der aktuellen Runde zurück
        - Setzt die Runde auf 1
        """
        self.persist['round_scores'] = []
        self.persist['total_scores'] = [0] * self.player_count
        self.persist['current_round_score'] = [0] * self.player_count
        self.round = 1

    def handle_action(self):
        """
        Handhabt die Aktion basierend auf der aktuell ausgewählten Menüoption.

        Aktionen:
        - Setzt beim Auswahlindex 0 die Scores zurück und wechselt zum "PLAYER_SELECT"-Zustand
        - Beendet das Spiel beim Auswahlindex 1
        """
        if self.active_index == 0:  # Neues Spiel
            self.reset_scores()  # Alle vorherigen Ergebnisse löschen
            self.next_state = "PLAYER_SELECT"
            self.done = True
        elif self.active_index == 1:  # Spiel Beenden
            self.quit = True

    def draw(self, screen):
        """
        Zeichnet das Scoreboard und die Optionen auf dem Bildschirm.

        Parameter:
        - screen: Die Pygame-Oberfläche, auf der gezeichnet wird

        Aktionen:
        - Zeichnet den Hintergrund
        - Zeichnet die Überschrift "Scoreboard"
        - Zeichnet die Rundenscores und Gesamtpunkte
        - Zeichnet den "Game Over"-Text und den Gewinner-Text
        - Zeichnet klickbare Menüoptionen
        """
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
        """
        Rendert den Text für eine Menüoption.

        Parameter:
        - index: Der Index der Option, die gerendert werden soll

        Rückgabewert:
        - Das gerenderte Text-Image
        """
        color = pygame.Color("red") if index == self.active_index else pygame.Color("white")
        return self.font.render(self.options[index], True, color)

    def get_text_position(self, text, index):
        """
        Berechnet die Position der Textelemente basierend auf der aktuellen Bildschirmgröße.

        Parameter:
        - text: Das gerenderte Text-Image
        - index: Der Index der Option

        Rückgabewert:
        - Das Rechteck, das die Position des Textes beschreibt
        """
        if index == 0:  # "New Game" in der rechten unteren Ecke
            position = (self.screen_rect.width - text.get_width() - 50, self.screen_rect.height - text.get_height() - 50)
        elif index == 1:  # "Quit Game" in der linken unteren Ecke
            position = (50, self.screen_rect.height - text.get_height() - 50)
        return text.get_rect(topleft=position)

    def update(self, dt):
        """
        Aktualisiert den Zustand basierend auf der Mausposition.

        Parameter:
        - dt: Delta-Zeit seit dem letzten Update

        Aktionen:
        - Setzt active_index auf den Index der Menüoption, über der sich die Maus befindet
        """
        mouse_pos = pygame.mouse.get_pos()
        for index, option in enumerate(self.options):
            text_render = self.render_text(index)
            text_rect = self.get_text_position(text_render, index)
            if text_rect.collidepoint(mouse_pos):
                self.active_index = index

    def cleanup(self):
        """
        Bereinigt Ressourcen und Daten vor einem Zustandswechsel.

        Rückgabewert:
        - Ein Dictionary, das die persistenten Daten enthält
        """
        return self.persist

    def resize(self, width, height):
        """
        Passt den Bildschirm an eine neue Größe an.

        Parameter:
        - width: Neue Breite des Bildschirms
        - height: Neue Höhe des Bildschirms

        Aktionen:
        - Aktualisiert screen_rect basierend auf der neuen Bildschirmgröße
        - Aktualisiert die Positionen der Textelemente
        """
        self.screen_rect = pygame.Rect(0, 0, width, height)
        self.update_text_positions()

    def update_text_positions(self):
        """
        Aktualisiert die Positionen der Menüoptionen basierend auf der aktuellen Bildschirmgröße.

        Aktionen:
        - Berechnet die Positionen der Text-Elemente und speichert sie in text_positions
        """
        self.text_positions = []
        for index in range(len(self.options)):
            text_render = self.render_text(index)
            text_rect = self.get_text_position(text_render, index)
            self.text_positions.append(text_rect)
