import random
from graphics.GraphicsBase import ScreenSprite, WorldSprite
from sprite.TextBox import TextBox
from sprite.SpriteSheet import get_sprite_store
import pygame

class CutsceneCommunication(ScreenSprite):
    # A sprite that has a text box and a character image for cutscene communication
    def __init__(self, character_image, position=(0, 0)):
        super().__init__(position=position)
        self.character_image = get_sprite_store().get_sprite(character_image)
        textbox_y_size=self.character_image.get_height() + 20 if self.character_image else 100
        self.text_box = TextBox(size=(400, textbox_y_size))
        self.text_box.has_border = False       
        self.my_text="Lorem Ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua." 
        self.on_character=0
        self.last_keystroke_time=0
        self.elapsed_time=0
        self.typing_error=0
        self.error_probability=0.2
        self.typed_text=""

    def set_position(self, position):
        self.set_screen_position(position)
        self.text_box.set_screen_position((position[0], position[1] ))

    def set_text(self, text):
        self.my_text=text
        self.on_character=0
        self.last_keystroke_time=0
        self.elapsed_time=0
        #self.text_box.set_text(text)    

    def update(self, time_delta):        
        typing_speed=5  #characters per second
        typing_rate=1/typing_speed
        self.elapsed_time += time_delta
        if self.typed_text == self.my_text:
            return
        #elif len(self.typed_text) == len(self.my_text):
         #   print("my text: {}, typed text: {}".format(self.my_text, self.typed_text))
        if self.elapsed_time - self.last_keystroke_time > typing_rate:
            self.last_keystroke_time = self.elapsed_time            
            if random.random() < self.error_probability:
                #choose a random letter from a to z
                error_char = chr(random.randint(ord('a'), ord('z')))                
                self.typed_text += error_char
                self.typing_error += 1
            else:                
                if self.typing_error > 0:
                    #fix an error
                    self.typed_text = self.typed_text[:-1]
                    self.typing_error -= 1
                else:
                    self.on_character += 1                            
                    self.typed_text += self.my_text[self.on_character-1:self.on_character]
            self.text_box.set_text(self.typed_text)
            

    def draw(self, surface,camera=None):       
        position=self.get_screen_position() 
        if self.character_image:
            #draw border around the whole thing
            total_width=self.character_image.get_width()+20 + self.text_box.size[0]
            total_height=max(self.character_image.get_height()+20,self.text_box.size[1])
            pygame.draw.rect(surface, (255, 255, 255), (position[0]-2, position[1]-2, total_width+4, total_height+4), 2)
            #draw border around character image
            #pygame.draw.rect(surface, (255, 255, 255), (position[0]-2, position[1]-2, self.character_image.get_width()+4, self.character_image.get_height()+4), 2)
            surface.blit(self.character_image, position)
            self.text_box.set_screen_position((position[0]+self.character_image.get_width(), position[1]))
        self.text_box.draw(surface,camera=None)
