import pygame
from graphics.GraphicsBase import WorldSprite

class TestCircle(WorldSprite):
    def __init__(self, position=(0,0),radius=50):
        super().__init__(position)
        self.radius = radius #radius in world coords

    def get_screen_rect(self, camera):
        pos=camera.world_to_screen(self.position)
        rect = (pos[0]-self.radius*camera.zoom, pos[1]-self.radius*camera.zoom,
                self.radius*2*camera.zoom, self.radius*2*camera.zoom)
        return rect

    def draw(self, screen, camera):
        # Draw a simple circle at the sprite's position
        screen_position = camera.world_to_screen(self.position)
        pygame.draw.circle(screen, (255, 0, 0), (int(screen_position[0]), int(screen_position[1])), int(self.radius * camera.zoom))