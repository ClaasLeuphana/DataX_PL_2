import pygame
from States.base import State

class Options(State):
    def __init__(self, assets=None):
        super(Options, self).__init__()
        self.assets = assets
        self.screen_rect = pygame.display.get_surface().get_rect()
        self.font = pygame.font.Font(None, 50)

        # Initiale Lautstärkewerte aus den GameAssets
        self.music_volume = self.assets.music_volume
        self.sfx_volume = self.assets.sfx_volume

        # Erstellen der Schieberegler
        self.music_slider = Slider(self.screen_rect.centerx - 150, self.screen_rect.centery - 50, 300, 20, self.music_volume)
        self.sfx_slider = Slider(self.screen_rect.centerx - 150, self.screen_rect.centery + 50, 300, 20, self.sfx_volume)

        # Erstellen des "Main Menu"-Buttons
        self.button_font = pygame.font.Font(None, 40)
        self.button_text = self.button_font.render("Main Menu", True, pygame.Color("white"))
        self.button_rect = self.button_text.get_rect(topleft=(10, self.screen_rect.height - self.button_text.get_height() - 30))


    def get_event(self, event):
        if event.type == pygame.QUIT:
            self.quit = True
        elif event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.MOUSEBUTTONUP or event.type == pygame.MOUSEMOTION:
            if self.music_slider.handle_event(event):
                self.music_volume = self.music_slider.value
                self.assets.set_music_volume(self.music_volume)  # Lautstärke über GameAssets anpassen
            if self.sfx_slider.handle_event(event):
                self.sfx_volume = self.sfx_slider.value
                self.assets.set_sfx_volume(self.sfx_volume)  # Lautstärke über GameAssets anpassen
            # Überprüfen, ob der "Main Menu"-Button geklickt wurde
            if event.type == pygame.MOUSEBUTTONUP:
                mouse_pos = pygame.mouse.get_pos()
                if self.button_rect.collidepoint(mouse_pos):
                    self.next_state = "MENU"
                    self.done = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                # Testen des Soundeffekts beim Drücken der Eingabetaste
                self.assets.card_turn_sfx.play()

    def draw(self, surface):
        # Skaliere das Hintergrundbild
        scaled_background = pygame.transform.scale(self.assets.background, (self.screen_rect.width, self.screen_rect.height))
        surface.blit(scaled_background, (0, 0))  # Zeichne den skalierten Hintergrund

        self.music_slider.draw(surface)
        self.sfx_slider.draw(surface)

        # Texte rendern
        music_text = self.font.render("Music Volume", True, pygame.Color("white"))
        sfx_text = self.font.render("SFX Volume", True, pygame.Color("white"))
        surface.blit(music_text, (self.screen_rect.centerx - music_text.get_width() // 2, self.screen_rect.centery - 100))
        surface.blit(sfx_text, (self.screen_rect.centerx - sfx_text.get_width() // 2, self.screen_rect.centery))

        # Zeichne den "Main Menu"-Button
        surface.blit(self.button_text, self.button_rect.topleft)

    def resize(self, width, height):
        """Passen Sie das Menü an die neue Bildschirmgröße an."""
        self.screen_rect = pygame.Rect(0, 0, width, height)
        # Aktualisieren Sie die Position der Slider
        self.music_slider.update_position(self.screen_rect.centerx - 150, self.screen_rect.centery - 50)
        self.sfx_slider.update_position(self.screen_rect.centerx - 150, self.screen_rect.centery + 50)
        # Aktualisieren Sie die Position des "Main Menu"-Buttons
        self.button_rect.topleft = (10, self.screen_rect.height - self.button_text.get_height() - 30)


class Slider:
    def __init__(self, x, y, width, height, initial_value):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = pygame.Color("gray")
        self.knob_color = pygame.Color("red")
        self.value = initial_value
        # Setze die Position des Knobs basierend auf dem initialen Wert
        self.knob_rect = pygame.Rect(x + width * initial_value - 10, y - 5, 20, height + 10)
        self.dragging = False  # Initialisiert den dragging-Zustand

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.knob_rect.collidepoint(event.pos):
                self.dragging = True  # Start dragging
        elif event.type == pygame.MOUSEBUTTONUP:
            self.dragging = False  # Stop dragging
        elif event.type == pygame.MOUSEMOTION:
            if self.dragging:
                # Berechnen Sie den neuen X-Wert und begrenzen Sie ihn auf den Slider-Bereich
                new_x = min(max(event.pos[0], self.rect.left), self.rect.right)
                # Aktualisieren Sie die Knopfposition basierend auf der Mausbewegung
                self.knob_rect.x = new_x - self.knob_rect.width // 2
                # Aktualisieren Sie den Wert basierend auf der neuen Knopfposition
                self.value = (self.knob_rect.centerx - self.rect.left) / self.rect.width
                return True  # Bedeutet, dass der Slider angepasst wurde
        return False

    def draw(self, surface):
        # Zeichne den Slider-Bereich
        pygame.draw.rect(surface, self.color, self.rect)
        # Zeichne den Slider-Knopf
        pygame.draw.rect(surface, self.knob_color, self.knob_rect)

    def update_position(self, x, y):
        """Aktualisiert die Position des Sliders und Knopfes."""
        self.rect.topleft = (x, y)
        # Knopfposition relativ zum neuen Slider aktualisieren, basierend auf dem aktuellen Wert
        self.knob_rect.center = (x + self.rect.width * self.value, y + self.rect.height // 2)


