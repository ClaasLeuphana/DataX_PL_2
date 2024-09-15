import pygame
from Online.network import Network
from Online.gameplay_online import GamePlay
import subprocess
import time
import socket
import pyperclip


class Button:
    def __init__(self, x, y, width, height, color, text):
        """
        Initialisiert einen Button mit Position, Größe, Farbe und Text.

        Parameter:
        - x: x-Position des Buttons
        - y: y-Position des Buttons
        - width: Breite des Buttons
        - height: Höhe des Buttons
        - color: Farbe des Buttons im Normalzustand
        - text: Text, der auf dem Button angezeigt wird
        """
        self.rect = pygame.Rect(x, y, width, height)  # Erstelle ein Rechteck für den Button
        self.color = color  # Setze die Farbe des Buttons
        self.text = text  # Setze den Text des Buttons
        self.font = pygame.font.SysFont(None, 36)  # Erstelle eine Schriftart für den Text
        self.hover_color = (255, 200, 200)  # Farbe des Buttons beim Hover-Effekt

    def draw(self, screen):
        """
        Zeichne den Button auf dem Bildschirm.

        Parameter:
        - screen: Das Pygame-Bildschirmobjekt
        """
        mouse_pos = pygame.mouse.get_pos()  # Erhalte die aktuelle Mausposition
        if self.rect.collidepoint(mouse_pos):
            pygame.draw.rect(screen, self.hover_color, self.rect)  # Zeichne den Button mit Hover-Farbe
        else:
            pygame.draw.rect(screen, self.color, self.rect)  # Zeichne den Button mit normaler Farbe

        # Erstelle und zeichne den Text auf dem Button
        text_surface = self.font.render(self.text, True, (0, 0, 0))
        screen.blit(text_surface, (self.rect.x + (self.rect.width - text_surface.get_width()) // 2,
                                   self.rect.y + (self.rect.height - text_surface.get_height()) // 2))

    def is_clicked(self):
        """
        Überprüfe, ob der Button geklickt wurde.

        Rückgabewert:
        - True, wenn der Button geklickt wurde, sonst False
        """
        mouse_click = pygame.mouse.get_pressed()  # Überprüfe, ob die linke Maustaste gedrückt ist
        if mouse_click[0] and self.rect.collidepoint(pygame.mouse.get_pos()):  # Überprüfe auf Klick im Button-Bereich
            return True
        return False


class Lobby:
    def __init__(self, w, h, is_host=False):
        """
        Initialisiert das Lobby-Fenster.

        Parameter:
        - w: Breite des Fensters
        - h: Höhe des Fensters
        - is_host: Boolean, der angibt, ob der Client als Host fungiert
        """
        pygame.init()  # Initialisiere Pygame
        self.server_process = None  # Prozess für den Server
        self.net = None  # Netzwerkverbindung
        self.width = w  # Fensterbreite
        self.height = h  # Fensterhöhe
        self.canvas = Canvas(self.width, self.height, "Lobby...")  # Erstelle ein Canvas für das Zeichnen
        self.name = "Player"  # Standardname für den Spieler
        self.text_field = TextField(self.width // 2 - 100, self.height // 2 - 25, 200, 50,
                                    self.name)  # Textfeld für den Namen
        self.font_size = 30  # Schriftgröße
        self.game_started = False  # Flag, das angibt, ob das Spiel gestartet wurde
        self.host_ip = None  # IP-Adresse des Hosts
        self.ip_input_box = TextField(self.width // 2 - 100, self.height // 2 - 25, 200, 50,
                                      "Enter server IP")  # Textfeld für IP-Eingabe
        self.error_message = ""  # Fehlermeldung für fehlgeschlagene Verbindungen

        # Button zum Starten des Spiels
        self.start_button = Button(self.width // 2 - 75, self.height - 100, 150, 50, (0, 255, 0), "Start Game")
        self.is_host = is_host  # Setze, ob der Client als Host agiert
        self.GamePlay = GamePlay(self.net, self.is_host)  # Erstelle eine Instanz für das Gameplay

        self.ip_display_text = None  # Text zur Anzeige der IP-Adresse des Hosts

    def startup(self):
        """
        Starte das Lobby-Fenster.
        Falls der Client ein Host ist, starte den Server, andernfalls zeige das IP-Eingabefeld an.
        """
        if self.is_host:
            self.host_ip = f"{socket.gethostbyname(socket.gethostname())}"  # Erhalte die lokale IP-Adresse des Hosts
            self.start_server()  # Starte den Server
            time.sleep(1)  # Warte eine Sekunde, um sicherzustellen, dass der Server läuft
            self.net = Network(self.host_ip)  # Erstelle eine Netzwerkverbindung zum Server
        else:
            self.enter_ip_dialog()  # Zeige das Dialogfeld zur Eingabe der IP-Adresse an

        self.run()  # Starte die Haupt-Event-Schleife

    def enter_ip_dialog(self):
        """
        Zeige ein Dialogfeld zur Eingabe der IP-Adresse an und versuche, eine Verbindung zum Server herzustellen.
        """
        running = True
        text_field = TextField(self.width // 2 - 100, self.height // 2 - 25, 200, 50,
                               font_size=30)  # Erstelle ein Textfeld für die IP-Eingabe

        while running:
            self.canvas.draw_background()  # Zeichne den Hintergrund des Canvas neu
            self.canvas.draw_text("Enter Server IP:", 30, self.width // 2, self.height // 2 - 70,
                                  center=True)  # Zeichne den Text "Enter Server IP:"
            text_field.draw(self.canvas.screen)  # Zeichne das Textfeld auf dem Bildschirm

            if self.error_message:
                self.canvas.draw_text(self.error_message, 30, self.width // 2, self.height // 2 + 50,
                                      center=True)  # Zeige Fehlermeldung an

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()  # Beende Pygame, wenn das Fenster geschlossen wird
                    return

                # Behandle die IP-Eingabe
                ip_input = text_field.handle_event(event)
                if ip_input:
                    try:
                        # Versuche, eine Verbindung mit der angegebenen IP-Adresse herzustellen
                        self.net = Network(ip_input)
                        self.error_message = ""
                        self.host_ip = ip_input
                        running = False  # Beende die Schleife, wenn die Verbindung erfolgreich ist
                    except Exception as e:
                        print(f"[DEBUG] Connection failed: {e}")  # Debug-Ausgabe bei Verbindungsfehler
                        self.error_message = "Connection failed! Please enter the IP again."  # Setze Fehlermeldung

            self.canvas.update()  # Aktualisiere den Bildschirm

    def start_server(self):
        """
        Starte den Serverprozess.
        """
        if self.server_process is None:
            self.server_process = subprocess.Popen(["python", "Online./server.py"])  # Starte den Serverprozess
            print("Server gestartet")  # Ausgabe zur Bestätigung, dass der Server gestartet wurde

    def stop_server(self):
        """
        Stoppe den Serverprozess.
        """
        if self.server_process is not None:
            self.server_process.terminate()  # Beende den Serverprozess
            self.server_process = None
            print("Server gestoppt")  # Ausgabe zur Bestätigung, dass der Server gestoppt wurde

    def run(self):
        """
        Starte die Haupt-Event-Schleife für das Lobby-Fenster.
        """
        clock = pygame.time.Clock()  # Erstelle ein Clock-Objekt für die Zeitkontrolle
        run = True

        while run:
            clock.tick(60)  # Begrenze die Schleife auf 60 FPS

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.stop_server()  # Stoppe den Server, wenn das Fenster geschlossen wird
                    run = False  # Beende die Schleife
                new_name = self.text_field.handle_event(event)  # Behandle Ereignisse im Textfeld
                if new_name:
                    self.send_name_change(new_name)  # Sende den neuen Namen an den Server
                    self.name = new_name  # Aktualisiere den Namen des Spielers

                if event.type == pygame.VIDEORESIZE:
                    self.resize(event.w, event.h)  # Behandle die Größenänderung des Fensters

            if not self.game_started:
                player_count, lobby_info = self.send_lobby_data()  # Hole Lobby-Daten vom Server

                # Aktualisiere das Canvas mit dem aktuellen Status
                self.canvas.draw_background()
                self.draw_player_list(lobby_info)  # Zeichne die Spieler-Liste

                # Zeige den Namen des Spielers an
                self.canvas.draw_text("Your player name:", self.font_size, self.width // 2, self.height // 2 - 70,
                                      center=True)
                self.text_field.draw(self.canvas.screen)  # Zeichne das Textfeld

                # Zeige die Server-IP-Adresse im GUI für den Host an
                if self.is_host and self.host_ip:
                    ip_text = f"Server IP: {self.host_ip}"
                    if self.ip_display_text is None:
                        self.ip_display_text = ip_text
                    self.canvas.draw_text(self.ip_display_text, 30, self.width // 2, 30, center=True)

                # Zeige den Start-Button, wenn der Client der Host ist
                if self.is_host:
                    self.start_button.draw(self.canvas.screen)
                    if self.start_button.is_clicked():
                        print("[DEBUG] Start Game button clicked")  # Debug-Ausgabe bei Button-Klick
                        self.net.send('start_game')  # Sende ein Signal zum Starten des Spiels

                self.canvas.update()  # Aktualisiere den Bildschirm

            if self.game_started:
                self.GamePlay.startup()  # Starte das Gameplay, wenn das Spiel begonnen hat
                break

        pygame.quit()  # Beende Pygame, wenn die Schleife endet

    def send_lobby_data(self):
        """
        Sende eine Anfrage an den Server, um die Lobby-Daten zu erhalten.

        Rückgabewert:
        - game_status: Status des Spiels
        - lobby_info: Informationen zur Lobby
        """
        try:
            reply = self.net.send("lobby")  # Sende Anfrage an den Server
            print(f"[DEBUG] Server response (send_lobby_data): {reply}")  # Debug-Ausgabe der Server-Antwort

            lines = reply.split('\n')  # Teile die Antwort in Zeilen auf
            if len(lines) > 1:
                game_status = lines[-1].strip()  # Der Status des Spiels befindet sich in der letzten Zeile
                self.game_started = (game_status == 'game_started')  # Setze das Flag für den Spielstatus

                print(f"[DEBUG] Game Status: {game_status}, Game Started: {self.game_started}")

                lobby_info = "\n".join(lines[:-1]) if len(
                    lines) > 1 else ""  # Lobby-Informationen sind alle Zeilen außer der letzten
                self.is_host = lines[1].startswith(f"Player 1:") if len(
                    lines) > 1 else False  # Überprüfe, ob der Client der Host ist

                print(f"[DEBUG] Lobby Info: {lobby_info}, Is Host: {self.is_host}")

                return game_status, lobby_info
            else:
                print("[DEBUG] Unexpected format for lobby data response.")  # Debug-Ausgabe für unerwartetes Format
                return "", ""
        except Exception as e:
            print(f"[DEBUG] Error sending lobby data request: {e}")  # Debug-Ausgabe bei Fehlern
            return "", ""

    def send_name_change(self, new_name):
        """
        Sende eine Anfrage an den Server, um den Namen des Spielers zu ändern.

        Parameter:
        - new_name: Neuer Name des Spielers
        """
        try:
            response = self.net.send(f"name:{new_name}")  # Sende die Namensänderung an den Server
            print(f"Server response (name change): {response}")  # Ausgabe der Server-Antwort
        except Exception as e:
            print(f"Error sending name change: {e}")  # Ausgabe bei Fehlern

    def draw_player_list(self, lobby_info):
        """
        Zeichne die Liste der Spieler in der Lobby.

        Parameter:
        - lobby_info: Informationen zur Lobby, die die Spielernamen enthalten
        """
        player_names = lobby_info.split('\n')  # Teile die Lobby-Informationen in Spielernamen auf
        y_offset = 100  # Anfangs-Offset für die y-Position der Spielernamen
        for player_name in player_names:
            self.canvas.draw_text(player_name, 30, self.width // 2, y_offset, center=True)  # Zeichne jeden Spielernamen
            y_offset += 40  # Erhöhe den y-Offset für den nächsten Spielernamen

    def resize(self, width, height):
        """
        Passe die Größe des Canvas und die Position der Elemente an die neue Fenstergröße an.

        Parameter:
        - width: Neue Breite des Fensters
        - height: Neue Höhe des Fensters
        """
        self.width = width  # Setze die neue Breite
        self.height = height  # Setze die neue Höhe
        self.canvas = Canvas(self.width, self.height, "Lobby...")  # Erstelle ein neues Canvas mit der neuen Größe

        # Aktualisiere die Position des Textfeldes und des Start-Buttons basierend auf der neuen Fenstergröße
        self.text_field.rect.topleft = (self.width // 2 - 100, self.height // 2 - 25)
        self.start_button.rect.topleft = (self.width // 2 - 75, self.height - 100)

        # Aktualisiere den IP-Anzeigetext, falls der Spieler der Host ist
        if self.is_host and self.host_ip:
            self.ip_display_text = f"Server IP: {self.host_ip}"  # Aktualisiere den IP-Anzeigetext


class Canvas:
    def __init__(self, w, h, name="None"):
        """
        Initialisiert das Canvas für das Zeichnen.

        Parameter:
        - w: Breite des Canvas
        - h: Höhe des Canvas
        - name: Titel des Fensters
        """
        self.width = w  # Setze die Breite des Canvas
        self.height = h  # Setze die Höhe des Canvas
        self.screen = pygame.display.set_mode((w, h), pygame.RESIZABLE)  # Erstelle ein resizable Fenster
        pygame.display.set_caption(name)  # Setze den Fenstertitel

    def update(self):
        """
        Aktualisiere den Bildschirm.
        """
        pygame.display.update()  # Aktualisiere die Anzeige

    def draw_text(self, text, size, x, y, center=False):
        """
        Zeichne Text auf dem Bildschirm.

        Parameter:
        - text: Der anzuzeigende Text
        - size: Schriftgröße
        - x: x-Position des Texts
        - y: y-Position des Texts
        - center: Ob der Text zentriert sein soll
        """
        pygame.font.init()  # Initialisiere die Schriftart
        font = pygame.font.SysFont("comicsans", size)  # Erstelle die Schriftart
        text = str(text)  # Stelle sicher, dass der Text als String vorliegt
        render = font.render(text, True, (0, 0, 0))  # Render den Text
        text_rect = render.get_rect(center=(x, y)) if center else pygame.Rect(x, y, render.get_width(),
                                                                              render.get_height())  # Bestimme die Text-Rechteckposition
        self.screen.blit(render, text_rect)  # Zeichne den Text auf dem Bildschirm

    def draw_background(self):
        """
        Zeichne den Hintergrund des Canvas.
        """
        self.screen.fill((255, 255, 255))  # Fülle den Hintergrund mit weißer Farbe

    def create_text(self, text, size, x, y):
        """
        Erstelle und returniere ein gerendertes Textobjekt.

        Parameter:
        - text: Der anzuzeigende Text
        - size: Schriftgröße
        - x: x-Position des Texts
        - y: y-Position des Texts

        Rückgabewert:
        - render: Das gerenderte Textobjekt
        - (x, y): Die Position des Texts
        """
        font = pygame.font.SysFont("comicsans", size)  # Erstelle die Schriftart
        text = str(text)  # Stelle sicher, dass der Text als String vorliegt
        render = font.render(text, True, (0, 0, 0))  # Render den Text
        return render, (x, y)  # Gebe das gerenderte Textobjekt und die Position zurück


class TextField:
    def __init__(self, x, y, width, height, text='', font_size=30):
        """
        Initialisiert ein Textfeld zur Eingabe von Text.

        Parameter:
        - x: x-Position des Textfelds
        - y: y-Position des Textfelds
        - width: Breite des Textfelds
        - height: Höhe des Textfelds
        - text: Anfangstext im Textfeld
        - font_size: Schriftgröße des Texts
        """
        self.rect = pygame.Rect(x, y, width, height)  # Erstelle ein Rechteck für das Textfeld
        self.color_inactive = pygame.Color('lightskyblue3')  # Farbe des Textfelds im inaktiven Zustand
        self.color_active = pygame.Color('dodgerblue2')  # Farbe des Textfelds im aktiven Zustand
        self.color = self.color_inactive  # Setze die anfängliche Farbe
        self.text = text  # Setze den Anfangstext
        self.font = pygame.font.Font(None, font_size)  # Erstelle die Schriftart
        self.txt_surface = self.font.render(text, True, self.color)  # Render den Anfangstext
        self.active = False  # Flag, das angibt, ob das Textfeld aktiv ist

    def handle_event(self, event):
        """
        Behandle Ereignisse wie Tasteneingaben und Mausklicks.

        Parameter:
        - event: Das Ereignis, das verarbeitet werden soll

        Rückgabewert:
        - Der aktuelle Text im Textfeld, wenn Enter gedrückt wird
        """
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Wenn der Benutzer im Textfeld klickt, aktiviere es.
            if self.rect.collidepoint(event.pos):
                self.active = not self.active
            else:
                self.active = False
            # Ändere die aktuelle Farbe des Textfelds.
            self.color = self.color_active if self.active else self.color_inactive

        if event.type == pygame.KEYDOWN:
            if self.active:
                # Handle Ctrl+V für das Einfügen von Text
                if event.key == pygame.K_v and pygame.key.get_mods() & pygame.KMOD_CTRL:
                    self.text += pyperclip.paste()  # Füge den Inhalt der Zwischenablage hinzu

                # Handle andere Tasteneingaben
                elif event.key == pygame.K_RETURN:
                    return self.text  # Reiche den aktuellen Text zurück, wenn Enter gedrückt wird
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]  # Entferne das letzte Zeichen, wenn Backspace gedrückt wird
                else:
                    self.text += event.unicode  # Füge das gedrückte Zeichen hinzu

                # Render den aktualisierten Text
                self.txt_surface = self.font.render(self.text, True, self.color)

    def draw(self, screen):
        """
        Zeichne das Textfeld auf dem Bildschirm.

        Parameter:
        - screen: Das Pygame-Screen-Objekt, auf dem gezeichnet wird
        """
        screen.blit(self.txt_surface, (self.rect.x + 5, self.rect.y + 5))  # Zeichne den Text
        pygame.draw.rect(screen, self.color, self.rect, 2)  # Zeichne den Rand des Textfelds
