class State:
    def __init__(self):
        self.done = False
        self.quit = False
        self.next_state = None
        self.persist = {}

    def get_event(self, event):
        pass

    def update(self, dt):
        pass

    def draw(self, surface):
        pass

    def startup(self, persistent):
        self.persist = persistent

    def cleanup(self):
        return self.persist
