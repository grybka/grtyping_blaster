#This is for a sprite made of several animated images layered on top of each other
#With several different animation modes

import pygame
from graphics.GraphicsBase import WorldSprite, ScreenSprite

class AnimInfo:
    def __init__(self):
        self.frames=[] #by frame index
        self.frame_durations=[] #by frame index

class SpriteComponent(ScreenSprite):
    def __init__(self,image,offset=(0,0),angle=0):
        super().__init__(image,(0,0),angle)
        self.offset=offset  #Offset from the CompositeSprite's position
        self.animations={}  #Dict of animation name to AnimInfo
        self.current_animation=None
        self.images=[]
        self.on_frame=0
        self.animation_time=0

    def from_object(self, obj):
        self.offset=obj.get("offset",(0,0))
        self.angle=obj.get("angle",0)
        for anim in obj.get("animations",[]):
            anim_info=AnimInfo()
            anim_info.frames=anim.get("frames",[])
            anim_info.frame_durations=anim.get("frame_durations",[])
            self.animations[anim.get("name","default")]=anim_info
        for img_name in obj.get("images",[]):
            image=pygame.image.load(img_name).convert_alpha()
            self.images.append(image)

    def get_screen_position(self, camera):
        parent_position=self.world_position
        return (parent_position[0]+self.offset[0], parent_position[1]+self.offset[1])
    
    def set_animation_mode(self, mode):
        if mode in self.animations:
            self.current_animation=self.animations[mode]
            self.on_frame=0
            self.animation_time=0

    def draw(self, screen, camera):
        if self.current_animation:
            image=self.current_animation.frames[self.on_frame]
            if camera.zoom !=1:
                image=pygame.transform.scale(image,(int(image.get_width()*camera.zoom),int(image.get_height()*camera.zoom)))        
            if self.angle!=0:
                image=pygame.transform.rotate(image,self.angle)
            screen_position = self.get_screen_position(camera)
            screen.blit(image,(screen_position[0]-image.get_width()/2,screen_position[1]-image.get_height()/2))
    

class CompositeSprite(WorldSprite):
    def __init__(self,components,world_position=(0,0)):
        WorldSprite.__init__(self,world_position)
        self.components=components  #List of WorldSprite objects

    def from_object(self, obj):
        self.components=[]
        for comp_obj in obj.get("components",[]):
            component=SpriteComponent(None)
            component.from_object(comp_obj)
            self.components.append(component)

    def update(self, time_delta):
        for component in self.components:
            component.update(time_delta)

    def set_animation_mode(self, mode):
        for component in self.components:
            component.set_animation_mode(mode)

    def get_screen_rect(self, camera):
        if not self.components:
            return (0,0,0,0)
        rects=[component.get_screen_rect(camera) for component in self.components]
        min_x=min(rect[0] for rect in rects)
        min_y=min(rect[1] for rect in rects)
        max_x=max(rect[0]+rect[2] for rect in rects)
        max_y=max(rect[1]+rect[3] for rect in rects)
        return (min_x,min_y,max_x-min_x,max_y-min_y)
    
    def draw(self, screen, camera):
        for component in self.components:
            component.draw(screen, camera)