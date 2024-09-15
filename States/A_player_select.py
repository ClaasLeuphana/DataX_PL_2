from States.base import State
from GameAssets import *
import pygame  # Stelle sicher, dass pygame importiert wird

class A_PlayerSelect(State):
    def __init__(self, assets=None):
        """
        Initialisiert den Zustand für die Spieler-Auswahl.

        Parameter:
        - assets: Die verfügbaren Assets (optional)

        Eigenschaften:
        - assets: Die zugewiesenen Assets
        - player_count: Anzahl der Spieler (1 = aktiver Spieler)
        - max_players: Maximale Anzahl der Spieler (inkl. automatisierter Gegner)
        - min_players_required: Mindestanzahl von Spielern
        - warn_message: Nachricht bei unzureichender Spieleranzahl
        - active_player_index: Index des aktiven Spielers (0 = Mensch)
        - selected_players: Liste, die angibt, welche Spieler ausgewählt sind
        - bot_difficulties: Liste der Schwierigkeitsgrade für die Bots
        - bot_names: Namen der Bots
        - next_state: Der nächste Zustand nach Abschluss
        - font: Schriftart für die Anzeige von Text
        - button_font: Schriftart für die Buttons
        - screen_rect: Rechteck, das die Bildschirmgröße repräsentiert
        - icon_size: Größe der Icons
        - icon_positions: Positionen der Icons auf dem Bildschirm
        - confirm_text: Text für den Bestätigungs-Button
        - confirm_rect: Rechteck für den Bestätigungs-Button
        - back_text: Text für den Zurück-Button
        - back_rect: Rechteck für den Zurück-Button
        - input_active: Gibt an, ob das Eingabefeld aktiv ist
        - player_name: Name des menschlichen Spielers
        - input_box: Rechteck für das Eingabefeld
        """
        super(A_PlayerSelect, self).__init__()
        self.assets = assets
        self.player_count = 1
        self.max_players = 4
        self.min_players_required = 2
        self.warn_message = None
        self.active_player_index = 0
        self.selected_players = [True, False, False, False]
        self.bot_difficulties = ["Medium"] * 4
        self.bot_names = self.generate_random_bot_names()
        self.next_state = "GAMEPLAY_AUTOMATED"
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
        self.input_active = False
        self.player_name = "Player 1"
        self.input_box = pygame.Rect(self.icon_positions[0][0], self.icon_positions[0][1] + 140, 140, 50)
        self.resize(self.screen_rect.width, self.screen_rect.height)

    def resize(self, width, height):
        """
        Passt die GUI-Elemente an die neue Fenstergröße an.

        Parameter:
        - width: Neue Breite des Fensters
        - height: Neue Höhe des Fensters

        Diese Methode aktualisiert die Bildschirmgröße und die Positionen der Icons.
        """
        self.screen_rect = pygame.Rect(0, 0, width, height)
        self.icon_positions = self.calculate_icon_positions()

    def calculate_icon_positions(self):
        """
        Berechnet die Positionen der Icons relativ zur Bildschirmgröße.

        Rückgabewert:
        - Eine Liste von Tupeln, die die Positionen der Icons enthalten.
        """
        screen_width, screen_height = self.screen_rect.width, self.screen_rect.height
        player_x = screen_width * 0.25
        player_y = screen_height * 0.25
        bot1_x = screen_width * 0.55
        bot1_y = screen_height * 0.25
        bot2_x = screen_width * 0.25
        bot2_y = screen_height * 0.55
        bot3_x = screen_width * 0.55
        bot3_y = screen_height * 0.55

        return [
            (player_x, player_y),
            (bot1_x, bot1_y),
            (bot2_x, bot2_y),
            (bot3_x, bot3_y)
        ]

    def generate_random_bot_names(self):
        """
        Generiert zufällige Namen für die KI-Gegner.

        Rückgabewert:
        - Eine Liste von drei zufällig ausgewählten Namen für die Bots.
        """
        names = ["Ava", "Mia", "Zoe", "Lily", "Emma", "Nora", "Ella", "Ruby", "Isla", "Lena",
                 "Grace", "Lucy", "Alice", "Chloe", "Daisy", "Hazel", "Julia", "Leah", "Maria", "Sarah",
                 "Naomi", "Sophie", "Stella", "Eliza", "Hannah", "Leo", "Max", "Eli", "Ben", "Sam",
                 "Jack", "Luke", "Noah", "Alex", "Ryan", "Jake", "Owen", "Henry", "Liam", "Adam",
                 "James", "Daniel", "Thomas", "Ethan", "Mason", "Caleb", "Joseph", "Oliver", "David", "Charles"]
        random.shuffle(names)
        return names[:3]

    def get_event(self, event):
        """
        Verarbeitet Eingaben wie Maus- und Tastaturereignisse.

        Parameter:
        - event: Das Ereignis, das verarbeitet werden soll

        Diese Methode führt verschiedene Aktionen basierend auf dem Ereignistyp durch:
        - Beenden des Spiels, wenn das Fenster geschlossen wird
        - Bestätigung oder Rückkehr zum Hauptmenü bei Button-Klicks
        - Bearbeitung der Namens- und Schwierigkeitsänderungen
        """
        if event.type == pygame.QUIT:
            self.quit = True

        elif event.type == pygame.MOUSEBUTTONUP:
            mouse_pos = pygame.mouse.get_pos()

            # Bestätigung
            if self.confirm_rect.collidepoint(mouse_pos):
                active_players = sum(self.selected_players)
                if active_players >= self.min_players_required:
                    self.player_count = active_players
                    self.done = True
                else:
                    self.warn_message = "Bitte wähle mindestens 2 Spieler aus"

            # Zurück zum Hauptmenü
            elif self.back_rect.collidepoint(mouse_pos):
                self.next_state = "GAMEMODE"
                self.done = True

            # Überprüfung des Eingabefelds
            if self.input_box.collidepoint(mouse_pos):
                self.input_active = True
            else:
                self.input_active = False

            # Überprüfen der Spieler- und Bot-Icons
            for i, (x, y) in enumerate(self.icon_positions):
                icon_rect = pygame.Rect(x, y, self.icon_size, self.icon_size)
                if icon_rect.collidepoint(mouse_pos):
                    if i > 0:
                        self.selected_players[i] = not self.selected_players[i]
                        self.player_count = sum(self.selected_players)

            # Überprüfen der Plus- und Minus-Buttons für die Bot-Schwierigkeit
            for i in range(1, 4):
                plus_rect = pygame.Rect(self.icon_positions[i][0] + 150, self.icon_positions[i][1] + 170, 30, 30)
                minus_rect = pygame.Rect(self.icon_positions[i][0] - 70, self.icon_positions[i][1] + 170, 30, 30)

                if plus_rect.collidepoint(mouse_pos):
                    self.change_bot_difficulty(i, 1)
                elif minus_rect.collidepoint(mouse_pos):
                    self.change_bot_difficulty(i, -1)

        # Eingaben für den Spielernamen
        if event.type == pygame.KEYDOWN and self.input_active:
            if event.key == pygame.K_BACKSPACE:
                self.player_name = self.player_name[:-1]
            else:
                if self.player_name == "Player 1":
                    self.player_name = ""
                self.player_name += event.unicode

    def change_bot_difficulty(self, index, direction):
        """
        Ändert die Schwierigkeitsstufe eines Bots.

        Parameter:
        - index: Der Index des Bots in der Liste der Bots
        - direction: Die Richtung, in die die Schwierigkeit geändert werden soll (1 für Erhöhung, -1 für Verringerung)

        Diese Methode passt die Schwierigkeit des Bots an, indem sie zwischen den Schwierigkeitsgraden "Easy", "Medium" und "Hard" wechselt.
        """
        difficulties = ["Easy", "Medium", "Hard"]
        current_index = difficulties.index(self.bot_difficulties[index])
        new_index = (current_index + direction) % 3
        self.bot_difficulties[index] = difficulties[new_index]

    def draw(self, surface):
        """
        Zeichnet das Spieler-Auswahl-Menü auf die gegebene Oberfläche.

        Parameter:
        - surface: Die Pygame-Oberfläche, auf der gezeichnet wird

        Diese Methode zeichnet Hintergrund, Icons, Namen, Schwierigkeitsgrade, Buttons und das Eingabefeld.
        """
        scaled_background = pygame.transform.scale(self.assets.background, (self.screen_rect.width, self.screen_rect.height))
        surface.blit(scaled_background, (0, 0))

        for i, (x, y) in enumerate(self.icon_positions):
            icon_rect = pygame.Rect(x, y, self.icon_size, self.icon_size)
            if i == 0:
                icon_image = self.assets.Player
            else:
                icon_image = self.assets.bot_icons[i - 1]
            surface.blit(icon_image, icon_rect)

            if self.selected_players[i]:
                pygame.draw.rect(surface, pygame.Color("green"), icon_rect, 5)

            if i == 0:
                name_text = self.font.render(self.player_name, True, pygame.Color("white"))
                surface.blit(name_text, (x, y + 100))
            else:
                name_text = self.font.render(self.bot_names[i - 1], True, pygame.Color("white"))
                surface.blit(name_text, (x, y + 110))

            if i > 0:
                difficulty_text = self.font.render(self.bot_difficulties[i], True, pygame.Color("white"))
                surface.blit(difficulty_text, (x, y + 170))

                plus_text = self.font.render("+", True, pygame.Color("white"))
                minus_text = self.font.render("-", True, pygame.Color("white"))
                surface.blit(plus_text, (x + 150, y + 170))
                surface.blit(minus_text, (x - 70, y + 170))

        if self.input_active:
            color = pygame.Color("yellow")
        else:
            color = pygame.Color("white")

        pygame.draw.rect(surface, color, self.input_box, 2)

        name_text = self.font.render(self.player_name, True, color)
        surface.blit(name_text, (self.input_box.x + 10, self.input_box.y + 10))

        surface.blit(self.confirm_text, self.confirm_rect)
        surface.blit(self.back_text, self.back_rect)

        if self.warn_message:
            warn_text = self.font.render(self.warn_message, True, pygame.Color("red"))
            surface.blit(warn_text, (self.screen_rect.centerx - warn_text.get_width() // 2, self.screen_rect.centery))

    def cleanup(self):
        """
        Speichert die aktuellen Einstellungen und Daten des Zustands.

        Rückgabewert:
        - Die aktualisierten persistierenden Daten
        """
        self.persist['player_count'] = self.player_count
        self.persist['active_player_index'] = self.active_player_index
        self.persist['selected_players'] = self.selected_players
        self.persist['bot_difficulties'] = self.bot_difficulties
        self.persist['player_name'] = self.player_name
        self.persist['bot_names'] = self.bot_names
        return super(A_PlayerSelect, self).cleanup()
