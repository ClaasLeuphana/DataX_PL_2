import GameAssets

class Card:
    def __init__(self, value, visible=True):
        self.value = value
        self.visible = visible

    def get_image(self):
        if not self.visible:
            return GameAssets.GameAssets.CardBack
        return GameAssets.GameAssets.cards[self.value]
