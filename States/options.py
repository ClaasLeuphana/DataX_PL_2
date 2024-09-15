import pygame
from States.base import State


class Options(State):
    def __init__(self, assets=None):
        """
        Initialisiert die Optionen-Seite des Spiels, einschließlich Lautstärkereglern und eines Menütaste.

        Input:
        - assets: Ein Objekt, das die benötigten Grafiken und Sounds bereitstellt (optional).

        """
        super(Options, self).__init__()
        self.assets = assets
        self.screen_rect = pygame.display.get_surface().get_rect()
        self.font = pygame.font.Font(None, 50)

        # Initiale Lautstärkewerte aus den GameAssets
        self.music_volume = self.assets.music_volume
        self.sfx_volume = self.assets.sfx_volume

        # Erstellen der Schieberegler
        self.music_slider = Slider(self.screen_rect.centerx - 150, self.screen_rect.centery - 50, 300, 20,
                                   self.music_volume)
        self.sfx_slider = Slider(self.screen_rect.centerx - 150, self.screen_rect.centery + 50, 300, 20,
                                 self.sfx_volume)

        # Erstellen des "Main Menu"-Buttons
        self.button_font = pygame.font.Font(None, 40)
        self.button_text = self.button_font.render("Main Menu", True, pygame.Color("white"))
        self.button_rect = self.button_text.get_rect(
            topleft=(10, self.screen_rect.height - self.button_text.get_height() - 30))

    def get_event(self, event):
        """
        Verarbeitet Eingabeereignisse wie Mausklicks und Tastatureingaben.

        Input:
        - event: Das Pygame-Ereignis, das verarbeitet werden soll.

        """
        if event.type == pygame.QUIT:
            self.quit = True
        elif event.type in [pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP, pygame.MOUSEMOTION]:
            if self.music_slider.handle_event(event):
                self.music_volume = self.music_slider.value
                self.assets.set_music_volume(self.music_volume)
            if self.sfx_slider.handle_event(event):
                self.sfx_volume = self.sfx_slider.value
                self.assets.set_sfx_volume(self.sfx_volume)
            if event.type == pygame.MOUSEBUTTONUP:
                mouse_pos = pygame.mouse.get_pos()
                if self.button_rect.collidepoint(mouse_pos):
                    self.next_state = "MENU"
                    self.done = True
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            self.assets.card_turn_sfx.play()

    def draw(self, surface):
        """
        Zeichnet die Optionen-Seite auf der angegebenen Oberfläche.

        Input:
        - surface: Die Oberfläche, auf der die Optionen gezeichnet werden sollen.

        """
        scaled_background = pygame.transform.scale(self.assets.background,
                                                   (self.screen_rect.width, self.screen_rect.height))
        surface.blit(scaled_background, (0, 0))

        self.music_slider.draw(surface)
        self.sfx_slider.draw(surface)

        music_text = self.font.render("Music Volume", True, pygame.Color("white"))
        sfx_text = self.font.render("SFX Volume", True, pygame.Color("white"))
        surface.blit(music_text,
                     (self.screen_rect.centerx - music_text.get_width() // 2, self.screen_rect.centery - 100))
        surface.blit(sfx_text, (self.screen_rect.centerx - sfx_text.get_width() // 2, self.screen_rect.centery))

        surface.blit(self.button_text, self.button_rect.topleft)

    def resize(self, width, height):
        """
        Passt die Optionen-Seite an eine neue Bildschirmgröße an.

        Input:
        - width: Die neue Breite des Bildschirms.
        - height: Die neue Höhe des Bildschirms.

        """
        self.screen_rect = pygame.Rect(0, 0, width, height)
        self.music_slider.update_position(self.screen_rect.centerx - 150, self.screen_rect.centery - 50)
        self.sfx_slider.update_position(self.screen_rect.centerx - 150, self.screen_rect.centery + 50)
        self.button_rect.topleft = (10, self.screen_rect.height - self.button_text.get_height() - 30)


class Slider:
    def __init__(self, x, y, width, height, initial_value):
        """
        Initialisiert einen Schieberegler zur Anpassung von Werten wie Lautstärke.

        Input:
        - x: Die X-Position des Schiebereglers.
        - y: Die Y-Position des Schiebereglers.
        - width: Die Breite des Schiebereglers.
        - height: Die Höhe des Schiebereglers.
        - initial_value: Der anfängliche Wert des Schiebereglers (zwischen 0 und 1).

        """
        self.rect = pygame.Rect(x, y, width, height)
        self.color = pygame.Color("gray")
        self.knob_color = pygame.Color("red")
        self.value = initial_value
        self.knob_rect = pygame.Rect(x + width * initial_value - 10, y - 5, 20, height + 10)
        self.dragging = False

    def handle_event(self, event):
        """
        Verarbeitet Ereignisse wie Mausklicks und -bewegungen zur Steuerung des Schiebereglers.

        Input:
        - event: Das Pygame-Ereignis, das verarbeitet werden soll.

        Output:
        - bool: Gibt an, ob der Schieberegler angepasst wurde.
        """
        if event.type == pygame.MOUSEBUTTONDOWN and self.knob_rect.collidepoint(event.pos):
            self.dragging = True
        elif event.type == pygame.MOUSEBUTTONUP:
            self.dragging = False
        elif event.type == pygame.MOUSEMOTION and self.dragging:
            new_x = min(max(event.pos[0], self.rect.left), self.rect.right)
            self.knob_rect.x = new_x - self.knob_rect.width // 2
            self.value = (self.knob_rect.centerx - self.rect.left) / self.rect.width
            return True
        return False

    def draw(self, surface):
        """
        Zeichnet den Schieberegler und seinen Knopf auf der angegebenen Oberfläche.

        Input:
        - surface: Die Oberfläche, auf der der Schieberegler gezeichnet werden soll.

        """
        pygame.draw.rect(surface, self.color, self.rect)
        pygame.draw.rect(surface, self.knob_color, self.knob_rect)

    def update_position(self, x, y):
        """
        Aktualisiert die Position des Schiebereglers und seines Knopfes.

        Input:
        - x: Die neue X-Position des Schiebereglers.
        - y: Die neue Y-Position des Schiebereglers.

        """
        self.rect.topleft = (x, y)
        self.knob_rect.center = (x + self.rect.width * self.value, y + self.rect.height // 2)
