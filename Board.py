import pygame

# pygame.init()
screen = pygame.display.set_mode((500, 600), pygame.RESIZABLE)

clock = pygame.time.Clock()

current_player = 1

cards_Player1 = [(True, "null") for _ in range(12)] # List of all cards of player , each card is a tuple with a boolean and a string, the boolean is True if the card is visible, False if not and the string is the Value of the card
cards_Player2 = [(True, "null") for _ in range(12)]

Board = pygame.image.load("C:\\Users\\claas\\.Dev\\Leuphana\\Datax\\MainProject\\Grafiken\\Board.png")
CardBack = pygame.image.load("C:\\Users\\claas\\.Dev\\Leuphana\\Datax\\MainProject\\Grafiken\\CardBack.png")
Card12 = pygame.image.load("C:\\Users\\claas\\.Dev\\Leuphana\\Datax\\MainProject\\Grafiken\\Card12.png")
Card11 = pygame.image.load("C:\\Users\\claas\\.Dev\\Leuphana\\Datax\\MainProject\\Grafiken\\Card11.png")
Card10 = pygame.image.load("C:\\Users\\claas\\.Dev\\Leuphana\\Datax\\MainProject\\Grafiken\\Card10.png")
Card9 = pygame.image.load("C:\\Users\\claas\\.Dev\\Leuphana\\Datax\\MainProject\\Grafiken\\Card9.png")
Card8 = pygame.image.load("C:\\Users\\claas\\.Dev\\Leuphana\\Datax\\MainProject\\Grafiken\\Card8.png")
Card7 = pygame.image.load("C:\\Users\\claas\\.Dev\\Leuphana\\Datax\\MainProject\\Grafiken\\Card7.png")
Card6 = pygame.image.load("C:\\Users\\claas\\.Dev\\Leuphana\\Datax\\MainProject\\Grafiken\\Card6.png")
Card5 = pygame.image.load("C:\\Users\\claas\\.Dev\\Leuphana\\Datax\\MainProject\\Grafiken\\Card5.png")
Card4 = pygame.image.load("C:\\Users\\claas\\.Dev\\Leuphana\\Datax\\MainProject\\Grafiken\\Card4.png")
Card3 = pygame.image.load("C:\\Users\\claas\\.Dev\\Leuphana\\Datax\\MainProject\\Grafiken\\Card3.png")
Card2 = pygame.image.load("C:\\Users\\claas\\.Dev\\Leuphana\\Datax\\MainProject\\Grafiken\\Card2.png")
Card1 = pygame.image.load("C:\\Users\\claas\\.Dev\\Leuphana\\Datax\\MainProject\\Grafiken\\Card1.png")
Card0 = pygame.image.load("C:\\Users\\claas\\.Dev\\Leuphana\\Datax\\MainProject\\Grafiken\\Card0.png")
CardN1 = pygame.image.load("C:\\Users\\claas\\.Dev\\Leuphana\\Datax\\MainProject\\Grafiken\\CardN1.png")
CardN2 = pygame.image.load("C:\\Users\\claas\\.Dev\\Leuphana\\Datax\\MainProject\\Grafiken\\CardN2.png")
#card draw =[pygame.image.laod("C:\\Users\\claas\\.Dev\\Leuphana\\Datax\\MainProject\\Grafiken\\CDraw1.png"),...,pygame.image.laod("C:\\Users\\claas\\.Dev\\Leuphana\\Datax\\MainProject\\Grafiken\\CDrawx.png")
#card flip
#stack cards -> KArtenstapel

pygame.display.set_caption("Kartenspiel")

# Function to get the current measurements of a card
def get_card_measurements():
    card_width = screen.get_width() / 10
    card_height = screen.get_height() / 10
    card_gap = card_width / 20
    return card_width, card_height, card_gap


# Function to update a position in the list of cards of current player
def update_card_data(index, boolean_value, string_value):
    if current_player == 1:
        card_positions = cards_Player1
    else:
        card_positions = cards_Player2

    if 0 <= index < len(card_positions):
        card_positions[index] = (boolean_value, string_value)
    else:
        print("Index out of range")

# Function to get the data of a card in the list of cards of current player
def get_card_data(index):
    if current_player == 1:
        card_positions = cards_Player1
    else:
        card_positions = cards_Player2

    if 0 <= index < len(card_positions):
        return card_positions[index]
    else:
        print("Index out of range")
        return None

def get_card_icon(index):
    if current_player == 1:
        cards = cards_Player1
    else:
        cards = cards_Player2
    if cards [index][0]==True:
        return CardBack
    elif cards[0] [index] == CardN2:
        return CardN2
    elif cards[0] [index] == CardN1:
        return CardN1
    elif cards[0] [index] == Card0:
        return Card0
    elif cards[0] [index] == Card1:
        return Card1
    elif cards[0] [index] == Card2:
        return Card2
    elif cards[0] [index] == Card3:
        return Card3
    elif cards[0] [index] == Card4:
        return Card4
    elif cards[0] [index] == Card5:
        return Card5
    elif cards[0] [index] == Card6:
        return Card6
    elif cards[0] [index] == Card7:
        return Card7
    elif cards[0] [index] == Card8:
        return Card8
    elif cards[0] [index] == Card9:
        return Card9
    elif cards[0] [index] == Card10:
        return Card10
    elif cards[0] [index] == Card11:
        return Card11
    elif cards[0] [index] == Card12:
        return Card12


def draw_stack_cards():
    card_width, card_height, card_gap = get_card_measurements()
    scaled_board = pygame.transform.scale(CardBack, (screen.get_width()/10, screen.get_height()/10))
    screen.blit(scaled_board, (screen.get_width() / 2 - card_width - card_gap / 2, screen.get_height() / 2 - card_height/2))  # Draw the scaled Cards
    screen.blit(scaled_board, (screen.get_width() / 2 + card_gap / 2, screen.get_height() / 2 - card_height/2))  # Draw the scaled Cards
    pygame.display.flip()

def draw_cards_player1():
    card_width, card_height, card_gap = get_card_measurements()
    start_x = screen.get_width() / 2 - 2 * (card_width) - 2.5 * card_gap
    start_y = screen.get_height() - 3 * (card_height + card_gap)

    for row in range(3):
        for col in range(4):
            x = start_x + col * (card_width + card_gap)
            y = start_y + row * (card_height + card_gap)
            scaled_card_back = pygame.transform.scale(CardBack, (int(card_width), int(card_height)))
            screen.blit(scaled_card_back, (x, y))
    pygame.display.flip()

def draw_cards_player2():
    card_width, card_height, card_gap = get_card_measurements()
    start_x = screen.get_width() / 2 - 2 * (card_width) - 2.5 * card_gap
    start_y = card_gap

    for row in range(3):
        for col in range(4):
            index = row + col
            card_icon = get_card_icon(index)
            x = start_x + col * (card_width + card_gap)
            y = start_y + row * (card_height + card_gap)
            scaled_card_back = pygame.transform.scale(card_icon, (int(card_width), int(card_height)))
            screen.blit(scaled_card_back, (x, y))
    pygame.display.flip()

def draw_field():
    # Scale the background image to the size of the window
    scaled_board = pygame.transform.scale(Board, (screen.get_width(), screen.get_height()))
    screen.blit(scaled_board, (0, 0))  # Draw the scaled background image
    pygame.display.flip()
    draw_stack_cards()
    draw_cards_player1()
    draw_cards_player2()


