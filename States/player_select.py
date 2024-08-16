import pygame
from .base import State

class PlayerSelect(State):
    def __init__(self):
        super(PlayerSelect, self).__init__()
        self.player_count = 1
        self.max_players = 4  # Maximale Anzahl der Spieler
        self.next_state = "GAMEPLAY"
        self.font = pygame.font.Font(None, 50)
        self.resize(pygame.display.get_surface().get_width(), pygame.display.get_surface().get_height())

    def resize(self, width, height):
        """Passt die GUI-Elemente an die neue Fenstergröße an."""
        self.screen_rect = pygame.Rect(0, 0, width, height)
        # Positioniere die GUI-Elemente relativ zur neuen Fenstergröße
        self.update_rects()

    def update_rects(self):
        """Aktualisiert die Position und Größe der GUI-Elemente basierend auf der Fenstergröße."""
        self.text_rect = self.font.render(f"Player Count: {self.player_count}", True, pygame.Color("white")).get_rect(
            center=self.screen_rect.center)

        self.increase_rect = self.font.render("+", True, pygame.Color("green")).get_rect(
            center=(self.screen_rect.centerx + 200, self.screen_rect.centery))
        self.decrease_rect = self.font.render("-", True, pygame.Color("red")).get_rect(
            center=(self.screen_rect.centerx - 200, self.screen_rect.centery))
        self.confirm_rect = self.font.render("Confirm", True, pygame.Color("blue")).get_rect(
            center=(self.screen_rect.centerx, self.screen_rect.centery + 100))

    def get_event(self, event):
        if event.type == pygame.QUIT:
            self.quit = True
        elif event.type == pygame.MOUSEBUTTONUP:
            mouse_pos = pygame.mouse.get_pos()
            if self.increase_rect.collidepoint(mouse_pos):
                if self.player_count < self.max_players:  # Überprüfen, ob die maximale Anzahl erreicht wurde
                    self.player_count += 1
            elif self.decrease_rect.collidepoint(mouse_pos):
                self.player_count = max(1, self.player_count - 1)
            elif self.confirm_rect.collidepoint(mouse_pos):
                self.done = True

    def draw(self, surface):
        surface.fill(pygame.Color("blue"))
        text = self.font.render(f"Player Count: {self.player_count}", True, pygame.Color("white"))
        self.text_rect = text.get_rect(center=self.screen_rect.center)
        surface.blit(text, self.text_rect)

        increase_text = self.font.render("+", True, pygame.Color("green"))
        self.increase_rect = increase_text.get_rect(center=(self.screen_rect.centerx + 200, self.screen_rect.centery))
        surface.blit(increase_text, self.increase_rect)

        decrease_text = self.font.render("-", True, pygame.Color("red"))
        self.decrease_rect = decrease_text.get_rect(center=(self.screen_rect.centerx - 200, self.screen_rect.centery))
        surface.blit(decrease_text, self.decrease_rect)

        confirm_text = self.font.render("Confirm", True, pygame.Color("yellow"))
        self.confirm_rect = confirm_text.get_rect(center=(self.screen_rect.centerx, self.screen_rect.centery + 100))
        surface.blit(confirm_text, self.confirm_rect)

    def cleanup(self):
        self.persist['player_count'] = self.player_count
        return super(PlayerSelect, self).cleanup()
