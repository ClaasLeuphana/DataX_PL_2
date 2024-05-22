import pygame
import Grafiken
import os


def load_image(filename):
    return pygame.image.load(os.path.join("Grafiken", filename))

class GameAssets:
    # Laden der Bilder
    Board = load_image("Board.png")
    CardBack = load_image("CardBack.png")
    Card12 = load_image("Card12.png")
    Card11 = load_image("Card11.png")
    Card10 = load_image("Card10.png")
    Card9 = load_image("Card9.png")
    Card8 = load_image("Card8.png")
    Card7 = load_image("Card7.png")
    Card6 = load_image("Card6.png")
    Card5 = load_image("Card5.png")
    Card4 = load_image("Card4.png")
    Card3 = load_image("Card3.png")
    Card2 = load_image("Card2.png")
    Card1 = load_image("Card1.png")
    Card0 = load_image("Card0.png")
    CardN1 = load_image("CardN1.png")
    CardN2 = load_image("CardN2.png")
        # draw animation
        # flip animation
        # deal animation
        # card stack
        # hover animation
