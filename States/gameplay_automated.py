
import time
from States.base import State
from GameAssets import *


def remove_three_in_a_row(cards):
    """Setzt elim der Karten auf True."""
    for card in cards:
        card.elim = True

class Gameplay_Automated(State):
    def __init__(self, assets=None):
        super(Gameplay_Automated, self).__init__(assets=assets)
        self.assets = assets
        self.player_count = 1
        self.active_player_index = 0
        self.current_player = 0
        self.cards_turned = 0
        self.initial_round = True
        self.stack_clicked = False
        self.deck_clicked = False
        self.deck_action_taken = False
        self.font = pygame.font.Font(None, 50)
        self.screen = pygame.display.get_surface()
        self.screen_rect = self.screen.get_rect()
        self.card_width, self.card_height, self.card_gap = self.get_card_measurements()
        self.selected_stack_card = None
        self.first_to_finish = None
        self.stack= Stack()
        self.deck= Deck(assets=self.assets)
        self.last_turn_active = False
        self.last_turn_player = None
        self.turn_counter = 0
        self.player_names = []  # Add this line

    def resize(self, width, height):
        """Passt die Spielanzeige an die neue Fenstergröße an."""
        self.screen_rect = pygame.Rect(0, 0, width, height)
        self.screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
        self.card_width, self.card_height, self.card_gap = self.get_card_measurements()

    def get_card_measurements(self):
        """Berechnet die Maße und Abstände der Karten basierend auf der Bildschirmgröße."""
        self.card_width = self.screen.get_width() / 25
        self.card_height = self.card_width * 1.5
        self.card_gap = self.card_width / 12
        return self.card_width, self.card_height, self.card_gap

    def startup(self, persistent):
        self.persist = persistent
        self.player_count = self.persist.get('player_count', 1)
        self.current_player = 0
        self.assets = self.persist.get('assets', GameAssets())
        self.bot_difficulties = self.persist.get('bot_difficulties', ["Medium"] * 4)
        self.player_names = [self.persist.get('player_name', 'Player 1')]
        self.bot_names = self.persist.get('bot_names', [])  # Add this line to retrieve bot names
        print(f"Debug: Player names retrieved from persistent: {self.player_names}, Bot names retrieved from persistent: {self.bot_names}")
        self.GameStart()

    def GameStart(self):
        """Bereitet alles für den Spielstart vor."""
        self.deck = Deck(assets=self.assets)
        self.stack = Stack()
        self.players_hands = self.deck.deal(self.player_count)
        self.deck.turn_top_card(self.stack)

        for i, hand in enumerate(self.players_hands):
            print(f"Spieler {i + 1}: {[card.value for card in hand]}")

        self.cards_turned = 0
        self.initial_round = True

    def determine_starting_player(self):
        """Bestimmt den Spieler, der beginnt, basierend auf der höchsten Summe der ersten zwei aufgedeckten Karten."""
        highest_sum = -1
        starting_player = 0

        for i in range(self.player_count):
            visible_cards = [card for card in self.players_hands[i] if card.visible]
            if len(visible_cards) >= 2:
                card_sum = visible_cards[0].value + visible_cards[1].value
                if card_sum > highest_sum:
                    highest_sum = card_sum
                    starting_player = i
        self.draw(self.screen)
        self.current_player = starting_player

        self.show_starting_player_message(starting_player + 1)

    def show_starting_player_message(self, player_number):
        """Zeigt eine Nachricht an, welcher Spieler beginnt, und wartet 5 Sekunden."""
        message = f"Spieler {player_number} beginnt!"
        text_surface = self.font.render(message, True, pygame.Color("yellow"))
        text_rect = text_surface.get_rect(center=self.screen_rect.center)

        background_rect = pygame.Rect(
            text_rect.left - 10,
            text_rect.top - 5,
            text_rect.width + 20,
            text_rect.height + 10
        )

        pygame.draw.rect(self.screen, pygame.Color("black"), background_rect)
        self.screen.blit(text_surface, text_rect)
        pygame.display.flip()
        pygame.time.wait(5000)

    def get_event(self, event=None):
        if self.initial_round:
            if self.current_player == 0:
                if event and event.type == pygame.MOUSEBUTTONDOWN:
                    self.handle_initial_turn(event)
            else:
                self.automated_initial_turn()
        else:
            if self.current_player == 0:
                if event and event.type == pygame.MOUSEBUTTONDOWN:
                    self.gameLogic(event)
            else:
                self.automated_player_turn()

    def handle_initial_turn(self, event=None):
        if self.current_player == 0 and event is not None:
            mouse_pos = event.pos
            selected_card = self.get_card_at_pos(self.current_player, mouse_pos)
            if selected_card is not None:
                card = self.players_hands[self.current_player][selected_card]
                if not card.visible:
                    self.deck.turn_card(card)
                    self.cards_turned += 1
                    if self.cards_turned >= 2:
                        self.end_turn()
                        self.cards_turned = 0
                        if self.current_player == 0:
                            self.initial_round = False
                            self.determine_starting_player()
        elif self.current_player != 0:
            self.automated_initial_turn()


    def gameLogic(self, event):
        """Zentraler Ablauf der Spiellogik ruft die einzelnen Schritte auf."""
        mouse_pos = event.pos

        if self.is_over_deck(mouse_pos):
            self.handle_deck_click()
        elif self.is_over_stack(mouse_pos):
            self.handle_stack_click()
        else:
            if self.selected_stack_card:
                selected_card_index = self.get_card_at_pos(self.current_player, mouse_pos)
                if selected_card_index is not None:
                    self.swap_with_stack(selected_card_index)
                    self.selected_stack_card = None
                    self.stack_clicked = False

                    if self.check_all_cards_visible(self.current_player):
                        self.start_last_turn()
                    else:
                        self.end_turn()

                else:
                    self.selected_stack_card = None
                    self.stack_clicked = False

            else:
                selected_card_index = self.get_card_at_pos(self.current_player, mouse_pos)
                if selected_card_index is not None:
                    card = self.players_hands[self.current_player][selected_card_index]
                    if not card.visible:
                        self.deck.turn_card(card)
                        self.check_three_in_a_row(self.current_player)

                    if self.check_all_cards_visible(self.current_player):
                        self.start_last_turn()
                    else:
                        self.end_turn()

    def start_last_turn(self):
        """Aktiviert den letzten Zug für alle Spieler."""
        if not self.last_turn_active:
            self.last_turn_active = True
            self.last_turn_player = self.current_player
            self.turn_counter = 0
            print(f"Spieler {self.last_turn_player + 1} hat alle Karten umgedreht. Letzte Runde beginnt!")

        self.end_turn()  # Setze den Zug fort

    def handle_deck_click(self):
        """Handles the event when the deck is clicked."""
        top_card = self.deck.draw(self.stack)
        if top_card:
            top_card.visible = True
            self.save_top_card_value()

    def handle_stack_click(self):
        """Wählt die oberste Karte des Stacks aus oder tauscht Karten, wenn eine Handkarte ausgewählt wird."""
        if not self.stack_clicked:
            self.stack_clicked = True
            self.selected_stack_card = self.stack.peek()
        else:
            mouse_pos = pygame.mouse.get_pos()
            selected_card_index = self.get_card_at_pos(self.current_player, mouse_pos)
            if selected_card_index is not None:
                player_card = self.players_hands[self.current_player][selected_card_index]
                self.players_hands[self.current_player][selected_card_index] = self.selected_stack_card
                self.stack.add_card(player_card)
                self.selected_stack_card = None
                self.stack_clicked = False
                self.deck_action_taken = True
            else:
                self.selected_stack_card = None
                self.stack_clicked = False

    def swap_with_stack(self, selected_card_index):
        """Tauscht die ausgewählte Karte des Spielers mit der obersten Karte des Stacks."""
        player_card = self.players_hands[self.current_player][selected_card_index]
        top_stack_card = self.stack.draw()
        if top_stack_card:
            top_stack_card.visible = True
        if player_card:
            player_card.visible = True
            self.stack.add_card(player_card)
        self.players_hands[self.current_player][selected_card_index] = top_stack_card
        self.check_three_in_a_row(self.current_player)

    def turn_top_card(self):
        """Draws the top card from the deck and places it on the stack."""
        top_card = self.deck.draw(self.stack)
        if top_card:
            top_card.visible = True
            self.save_top_card_value()

    def save_top_card_value(self):
        """Updates the saved value of the top card on the stack."""
        top_card = self.stack.peek()
        if top_card:
            self.saved_value = top_card.value
        else:
            self.saved_value = None

    def automated_initial_turn(self):
        """Automatische Aufdeckung von zwei Karten durch einen KI-Spieler in der Anfangsrunde."""
        visible_cards = [card for card in self.players_hands[self.current_player] if card.visible]
        if len(visible_cards) < 2:
            hidden_cards = [index for index, card in enumerate(self.players_hands[self.current_player]) if
                            not card.visible]
            selected_indices = random.sample(hidden_cards, k=2)
            for index in selected_indices:
                card = self.players_hands[self.current_player][index]
                if not card.visible:
                    self.deck.turn_card(card)
                    self.cards_turned += 1
            self.end_turn()
            self.cards_turned = 0
            if self.current_player == 0:
                self.initial_round = False
                self.determine_starting_player()

    def automated_player_turn_easy(self):
        """Einfache Automatisierung für den Zug eines Bots."""
        if self.current_player != 0:
            hand = self.players_hands[self.current_player]
            hidden_cards = [index for index, card in enumerate(hand) if not card.visible]
            visible_cards = [card for card in hand if card.visible]

            value_top_card = self.stack.peek().value if self.stack.peek() else None

            if value_top_card is not None:
                if -2 <= value_top_card <= 4:
                    self.select_stack = True

                    open_cards = [index for index, card in enumerate(hand) if card.visible and 5 <= card.value <= 12]

                    if open_cards:
                        selected_card_index = random.choice(open_cards)
                        self.swap_with_stack(selected_card_index)
                    else:
                        if hidden_cards:
                            selected_card_index = random.choice(hidden_cards)
                            self.swap_with_stack(selected_card_index)

                elif 5 <= value_top_card <= 12:
                    self.select_deck = True
                    self.turn_top_card()
                    self.deck_action_taken = True

                    value_top_card = self.stack.peek().value if self.stack.peek() else None

                    if value_top_card is not None:
                        if -2 <= value_top_card <= 4:
                            self.select_stack = True

                            open_cards = [index for index, card in enumerate(hand) if
                                          card.visible and 5 <= card.value <= 12]

                            if open_cards:
                                selected_card_index = random.choice(open_cards)
                                self.swap_with_stack(selected_card_index)
                            else:
                                if hidden_cards:
                                    selected_card_index = random.choice(hidden_cards)
                                    self.swap_with_stack(selected_card_index)
                        elif 5 <= value_top_card <= 12:
                            if hidden_cards:
                                card_to_turn_index = random.choice(hidden_cards)
                                card_to_turn = hand[card_to_turn_index]
                                self.deck.turn_card(card_to_turn)

            self.check_three_in_a_row(self.current_player)

            if self.check_all_cards_visible(self.current_player):
                self.start_last_turn()
            else:
                self.end_turn()
            print(f"Automated player {self.current_player} ends turn")

    def automated_player_turn_medium(self):
        """Automatisierung für den Zug eines Bots im Medium-Schwierigkeitsgrad."""
        if self.current_player != 0:
            hand = self.players_hands[self.current_player]
            hidden_cards = [index for index, card in enumerate(hand) if not card.visible]
            visible_cards = [card for card in hand if card.visible]

            value_top_card = self.stack.peek().value if self.stack.peek() else None

            if value_top_card is not None:
                if -2 <= value_top_card <= 4:
                    self.select_stack = True

                    open_cards = [index for index, card in enumerate(hand) if card.visible and 5 <= card.value <= 12]

                    if open_cards:
                        selected_card_index = random.choice(open_cards)
                        self.swap_with_stack(selected_card_index)
                    else:
                        if hidden_cards:
                            selected_card_index = random.choice(hidden_cards)
                            self.swap_with_stack(selected_card_index)

                    column_values = [card.value for card in visible_cards]
                    if column_values.count(-2) >= 2 or column_values.count(-1) >= 2:
                        self.remove_card_from_column_with_value(column_values, -2, -1)

                elif 5 <= value_top_card <= 12:
                    self.select_deck = True
                    self.turn_top_card()
                    self.deck_action_taken = True

                    value_top_card = self.stack.peek().value if self.stack.peek() else None

                    if value_top_card is not None:
                        if -2 <= value_top_card <= 4:
                            self.select_stack = True

                            open_cards = [index for index, card in enumerate(hand) if
                                          card.visible and 5 <= card.value <= 12]

                            if open_cards:
                                selected_card_index = random.choice(open_cards)
                                self.swap_with_stack(selected_card_index)
                            else:
                                if hidden_cards:
                                    selected_card_index = random.choice(hidden_cards)
                                    self.swap_with_stack(selected_card_index)
                        elif 5 <= value_top_card <= 12:
                            open_cards = [card for card in hand if card.visible]
                            column_values = [card.value for card in open_cards]

                            prev_player = (self.current_player - 1) % self.player_count
                            prev_open_cards = [card for card in self.players_hands[prev_player] if card.visible]
                            prev_column_values = [card.value for card in prev_open_cards]

                            if any(card.value == value_top_card for card in open_cards):
                                if not any(v in column_values for v in [-2, -1, -3]):
                                    if any(card.value == value_top_card for card in prev_open_cards):
                                        self.select_stack = True
                                        self.swap_with_stack(self.get_card_index_to_swap(hand, value_top_card))
                                    else:
                                        self.open_random_hidden_card()
                            else:
                                self.open_random_hidden_card()

                            if len(open_cards) >= 11:
                                self.swap_with_highest_value_card_if_needed()

            self.check_three_in_a_row(self.current_player)

            if self.check_all_cards_visible(self.current_player):
                self.start_last_turn()
            else:
                self.end_turn()
            print(f"Automated player {self.current_player} ends turn")

    def automated_player_turn_hard(self):
        """Automatisierung für den Zug eines Bots im Hard-Schwierigkeitsgrad mit Priorisierung des Tauschs höherer Karten."""
        if self.current_player != 0:
            hand = self.players_hands[self.current_player]
            hidden_cards = [index for index, card in enumerate(hand) if not card.visible]
            visible_cards = [card for card in hand if card.visible]

            print(
                f"Player {self.current_player} Hand: {[card.value for card in hand]} (Visible: {[card.value for card in visible_cards]})")

            value_top_card = self.stack.peek().value if self.stack.peek() else None
            print(f"Player {self.current_player} Top Stack Card: {value_top_card}")

            if value_top_card is not None:
                if -2 <= value_top_card <= 4:
                    self.select_stack = True
                    print(f"Player {self.current_player} chooses stack (Card: {value_top_card})")

                    highest_card_index = self.get_highest_visible_card_index(hand)
                    print(
                        f"Player {self.current_player} swaps card at index {highest_card_index} with value {hand[highest_card_index].value}")
                    self.swap_with_stack(highest_card_index)

                elif 5 <= value_top_card <= 12:
                    self.select_deck = True
                    print(f"Player {self.current_player} chooses to draw from the deck")

                    self.turn_top_card()
                    self.deck_action_taken = True

                    value_top_card = self.stack.peek().value if self.stack.peek() else None
                    print(f"Player {self.current_player} new top card from deck: {value_top_card}")

                    if value_top_card is not None and -2 <= value_top_card <= 4:
                        self.select_stack = True
                        highest_card_index = self.get_highest_visible_card_index(hand)
                        print(
                            f"Player {self.current_player} swaps card at index {highest_card_index} with value {hand[highest_card_index].value}")
                        self.swap_with_stack(highest_card_index)
                    else:
                        print(f"Player {self.current_player} reveals a hidden card as no match found")
                        self.open_random_hidden_card()

            self.check_three_in_a_row(self.current_player)

            if self.check_all_cards_visible(self.current_player):
                print(f"Player {self.current_player} has revealed all cards, ending round")
                self.start_last_turn()
            else:
                print(f"Player {self.current_player} ends turn")
                self.end_turn()

    def remove_card_from_column_with_value(self, column_values, *values):
        """Entfernt eine Karte aus einer Spalte, wenn bereits zwei Karten mit den gleichen negativen Werten vorhanden sind."""
        for value in values:
            if column_values.count(value) >= 2:
                for index, card in enumerate(column_values):
                    if card == value:
                        column_values.pop(index)
                        break

    def get_card_index_to_swap(self, hand, value_top_card):
        """Findet den besten Kartenindex in der Hand, um ihn mit der obersten Karte des Stapels zu tauschen."""
        # Suche nach der Karte, die am wenigsten Punkte einbringt oder eine Spalte komplettiert
        visible_cards = [index for index, card in enumerate(hand) if card.visible]
        if visible_cards:
            # Wähle die Karte mit dem größten Unterschied zur Stapelkarte, um hohe Punktwerte zu minimieren
            best_card_index = min(visible_cards, key=lambda i: abs(hand[i].value - value_top_card))
            return best_card_index
        else:
            # Wenn keine Karten aufgedeckt sind, zufällig eine verdeckte Karte wählen
            return random.choice(range(len(hand)))

    def open_random_hidden_card(self):
        """Deckt eine zufällige versteckte Karte in der Hand auf."""
        hand = self.players_hands[self.current_player]
        hidden_cards = [index for index, card in enumerate(hand) if not card.visible]
        if hidden_cards:
            selected_card_index = random.choice(hidden_cards)
            hand[selected_card_index].visible = True
            print(
                f"Automated player {self.current_player} reveals card at index {selected_card_index} with value {hand[selected_card_index].value}")

    def swap_with_highest_value_card_if_needed(self):
        """Tauscht die Karte mit dem höchsten Wert, wenn der Spieler in einer kritischen Phase ist (z.B. 11 Karten aufgedeckt)."""
        hand = self.players_hands[self.current_player]
        visible_cards = [card for card in hand if card.visible]

        # Wenn alle Karten aufgedeckt sind, finde die Karte mit dem höchsten Wert
        if len(visible_cards) >= 11:
            highest_value_card = max(visible_cards, key=lambda card: card.value)
            highest_value_index = hand.index(highest_value_card)

            # Tausche die höchste Karte mit der Stapelkarte
            self.swap_with_stack(highest_value_index)
            print(
                f"Automated player {self.current_player} swaps card at index {highest_value_index} with value {highest_value_card.value}")

    def select_best_card_for_swap(self, hand, value_top_card):
        """Wählt die beste Karte zum Tauschen basierend auf dem Wert der obersten Karte vom Stapel."""
        # Sortiere die offenen Karten nach Wert, um die beste Karte auszuwählen
        visible_cards = [index for index, card in enumerate(hand) if card.visible]
        if visible_cards:
            # Bevorzugen Karten, die den Wert der obersten Karte des Stapels ergänzen
            best_card_index = min(visible_cards, key=lambda i: abs(hand[i].value - value_top_card))
            return best_card_index
        else:
            return random.choice(range(len(hand)))

    def player_has_lowest_score(self, player_index):
        """Prüft, ob der Spieler den niedrigsten Punktestand hat."""
        current_player_score = self.Calculate_player_score(self.players_hands[player_index])
        other_players_scores = [self.Calculate_player_score(hand) for i, hand in enumerate(self.players_hands) if
                                i != player_index]
        return current_player_score <= min(other_players_scores)

    def get_highest_visible_card_index(self, hand):
        """Ermittelt den Index der höchsten sichtbaren Karte."""
        # Finde die sichtbaren Karten
        visible_cards = [card for card in hand if card.visible]

        # Höchste Karte unter den sichtbaren Karten ermitteln
        highest_value = max(visible_cards, key=lambda card: card.value).value

        # Finde den Index der höchsten sichtbaren Karte
        for index, card in enumerate(hand):
            if card.value == highest_value and card.visible:
                return index

    def automated_player_turn(self):
        """Ruft die entsprechende Funktion für den aktuellen Schwierigkeitsgrad des Bots auf."""
        bot_difficulty = self.persist.get('bot_difficulties', ["Medium"] * self.player_count)[self.current_player]
        if bot_difficulty == "Easy":
            self.automated_player_turn_easy()
        elif bot_difficulty == "Medium":
            self.automated_player_turn_medium()
        elif bot_difficulty == "Hard":
            self.automated_player_turn_hard()
        else:
            raise ValueError("Unbekannter Schwierigkeitsgrad")

    #für maus steuerung
    def get_card_at_pos(self, player_index, pos):
        global start_x, start_y
        card_width, card_height, card_gap = self.get_card_measurements()
        rows = 3
        cols = 4

        if player_index == 0:  # Spieler unten
            start_x = self.screen.get_width() / 2 - cols / 2 * (card_width + card_gap)
            start_y = self.screen.get_height() - rows * (card_height + card_gap)
        elif player_index == 1:  # Spieler links
            start_x = card_gap
            start_y = self.screen.get_height() / 2 - (cols / 2) * (card_width + card_gap)
        elif player_index == 2:  # Spieler oben
            start_x = self.screen.get_width() / 2 - (cols / 2) * (card_width + card_gap)
            start_y = card_gap
        elif player_index == 3:  # Spieler rechts
            start_x = self.screen.get_width() - rows * (card_height + card_gap)
            start_y = self.screen.get_height() / 2 - (cols / 2) * (card_width + card_gap)

        for row in range(rows):
            for col in range(cols):
                if player_index == 0 or player_index == 1 or player_index == 2 or player_index == 3:  # Spieler unten oder oben
                    x = start_x + col * (card_width + card_gap)
                    y = start_y + row * (card_height + card_gap)
                    card_rect = pygame.Rect(x, y, card_width, card_height)


                if card_rect.collidepoint(pos):
                    return row * cols + col

        return None

    def is_over_deck(self, pos):
        """Überprüft, ob die Maus über dem Deck ist."""
        card_width, card_height, card_gap = self.get_card_measurements()
        x = self.screen.get_width() / 2 - (card_width + card_gap / 2)
        y = self.screen.get_height() / 2 - card_height / 2
        deck_rect = pygame.Rect(x, y, card_width, card_height)
        return deck_rect.collidepoint(pos)

    def is_over_stack(self, pos):
        """Überprüft, ob die Maus über dem Stack ist."""
        card_width, card_height, card_gap = self.get_card_measurements()
        x = self.screen.get_width() / 2 + card_gap / 2
        y = self.screen.get_height() / 2 - card_height / 2
        stack_rect = pygame.Rect(x, y, card_width, card_height)
        return stack_rect.collidepoint(pos)
