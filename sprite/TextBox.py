from graphics.GraphicsBase import ScreenSprite, WorldSprite
import pygame


class TextBox(ScreenSprite):
    def __init__(self, position=(0, 0), size=(200, 100), font_size=24, text="", text_color=(255, 255, 255), bg_color=(0, 0, 0)):
        super().__init__(position)
        self.size = size
        self.font_size = font_size
        self.text = text
        self.text_color = text_color
        self.bg_color = bg_color
        self.font = pygame.font.Font(None, self.font_size)
        #self.text_surface = self.font.render(self.text, True, self.text_color)
        self.text_surface = None #none mean it isn't rendered yet
        self.background_surface = pygame.Surface(self.size)
        self.background_surface.fill(self.bg_color)
        self.has_border = True
        self.text_wrap = True        
        self.top_justify = True
    

    def set_text(self, text):
        self.text = text
        self.text_surface = None  # Mark for re-rendering

    def render_text(self):
        #figure out where to break the text if wrapping is enabled
        if self.text_wrap:
            words = self.text.split(' ')
            lines = []
            current_line = ""
            for word in words:
                test_line = current_line + word + " "
                test_width, _ = self.font.size(test_line)
                if test_width <= self.size[0] - 10:  # 10 pixel padding
                    current_line = test_line
                else:
                    lines.append(current_line)
                    current_line = word + " "
            lines.append(current_line)  # add the last line
            self.text = '\n'.join(lines)
        self.text_surface = self.font.render(self.text, True, self.text_color)
        


    def draw(self, screen, camera):
        # Draw background
        screen.blit(self.background_surface, self.position)
        if self.has_border:
            pygame.draw.rect(screen, (255, 255, 255), (self.position[0], self.position[1], self.size[0], self.size[1]), 2)
        # Draw text
        if self.text_surface is None:
            self.render_text()
        if not self.top_justify:
            text_rect = self.text_surface.get_rect(center=(self.position[0] + self.size[0] // 2,
                                                        self.position[1] + self.size[1] // 2))   
        else:
            text_rect = self.text_surface.get_rect(topleft=(self.position[0] + 5, self.position[1] + 5))
        screen.blit(self.text_surface, text_rect)