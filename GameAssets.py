import pygame
import os
import random
import json


def load_image(filename):
    """
    Lädt ein Bild aus dem Verzeichnis "Grafiken".

    Input:
    - filename: Der Dateiname des zu ladenden Bildes.

    Output:
    - Das geladene Bild als Pygame-Oberfläche.
    """
    return pygame.image.load(os.path.join("Grafiken", filename))


def load_sound(filename):
    """
    Lädt einen Sound aus dem Verzeichnis "Sounds".

    Input:
    - filename: Der Dateiname des zu ladenden Sounds.

    Output:
    - Der geladene Sound als Pygame Sound-Objekt.
    """
    return pygame.mixer.Sound(os.path.join("Sounds", filename))


class GameAssets:
    def __init__(self):
        """
        Initialisiert die Assets (Bilder, Sounds) und setzt die Lautstärkewerte.

        Output:
        - Geladene Bilder und Sounds sowie eingestellte Lautstärke.
        """
        self.bot_icons = None
        pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=4096)
        pygame.mixer.music.load(os.path.join("Sounds", "main-menu.mp3"))

        self.load_volume_settings()

        pygame.mixer.music.set_volume(self._music_volume)
        pygame.mixer.music.play(-1)

        self.load_assets()

    def load_assets(self):
        """
        Lädt alle Bilder und Sounds und speichert sie als Instanzvariablen.

        Input:
        - Keine Eingabe.

        Output:
        - Geladene Assets als Instanzvariablen.
        """
        self.CardBack = load_image("Back of Card.png")
        self.Card12 = load_image("Playingcard 12.jpg")
        self.Card11 = load_image("Playingcard 11.jpg")
        self.Card10 = load_image("Playingcard 10.jpg")
        self.Card9 = load_image("Playingcard 9.png")
        self.Card8 = load_image("Playingcard 8.jpg")
        self.Card7 = load_image("Playingcard 7.jpg")
        self.Card6 = load_image("Playingcard 6.jpg")
        self.Card5 = load_image("Playingcard 5.jpg")
        self.Card4 = load_image("Playingcard 4.jpg")
        self.Card3 = load_image("Playingcard 3.jpg")
        self.Card2 = load_image("Playingcard 2.png")
        self.Card1 = load_image("Playingcard 1.png")
        self.Card0 = load_image("Playingcard 0.png")
        self.CardN1 = load_image("Playingcard -1.png")
        self.CardN2 = load_image("Playingcard -2.png")
        self.background = load_image("Background.jpg")
        self.Bot1 = load_image("Bot_1.png")
        self.Bot2 = load_image("Bot_2.png")
        self.Bot3 = load_image("Bot_3.png")
        self.Player = load_image("Player.png")

        self.bot_icons = [
            load_image("Bot_1.png"),
            load_image("Bot_2.png"),
            load_image("Bot_3.png")
        ]

        self.card_turn_sfx = load_sound("flipcard.mp3")
        self.card_turn_sfx.set_volume(self._sfx_volume)

    @property
    def music_volume(self):
        """Gibt die aktuelle Musiklautstärke zurück."""
        return self._music_volume

    @music_volume.setter
    def music_volume(self, volume):
        """
        Setzt die Musiklautstärke und speichert sie.

        Input:
        - volume: Die neue Musiklautstärke (float zwischen 0.0 und 1.0).

        Output:
        - Aktualisierte Musiklautstärke.
        """
        self._music_volume = volume
        pygame.mixer.music.set_volume(volume)
        self.save_volume_settings()

    @property
    def sfx_volume(self):
        """Gibt die aktuelle Effektlautstärke zurück."""
        return self._sfx_volume

    @sfx_volume.setter
    def sfx_volume(self, volume):
        """
        Setzt die Effektlautstärke und speichert sie.

        Input:
        - volume: Die neue Effektlautstärke (float zwischen 0.0 und 1.0).

        Output:
        - Aktualisierte Effektlautstärke.
        """
        self._sfx_volume = volume
        self.card_turn_sfx.set_volume(volume)
        self.save_volume_settings()

    def set_music_volume(self, volume):
        """
        Setzt die Musiklautstärke.

        Input:
        - volume: Die neue Musiklautstärke.

        Output:
        - Musiklautstärke wird angepasst.
        """
        self.music_volume = volume

    def set_sfx_volume(self, volume):
        """
        Setzt die Effektlautstärke.

        Input:
        - volume: Die neue Effektlautstärke.

        Output:
        - Effektlautstärke wird angepasst.
        """
        self.sfx_volume = volume

    def save_volume_settings(self):
        """
        Speichert die aktuellen Lautstärke-Einstellungen in einer JSON-Datei.

        Input:
        - Keine Eingabe.

        Output:
        - Lautstärkedaten werden in 'volume_settings.json' gespeichert.
        """
        with open('volume_settings.json', 'w') as file:
            json.dump({
                'music_volume': self._music_volume,
                'sfx_volume': self._sfx_volume
            }, file)

    def load_volume_settings(self):
        """
        Lädt die Lautstärke-Einstellungen aus einer Datei oder setzt Standardwerte.

        Input:
        - Keine Eingabe.

        Output:
        - Geladene oder standardisierte Lautstärkeeinstellungen.
        """
        if os.path.exists('volume_settings.json'):
            with open('volume_settings.json', 'r') as file:
                settings = json.load(file)
                self._music_volume = settings.get('music_volume', 0.5)
                self._sfx_volume = settings.get('sfx_volume', 0.5)
        else:
            self._music_volume = 0.5
            self._sfx_volume = 0.5


