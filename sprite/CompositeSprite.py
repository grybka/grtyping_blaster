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
        super().__init__(image)
        self.offset=offset  #Offset from the CompositeSprite's position
        self.animations={}  #Dict of animation name to AnimInfo
        self.current_animation=None
        self.images=[]
        self.image_offsets=[]
        self.on_frame=0
        self.animation_time=0

    def from_object(self, obj):
        self.offset=obj.get("offset",(0,0))
        self.angle=obj.get("angle",0)
        if "animations" in obj:
            for anim_key, anim in obj.get("animations",{}).items():
                anim_info=AnimInfo()
                anim_info.frames=anim.get("frames",[])
                anim_info.frame_durations=anim.get("frame_durations",[])
                self.animations[anim_key]=anim_info
        else:
            #single image animation
            anim_info=AnimInfo()
            anim_info.frames=[0]
            anim_info.frame_durations=[1000]  #1 second
            self.animations["default"]=anim_info   
        for img_info in obj.get("images",[]):
            if isinstance(img_info, str):
                img_name=img_info
                offset=(0,0)
            else:
                img_name=img_info[0]
                offset=img_info[1] if len(img_info)>1 else (0,0)
            self.image_offsets.append(offset)
            image=pygame.image.load(img_name).convert_alpha()
            self.images.append(image)            
        self.current_animation=self.animations[self.animations.keys().__iter__().__next__()]
        
    def update(self, time_delta):
        if self.current_animation:
            self.animation_time+=time_delta
            while self.animation_time >= self.current_animation.frame_durations[self.on_frame]:
                self.animation_time-=self.current_animation.frame_durations[self.on_frame]
                self.on_frame+=1
                if self.on_frame >= len(self.current_animation.frames):
                    self.on_frame=0

    def get_screen_position(self, camera):
        parent_position=self.world_position
        return (parent_position[0]+self.offset[0], parent_position[1]+self.offset[1])
    
    def set_animation_mode(self, mode):
        if mode in self.animations:
            self.current_animation=self.animations[mode]
            self.on_frame=0
            self.animation_time=0

    def draw(self, screen, camera,position):
        if self.current_animation:
            image=self.images[self.current_animation.frames[self.on_frame]]
            offset=self.image_offsets[self.current_animation.frames[self.on_frame]]
            if camera.zoom !=1:
                image=pygame.transform.scale(image,(int(image.get_width()*camera.zoom),int(image.get_height()*camera.zoom)))        
            if self.angle!=0:
                image=pygame.transform.rotate(image,self.angle)
            #screen_position = self.get_screen_position(camera)
            screen.blit(image,(position[0]+offset[0],position[1]+offset[1]))
    

class CompositeSprite(WorldSprite):
    def __init__(self,world_position=(0,0),components=[]):
        WorldSprite.__init__(self,world_position)
        self.components=components  #List of WorldSprite objects
        self.offset=(0,0)

    def from_object(self, obj):
        self.components=[]
        self.offset=obj.get("offset",(0,0))
        for comp_key,comp_obj in obj.get("components",{}).items():
            component=SpriteComponent(None)
            component.from_object(comp_obj)
            self.components.append(component)
        if "starting_animation" in obj:
            self.set_animation_mode(obj["starting_animation"])

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
        position=self.get_screen_position(camera)
        offset_position=(position[0]-self.offset[0], position[1]-self.offset[1])
        for component in self.components:
            component.draw(screen, camera,offset_position)