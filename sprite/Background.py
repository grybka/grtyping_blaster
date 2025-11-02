import pygame
import random
from graphics.GraphicsBase import WorldSprite,ScreenSprite

class Background(ScreenSprite):
    def __init__(self):
        super().__init__()

    def update_property(self, property_name, property_value):
        #Override in subclasses to handle property updates
        pass

class BackgroundStarField(Background):
    def __init__(self, avg_num_stars, velocity=0):
        super().__init__()
        self.avg_num_stars = avg_num_stars
        self.velocity = velocity
        self.stars=[]
        #let's assume the velocity is only in the y direction

    def start(self,screen,camera):
        screen_size = screen.get_size()
        self.screen_wh = screen_size
        for _ in range(self.avg_num_stars):
            x = random.randint(0, screen_size[0])
            y = random.randint(0, screen_size[1])
            self.stars.append((x, y))
        print("velocity:", self.velocity)

    
    def update_property(self, property_name, property_value):
        if property_name=="velocity":
            print("BackgroundStarField: updating velocity to", property_value)
            self.velocity=property_value
            return True
        return super().update_property(property_name, property_value)

    def draw(self, screen, camera):
        if len(self.stars)==0:
            self.start(screen,camera)
        for star in self.stars:
            star_pos = camera.world_to_screen(star)
            pygame.draw.circle(screen, (255, 255, 255), star_pos, 2)

    def update(self, time_delta):
        for i, star in enumerate(self.stars):
            x, y = star
            y += self.velocity * time_delta
            if y > self.screen_wh[1] or y < 0:
                if self.velocity > 0:
                    y = 0
                else:
                    y = self.screen_wh[1]
                x = random.randint(0, self.screen_wh[0])
            self.stars[i] = (x, y)
