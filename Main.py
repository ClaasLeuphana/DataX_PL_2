import pygame
from States.menu import Menu
from States.player_select import PlayerSelect
from States.gameplay_main import Gameplay
from Game import Game

class Main:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1920, 1080))
        self.clock = pygame.time.Clock()
        self.done = False

        # Zustände initialisieren
        states = {
            "MENU": Menu(),
            "PLAYER_SELECT": PlayerSelect(),
            "GAMEPLAY": Gameplay()
        }

        # Spielinstanz erstellen
        self.game = Game(self.screen, states, "MENU")

    def run(self):
        while not self.done:
            dt = self.clock.tick(60) / 1000  # Framerate auf 60 FPS begrenzen
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.done = True
                self.game.get_event(event)
            self.game.update(dt)
            self.screen.fill((0, 0, 0))
            self.game.draw(self.screen)
            pygame.display.flip()

        pygame.quit()

if __name__ == "__main__":
    main = Main()
    main.run()
