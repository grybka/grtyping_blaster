from .GraphicsBase import Camera
from graphics.GraphicsOverlay import GraphicsOverlay

class Graphics:
    # Handles the background and various sprites to render to screen
    def __init__(self,screen):
        self.camera = Camera()
        self.overlay = GraphicsOverlay()
        self.sprites = []
        self.backgrounds = []
        self.screen_size = screen.get_size()

    def add_sprite(self, sprite):
        self.sprites.append(sprite)

    def add_background(self, background):
        self.backgrounds.append(background) 

    def draw(self,screen):
        self.screen_size = screen.get_size()
        screen.fill((0, 0, 0))
        #Draw the backgrounds first
        for background in self.backgrounds:
            background.draw(screen, self.camera)
        # iterate through sprites, and draw each one
        for sprite in self.sprites:
            sprite.draw(screen, self.camera)
        #draw the grahphics overlay last
        self.overlay.draw(screen)

    def update(self, time_delta):
        # Update all backgrounds
        for background in self.backgrounds:
            background.update(time_delta)
        # Update all sprites
        for sprite in self.sprites:
            sprite.update(time_delta)
        # Remove any sprites that should be removed
        self.sprites = [s for s in self.sprites if not s.should_remove()]