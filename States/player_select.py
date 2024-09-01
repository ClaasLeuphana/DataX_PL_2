import pygame
from States.base import State

class PlayerSelect(State):
    def __init__(self, assets=None):
        super(PlayerSelect, self).__init__()
        self.assets = assets
        self.player_count = 1
        self.max_players = 4  # Maximale Anzahl der Spieler
        self.next_state = "GAMEPLAY"
        self.font = pygame.font.Font(None, 50)
        self.button_font = pygame.font.Font(None, 40)

        # Initialisiere screen_rect zuerst
        self.screen_rect = pygame.display.get_surface().get_rect()

        # Erstellen des "Main Menu"-Buttons
        self.button_text = self.button_font.render("Main Menu", True, pygame.Color("white"))
        self.button_rect = self.button_text.get_rect(topleft=(10, self.screen_rect.height - self.button_text.get_height() - 30))

        # Initiale Größe anpassen
        self.resize(self.screen_rect.width, self.screen_rect.height)

    def resize(self, width, height):
        """Passt die GUI-Elemente an die neue Fenstergröße an."""
        self.screen_rect = pygame.Rect(0, 0, width, height)
        # Positioniere die GUI-Elemente relativ zur neuen Fenstergröße
        self.update_rects()

    def update_rects(self):
        """Aktualisiert die Position und Größe der GUI-Elemente basierend auf der Fenstergröße."""
        # Aktualisiere den Text und die Rechtecke neu
        self.text = self.font.render(f"Player Count: {self.player_count}", True, pygame.Color("white"))
        self.text_rect = self.text.get_rect(center=self.screen_rect.center)

        self.increase_text = self.font.render("+", True, pygame.Color("green"))
        self.increase_rect = self.increase_text.get_rect(center=(self.screen_rect.centerx + 200, self.screen_rect.centery))

        self.decrease_text = self.font.render("-", True, pygame.Color("red"))
        self.decrease_rect = self.decrease_text.get_rect(center=(self.screen_rect.centerx - 200, self.screen_rect.centery))

        self.confirm_text = self.font.render("Confirm", True, pygame.Color("yellow"))
        self.confirm_rect = self.confirm_text.get_rect(center=(self.screen_rect.centerx, self.screen_rect.centery + 100))

        # Aktualisiere die Position des "Main Menu"-Buttons
        self.button_rect.topleft = (10, self.screen_rect.height - self.button_text.get_height() - 30)

    def get_event(self, event):
        if event.type == pygame.QUIT:
            self.quit = True
        elif event.type == pygame.MOUSEBUTTONUP:
            mouse_pos = pygame.mouse.get_pos()
            if self.increase_rect.collidepoint(mouse_pos):
                if self.player_count < self.max_players:  # Überprüfen, ob die maximale Anzahl erreicht wurde
                    self.player_count += 1
                    self.update_rects()  # Rechtecke nach der Aktualisierung des Spieleranzahltextes aktualisieren
            elif self.decrease_rect.collidepoint(mouse_pos):
                self.player_count = max(1, self.player_count - 1)
                self.update_rects()  # Rechtecke nach der Aktualisierung des Spieleranzahltextes aktualisieren
            elif self.confirm_rect.collidepoint(mouse_pos):
                self.done = True
            # Überprüfen, ob der "Main Menu"-Button geklickt wurde
            elif self.button_rect.collidepoint(mouse_pos):
                self.next_state = "MENU"
                self.done = True

    def draw(self, surface):
        surface.fill(pygame.Color("blue"))
        surface.blit(self.text, self.text_rect)
        surface.blit(self.increase_text, self.increase_rect)
        surface.blit(self.decrease_text, self.decrease_rect)
        surface.blit(self.confirm_text, self.confirm_rect)

        # Zeichne den "Main Menu"-Button
        surface.blit(self.button_text, self.button_rect.topleft)

    def cleanup(self):
        self.persist['player_count'] = self.player_count
        return super(PlayerSelect, self).cleanup()
