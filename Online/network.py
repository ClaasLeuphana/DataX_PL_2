import socket
import uuid


class Network:
    def __init__(self, host):
        """
        Initialisiert die Netzwerkverbindung zum angegebenen Host.

        Parameter:
        - host: Die IP-Adresse oder der Hostname des Servers, zu dem verbunden werden soll
        """
        # Erstelle einen neuen TCP/IP-Socket für die Kommunikation
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.host = host  # Setze den Host (Server-IP oder Hostname)
        self.port = 5555  # Setze den Port, auf dem der Server lauscht
        self.addr = (self.host, self.port)  # Adresse des Servers als Tuple (Host, Port)

        # Generiere eine eindeutige Geräte-ID für den Client
        self.device_id = str(uuid.uuid4())

        self.id = None  # Initialisiere die ID des Clients (wird später vom Server zugewiesen)

        self.connect()  # Stelle die Verbindung zum Server her

    def connect(self):
        """
        Stellt eine Verbindung zum Server her und sendet die Geräte-ID.
        """
        try:
            # Verbinde den Socket mit der Server-Adresse
            self.client.connect(self.addr)

            # Sende die Geräte-ID an den Server, um sich zu identifizieren
            self.client.send(str.encode(self.device_id))

            # Empfange die Spieler-ID vom Server und speichere sie
            self.id = self.client.recv(2048).decode()
        except Exception as e:
            # Fange alle Ausnahmen ab, die beim Verbindungsaufbau auftreten können
            print(f"Error during connection: {e}")

    def send(self, data):
        """
        Sendet Daten an den Server und empfängt eine Antwort.

        Parameter:
        - data: Die Daten, die an den Server gesendet werden sollen (als String)

        Rückgabewert:
        - Antwort des Servers (als String) oder eine Fehlermeldung, falls ein Fehler auftritt
        """
        try:
            # Sende die Daten an den Server
            self.client.send(str.encode(data))

            # Empfange die Antwort des Servers
            reply = self.client.recv(2048).decode()

            return reply  # Gebe die Antwort des Servers zurück
        except socket.error as e:
            # Fange alle Socket-Fehler ab und gebe die Fehlermeldung zurück
            return str(e)


