import pygame
from graphics.GraphicsBase import Sprite, WorldSprite
from sprite.TargetTextWindow import TargetTextWindow

class SpriteWithTextWindow(WorldSprite):
    def __init__(self, position=(0, 0), text="", sprite: WorldSprite=None, visibility=True):
        #This is a world sprite with an associated text window
        #position is world coords of sprite center
        super().__init__(position)
        self.text_window_offset_y = 5 # pixels above the sprite
        self.text_window = TargetTextWindow(text=text)
        self.text_window.visible = visibility
        self.sprite = sprite
        self.sprite.set_world_position(position)

    def set_text_window_visibility(self, visible: bool):
        self.text_window.visible = visible

    def get_text_window_visibility(self) -> bool:
        return self.text_window.visible

    def set_position(self, position):        
        super().set_world_position(position)
        self.sprite.set_world_position(position)

    def draw(self, screen, camera):        
        #update the text window position to be centered above the sprite        
        sprite_rect = self.sprite.get_screen_rect(camera)
        self.text_window.set_screen_position( (sprite_rect[0]+sprite_rect[2]//2 - self.text_window.screen_wh[0]//2, sprite_rect[1] - self.text_window.screen_wh[1]-self.text_window_offset_y) )
        super().draw(screen, camera)
        self.text_window.draw(screen, camera)
        if self.sprite:
            #print("sprite position in SpriteWithTextWindow draw:", self.sprite.position)
            self.sprite.draw(screen, camera)

    def update(self, time_delta):
        super().update(time_delta)
        self.text_window.update(time_delta)
        if self.sprite:
            self.sprite.update(time_delta)