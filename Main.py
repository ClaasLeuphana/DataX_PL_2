import pygame
from States.menu import Menu
from States.player_select import PlayerSelect
from States.A_player_select import A_PlayerSelect
from States.gameplay_main import Gameplay
from States.gameplay_automated import Gameplay_Automated
from States.game_over import GameOver
from States.A_Gameover import A_Gameover
from States.Scoreboard import Scoreboard
from States.A_Scoreboard import A_Scoreboard
from States.Rules import Rules
from States.options import Options
from States.gamemode import Gamemode
from States.local import Local
from States.host_lobby import HostLobby
from States.client_lobby import ClientLobby
from Game import Game
from GameAssets import GameAssets


class Main:
    def __init__(self):
        """
        Initialisiert das Hauptspiel, die Bildschirmgröße, die GameAssets und die Spielzustände.
        Es stellt sicher, dass Pygame initialisiert wird und die erforderlichen Zustände und Assets geladen sind.

        Input:
        - Keine expliziten Eingaben, aber es werden Ressourcen geladen.

        Output:
        - Initialisierte GameAssets und Spielzustände, Spiel läuft im "MENU"-Zustand.
        """

        pygame.init()

        self.assets = GameAssets()

        self.screen_info = pygame.display.Info()
        self.screen = pygame.display.set_mode(
            (self.screen_info.current_w, self.screen_info.current_h - 50),
            pygame.RESIZABLE
        )

        pygame.display.set_caption("SkyJo a DataX Project")

        self.clock = pygame.time.Clock()
        self.done = False

        # Zustände (States) initialisieren. Jeder Zustand repräsentiert eine Phase des Spiels
        states = {
            "MENU": Menu(assets=self.assets),
            "PLAYER_SELECT": PlayerSelect(assets=self.assets),
            "A_PLAYER_SELECT": A_PlayerSelect(assets=self.assets),
            "RULES": Rules(assets=self.assets),
            "OPTIONS": Options(assets=self.assets),
            "GAMEMODE": Gamemode(assets=self.assets),
            "HOST_LOBBY": HostLobby(assets=self.assets),
            "CLIENT_LOBBY": ClientLobby(assets=self.assets),
            "LOCAL": Local(assets=self.assets),
            "SCOREBOARD": Scoreboard(assets=self.assets),
            "A_SCOREBOARD": A_Scoreboard(assets=self.assets),
            "GAMEPLAY": Gameplay(assets=self.assets),
            "GAMEPLAY_AUTOMATED": Gameplay_Automated(assets=self.assets),
            'GAMEOVER': GameOver(assets=self.assets),
            "A_GAMEOVER": A_Gameover(assets=self.assets)
        }

        self.game = Game(self.screen, states, "MENU")

    def run(self):
        """
        Hauptspieldurchlauf. Steuert den Spielzyklus, verarbeitet Eingaben, aktualisiert den Zustand
        und zeichnet die Grafiken.

        Input:
        - Keine direkten Eingaben, aber es werden Ereignisse von Pygame erfasst (z.B. Tastendrücke, Fenstergröße).

        Output:
        - Aktualisierte Spiellogik und -darstellung. Das Spiel läuft, bis "done" auf True gesetzt wird.
        """

        while not self.done:
            dt = self.clock.tick(60) / 1000

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.done = True
                elif event.type == pygame.VIDEORESIZE:
                    self.screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
                    self.game.resize(event.w, event.h)
                self.game.get_event(event)

            if self.game.done or self.game.quit:
                self.done = True

            self.game.update(dt)
            self.screen.fill((0, 0, 0))

            self.game.draw(self.screen)

            pygame.display.flip()

        pygame.quit()


if __name__ == "__main__":
    """
    Startpunkt des Programms. Erstellt eine Instanz der Main-Klasse und startet das Spiel.
    """

    main = Main()
    main.run()
