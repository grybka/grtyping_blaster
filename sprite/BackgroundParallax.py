from sprite.Background import Background
import pygame
import random
import yaml

# A single layer of parallax background for scrolling effect in the x direction
class BackgroundParallaxLayer:
    def __init__(self, image_name, parallax_factor):
        self.image_name = image_name
        self.image=None        
        self.parallax_factor = parallax_factor
        self.offset = 0

    def update(self, time_delta, velocity=0):
        self.offset -= velocity * self.parallax_factor * time_delta
        self.offset = self.offset % self.image.get_width()

    def load_image(self,screen):
        if self.image is None:
            image = pygame.image.load(self.image_name).convert_alpha()
            #print("original image size:", image.get_size())
            scale_factor = screen.get_height() / image.get_height()
            #print("scale factor:", scale_factor)
            new_width = int(image.get_width() * scale_factor)
            self.image = pygame.transform.scale(image, (new_width, screen.get_height()))
        self.screen_size = screen.get_size()

    def draw(self, screen,camera):
        if self.image is None:
            self.load_image(screen)
        start_offset=self.offset
        while start_offset>0:
            start_offset-=self.image.get_width()
        while start_offset<screen.get_width():
            screen.blit(self.image, (start_offset, 0))
            start_offset+=self.image.get_width()

#TODO make a version of the background parallax layer that alternates or picks random images for variety


class BackgroundParallax(Background):
    def __init__(self,image_names=[], parallax_factors=[],velocity=0):
        super().__init__()
        self.layers = []
        for i, image_name in enumerate(image_names):
            parallax_factor = parallax_factors[i] if i < len(parallax_factors) else 1.0
            layer = BackgroundParallaxLayer(image_name, parallax_factor=parallax_factor)
            self.layers.append(layer)
        self.velocity = velocity # x velocity
        self.initialized = False

    def initialize(self, screen):
        self.screen_size = screen.get_size()
        self.initialized = True

    def add_layer(self, image, parallax_factor):
        layer = BackgroundParallaxLayer(image, parallax_factor)
        self.layers.append(layer)

    def update(self, time_delta):
        for layer in self.layers:
            layer.update(time_delta, velocity=self.velocity)

    def draw(self, screen,camera):
        if not self.initialized:
            self.initialize(screen)
        for layer in self.layers:
            layer.draw(screen,camera)

    def update_property(self, property_name, property_value):
        if property_name=="velocity":            
            self.velocity=property_value
            return True
        #Override in subclasses to handle property updates
        return super().update_property(property_name, property_value)
    
class BackgroundParallaxStarField(BackgroundParallax):
    def __init__(self, stars_per_layer,n_layers,parallax_factors=[], velocity=0):
        super().__init__()
        self.stars_per_layer = stars_per_layer
        self.n_layers = n_layers
        self.parallax_factors = parallax_factors
        self.velocity = velocity
        self.layers = []

    def initialize(self, screen):
        self.screen_size = screen.get_size()
        for i in range(self.n_layers):
            background_image=pygame.Surface((2*self.screen_size[0],self.screen_size[1]),pygame.SRCALPHA)
            background_image.fill((0, 0, 0, 0))  # Transparent background
            for _ in range(self.stars_per_layer):
                x = random.randint(0, background_image.get_width()-1)
                y = random.randint(0, background_image.get_height()-1)
                brightness = random.randint(150, 255)
                pygame.draw.circle(background_image, (brightness, brightness, brightness), (x, y), 1)
            layer=BackgroundParallaxLayer(None, parallax_factor=self.parallax_factors[i] if i < len(self.parallax_factors) else (i+1)/self.n_layers)
            layer.image=background_image
            self.layers.append(layer)
            #print("adding layer",i,"with parallax factor",layer.parallax_factor)
        self.initialized = True

def load_background(background_name, info_file="data/background_info.yaml",velocity=0):
    print("loading background info from",info_file)
    with open(info_file, 'r') as file:
        background_info = yaml.safe_load(file)
    if background_name not in background_info:
        raise Exception("Background not found: "+background_name)
    bg_data = background_info[background_name]
    if "special" in bg_data:
        if bg_data["special"]=="star_field":
            stars_per_layer=bg_data.get("stars_per_layer",100)
            n_layers=bg_data.get("n_layers",3)
            parallax_factors=bg_data.get("parallax_factors",[])
            return BackgroundParallaxStarField(stars_per_layer=stars_per_layer,n_layers=n_layers,velocity=velocity,parallax_factors=parallax_factors)
        
    image_names = bg_data.get("images", [])
    parallax_factors = bg_data.get("parallax_factors", [])
    return BackgroundParallax(image_names=image_names, parallax_factors=parallax_factors,velocity=velocity)