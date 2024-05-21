import Card

class Player:
    def __init__(self, player_id):
        self.player_id = player_id
        self.cards = [Card.Card("null", False) for _ in range(12)]

    def update_card(self, index, visible, value):
        if 0 <= index < len(self.cards):
            self.cards[index].visible = visible
            self.cards[index].value = value
        else:
            print("Index out of range")

    def get_card(self, index):
        if 0 <= index < len(self.cards):
            return self.cards[index]
        else:
            print("Index out of range")
            return None