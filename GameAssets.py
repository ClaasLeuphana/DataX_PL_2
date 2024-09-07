import pygame
import os
import random
import json


# Funktion zum Laden von Bildern
def load_image(filename):
    return pygame.image.load(os.path.join("Grafiken", filename))

# Funktion zum Laden von Sounds
def load_sound(filename):
    return pygame.mixer.Sound(os.path.join("Sounds", filename))

class GameAssets:
    def __init__(self):
        # Initialisiere den Mixer
        pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=4096)
        pygame.mixer.music.load(os.path.join("Sounds", "main-menu.mp3"))

        # Lade Lautstärkewerte aus Datei oder setze auf Standardwerte
        self.load_volume_settings()

        # Setze die Musiklautstärke und starte die Musik
        pygame.mixer.music.set_volume(self._music_volume)
        pygame.mixer.music.play(-1)  # Endlosschleife

        # Lade die Bilder und Sounds
        self.load_assets()

    def load_assets(self):
        """Lädt alle Bilder und Sounds und speichert sie als Instanzvariablen."""
        # Laden der Bilder

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
        self.background = load_image("Background.png")  # Hintergrundbild

        # Laden der Sounds
        self.card_turn_sfx = load_sound("flipcard.mp3")
        self.card_turn_sfx.set_volume(self._sfx_volume)

    @property
    def music_volume(self):
        return self._music_volume

    @music_volume.setter
    def music_volume(self, volume):
        self._music_volume = volume
        pygame.mixer.music.set_volume(volume)
        self.save_volume_settings()  # Lautstärke speichern

    @property
    def sfx_volume(self):
        return self._sfx_volume

    @sfx_volume.setter
    def sfx_volume(self, volume):
        self._sfx_volume = volume
        self.card_turn_sfx.set_volume(volume)
        self.save_volume_settings()  # Lautstärke speichern

    def set_music_volume(self, volume):
        self.music_volume = volume

    def set_sfx_volume(self, volume):
        self.sfx_volume = volume

    def save_volume_settings(self):
        """Speichert die Lautstärke-Einstellungen in einer Datei."""
        with open('volume_settings.json', 'w') as file:
            json.dump({
                'music_volume': self._music_volume,
                'sfx_volume': self._sfx_volume
            }, file)

    def load_volume_settings(self):
        """Lädt die Lautstärke-Einstellungen aus einer Datei."""
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
        self.value = value
        self.visible = visible
        self.assets = assets
        self.highlighted = highlighted
        self.elim = elim

    def get_image(self):
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


# Alle Spielkarten
class Deck:
    def __init__(self, assets):
        self.assets = assets  # Speichern Sie die GameAssets-Instanz
        self.cards = self.generate_deck()
        self.shuffle()

    def generate_deck(self):
        cards = []
        for value in range(1, 13):
            cards.extend([Card(value, self.assets) for _ in range(10)])
        cards.extend([Card(-1, self.assets) for _ in range(10)])
        cards.extend([Card(0, self.assets) for _ in range(15)])
        cards.extend([Card(-2, self.assets) for _ in range(5)])
        return cards


    def shuffle(self):
        random.shuffle(self.cards)

    def draw_card(self):
        if self.cards:
            return self.cards.pop()
        return None

    def turn_top_card(self, stack):
        if self.cards:
            top_card = self.cards.pop()
            top_card.visible = True
            stack.add_card(top_card)

    def turn_card(self, card):
        if card is not None:
            card.visible = True
            self.assets.card_turn_sfx.play()

    def deal(self, playercount):
        players_hands = [[] for _ in range(playercount)]
        for _ in range(12):
            for player_hand in players_hands:
                player_hand.append(self.draw_card())
        return players_hands

    def draw(self, stack):
        """Bewegt die oberste Karte des Decks auf den Stack und dreht sie um."""
        if self.cards:
            top_card = self.cards.pop()
            top_card.visible = True
            stack.add_card(top_card)

    def __len__(self):
        return len(self.cards)


# Mittelstapel von dem die Spieler Karten ziehen können
class Stack:
    def __init__(self):
        self.cards = []

    def add_card(self, card):
        """Fügt eine Karte zum Stapel hinzu."""
        self.cards.append(card)

    def get_top_card(self):
        """Gibt die oberste Karte des Stapels zurück (falls vorhanden)."""
        if self.cards:
            return self.cards[-1]
        return None

    def get_second_top_card(self):
        """Gibt die zweitoberste Karte des Stapels zurück (falls vorhanden)."""
        if len(self.cards) > 1:
            return self.cards[-2]
        return None

    def clear(self):
        """Entfernt alle Karten vom Stapel."""
        self.cards.clear()

    def draw(self):
        """Entfernt und gibt die oberste Karte des Stapels zurück. Sichtbarkeit wird umgeschaltet."""
        if self.cards:
            top_card = self.cards.pop()
            top_card.visible = not top_card.visible
            return top_card
        return None

    def turn_second_top_card(self):
        """Schaltet die Sichtbarkeit der zweitobersten Karte um (falls vorhanden)."""
        if len(self.cards) > 1:
            self.cards[-2].visible = not self.cards[-2].visible

    def peek(self):
        """Gibt die oberste Karte des Stacks zurück, ohne sie zu entfernen oder ihre Sichtbarkeit zu ändern."""
        if self.cards:
            return self.cards[-1]
        return None

    def is_empty(self):
        """Überprüft, ob der Stapel leer ist."""
        return len(self.cards) == 0


class Button:
    def __init__(self, text, x, y, width, height, font, text_color, button_color, action=None):
        self.text = text
        self.rect = pygame.Rect(x, y, width, height)
        self.font = font
        self.text_color = text_color
        self.button_color = button_color
        self.action = action

    def draw(self, surface):
        pygame.draw.rect(surface, self.button_color, self.rect)
        text_surface, text_rect = self.font.render(self.text, True, self.text_color)
        text_rect.center = self.rect.center
        surface.blit(text_surface, text_rect)

    def check_click(self, pos):
        if self.rect.collidepoint(pos):
            if self.action:
                self.action()
            return True
        return False


