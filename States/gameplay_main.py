from .base import State
from GameAssets import *


class Gameplay(State):
    def __init__(self):
        super(Gameplay, self).__init__()
        self.player_count = 1
        self.current_player = 0
        self.font = pygame.font.Font(None, 50)
        self.screen = pygame.display.get_surface()
        self.screen_rect = self.screen.get_rect()

    def startup(self, persistent):
        self.persist = persistent
        self.player_count = self.persist.get('player_count', 1)
        self.current_player = 0
        self.deck = Deck()
        self.stack = Stack()
        self.players_hands = self.deck.deal(self.player_count)
        self.deck.turn_top_card(self.stack)

        for i, hand in enumerate(self.players_hands):
            print(f"Spieler {i + 1}: {[card.value for card in hand]}")

    def get_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.handle_mouse_event(event)

    def handle_mouse_event(self, event):
        mouse_pos = event.pos
        selected_card = self.get_card_at_pos(self.current_player, mouse_pos)
        if selected_card is not None:
            card = self.players_hands[self.current_player][selected_card]
            if not card.visible:
                self.deck.turn_card(card)
                self.end_turn()

    def get_card_at_pos(self, player_index, pos):
        card_width, card_height, card_gap = self.get_card_measurements()
        rows = 3
        cols = 4

        if player_index == 0:  # Spieler unten
            start_x = self.screen.get_width() / 2 - cols / 2 * (card_width + card_gap)
            start_y = self.screen.get_height() - rows * (card_height + card_gap)
            rotation_angle = 0
        elif player_index == 1:  # Spieler links
            start_x = card_gap
            start_y = self.screen.get_height() / 2 - (cols / 2) * (card_width + card_gap)
            rotation_angle = 90
        elif player_index == 2:  # Spieler oben
            start_x = self.screen.get_width() / 2 - (cols / 2) * (card_width + card_gap)
            start_y = card_gap
            rotation_angle = 0
        elif player_index == 3:  # Spieler rechts
            start_x = self.screen.get_width() - rows * (card_height + card_gap)
            start_y = self.screen.get_height() / 2 - (cols / 2) * (card_width + card_gap)
            rotation_angle = 270

        for row in range(rows):
            for col in range(cols):
                if player_index == 0 or player_index == 2:  # Spieler unten oder oben
                    x = start_x + col * (card_width + card_gap)
                    y = start_y + row * (card_height + card_gap)
                    card_rect = pygame.Rect(x, y, card_width, card_height)
                else:  # Spieler links oder rechts
                    x = start_x + row * (card_height + card_gap)
                    y = start_y + col * (card_width + card_gap)
                    card_rect = pygame.Rect(x, y, card_height, card_width)  # Vertausche Breite und Höhe

                if card_rect.collidepoint(pos):
                    return row * cols + col

        return None

    def end_turn(self):
        self.current_player = (self.current_player + 1) % self.player_count

    def get_card_measurements(self):
        self.card_width = self.screen.get_width() / 22
        self.card_height = self.card_width * 1.5
        self.card_gap = self.card_width / 20
        return self.card_width, self.card_height, self.card_gap

    def draw(self, surface):
        surface.fill(pygame.Color("blue"))

        for i in range(self.player_count):
            self.draw_player_hand(i, self.player_count)

        self.draw_deck()
        self.draw_stack()

    def display_current_player(self, surface):
        text = self.font.render(f"Player {self.current_player + 1}'s turn", True, pygame.Color("white"))
        surface.blit(text, (10, 10))

    def draw_deck(self):
        card_width, card_height, card_gap = self.get_card_measurements()
        x = self.screen.get_width() / 2 - (card_width + card_gap / 2)
        y = self.screen.get_height() / 2 - card_height / 2

        card_surface = pygame.transform.scale(GameAssets.CardBack, (int(card_width), int(card_height)))
        self.screen.blit(card_surface, (x, y))

    def draw_stack(self):
        card_width, card_height, card_gap = self.get_card_measurements()
        x = self.screen.get_width() / 2 + card_gap / 2
        y = self.screen.get_height() / 2 - card_height / 2

        card = self.stack.cards[-1]
        card_image = Card.get_image(card)
        card_surface = pygame.transform.scale(card_image, (int(card_width), int(card_height)))
        self.screen.blit(card_surface, (x, y))

    def draw_player_hand(self, player_index, total_players):
        card_width, card_height, card_gap = self.get_card_measurements()

        rows = 3
        cols = 4

        if player_index == 0:
            start_x = self.screen.get_width() / 2 - cols / 2 * (card_width + card_gap)
            start_y = self.screen.get_height() - rows * (card_height + card_gap)
            rotation_angle = 0
        elif player_index == 1:
            start_x = card_gap
            start_y = self.screen.get_height() / 2 - (cols / 2) * (card_width + card_gap) + card_gap
            rotation_angle = 90
        elif player_index == 2:
            start_x = self.screen.get_width() / 2 - (cols / 2) * (card_width + card_gap)
            start_y = card_gap
            rotation_angle = 0
        elif player_index == 3:
            start_x = self.screen.get_width() - rows * (card_height + card_gap)
            start_y = self.screen.get_height() / 2 - (cols / 2) * (card_width + card_gap)
            rotation_angle = 270

        for row in range(rows):
            for col in range(cols):
                if player_index == 0 or player_index == 2:
                    x = start_x + col * (card_width + card_gap)
                    y = start_y + row * (card_height + card_gap)
                else:
                    x = start_x + row * (card_height + card_gap)
                    y = start_y + col * (card_width + card_gap)

                card = self.players_hands[player_index][row * cols + col]
                card_image = card.get_image()  # Holen des richtigen Bildes basierend auf dem visible-Wert
                card_surface = pygame.transform.scale(card_image, (int(card_width), int(card_height)))
                if rotation_angle != 0:
                    card_surface = pygame.transform.rotate(card_surface, rotation_angle)

                self.screen.blit(card_surface, (x, y))
