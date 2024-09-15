from States.base import State
from GameAssets import *
import time


def remove_three_in_a_row(cards):
    """
    Setzt das 'elim'-Attribut für alle Karten in der Liste auf True.

    Input:
    - cards: Eine Liste von Kartenobjekten, deren 'elim'-Attribut gesetzt werden soll.

    """
    for card in cards:
        card.elim = True


class Gameplay(State):
    def __init__(self, assets=None):
        """
        Initialisiert den Gameplay-Zustand.

        Input:
        - assets: Ein Objekt, das die benötigten Grafiken und Sounds bereitstellt (optional).

        """
        super(Gameplay, self).__init__()
        self.assets = assets
        self.player_count = 1
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
        self.last_turn_active = None
        self.last_turn_player = None
        self.turn_counter = 0
        self.player_names = []  # Liste der Spielernamen

    def resize(self, width, height):
        """
        Passt die Größe der Spielanzeige an die neue Fenstergröße an.

        Input:
        - width: Die neue Breite des Fensters.
        - height: Die neue Höhe des Fensters.

        """
        self.screen_rect = pygame.Rect(0, 0, width, height)
        self.screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)

        # Aktualisiere die Kartenmaße basierend auf der neuen Fenstergröße
        self.card_width, self.card_height, self.card_gap = self.get_card_measurements()

    def get_card_measurements(self):
        """
        Berechnet die Maße und Abstände der Karten basierend auf der Bildschirmgröße.

        Output:
        - card_width: Die Breite der Karten.
        - card_height: Die Höhe der Karten.
        - card_gap: Der Abstand zwischen den Karten.
        """
        self.card_width = self.screen.get_width() / 25
        self.card_height = self.card_width * 1.5
        self.card_gap = self.card_width / 12
        return self.card_width, self.card_height, self.card_gap

    def startup(self, persistent):
        """
        Initialisiert den Spielzustand basierend auf den persistierenden Daten.

        Input:
        - persistent: Ein Dictionary mit persistierenden Daten wie Spieleranzahl und Assets.

        """
        self.persist = persistent
        self.last_turn_active = False
        self.player_count = self.persist.get('player_count', 1)
        self.current_player = 0
        self.assets = self.persist.get('assets', GameAssets())
        self.player_names = self.persist.get('player_names', [])  # Setzt die Spielernamen
        print(f"Debug: Player names retrieved from persistent: {self.player_names}")
        self.GameStart()

    def GameStart(self):
        """
        Bereitet alle erforderlichen Elemente für den Spielstart vor.

        """
        # Initialisiere Deck und Stapel
        self.deck = Deck(assets=self.assets)
        self.stack = Stack()
        self.players_hands = self.deck.deal(self.player_count)
        self.deck.turn_top_card(self.stack)

        # Debug-Ausgabe der verteilten Karten
        for i, hand in enumerate(self.players_hands):
            print(f"Spieler {i + 1}: {[card.value for card in hand]}")

        self.cards_turned = 0
        self.initial_round = True

    def determine_starting_player(self):
        """
        Bestimmt den Startspieler basierend auf der höchsten Summe der ersten zwei aufgedeckten Karten.

        Output:
        - Keine. Setzt self.current_player auf den Index des Startspielers.
        """
        highest_sum = -1
        starting_player = 0

        # Durchlaufe alle Spieler und berechne die Summe der ersten zwei aufgedeckten Karten
        for i in range(self.player_count):
            visible_cards = [card for card in self.players_hands[i] if card.visible]
            if len(visible_cards) >= 2:
                card_sum = visible_cards[0].value + visible_cards[1].value
                if card_sum > highest_sum:
                    highest_sum = card_sum
                    starting_player = i

        # Aktualisiere den aktuellen Spieler und zeige eine Nachricht an
        self.draw(self.screen)
        self.current_player = starting_player
        self.show_starting_player_message(starting_player + 1)

    def show_starting_player_message(self, player_number):
        """
        Zeigt eine Nachricht an, welcher Spieler beginnt, und wartet 5 Sekunden.

        Input:
        - player_number: Die Nummer des Startspielers.
        """
        message = f"Spieler {player_number} beginnt!"
        text_surface = self.font.render(message, True, pygame.Color("yellow"))
        text_rect = text_surface.get_rect(center=self.screen_rect.center)

        # Erstelle und zeichne ein Hintergrundrechteck hinter dem Text
        background_rect = pygame.Rect(
            text_rect.left - 10,
            text_rect.top - 5,
            text_rect.width + 20,
            text_rect.height + 10
        )
        pygame.draw.rect(self.screen, pygame.Color("black"), background_rect)
        self.screen.blit(text_surface, text_rect)
        pygame.display.flip()

        # Warte 5 Sekunden, bevor der Bildschirm aktualisiert wird
        pygame.time.wait(5000)

    def get_event(self, event):
        """
        Verarbeitet Ereignisse wie Mausklicks, um das Spiel zu steuern.

        Input:
        - event: Das Pygame-Ereignis, das verarbeitet werden soll.
        """
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.initial_round:
                self.handle_initial_turn(event)
            else:
                self.gameLogic(event)

    def gameLogic(self, event):
        """
        Verarbeitet die Spiellogik basierend auf einem Mausklick-Ereignis.

        Input:
        - event: Ein Pygame-Ereignis, das Informationen über die Mausposition enthält.
        """
        mouse_pos = event.pos

        if self.is_over_deck(mouse_pos):
            self.handle_deck_click()
        elif self.is_over_stack(mouse_pos):
            self.handle_stack_click()
        else:
            if self.selected_stack_card:
                # Prüfe, ob eine Karte an der Position des Mausklicks ausgewählt wurde
                selected_card_index = self.get_card_at_pos(self.current_player, mouse_pos)

                if selected_card_index is not None:
                    self.swap_with_stack(selected_card_index)

                    # Rücksetzen der ausgewählten Stack-Karte und Stack-Klick-Status
                    self.selected_stack_card = None
                    self.stack_clicked = False

                    # Überprüfe den Status des Spiels nach dem Zug
                    if self.check_all_cards_visible(self.current_player):
                        self.start_last_turn()  # Letzten Zug starten, wenn alle Karten sichtbar sind
                    else:
                        self.end_turn()

                else:
                    # Rücksetzen der ausgewählten Stack-Karte und Stack-Klick-Status
                    self.selected_stack_card = None
                    self.stack_clicked = False

            else:
                # Prüfe, ob eine Karte an der Position des Mausklicks ausgewählt wurde
                selected_card_index = self.get_card_at_pos(self.current_player, mouse_pos)
                if selected_card_index is not None:
                    card = self.players_hands[self.current_player][selected_card_index]
                    if not card.visible:
                        self.deck.turn_card(card)
                        self.check_three_in_a_row(self.current_player)

                    # Überprüfe den Status des Spiels nach dem Zug
                    if self.check_all_cards_visible(self.current_player):
                        self.start_last_turn()  # Letzten Zug starten, wenn alle Karten sichtbar sind
                    else:
                        self.end_turn()

    def handle_initial_turn(self, event):
        """
        Lässt den aktuellen Spieler zwei seiner Karten aufdecken.

        Input:
        - event: Ein Pygame-Ereignis, das Informationen über die Mausposition enthält.
        """
        mouse_pos = event.pos
        selected_card = self.get_card_at_pos(self.current_player, mouse_pos)
        if selected_card is not None:
            card = self.players_hands[self.current_player][selected_card]
            if not card.visible:
                self.deck.turn_card(card)
                self.cards_turned += 1
                if self.cards_turned >= 2:  # Zwei Karten aufgedeckt
                    self.end_turn()
                    self.cards_turned = 0  # Zähler zurücksetzen
                    if self.current_player == 0:  # Nach der letzten Runde des letzten Spielers
                        self.initial_round = False  # Reguläre Spielrunde starten
                        self.determine_starting_player()  # Bestimme den Startspieler

    def handle_deck_click(self):
        """
        Legt die oberste Karte des Decks auf den Stack und markiert die Deck-Aktion als durchgeführt.
        """
        if not self.deck_action_taken:
            top_card = self.deck.draw(self.stack)  # Ziehe die oberste Karte vom Deck
            if top_card:
                top_card.visible = True  # Setze die Karte sichtbar
                self.stack.add_card(top_card)  # Lege sie auf den Stack
            self.deck_action_taken = True  # Markiere die Deck-Aktion als abgeschlossen

    def handle_stack_click(self):
        """
        Wählt die oberste Karte des Stacks aus oder tauscht Karten, wenn eine Handkarte ausgewählt wird.

        Input:
        - Keine.

        Output:
        - Keine.
        """
        if not self.stack_clicked:
            # Erster Klick auf den Stack
            self.stack_clicked = True
            self.selected_stack_card = self.stack.peek()  # Wählt die oberste Karte des Stacks aus
        else:
            # Zweiter Klick auf den Stack
            mouse_pos = pygame.mouse.get_pos()
            selected_card_index = self.get_card_at_pos(self.current_player, mouse_pos)
            if selected_card_index is not None:
                player_card = self.players_hands[self.current_player][selected_card_index]

                # Tauscht die Handkarte mit der ausgewählten Stack-Karte
                self.players_hands[self.current_player][selected_card_index] = self.selected_stack_card
                self.stack.add_card(player_card)  # Lege die Handkarte auf den Stack

                # Rücksetzen der ausgewählten Stack-Karte und Stack-Klick-Status
                self.selected_stack_card = None
                self.stack_clicked = False
                self.deck_action_taken = True  # Markiert, dass eine Deck-Aktion stattgefunden hat
            else:
                # Kein Klick auf eine Handkarte, daher wird die Auswahl aufgehoben
                self.selected_stack_card = None
                self.stack_clicked = False

    def swap_with_stack(self, selected_card_index):
        """
        Tauscht die ausgewählte Karte des Spielers mit der obersten Karte des Stacks.

        Input:
        - selected_card_index: Der Index der Karte in der Hand des Spielers, die getauscht werden soll.
        """
        player_card = self.players_hands[self.current_player][selected_card_index]
        top_stack_card = self.stack.draw()  # Entfernt die oberste Karte vom Stack

        # Setze die Sichtbarkeit der Stack-Karte auf True
        if top_stack_card:
            top_stack_card.visible = True

        # Lege die Spielerkarte auf den Stack
        if player_card:
            player_card.visible = True
            self.stack.add_card(player_card)

        # Ersetze die Spielerkarte durch die Stack-Karte
        self.players_hands[self.current_player][selected_card_index] = top_stack_card

        # Überprüfe, ob der aktuelle Spieler drei gleiche Karten in einer Reihe hat
        self.check_three_in_a_row(self.current_player)

    def get_card_at_pos(self, player_index, pos):
        """
        Bestimmt die Karte an einer bestimmten Mausposition für einen bestimmten Spieler.

        Input:
        - player_index: Der Index des Spielers, dessen Karten überprüft werden sollen.
        - pos: Die Mausposition als Tupel (x, y).

        Output:
        - Der Index der Karte in der Hand des Spielers, die an der Position gefunden wurde.
        - None, wenn keine Karte an der Position gefunden wurde.
        """
        global start_x, start_y
        card_width, card_height, card_gap = self.get_card_measurements()
        rows = 3
        cols = 4

        # Berechne den Startpunkt basierend auf dem Spielerindex
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

        # Durchlaufe alle Kartenpositionen und überprüfe, ob die Mausposition innerhalb der Karte liegt
        for row in range(rows):
            for col in range(cols):
                x = start_x + col * (card_width + card_gap)
                y = start_y + row * (card_height + card_gap)
                card_rect = pygame.Rect(x, y, card_width, card_height)

                if card_rect.collidepoint(pos):
                    return row * cols + col

        return None

    def is_over_deck(self, pos):
        """
        Überprüft, ob die Mausposition über dem Deck ist.

        Input:
        - pos: Die Mausposition als Tupel (x, y).

        Output:
        - True, wenn die Maus über dem Deck ist.
        - False, wenn die Maus nicht über dem Deck ist.
        """
        card_width, card_height, card_gap = self.get_card_measurements()
        x = self.screen.get_width() / 2 - (card_width + card_gap / 2)
        y = self.screen.get_height() / 2 - card_height / 2
        deck_rect = pygame.Rect(x, y, card_width, card_height)
        return deck_rect.collidepoint(pos)

    def is_over_stack(self, pos):
        """
        Überprüft, ob die Mausposition über dem Stack liegt.

        Input:
        - pos: Die Mausposition als Tupel (x, y).

        Output:
        - True, wenn die Maus über dem Stack ist.
        - False, wenn die Maus nicht über dem Stack ist.
        """
        card_width, card_height, card_gap = self.get_card_measurements()
        x = self.screen.get_width() / 2 + card_gap / 2
        y = self.screen.get_height() / 2 - card_height / 2
        stack_rect = pygame.Rect(x, y, card_width, card_height)
        return stack_rect.collidepoint(pos)

    def start_last_turn(self):
        """
        Aktiviert den letzten Zug für alle Spieler und setzt die nötigen Statusvariablen.
        """
        if not self.last_turn_active:
            self.last_turn_active = True
            self.last_turn_player = self.current_player  # Speichere den Spieler, der als erstes fertig war
            self.turn_counter = 0  # Zähler für die Anzahl der Spieler, die ihren letzten Zug gemacht haben
            print(f"Spieler {self.last_turn_player + 1} hat alle Karten umgedreht. Letzte Runde beginnt!")

        self.end_turn()  # Beendet den aktuellen Zug und wechselt zum nächsten Spieler

    def end_turn(self):
        """
        Wechselt zum nächsten Spieler und überprüft, ob die Runde endet.
        """
        if self.last_turn_active:
            self.turn_counter += 1
            print(f"Spieler {self.current_player + 1} hat seinen letzten Zug gemacht.")

            # Überprüfe, ob alle Spieler ihren letzten Zug gemacht haben
            if self.turn_counter >= self.player_count:
                print("Letzter Zug abgeschlossen. Runde endet.")
                self.round_over()  # Beende die Runde
                return

        # Wechsle zum nächsten Spieler
        self.current_player = (self.current_player + 1) % self.player_count
        self.stack_clicked = False
        self.deck_clicked = False
        self.deck_action_taken = False  # Zurücksetzen der Status für den nächsten Zug

    def check_all_cards_visible(self, player_index):
        """
        Überprüft, ob alle Karten des angegebenen Spielers aufgedeckt sind.

        Input:
        - player_index: Der Index des Spielers, dessen Karten überprüft werden sollen.

        Output:
        - True, wenn alle Karten sichtbar sind.
        - False, wenn nicht alle Karten sichtbar sind.
        """
        all_visible = all(card.visible for card in self.players_hands[player_index])

        if all_visible and self.first_to_finish is None:
            # Speichere den ersten Spieler, der alle Karten umgedreht hat
            self.first_to_finish = player_index + 1  # +1, um den Spieler 1-basiert anzugeben
            self.persist['first_to_finish'] = self.first_to_finish  # Speichere dies in self.persist

        return all_visible

    def draw(self, surface):
        """
        Zeichnet das gesamte Spielfeld, den Stapel, das Deck und die Karten der Spieler.

        Input:
        - surface: Die Oberfläche, auf der gezeichnet werden soll.
        """
        surface.fill(pygame.Color("blue"))  # Setzt den Hintergrund auf Blau

        # Zeichne die Kartenhand jedes Spielers
        for i in range(self.player_count):
            self.draw_player_hand(i)

        self.draw_deck()  # Zeichne das Deck
        self.draw_stack()  # Zeichne den Stapel
        self.draw_player_score()  # Zeichne die Punktzahl der Spieler
        pygame.display.flip()  # Aktualisiere die Anzeige

    def draw_stack(self):
        """
        Zeichnet den Stapel auf den Bildschirm.
        """
        card_width, card_height, card_gap = self.get_card_measurements()
        x = self.screen.get_width() / 2 + card_gap / 2
        y = self.screen.get_height() / 2 - card_height / 2

        if self.stack.cards:
            card = self.stack.cards[-1]  # Wähle die oberste Karte des Stapels
            card_image = card.get_image()
            card_surface = pygame.transform.scale(card_image, (int(card_width), int(card_height)))
            self.screen.blit(card_surface, (x, y))  # Zeichne die Karte auf der Oberfläche

    def draw_deck(self):
        """
        Zeichnet das Deck auf den Bildschirm.
        """
        card_width, card_height, card_gap = self.get_card_measurements()
        x = self.screen.get_width() / 2 - (card_width + card_gap / 2)
        y = self.screen.get_height() / 2 - card_height / 2

        card_surface = pygame.transform.scale(self.assets.CardBack, (int(card_width), int(card_height)))
        self.screen.blit(card_surface, (x, y))  # Zeichne die Rückseite der Deckkarte

    def draw_player_hand(self, player_index):
        """
        Zeichnet die Kartenhand des angegebenen Spielers auf den Bildschirm.

        Input:
        - player_index: Der Index des Spielers, dessen Kartenhand gezeichnet werden soll.
        """
        global start_x, start_y, rotation_angle
        card_width, card_height, card_gap = self.get_card_measurements()
        rows = 3
        cols = 4

        # Bestimme die Startposition und Rotation basierend auf dem Spielerindex
        if player_index == 0:
            start_x = self.screen.get_width() / 2 - cols / 2 * (card_width + card_gap)
            start_y = self.screen.get_height() - rows * (card_height + card_gap)
            rotation_angle = 0
        elif player_index == 1:
            start_x = card_gap
            start_y = self.screen.get_height() / 2 - (cols / 2) * (card_width + card_gap) + card_gap
            rotation_angle = 0
        elif player_index == 2:
            start_x = self.screen.get_width() / 2 - (cols / 2) * (card_width + card_gap)
            start_y = card_gap
            rotation_angle = 0
        elif player_index == 3:
            start_x = self.screen.get_width() - rows * (card_height + card_gap)
            start_y = self.screen.get_height() / 2 - (cols / 2) * (card_width + card_gap)
            rotation_angle = 0

        # Zeichne jede Karte in der Hand des Spielers
        for row in range(rows):
            for col in range(cols):
                index = row * cols + col
                card = self.players_hands[player_index][index]

                if card.elim:
                    continue  # Überspringe eliminierte Karten

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

                self.screen.blit(card_surface, (x, y))  # Zeichne die Karte auf der Oberfläche

    def check_three_in_a_row(self, player_index):
        """
        Überprüft, ob der angegebene Spieler drei gleiche, hervorgehobene Karten in einer vertikalen Reihe hat.

        Input:
        - player_index: Der Index des Spielers, dessen Karten überprüft werden sollen.

        Output:
        - Keine.
        """
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

                    if (card1.value == card2.value == card3.value and
                            -2 <= card1.value and
                            card1.visible and
                            card2.visible and
                            card3.visible):
                        remove_three_in_a_row([card1, card2, card3])

    def Calculate_player_score(self, player_index):
        """
        Berechnet die Punktzahl eines Spielers basierend auf den offenen Karten.

        Input:
        - player_index: Der Index des Spielers, dessen Punktzahl berechnet werden soll.

        Output:
        - player_score: Die berechnete Punktzahl des Spielers.
        """
        player_score = 0
        for card in self.players_hands[player_index]:
            if card.visible and not card.elim:
                player_score += card.value
        return player_score

    def draw_player_score(self):
        """
        Zeichnet die Punktzahl aller Spieler rechts neben der Spielerhand auf den Bildschirm.

        """
        for i in range(self.player_count):
            player_score = self.Calculate_player_score(i)
            player_name = self.player_names[i] if i < len(self.player_names) else f"Player {i + 1}"

            # Render den Text für Punktzahl und Namen
            score_text = self.font.render(f"Score: {player_score}", True, pygame.Color("white"))
            name_text = self.font.render(player_name, True, pygame.Color("yellow"))

            # Berechne die Position des Textes basierend auf der Spielerposition
            if i == 0:  # Spieler unten
                x = self.screen.get_width() / 2 + 2 * (self.card_width + self.card_gap)
                y = self.screen.get_height() - 2 * (self.card_height + self.card_gap)
            elif i == 1:  # Spieler links
                x = self.card_width * 1 + 5 * self.card_gap
                y = self.screen.get_height() / 2 - 3 * (self.card_width + self.card_gap) + self.card_gap
            elif i == 2:  # Spieler oben
                x = self.screen.get_width() / 2 + 2 * (self.card_width + self.card_gap)
                y = 2 * self.card_height
            elif i == 3:  # Spieler rechts
                x = self.screen.get_width() - 3 * (self.card_height + self.card_gap)
                y = self.screen.get_height() / 2 - 3 * (self.card_width + self.card_gap) + self.card_gap

            # Zeichne den Namen oberhalb der Punktzahl
            self.screen.blit(name_text, (x, y - 30))  # Position des Namens anpassen
            self.screen.blit(score_text, (x, y))  # Position der Punktzahl

    def round_over(self):
        """
        Wechselt den Spielzustand zu 'Round Summary', deckt alle verdeckten Karten auf, berechnet die Punktzahlen
        und wechselt zum nächsten Zustand.

        """
        # 1. Decke alle verdeckten Karten aller Spieler auf
        for i in range(self.player_count):
            for card in self.players_hands[i]:
                if not card.visible:
                    self.deck.turn_card(card)

        # 2. Warte 5 Sekunden
        self.draw(self.screen)  # Aktualisiere den Bildschirm, damit die Spieler die aufgedeckten Karten sehen können
        time.sleep(5)

        # 3. Berechne die Punktzahlen der Spieler
        current_round_score = []
        for i in range(self.player_count):
            score = self.Calculate_player_score(i)
            current_round_score.append(score)

        self.persist['current_round_score'] = current_round_score

        # Prüfen, ob der erste Spieler, der alle Karten umgedreht hat, gespeichert wurde
        if self.first_to_finish is not None:
            print(f"Player {self.first_to_finish} was the first to flip all their cards!")

        # Wechsel zum nächsten Zustand
        self.next_state = "SCOREBOARD"
        self.done = True


