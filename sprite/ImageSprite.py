import pygame
import math
from graphics.GraphicsBase import ScreenSprite, WorldSprite

class ImageSprite(WorldSprite):
    def __init__(self,image,world_position=(0,0),angle=0):
        WorldSprite.__init__(self,world_position)
        self.angle=angle
        self.image=image

    def get_screen_rect(self, camera):
        screen_position = self.get_screen_position(camera)
        width=self.image.get_width()*camera.zoom
        height=self.image.get_height()*camera.zoom
        rotated_width=abs(width*math.cos(self.angle)+abs(height*math.sin(self.angle)))
        rotated_height=abs(height*math.cos(self.angle)+abs(width*math.sin(self.angle)))
        return (screen_position[0]-rotated_width/2,screen_position[1]-rotated_height/2,rotated_width,rotated_height)
    
    def draw(self, screen, camera):
        image=self.image
        if camera.zoom !=1:
            image=pygame.transform.scale(image,(int(image.get_width()*camera.zoom),int(image.get_height()*camera.zoom)))        
        if self.angle!=0:
            image=pygame.transform.rotate(image,self.angle)
        screen_position = self.get_screen_position(camera)
        screen.blit(image,(screen_position[0]-image.get_width()/2,screen_position[1]-image.get_height()/2))

    
class ScreenImageSprite(ScreenSprite):
    def __init__(self,image,screen_position=(0,0)):
        super().__init__(self)        
        self.image=image
        self.position=screen_position
        self.hidden=False

    def set_screen_position(self, position):
        self.position = position

    def set_hidden(self,hidden):
        self.hidden=hidden

    def get_screen_rect(self, camera):
        width=self.image.get_width()
        height=self.image.get_height()
        return (self.position[0],self.position[1],width,height)
        
    
    def draw(self, screen, camera):
        if self.hidden:
            return  
        image=self.image                
        screen.blit(image,(self.position[0],self.position[1]))

class AnimatedImageSprite(WorldSprite):
    #This is just like ImageSprite but it supports frame-based animation
    #It cycles through a list of images at a given frame duration
    def __init__(self,images,world_position=(0,0),angle=0,frame_duration=0.1):
        WorldSprite.__init__(self,world_position)
        self.angle=angle
        self.images=images
        self.frame_duration=frame_duration
        self.current_time=0
        self.current_frame=0
        self.cyclic=True
        self.end_on_last_frame=True

    def update(self, time_delta):
        self.current_time+=time_delta
        while self.current_time>=self.frame_duration:
            self.current_time-=self.frame_duration
            if self.end_on_last_frame and self.current_frame==len(self.images)-1:
                self.scheduled_for_removal=True
            if self.cyclic:
                self.current_frame=(self.current_frame+1)%len(self.images)
            else:
                self.current_frame=min(self.current_frame+1,len(self.images)-1)

    def get_screen_rect(self, camera):
        image=self.images[self.current_frame]
        screen_position = self.get_screen_position(camera)
        width=image.get_width()*camera.zoom
        height=image.get_height()*camera.zoom
        rotated_width=abs(width*math.cos(self.angle)+abs(height*math.sin(self.angle)))
        rotated_height=abs(height*math.cos(self.angle)+abs(width*math.sin(self.angle)))
        return (screen_position[0]-rotated_width/2,screen_position[1]-rotated_height/2,rotated_width,rotated_height)
    
    def draw(self, screen, camera):        
        image=self.images[self.current_frame]
        if camera.zoom !=1:
            image=pygame.transform.scale(image,(int(image.get_width()*camera.zoom),int(image.get_height()*camera.zoom)))        
        if self.angle!=0:
            image=pygame.transform.rotate(image,self.angle)
        screen_position = self.get_screen_position(camera)
        screen.blit(image,(screen_position[0]-image.get_width()/2,screen_position[1]-image.get_height()/2))

class ShrinkingSprite(ImageSprite):
    #This is an ImageSprite that shrinks over time until it disappears
    def __init__(self,image,world_position=(0,0),angle=0,shrink_duration=1.):
        ImageSprite.__init__(self,image,world_position,angle)
        self.shrink_duration=shrink_duration
        self.current_scale=1.0
        self.elapsed_time=0

    def update(self, time_delta):
        self.elapsed_time+=time_delta
        self.current_scale=(1.0-self.elapsed_time/self.shrink_duration)        
        if self.current_scale<=0:
            self.scheduled_for_removal=True

    def draw(self, screen, camera):
        image=pygame.transform.scale(self.image,(int(self.image.get_width()*self.current_scale),int(self.image.get_height()*self.current_scale)))
        if camera.zoom !=1:
            image=pygame.transform.scale(image,(int(image.get_width()*camera.zoom),int(image.get_height()*camera.zoom)))        
        if self.angle!=0:
            image=pygame.transform.rotate(image,self.angle)
        screen_position = self.get_screen_position(camera)
        screen.blit(image,(screen_position[0]-image.get_width()/2,screen_position[1]-image.get_height()/2))