#weitere Funktionen
    def end_turn(self):
        """Wechselt zum nächsten Spieler und überprüft, ob die Runde endet."""
        if self.last_turn_active:
            # Erhöhe den Zähler, wenn alle Spieler noch einmal an der Reihe waren
            self.turn_counter += 1
            print(f"Spieler {self.current_player + 1} hat seinen letzten Zug gemacht.")

            # Wenn alle Spieler einschließlich des Startspielers des letzten Zuges dran waren
            if self.turn_counter >= self.player_count:
                print("Letzter Zug abgeschlossen. Runde endet.")
                self.round_over()  # Runde beenden
                return

        # Zum nächsten Spieler wechseln
        self.current_player = (self.current_player + 1) % self.player_count
        self.stack_clicked = False
        self.deck_clicked = False
        self.deck_action_taken = False

    def check_all_cards_visible(self, player_index):
        """Überprüft, ob alle Karten des aktuellen Spielers aufgedeckt sind."""
        all_visible = all(card.visible for card in self.players_hands[player_index])

        if all_visible and self.first_to_finish is None:
            # Speichere den ersten Spieler, der alle Karten umgedreht hat
            self.first_to_finish = player_index + 1  # +1 um den Spieler 1-basiert anzugeben
            self.persist['first_to_finish'] = self.first_to_finish  # Speichere dies in self.persist

        return all_visible

    def check_three_in_a_row(self, player_index):
        """Überprüft, ob drei gleiche Karten in einer vertikalen Reihe des angegebenen Spielers vorhanden sind und
        alle hervorgehoben sind."""
        hand = self.players_hands[player_index]
        rows = 3
        cols = 4

        # Überprüfe alle möglichen 3er-Reihen vertikal
        for col in range(cols):
            for row in range(rows - 2):  # Es gibt nur rows - 2 Möglichkeiten, eine 3er-Reihe zu beginnen
                index1 = row * cols + col
                index2 = (row + 1) * cols + col
                index3 = (row + 2) * cols + col

                if (0 <= index1 < len(hand) and
                        0 <= index2 < len(hand) and
                        0 <= index3 < len(hand)):

                    card1 = hand[index1]
                    card2 = hand[index2]
                    card3 = hand[index3]

                    if card1.value == card2.value == card3.value and -2 <= card1.value and card1.visible and card2.visible and card3.visible:
                        remove_three_in_a_row([card1, card2, card3])


        #alle draw funktionen

