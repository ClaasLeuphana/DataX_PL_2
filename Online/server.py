import socket
from _thread import *
import time
import threading

# Globale Variablen
clients = {}  # Dictionary zur Speicherung der Clients mit UUID, Spieler-ID und Namen
game_started = False  # Status, ob das Spiel gestartet wurde
host_id = None  # Variable für den Host (erster Client, der sich verbindet)
lock = threading.Lock()  # Lock für Thread-Sicherheit

def create_server_socket():
    """
    Erstellt und konfiguriert einen Server-Socket.

    Rückgabewert:
    - Der erstellte Server-Socket, wenn erfolgreich; sonst None
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Erstelle einen TCP/IP-Socket
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # Setze SO_REUSEADDR, um Port-Konflikte zu vermeiden
    server = socket.gethostbyname(socket.gethostname())  # Hole die IP-Adresse des Hosts
    port = 5555  # Setze den Port auf 5555
    try:
        s.bind((server, port))  # Binde den Socket an die IP-Adresse und den Port
        s.listen(4)  # Erlaube bis zu 4 Verbindungen (Spieler)
        print(f"Server listening on {server}:{port}")
        return s
    except socket.error as e:
        print(f"Socket error: {e}")
        s.close()  # Schließe den Socket bei Fehler
        return None

def monitor_game_status():
    """
    Überwacht den Status des Spiels und gibt diesen alle 5 Sekunden aus.
    """
    global game_started
    while True:
        print(f"Game Started: {game_started}")  # Gib den aktuellen Spielstatus aus
        time.sleep(5)  # Warte 5 Sekunden vor der nächsten Überprüfung

def close_all_connections():
    """
    Schließt alle Verbindungen und leert das Clients-Dictionary.
    """
    global clients
    try:
        print("[DEBUG] Closing all connections...")
        for device_id, client_info in list(clients.items()):
            try:
                client_info['connection'].close()  # Schließe die Verbindung zum Client
                print(f"[DEBUG] Connection closed for {device_id}")
            except Exception as e:
                print(f"[DEBUG] Error closing connection for {device_id}: {e}")
        clients.clear()  # Leere das Dictionary der Clients
        print("[DEBUG] All connections closed and clients cleared.")
    except Exception as e:
        print(f"[DEBUG] Error while closing all connections: {e}")

def threaded_client(conn):
    """
    Behandelt die Kommunikation mit einem einzelnen Client in einem eigenen Thread.

    Parameter:
    - conn: Die Verbindung zum Client
    """
    global game_started, host_id
    try:
        # Empfange die UUID des Clients und dekodiere sie
        device_id = conn.recv(2048).decode('utf-8')
        print(f"[DEBUG] Received device_id: {device_id}")

        if device_id not in clients:
            # Wenn der Client neu ist, weise ihm eine Spieler-ID zu
            player_id = str(len(clients) + 1)
            clients[device_id] = {'id': player_id, 'name': f'Player {player_id}'}
            print(f"[DEBUG] New client connected: Player {player_id}")

            if host_id is None:
                # Setze den ersten Client als Host
                host_id = device_id
                print(f"[DEBUG] Client {device_id} is set as Host.")
        else:
            # Wenn der Client bereits existiert, hole die Spieler-ID
            player_id = clients[device_id]['id']
            print(f"[DEBUG] Existing client reconnected: Player {player_id}")

        # Sende die Spieler-ID zurück an den Client
        conn.send(str.encode(player_id))

        while True:
            try:
                # Empfange Daten vom Client
                data = conn.recv(2048).decode('utf-8')
                if not data:
                    break  # Beende die Schleife, wenn keine Daten empfangen werden

                # Verarbeite die empfangenen Daten
                if data.startswith('name:'):
                    new_name = data.split(':')[1]
                    clients[device_id]['name'] = new_name
                    print(f"[DEBUG] Name changed for {device_id} to {new_name}")

                elif data == 'start_game':
                    game_started = True
                    print("[DEBUG] Game Started command received.")

                elif data == 'check_host':
                    host = 'True' if device_id == host_id else 'False'
                    response = f"Host: {host}"
                    conn.sendall(str.encode(response))

                elif data == 'lobby':
                    status = 'game_started' if game_started else 'waiting'
                    lobby_info = f"{len(clients)}/4\n" + '\n'.join(
                        f"Player {info['id']}: {info['name']}" for info in clients.values())

                    # Spielstatus an Lobby-Info anhängen
                    response = f"{lobby_info}\n{status}"
                    conn.sendall(str.encode(response))
            except ConnectionResetError:
                print("Connection was reset by the client.")
                break
            except Exception as e:
                print(f"An error occurred: {e}")
                break
    finally:
        # Schließe die Verbindung und entferne den Client aus der Liste
        conn.close()
        if device_id in clients:
            del clients[device_id]
            print(f"[DEBUG] Client {device_id} disconnected and removed.")
        if device_id == host_id:
            # Setze den Host zurück, wenn der Host die Verbindung trennt
            host_id = None
            print("[DEBUG] Host disconnected, host reset.")

# Starte den Status-Überwachungs-Thread
start_new_thread(monitor_game_status, ())

# Erstelle den Server-Socket
s = create_server_socket()
if s:
    try:
        while True:
            # Akzeptiere eingehende Verbindungen und starte für jede eine neue Thread
            conn, addr = s.accept()
            start_new_thread(threaded_client, (conn,))
    except KeyboardInterrupt:
        print("[DEBUG] Server shutting down due to KeyboardInterrupt.")
    finally:
        # Schließe alle Verbindungen und den Server-Socket
        close_all_connections()
        s.close()
else:
    print("Failed to create server socket.")
