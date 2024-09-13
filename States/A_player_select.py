from States.base import State
from GameAssets import *
import pygame  # Make sure to import pygame
class A_PlayerSelect(State):
    def __init__(self, assets=None):
        super(A_PlayerSelect, self).__init__()
        self.assets = assets
        self.player_count = 1  # Anzahl der Spieler (1 = aktiver Spieler)
        self.max_players = 4  # Maximal 4 Spieler (inkl. automatisierter Gegner)
        self.active_player_index = 0  # Index des aktiven Spielers (0 = Mensch)
        self.selected_players = [True, False, False, False]  # Mensch ist aktiv, Rest sind Gegner
        self.bot_difficulties = ["Medium"] * 4  # Startschwierigkeit für die Bots (1 Mensch + 3 Bots)
        self.bot_names = self.generate_random_bot_names()
        self.next_state = "GAMEPLAY_AUTOMATED"
        self.font = pygame.font.Font(None, 50)
        self.button_font = pygame.font.Font(None, 40)

        # Initialisiere screen_rect und lade Hintergrund
        self.screen_rect = pygame.display.get_surface().get_rect()


        # Initialisiere die Positionen für die Icons und Buttons
        self.icon_size = 100  # Größe der Icons
        self.icon_positions = self.calculate_icon_positions()

        # Bestätigungs- und Zurück-Buttons
        self.confirm_text = self.font.render("Confirm", True, pygame.Color("yellow"))
        self.confirm_rect = self.confirm_text.get_rect(
            bottomright=(self.screen_rect.width - 20, self.screen_rect.height - 20))
        self.back_text = self.font.render("Back", True, pygame.Color("white"))
        self.back_rect = self.back_text.get_rect(bottomleft=(20, self.screen_rect.height - 20))

        # Texteingabefeld für den menschlichen Spieler
        self.input_active = False
        self.player_name = "Player 1"
        self.input_box = pygame.Rect(self.icon_positions[0][0], self.icon_positions[0][1] + 140, 140, 50)

        # Initiale Größe anpassen
        self.resize(self.screen_rect.width, self.screen_rect.height)

    def resize(self, width, height):
        """Passt die GUI-Elemente an die neue Fenstergröße an."""
        self.screen_rect = pygame.Rect(0, 0, width, height)
        self.icon_positions = self.calculate_icon_positions()

    def calculate_icon_positions(self):
        """Berechnet die Positionen relativ zur Bildschirmgröße."""
        screen_width, screen_height = self.screen_rect.width, self.screen_rect.height

        # Berechne die Positionen als Prozentsatz der Bildschirmgröße
        player_x = screen_width * 0.25
        player_y = screen_height * 0.25
        bot1_x = screen_width * 0.55
        bot1_y = screen_height * 0.25
        bot2_x = screen_width * 0.25
        bot2_y = screen_height * 0.55
        bot3_x = screen_width * 0.55
        bot3_y = screen_height * 0.55

        return [
            (player_x, player_y),  # Player
            (bot1_x, bot1_y),  # Bot 1
            (bot2_x, bot2_y),  # Bot 2
            (bot3_x, bot3_y)  # Bot 3
        ]

    def generate_random_bot_names(self):
        """Generiert zufällige Namen für die KI-Gegner."""
        names = ["Ava", "Mia", "Zoe", "Lily", "Emma", "Nora", "Ella", "Ruby", "Isla", "Lena",
                 "Grace", "Lucy", "Alice", "Chloe", "Daisy", "Hazel", "Julia", "Leah", "Maria", "Sarah",
                 "Naomi", "Sophie", "Stella", "Eliza", "Hannah", "Leo", "Max", "Eli", "Ben", "Sam",
                 "Jack", "Luke", "Noah", "Alex", "Ryan", "Jake", "Owen", "Henry", "Liam", "Adam",
                 "James", "Daniel", "Thomas", "Ethan", "Mason", "Caleb", "Joseph", "Oliver", "David", "Charles"]
        random.shuffle(names)
        return names[:3]

    def get_event(self, event):
        if event.type == pygame.QUIT:
            self.quit = True

        elif event.type == pygame.MOUSEBUTTONUP:
            mouse_pos = pygame.mouse.get_pos()

            # Bestätigung
            if self.confirm_rect.collidepoint(mouse_pos):
                self.done = True

            # Zurück zum Hauptmenü
            elif self.back_rect.collidepoint(mouse_pos):
                self.next_state = "GAMEMODE"
                self.done = True

            # Überprüfe, ob auf das Namenseingabefeld geklickt wurde
            if self.input_box.collidepoint(mouse_pos):
                self.input_active = True
            else:
                self.input_active = False

            # Überprüfe, ob auf den Player oder Bot geklickt wurde
            for i, (x, y) in enumerate(self.icon_positions):
                icon_rect = pygame.Rect(x, y, self.icon_size, self.icon_size)
                if icon_rect.collidepoint(mouse_pos):
                    if i > 0:
                        self.selected_players[i] = not self.selected_players[i]  # Wechsel zwischen ausgewählt und nicht
                        self.player_count = sum(self.selected_players)

            # Überprüfe Plus- und Minus-Buttons für die Bot-Schwierigkeit
            for i in range(1, 4):  # Nur für die Bots
                plus_rect = pygame.Rect(self.icon_positions[i][0] + 150, self.icon_positions[i][1] + 170, 30, 30)
                minus_rect = pygame.Rect(self.icon_positions[i][0] - 70, self.icon_positions[i][1] + 170, 30, 30)

                if plus_rect.collidepoint(mouse_pos):
                    self.change_bot_difficulty(i, 1)
                elif minus_rect.collidepoint(mouse_pos):
                    self.change_bot_difficulty(i, -1)

        # Nameingabe für den Player
        if event.type == pygame.KEYDOWN and self.input_active:
            if event.key == pygame.K_BACKSPACE:
                self.player_name = self.player_name[:-1]  # Entfernt das letzte Zeichen
            else:
                if self.player_name == "Player 1":  # Lösche den Standardtext bei erster Eingabe
                    self.player_name = ""
                self.player_name += event.unicode  # Fügt das eingegebene Zeichen hinzu

    def change_bot_difficulty(self, index, direction):
        """Ändert die Schwierigkeitsstufe des Bots durch Plus und Minus Buttons."""
        difficulties = ["Easy", "Medium", "Hard"]
        current_index = difficulties.index(self.bot_difficulties[index])
        new_index = (current_index + direction) % 3
        self.bot_difficulties[index] = difficulties[new_index]

    def draw(self, surface):
        # Skaliere das Hintergrundbild, damit es weniger herangezoomt ist
        scaled_background = pygame.transform.scale(self.assets.background, (self.screen_rect.width, self.screen_rect.height))
        surface.blit(scaled_background, (0, 0))  # Zeichne den skalierten Hintergrund

        # Zeichne Icons und Namen
        for i, (x, y) in enumerate(self.icon_positions):
            # Icon für Spieler oder Bot
            icon_rect = pygame.Rect(x, y, self.icon_size, self.icon_size)
            if i == 0:
                icon_image = self.assets.Player
            else:
                icon_image = self.assets.bot_icons[i - 1]  # Lade spezifisches Bot-Icon
            surface.blit(icon_image, icon_rect)

            # Hervorhebung der ausgewählten Bots
            if self.selected_players[i]:
                pygame.draw.rect(surface, pygame.Color("green"), icon_rect, 5)  # Hervorheben

            # Name des Spielers/Bots
            if i == 0:
                name_text = self.font.render(self.player_name, True, pygame.Color("white"))
                surface.blit(name_text, (x, y + 100))  # Name des Spielers (weiter oben: +100 statt +110)
            else:
                name_text = self.font.render(self.bot_names[i - 1], True, pygame.Color("white"))
                surface.blit(name_text, (x, y + 110))  # Name der Bots

            # Schwierigkeitsstufe für Bots
            if i > 0:
                difficulty_text = self.font.render(self.bot_difficulties[i], True, pygame.Color("white"))
                surface.blit(difficulty_text, (x, y + 170))  # Schwierigkeitsstufe weiter unten

                # Zeichne Plus- und Minus-Buttons für die Schwierigkeit
                plus_text = self.font.render("+", True, pygame.Color("white"))
                minus_text = self.font.render("-", True, pygame.Color("white"))
                surface.blit(plus_text, (x + 150, y + 170))  # Plus-Button weiter rechts (+150 statt +120)
                surface.blit(minus_text, (x - 70, y + 170))  # Minus-Button weiter links (-70 statt -40)

        # Zeichne das Namenseingabefeld für den Spieler
        if self.input_active:
            color = pygame.Color("yellow")  # Highlight das Eingabefeld, wenn es aktiv ist
        else:
            color = pygame.Color("white")  # Normales Weiß, wenn es inaktiv ist

        pygame.draw.rect(surface, color, self.input_box, 2)  # Zeichne das Eingabefeld

        # Zeige den aktuellen Namen des Spielers an
        name_text = self.font.render(self.player_name, True, color)
        surface.blit(name_text, (self.input_box.x + 10, self.input_box.y + 10))  # Zeichne den Text im Eingabefeld

        # Zeichne den Bestätigungs- und Zurück-Button
        surface.blit(self.confirm_text, self.confirm_rect)
        surface.blit(self.back_text, self.back_rect)

    def cleanup(self):
        # Speichere die Anzahl der Spieler und deren Einstellungen
        self.persist['player_count'] = self.player_count
        self.persist['active_player_index'] = self.active_player_index
        self.persist['selected_players'] = self.selected_players
        self.persist['bot_difficulties'] = self.bot_difficulties
        self.persist['player_name'] = self.player_name
        self.persist['bot_names'] = self.bot_names  # Add this line to store bot names
        return super(A_PlayerSelect, self).cleanup()
