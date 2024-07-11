import pygame
import os


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
    Card5 = load_image("Playingcard 5.png")
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
        # card stack
        # hover animation
