import pygame
from .base import State
from GameAssets import *

class Gameplay(State):
    def __init__(self):
        super(Gameplay, self).__init__()
        self.player_count = 1
        self.font = pygame.font.Font(None, 50)
        self.screen = pygame.display.get_surface()
        self.screen_rect = self.screen.get_rect()

    def get_card_measurements(self):
        self.card_width = self.screen.get_width() / 22
        self.card_height = self.card_width * 1.5
        self.card_gap = self.card_width / 20
        return self.card_width, self.card_height, self.card_gap

    def startup(self, persistent):
        self.persist = persistent
        self.player_count = self.persist.get('player_count', 1)
        self.deck = Deck()  # Erstelle und mische das Deck
        self.players_hands = self.deck.deal(self.player_count)

        for i, hand in enumerate(self.players_hands):
            print(f"Spieler {i + 1}: {[card.value for card in hand]}")


    def update(self, dt):
        pass  # Gameplay-Logik hier

    def draw_stack(self):
        card_width, card_height, card_gap = self.get_card_measurements()
        x = self.screen.get_width() / 2 - (card_width + card_gap / 2)
        y = self.screen.get_height() / 2 - card_height / 2

        card_surface = pygame.transform.scale(GameAssets.CardBack, (int(card_width), int(card_height)))
        self.screen.blit(card_surface, (x, y))
        pygame.display.flip()

    def draw_player_hand(self, player_index, total_players):
        card_width, card_height, card_gap = self.get_card_measurements()

        rows = 3
        cols = 4

        if player_index == 0:
            start_x = self.screen.get_width() / 2 - cols / 2 * (card_width + card_gap)
            start_y = self.screen.get_height() - rows* (card_height + card_gap)
            rotation_angle = 0  # Keine Rotation
        elif player_index == 1:
            start_x = card_gap
            start_y = self.screen.get_height() / 2 - (cols / 2) * (card_width + card_gap) + card_width + card_gap
            rotation_angle = 90  # 90 Grad Rotation für die Karten am linken Bildschirmrand
        elif player_index == 2:
            start_x = self.screen.get_width() / 2 - (cols / 2) * (card_width + card_gap)
            start_y = card_gap
            rotation_angle = 0  # Keine Rotation
        elif player_index == 3:
            start_x = self.screen.get_width() - (cols + 1) * (card_width + card_gap)
            start_y = self.screen.get_height() / 2 - (cols / 2) * (card_width + card_gap)
            rotation_angle = 270  # 270 Grad Rotation für die Karten am rechten Bildschirmrand

        for row in range(rows):
            for col in range(cols):
                x = start_x + col * (card_width + card_gap)
                y = start_y + row * (card_height + card_gap)

                card_surface = pygame.transform.scale(GameAssets.CardBack, (int(card_width), int(card_height)))
                if rotation_angle != 0:
                    card_surface = pygame.transform.rotate(card_surface, rotation_angle)

                self.screen.blit(card_surface, (x, y))



    def draw(self, surface):
        surface.fill(pygame.Color("blue"))

        for i in range(self.player_count):
            self.draw_player_hand(i, self.player_count)

        self.draw_stack()
        pygame.display.flip()