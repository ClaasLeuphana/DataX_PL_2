import pygame
import os
import random


# Funktion um Bilder zu laden
def load_image(filename):
    return pygame.image.load(os.path.join("Grafiken", filename))

class GameAssets:
    # Laden der Bilder
    Board = load_image("Board.png")
    CardBack = load_image("Back of Card.png")
    Card12 = load_image("Playingcard 12.jpg")
    Card11 = load_image("Playingcard 11.jpg")
    Card10 = load_image("Playingcard 10.jpg")
    Card9 = load_image("Playincard 9.png")
    Card8 = load_image("Playingcard 8.jpg")
    Card7 = load_image("Playingcard 7.jpg")
    Card6 = load_image("Playingcard 6.jpg")
    Card5 = load_image("Playingcard 5.jpg")
    Card4 = load_image("Playingcard 4.jpg")
    Card3 = load_image("Playingcard 3.jpg")
    Card2 = load_image("Playingcard 2.png")
    Card1 = load_image("Playingcard 1.png")
    Card0 = load_image("Playingcard 0.png")
    CardN1 = load_image("Playingcard -1.png")
    CardN2 = load_image("Playingcard -2.png")
        # draw animation
        # flip animation
        # deal animation
        # hover animation
class Card:
    def __init__(self, value, visible=False):
        self.value = value
        self.visible = visible

    def get_image(self):
        if not self.visible:
            return GameAssets.CardBack
        return getattr(GameAssets, f'Card{self.value}')


class Deck:
    def __init__(self):
        self.cards = self.generate_deck()
        self.shuffle()

    def generate_deck(self):
        cards = []
        # 10 cards each for values 1 to 12
        for value in range(1, 13):
            cards.extend([Card(value) for _ in range(10)])
        # 10 cards with value -1
        cards.extend([Card(-1) for _ in range(10)])
        # 15 cards with value 0
        cards.extend([Card(0) for _ in range(15)])
        # 5 cards with value -2
        cards.extend([Card(-2) for _ in range(5)])
        return cards

    def shuffle(self):
        random.shuffle(self.cards)

    def draw_new_card(self):
        if self.cards:
            return self.cards.pop()
        else:
            return None

    def deal(self, playercount):
        players_hands = [[] for _ in range(playercount)]
        for _ in range(12):
            for player_hand in players_hands:
                player_hand.append(self.draw_card())
        return players_hands
    def add_card(self, card):
        self.cards.append(card)

    def __len__(self):
        return len(self.cards)