class Card:
    def __init__(self, value, assets, visible=False, highlighted=False, elim=False):
        """
        Erstellt eine Spielkarte.

        Input:
        - value: Der Wert der Karte.
        - assets: Die GameAssets, die die Kartengrafiken enthalten.
        - visible: Ob die Karte sichtbar ist.
        - highlighted: Ob die Karte hervorgehoben ist.
        - elim: Ob die Karte eliminiert ist.

        Output:
        - Erstellte Karte mit angegebenen Attributen.
        """
        self.value = value
        self.visible = visible
        self.assets = assets
        self.highlighted = highlighted
        self.elim = elim

    def get_image(self):
        """
        Gibt das Bild der Karte zurück, je nach Sichtbarkeit und Wert.

        Input:
        - Keine Eingabe.

        Output:
        - Das Bild der Karte (Pygame-Oberfläche).
        """
        if not self.visible:
            return self.assets.CardBack

        value_to_image = {
            -2: self.assets.CardN2,
            -1: self.assets.CardN1,
            0: self.assets.Card0,
            1: self.assets.Card1,
            2: self.assets.Card2,
            3: self.assets.Card3,
            4: self.assets.Card4,
            5: self.assets.Card5,
            6: self.assets.Card6,
            7: self.assets.Card7,
            8: self.assets.Card8,
            9: self.assets.Card9,
            10: self.assets.Card10,
            11: self.assets.Card11,
            12: self.assets.Card12
        }
        return value_to_image.get(self.value, self.assets.CardBack)


class Deck:
    def __init__(self, assets):
        """
        Erstellt ein Kartendeck mit den vorgegebenen Werten und mischt es.

        Input:
        - assets: Die GameAssets, die die Kartengrafiken enthalten.

        Output:
        - Ein gemischtes Kartendeck.
        """
        self.assets = assets
        self.cards = self.generate_deck()
        self.shuffle()

    def generate_deck(self):
        """
        Generiert das komplette Deck aus Spielkarten.

        Output:
        - Eine Liste von Spielkarten (Cards).
        """
        cards = []
        for value in range(1, 13):
            cards.extend([Card(value, self.assets) for _ in range(10)])
        cards.extend([Card(-1, self.assets) for _ in range(10)])
        cards.extend([Card(0, self.assets) for _ in range(15)])
        cards.extend([Card(-2, self.assets) for _ in range(5)])
        return cards

    def shuffle(self):
        """
        Mischt die Karten im Deck.

        Output:
        - Gemischtes Deck.
        """
        random.shuffle(self.cards)

    def draw_card(self):
        """
        Zieht die oberste Karte vom Deck.

        Output:
        - Die gezogene Karte oder None, falls das Deck leer ist.
        """
        if self.cards:
            return self.cards.pop()
        return None

    def deal(self, playercount):
        """
        Teilt Karten an die Spieler aus.

        Input:
        - playercount: Anzahl der Spieler.

        Output:
        - Eine Liste mit Kartenhänden für jeden Spieler.
        """
        players_hands = [[] for _ in range(playercount)]
        for _ in range(12):  # 12 Karten pro Spieler
            for player_hand in players_hands:
                player_hand.append(self.draw_card())
        return players_hands

    def draw(self, stack):
        """Bewegt die oberste Karte des Decks auf den Stack und dreht sie um."""
        if self.cards:
            if self.cards:
                top_card = self.cards.pop()
                stack.add_card(top_card)
                return top_card
            return None

    def __len__(self):
        return len(self.cards)


