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
        value_to_image = {
            -2: GameAssets.CardN2,
            -1: GameAssets.CardN1,
            0: GameAssets.Card0,
            1: GameAssets.Card1,
            2: GameAssets.Card2,
            3: GameAssets.Card3,
            4: GameAssets.Card4,
            5: GameAssets.Card5,
            6: GameAssets.Card6,
            7: GameAssets.Card7,
            8: GameAssets.Card8,
            9: GameAssets.Card9,
            10: GameAssets.Card10,
            11: GameAssets.Card11,
            12: GameAssets.Card12
        }
        return value_to_image.get(self.value, GameAssets.CardBack)


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

    def draw_card(self):
        if self.cards:
            return self.cards.pop()
        else:
            return None

    def turn_top_card(self, stack):
        if self.cards:
            top_card = self.cards.pop()
            top_card.visible = True
            stack.add_card(top_card)

    def turn_card(self, card):
        if card is not None:
            card.visible = True



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


class Stack:
    def __init__(self):
        self.cards = []

    def add_card(self, card):
        self.cards.append(card)


    def get_top_card(self):
        if self.cards:
            return self.cards[-1]
        return None

    def get_second_top_card(self):
        if len(self.cards) > 1:
            return self.cards[-2]
        # ToDo

    def clear(self):
        self.cards.clear()
        # ToDo

    def take_top_card(self):
        if self.cards:
            self.cards[-1].visible = not self.cards[-1].visible
            # ToDo

    def turn_second_top_card(self):
        if len(self.cards) > 1:
            self.cards[-2].visible = not self.cards[-2].visible
            # ToDo
