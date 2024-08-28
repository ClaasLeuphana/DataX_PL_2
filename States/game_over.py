import pygame
from .base import State


class GameOver(State):
    def __init__(self, assets=None):
        super(GameOver, self).__init__()
        self.assets = assets
        self.font = pygame.font.Font(None, 100)
        self.screen = pygame.display.get_surface()
        self.screen_rect = self.screen.get_rect()
        self.screen_rect = pygame.display.get_surface().get_rect()

    def startup(self, persistent):
        self.persist = persistent
        self.winner = self.persist.get('winner', None)

    def get_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.quit = True

    def draw(self, surface):
        # Clear screen
        surface.fill(pygame.Color("black"))


        # Draw text
        if self.winner is not None:
            text = self.font.render(f"Player {self.winner} Wins!", True, pygame.Color("white"))
        else:
            text = self.font.render("Game Over", True, pygame.Color("white"))

        text_rect = text.get_rect(center=self.screen_rect.center)
        surface.blit(text, text_rect)

    def resize(self, width, height):
        pass
