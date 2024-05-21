import pygame
import GameAssets
import Player
class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((500, 600), pygame.RESIZABLE)
        pygame.display.set_caption("Kartenspiel")
        self.clock = pygame.time.Clock()
        self.current_player = 1
        self.players = [Player.Player(1), Player.Player(2)]


#Funktion um die aktuellen Maße einer Karte zu bekommen
    def get_card_measurements(self):
        card_width = self.screen.get_width() / 10 #holt sich die Breite des Fensters und teilt sie durch 10
        card_height = self.screen.get_height() / 10 #holt sich die Höhe des Fensters und teilt sie durch 10
        card_gap = card_width / 20 #berechnet den Abstand zwischen den Karten
        return card_width, card_height, card_gap #gibt die Maße zurück

#Ziechen des Kartenstapels
    def draw_stack_cards(self):
        card_width, card_height, card_gap = self.get_card_measurements() # holt sich die Maße der Karten aktuell zu screengröße
        scaled_card_back = pygame.transform.scale(GameAssets.GameAssets.CardBack, (int(card_width), int(card_height))) #holst Grafik für Kartenstapel und skaliert sie
        self.screen.blit(scaled_card_back, (self.screen.get_width() / 2 - card_width - card_gap / 2, self.screen.get_height() / 2 - card_height / 2)) # Draw the scaled Cards 1 (Stapel)
        self.screen.blit(scaled_card_back, (self.screen.get_width() / 2 + card_gap / 2, self.screen.get_height() / 2 - card_height / 2)) # Draw the scaled Cards 2 (später aufgedeckte Karte
        pygame.display.flip() # aktualisiert das Fenster

#Karten der Spieler zeichnen
    def draw_cards(self, player, start_y):
        card_width, card_height, card_gap = self.get_card_measurements()
        start_x = self.screen.get_width() / 2 - 2 * card_width - 2.5 * card_gap

        for row in range(3):
            for col in range(4):
                index = row * 4 + col #berechnet den Index der Karte (0*4 + col = 0 bis 3 1*4 + col = 4 bis 7 2*4 + col = 8 bis 11)
                card = player.get_card(index)
                if card:
                    card_image = card.get_image()
                    x = start_x + col * (card_width + card_gap)
                    y = start_y + row * (card_height + card_gap)
                    scaled_card = pygame.transform.scale(card_image, (int(card_width), int(card_height)))
                    self.screen.blit(scaled_card, (x, y))
        pygame.display.flip()

    #Funktion um das Spielfeld zu zeichnen
    def draw_field(self):
        scaled_board = pygame.transform.scale(GameAssets.GameAssets.Board, (self.screen.get_width(), self.screen.get_height())) #holt sich das Spielfeld und skaliert es auf die Größe des Fensters
        self.screen.blit(scaled_board, (0, 0)) #zeichnet das Spielfeld startend bei 0,0 (obere linke Ecke)
        pygame.display.flip() #aktualisiert das Fenster
        self.draw_cards(self.players[0],
                        self.screen.get_height() - 3 * (self.screen.get_height() / 10 + self.screen.get_width() / 200))
        # self.screen.get_height() -> Höhe des Fensters
        # 3 * (self.screen.get_height() / 10 -> berechnet die Höhe von 3 Karten
        # self.screen.get_width() / 200 -> berechnet den Abstand zwischen den Karten (CardGap)
        # 3 * (self.screen.get_height() / 10 + self.screen.get_width() / 200) -> Benötigter Abstand damit die Karten im Fenster bleiben

        self.draw_cards(self.players[1], self.screen.get_width() / 200)