import pygame
from States.menu import Menu
from States.player_select import PlayerSelect
from States.gameplay_main import Gameplay
from States.game_over import GameOver
from States.Rules import Rules
from States.options import Options
from Game import Game
from GameAssets import GameAssets

class Main:
    def __init__(self):
        pygame.init()

        # Initialisiere die GameAssets
        self.assets = GameAssets()  # Erstellen einer Instanz von GameAssets

        # Verwende Bildschirminformationen, um die Größe des Fensters zu bestimmen
        self.screen_info = pygame.display.Info()
        self.screen = pygame.display.set_mode(
            (self.screen_info.current_w, self.screen_info.current_h - 50),
            pygame.RESIZABLE
        )

        pygame.display.set_caption("Mein Spiel")  # Optional: Setze den Fenstertitel

        self.clock = pygame.time.Clock()
        self.done = False

        # Zustände initialisieren
        states = {
            "MENU": Menu(assets=self.assets),
            "PLAYER_SELECT": PlayerSelect(assets=self.assets),
            "RULES": Rules(assets=self.assets),
            "OPTIONS": Options(assets=self.assets),
            "GAMEPLAY": Gameplay(assets=self.assets),
            'GAMEOVER': GameOver(assets=self.assets)
        }

        # Spielinstanz erstellen
        self.game = Game(self.screen, states, "MENU")

    def run(self):
        while not self.done:
            dt = self.clock.tick(60) / 1000  # Framerate auf 60 FPS begrenzen
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.done = True
                elif event.type == pygame.VIDEORESIZE:
                    self.screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
                    self.game.resize(event.w, event.h)  # Größe anpassen
                self.game.get_event(event)

            # Check if the current state or the game itself requests to quit
            if self.game.done or self.game.quit:
                self.done = True

            self.game.update(dt)
            self.screen.fill((0, 0, 0))
            self.game.draw(self.screen)
            pygame.display.flip()

        pygame.quit()

if __name__ == "__main__":
    main = Main()
    main.run()
