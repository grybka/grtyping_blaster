import math
import pygame
from sprite.SpriteSheet import get_sprite_store
from sprite.ImageSprite import ImageSprite, AnimatedImageSprite

class SpriteFactory:
    def __init__(self):
        get_sprite_store().load_sheet_info("data/sprite_info.yaml")

    def create_image_sprite(self,sprite_name,world_position=(0,0),angle=0,scale=1):
        sprite_image=get_sprite_store().get_sprite(sprite_name,scale)
        return ImageSprite(sprite_image,world_position,angle)
    
    def create_animated_sprite(self,animation_name):
        images=get_sprite_store().get_animation(animation_name)
        info=get_sprite_store().get_sprite_info(animation_name)
        return AnimatedImageSprite(images,frame_duration=info["frame_duration"])
    

_sprite_factory=SpriteFactory()

def get_sprite_factory():
    return _sprite_factory