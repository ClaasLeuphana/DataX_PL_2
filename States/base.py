class State:
    """
    Basisklasse für Spielzustände.
    """
    def __init__(self, assets=None):
        """
        Initialisiert den State.

        Parameter:
        - assets: Die verfügbaren Assets (optional)

        Eigenschaften:
        - assets: Die zugewiesenen Assets
        - done: Gibt an, ob der Zustand abgeschlossen ist
        - quit: Gibt an, ob das Spiel beendet werden soll
        - next_state: Der nächste Zustand, der geladen werden soll
        - persist: Ein Dictionary für persistente Daten
        """
        self.assets = assets
        self.done = False
        self.quit = False
        self.next_state = None
        self.persist = {}

    def get_event(self, event):
        """
        Verarbeitet Ereignisse wie Tasteneingaben oder Mausklicks.

        Parameter:
        - event: Das Ereignis, das verarbeitet werden soll

        Diese Methode wird in abgeleiteten Klassen überschrieben, um spezifische Ereignisse zu behandeln.
        """
        pass

    def update(self, dt):
        """
        Aktualisiert den Zustand basierend auf der verstrichenen Zeit.

        Parameter:
        - dt: Delta-Zeit seit dem letzten Update

        Diese Methode wird in abgeleiteten Klassen überschrieben, um den Zustand basierend auf der verstrichenen Zeit zu aktualisieren.
        """
        pass

    def draw(self, surface):
        """
        Zeichnet den Zustand auf der angegebenen Oberfläche.

        Parameter:
        - surface: Die Pygame-Oberfläche, auf der gezeichnet wird

        Diese Methode wird in abgeleiteten Klassen überschrieben, um den Zustand auf der Oberfläche darzustellen.
        """
        pass

    def startup(self, persistent):
        """
        Initialisiert den Zustand mit persistierenden Daten.

        Parameter:
        - persistent: Ein Dictionary mit persistierenden Daten

        Dieser Zustand wird mit den bereitgestellten Daten initialisiert.
        """
        self.persist = persistent

    def cleanup(self):
        """
        Bereinigt Ressourcen und Daten vor einem Zustandswechsel.

        Rückgabewert:
        - Ein Dictionary mit den aktuellen persistierenden Daten
        """
        return self.persist