#alle draw funktionen
    def draw(self, surface):
        """Zeichnet das Spielfeld, den Stapel, das Deck und die Karten der Spieler."""
        surface.fill(pygame.Color("blue"))

        for i in range(self.player_count):
            self.draw_player_hand(i)

        self.draw_deck()
        self.draw_stack()
        self.draw_player_score()
        pygame.display.flip()

    def draw_deck(self):
        """Zeichnet das Deck auf den Bildschirm."""
        card_width, card_height, card_gap = self.get_card_measurements()
        x = self.screen.get_width() / 2 - (card_width + card_gap / 2)
        y = self.screen.get_height() / 2 - card_height / 2

        card_surface = pygame.transform.scale(self.assets.CardBack, (int(card_width), int(card_height)))
        self.screen.blit(card_surface, (x, y))

    def draw_stack(self):
        """Zeichnet den Stapel auf den Bildschirm."""
        card_width, card_height, card_gap = self.get_card_measurements()
        x = self.screen.get_width() / 2 + card_gap / 2
        y = self.screen.get_height() / 2 - card_height / 2

        if self.stack.cards:
            card = self.stack.cards[-1]
            card_image = card.get_image()
            card_surface = pygame.transform.scale(card_image, (int(card_width), int(card_height)))
            self.screen.blit(card_surface, (x, y))

    def draw_player_hand(self, player_index):
        """Zeichnet die Kartenhand des Spielers auf den Bildschirm."""
        global start_x, start_y, rotation_angle
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
            rotation_angle = 0  # Gleiche Ausrichtung wie Spieler 0
        elif player_index == 2:
            start_x = self.screen.get_width() / 2 - (cols / 2) * (card_width + card_gap)
            start_y = card_gap
            rotation_angle = 0
        elif player_index == 3:
            start_x = self.screen.get_width() - rows * (card_height + card_gap)
            start_y = self.screen.get_height() / 2 - (cols / 2) * (card_width + card_gap)
            rotation_angle = 0  # Gleiche Ausrichtung wie Spieler 0

        for row in range(rows):
            for col in range(cols):
                index = row * cols + col
                card = self.players_hands[player_index][index]

                if card.elim:
                    continue  # Überspringt die eliminierte Karte

                if player_index == 0 or player_index == 1 or player_index == 2 or player_index == 3:
                    x = start_x + col * (card_width + card_gap)
                    y = start_y + row * (card_height + card_gap)


                card_image = card.get_image()

                # Anpassung der Skalierung, wenn die Karte markiert ist
                scale = 1.1 if card.highlighted else 1.0
                card_width_scaled = int(card_width * scale)
                card_height_scaled = int(card_height * scale)

                card_surface = pygame.transform.scale(card_image, (card_width_scaled, card_height_scaled))
                if rotation_angle != 0:
                    card_surface = pygame.transform.rotate(card_surface, rotation_angle)

                self.screen.blit(card_surface, (x, y))

    def Calculate_player_score(self, player_index):
        """Berechnet die Punktzahl eines Spielers basierend auf den offenen Karten."""
        player_score = 0
        for card in self.players_hands[player_index]:
            if card.visible and not card.elim:
                player_score += card.value
        return player_score

    def draw_player_score(self):
        """Zeigt dauerhaft die Punktzahl aller Spieler rechts neben der Spielerhand an."""
        for i in range(self.player_count):

            player_score = self.Calculate_player_score(i)
            if i == 0:
                player_name = self.player_names[i] if i < len(self.player_names) else f"Player {i + 1}"
            else:
                player_name = self.bot_names[i - 1] if i - 1 < len(self.bot_names) else f"Bot {i}"

            # Render the text for the score and name
            score_text = self.font.render(f"Score: {player_score}", True, pygame.Color("white"))
            name_text = self.font.render(player_name, True, pygame.Color("yellow"))

            # Berechne die Position des Textes nahe der Spielerhand
            if i == 0:  # Spieler unten
                x = self.screen.get_width() / 2 + 2 * (self.card_width + self.card_gap)
                y = self.screen.get_height() - 2 * (self.card_height + self.card_gap)
                rotated_score_text = score_text
                rotated_name_text = name_text
            elif i == 1:  # Spieler links
                x = self.card_width * 1 + 5 * self.card_gap
                y = self.screen.get_height() / 2 - 3 * (self.card_width + self.card_gap) + self.card_gap
                rotated_score_text = score_text
                rotated_name_text = name_text
            elif i == 2:  # Spieler oben
                x = self.screen.get_width() / 2 + 2 * (self.card_width + self.card_gap)
                y = 2 * self.card_height
                rotated_score_text = score_text
                rotated_name_text = name_text
            elif i == 3:  # Spieler rechts
                x = self.screen.get_width() - 3 * (self.card_height + self.card_gap)
                y = self.screen.get_height() / 2 - 3 * (self.card_width + self.card_gap) + self.card_gap
                rotated_score_text = score_text
                rotated_name_text = name_text

            # Draw name above the score
            self.screen.blit(rotated_name_text, (x, y - 30))  # Adjust y position for name
            self.screen.blit(rotated_score_text, (x, y))

    def round_over(self):
        """Wechselt den Spielzustand zu 'Round Summary' und berechnet die Punkte."""
        # 1. Aufdecken aller noch nicht aufgedeckten Karten aller Spieler
        for i in range(self.player_count):
            for card in self.players_hands[i]:
                if not card.visible:
                    self.deck.turn_card(card)

        # 2. Pause für 5 Sekunden einfügen
        self.draw(self.screen)  # Aktualisiert den Bildschirm, damit die Spieler die aufgedeckten Karten sehen
        time.sleep(5)

        # 3. Berechne die Punkte und wechsle den Zustand
        current_round_score = []
        for i in range(self.player_count):
            score = self.Calculate_player_score(i)
            current_round_score.append(score)

        self.persist['current_round_score'] = current_round_score
        self.persist['player_names'] = self.player_names
        self.next_state = "A_SCOREBOARD"
        self.done = True