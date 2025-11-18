import math
import pygame
from sprite.SpriteSheet import get_sprite_store
from sprite.ImageSprite import ImageSprite, AnimatedImageSprite, ScreenImageSprite
from sprite.CompositeSprite import CompositeSprite


class SpriteFactory:
    def __init__(self):
        get_sprite_store().load_sheet_info("data/sprite_info.yaml")

    def create_image_sprite(self,sprite_name,world_position=(0,0),angle=0,scale=1):
        sprite_image=get_sprite_store().get_sprite(sprite_name,scale)
        return ImageSprite(sprite_image,world_position,angle)
    
    def create_screen_image_sprite(self,sprite_name,position=(0,0)):
        sprite_image=get_sprite_store().get_sprite(sprite_name,1.0)
        return ScreenImageSprite(sprite_image,position)
    
    def create_animated_sprite(self,animation_name):
        images=get_sprite_store().get_animation(animation_name)
        info=get_sprite_store().get_sprite_info(animation_name)
        return AnimatedImageSprite(images,frame_duration=info["frame_duration"])
    
    def create_composite_sprite(self,composite_name,world_position=(0,0),angle=0):
        composite_info=get_sprite_store().get_sprite_info(composite_name)
        composite_sprite=CompositeSprite(world_position,angle)
        composite_sprite.from_object(composite_info)
        return composite_sprite

_sprite_factory=SpriteFactory()

def get_sprite_factory():
    return _sprite_factory