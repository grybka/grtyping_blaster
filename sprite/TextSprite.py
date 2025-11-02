import pygame
import math
from graphics.GraphicsBase import WorldSprite

class TextSprite(WorldSprite):
    def __init__(self, text, position=(0,0), font_size=24, color=(255, 255, 255)):
        super().__init__(position)
        self.text = text
        self.font_size = font_size
        self.color = color
        self.font = pygame.font.Font(None, self.font_size)
        self.set_position(position)
        

    def set_position(self, position):
        self.position = position
        self.image = self.font.render(self.text, True, self.color)
        self.rect = self.image.get_rect(center=self.position)

    def get_screen_rect(self, camera):
        screen_position = self.get_screen_position(camera)
        width = self.image.get_width() * camera.zoom
        height = self.image.get_height() * camera.zoom
        return (screen_position[0] - width / 2, screen_position[1] - height / 2, width, height)


    def update(self, time_delta):
        # Update logic for the text sprite (if any)
        pass

    def draw(self, surface, camera):
        surface.blit(self.image, self.rect)
