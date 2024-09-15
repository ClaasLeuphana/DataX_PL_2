import pygame


class Game:
    def __init__(self, screen, states, start_state):
        """
        Initialisiert das Spiel und setzt den ersten Zustand.

        Input:
        - screen: Die Oberfläche (Display), auf der das Spiel gezeichnet wird.
        - states: Ein Dictionary, das die Zustände (States) des Spiels enthält.
        - start_state: Der Name des Startzustands (String).

        """
        self.screen = screen
        self.states = states
        self.state_name = start_state
        self.state = self.states.get(self.state_name)
        self.done = False
        self.quit = False
        self.state.startup({})

    def get_event(self, event):
        """
        Übergibt das Event an den aktuellen Zustand.

        Input:
        - event: Ein Pygame-Event (z.B. Tastendruck, Mausbewegung).

        """
        if self.state:
            self.state.get_event(event)

    def update(self, dt):
        """
        Aktualisiert den aktuellen Zustand des Spiels.

        Input:
        - dt: Die Zeit, die seit dem letzten Frame vergangen ist (Delta Time).

        """
        if self.state:
            self.state.update(dt)
            if self.state.done:
                self.flip_state()
            if self.state.quit:
                self.quit = True

    def draw(self, screen):
        """
        Zeichnet den aktuellen Zustand auf den Bildschirm.

        Input:
        - screen: Die Oberfläche, auf die gezeichnet werden soll.

        """
        self.state.draw(self.screen)

    def flip_state(self):
        """
        Wechselt zum nächsten Zustand in der State-Maschine.

        """
        if self.state:
            self.state.done = False
            previous, self.state_name = self.state_name, self.state.next_state
            persistent = self.state.cleanup()
            self.state = self.states.get(self.state_name)
            if not self.state:
                raise ValueError(
                    f"Next state '{self.state_name}' not found in states.")
            self.state.startup(persistent)

    def resize(self, width, height):
        """
        Passt das Spiel an eine neue Bildschirmgröße an.

        Input:
        - width: Die neue Breite des Bildschirms.
        - height: Die neue Höhe des Bildschirms.

        """
        self.screen = pygame.display.set_mode((width, height),
                                              pygame.RESIZABLE)
        if self.state:
            self.state.resize(width, height)