# Die Deck-Klasse repräsentiert einen Kartenstapel, aus dem Karten gezogen werden können.
class Deck:
    def __init__(self, assets):
        self.cards = []
        self.assets = assets

    def draw(self, stack):
        """
        Zieht die oberste Karte des Decks und legt sie auf den angegebenen Stack.
        Die Karte wird auch umgedreht, d.h. ihre Sichtbarkeit ändert sich.

        Input:
        - stack: Der Stack, auf den die gezogene Karte gelegt wird.

        Output:
        - top_card: Die gezogene Karte oder None, falls keine Karte im Deck vorhanden ist.
        """
        if self.cards:
            top_card = self.cards.pop()
            stack.add_card(top_card)
            return top_card
        return None

    def __len__(self):
        """
        Gibt die Anzahl der verbleibenden Karten im Deck zurück.

        Output:
        - Anzahl der Karten im Deck (int).
        """
        return len(self.cards)



class Stack:
    def __init__(self):
        self.cards = []
        self.saved_value = None

    def add_card(self, card):
        """
        Fügt eine Karte zum Stapel hinzu.

        Input:
        - card: Die hinzuzufügende Karte.

        """
        self.cards.append(card)

    def get_top_card(self):
        """
        Gibt die oberste Karte des Stapels zurück.

        Output:
        - Die oberste Karte (Card-Objekt) oder None, falls der Stapel leer ist.
        """
        if self.cards:
            return self.cards[-1]
        return None

    def get_second_top_card(self):
        """
        Gibt die zweitoberste Karte des Stapels zurück.

        Output:
        - Die zweitoberste Karte (Card-Objekt) oder None, falls der Stapel weniger als zwei Karten hat.
        """
        if len(self.cards) > 1:
            return self.cards[-2]
        return None

    def clear(self):
        """
        Entfernt alle Karten vom Stapel.

        """
        self.cards.clear()

    def draw(self):
        """
        Entfernt die oberste Karte des Stapels und ändert ihre Sichtbarkeit.

        Output:
        - Die gezogene Karte (Card-Objekt) oder None, falls der Stapel leer ist.
        """
        if self.cards:
            top_card = self.cards.pop()  # Entferne die oberste Karte
            top_card.visible = not top_card.visible  # Ändere die Sichtbarkeit der Karte
            return top_card  # Rückgabe der gezogenen Karte
        return None

    def turn_second_top_card(self):
        """
        Ändert die Sichtbarkeit der zweitobersten Karte des Stapels.

        """
        if len(self.cards) > 1:
            self.cards[-2].visible = not self.cards[-2].visible  # Sichtbarkeit der zweitobersten Karte ändern

    def peek(self):
        """
        Gibt die oberste Karte des Stapels zurück, ohne sie zu entfernen oder ihre Sichtbarkeit zu ändern.

        Output:
        - Die oberste Karte (Card-Objekt) oder None, falls der Stapel leer ist.
        """
        if self.cards:
            return self.cards[-1]
        return None

    def is_empty(self):
        """
        Überprüft, ob der Stapel leer ist.

        Output:
        - True, wenn der Stapel leer ist, andernfalls False.
        """
        return len(self.cards) == 0

    def save_top_card_value(self):
        """
        Speichert den Wert der obersten Karte des Stapels, falls vorhanden.

        """
        if self.cards:
            self.saved_value = self.cards[-1].value
        else:
            self.saved_value = None

    def get_saved_value(self):
        """
        Gibt den gespeicherten Wert der obersten Karte zurück, falls vorhanden.

        """
        return self.saved_value


# Die Button-Klasse repräsentiert einen klickbaren Knopf im Spiel.
class Button:
    def __init__(self, text, x, y, width, height, font, text_color, button_color, action=None):
        """
        Erstellt einen neuen Button.

        Input:
        - text: Der auf dem Button anzuzeigende Text.
        - x, y: Die Position des Buttons.
        - width, height: Die Größe des Buttons.
        - font: Die Schriftart für den Text.
        - text_color: Die Farbe des Textes.
        - button_color: Die Farbe des Buttons.
        - action: Eine Funktion, die beim Klicken auf den Button ausgeführt wird (optional).

        Output:
        - Erstellter Button.
        """
        self.text = text
        self.rect = pygame.Rect(x, y, width, height)
        self.font = font
        self.text_color = text_color
        self.button_color = button_color
        self.action = action

    def draw(self, surface):
        """
        Zeichnet den Button auf die angegebene Oberfläche.

        Input:
        - surface: Die Oberfläche, auf der der Button gezeichnet werden soll.

        Output:
        - Keine.
        """
        pygame.draw.rect(surface, self.button_color, self.rect)
        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)

    def check_click(self, pos):
        """
        Überprüft, ob der Button angeklickt wurde, und führt ggf. die Aktion aus.

        Input:
        - pos: Die Position des Mausklicks.

        Output:
        - True, wenn der Button angeklickt wurde, sonst False.
        """
        if self.rect.collidepoint(pos):
            if self.action:
                self.action()
            return True
        return False
