
from numpy import size


class Camera:
    #info for mapping 2d world coords to 2d screen coords
    def __init__(self, position=(0, 0), zoom=1.0):
        self.position = position
        self.zoom = zoom

    def world_to_screen(self, world_position):
        # Convert world coordinates to screen coordinates
        screen_x = (world_position[0] - self.position[0]) * self.zoom
        screen_y = (world_position[1] - self.position[1]) * self.zoom
        return (screen_x, screen_y)
    
    def screen_to_world(self, screen_position):
        # Convert screen coordinates to world coordinates
        world_x = screen_position[0] / self.zoom + self.position[0]
        world_y = screen_position[1] / self.zoom + self.position[1]
        return (world_x, world_y)
    
    def rect_world_to_screen(self, world_rect):
        # Convert a rectangle from world to screen coordinates
        screen_x, screen_y = self.world_to_screen((world_rect[0], world_rect[1]))
        screen_width = world_rect[2] * self.zoom
        screen_height = world_rect[3] * self.zoom
        return (screen_x, screen_y, screen_width, screen_height)

class Sprite:
    #base class for all sprites
    def __init__(self, position=(0, 0)):
        # if the Sprite is a World Sprite, position in world coordinates of the center of the sprite
        # if the Sprite is a Screen Sprite, position in screen coordinates of the upper left of the sprite
        self.position = position 
        self.scheduled_for_removal = False

    def schedule_for_removal(self):
        self.scheduled_for_removal = True

    def set_position(self, position):
        self.position = position

    def get_screen_rect(self, camera):
        # Returns the bounding box in screen coordinates as (x, y, width, height)
        return (0,0,0,0)
    
    def set_world_position(self, position,camera):
        # Sets the position in world coordinates
        self.position = position

    def set_screen_position(self, position,camera):
        # Sets the position in screen coordinates
        self.position = position

    def get_screen_position(self, camera):
        # Returns the position in screen coordinates as (x, y)
        return (0,0)
    
    def get_world_position(self, camera):
        # Returns the position in world coordinates as (x, y)
        return (0,0)

    def draw(self, screen, camera):
        #TODO implement drawing logic using camera
        pass

    def update(self, time_delta):
        #TODO implement update logic
        pass

    def should_remove(self):
        return self.scheduled_for_removal

class WorldSprite(Sprite):
    # A sprite that exists in world coordinates
    def __init__(self, position=(0, 0)):
        super().__init__(position)

    def set_screen_position(self, position,camera):
        # Sets the position in screen coordinates
        self.position = camera.screen_to_world(position)


    def get_screen_position(self, camera):
        # Returns the position in screen coordinates as (x, y)
        return camera.world_to_screen(self.position)

    def get_world_position(self, camera):
        # Returns the position in world coordinates as (x, y)
        return self.position
    
class ScreenSprite(Sprite):
    # A sprite that exists in screen coordinates
    def __init__(self, position=(0, 0), screen_wh=(0, 0)):
        super().__init__(position)
        self.screen_wh = screen_wh

    def get_screen_rect(self, camera):
        # Returns the bounding box in screen coordinates as (x, y, width, height)
        return (self.position[0], self.position[1], self.screen_wh[0], self.screen_wh[1])

    def get_screen_position(self, camera):
        # Returns the position in screen coordinates as (x, y)
        return self.position

    def get_world_position(self, camera):
        # Returns the position in world coordinates as (x, y)
        return camera.screen_to_world(self.position)