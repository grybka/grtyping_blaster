import math
import pygame
from graphics.GraphicsBase import ScreenSprite

default_font_size=36

class HitLetter(ScreenSprite):
    # An animation of a single letter correctly typed that starts slightly larger
    # and shrinks to the right size
    def __init__(self, position=(0, 0), letter="A"):
        #the position given should be where the letter's upper left will be at the end of the animation
        super().__init__(position)
        self.letter = letter
        self.elapsed_time = 0
        self.duration = 0.5  # seconds
        self.start_scale = 1.5
        self.end_scale = 1.0
        font = pygame.font.Font(None, default_font_size)
        self.text_surface = font.render(self.letter, True, (255, 255, 255))
        surf_size = self.text_surface.get_size()
        self.screen_wh = (surf_size[0], surf_size[1])

    def draw(self, screen, camera):
        # Calculate current scale
        progress = min(self.elapsed_time / self.duration, 1.0)
        current_scale = self.start_scale + (self.end_scale - self.start_scale) * progress
        # Scale the text surface
        scaled_width = int(self.text_surface.get_width() * current_scale)
        scaled_height = int(self.text_surface.get_height() * current_scale)
        scaled_surface = pygame.transform.scale(self.text_surface, (scaled_width, scaled_height))
        # Calculate position to keep it centered
        draw_x = self.position[0] - (scaled_width - self.screen_wh[0]) // 2
        draw_y = self.position[1] - (scaled_height - self.screen_wh[1]) // 2
        screen.blit(scaled_surface, (draw_x, draw_y))

    def update(self, time_delta):
        self.elapsed_time += time_delta
        if self.elapsed_time >= self.duration:
            self.scheduled_for_removal = True

class WrongLetter(ScreenSprite):
    # An animation of a single letter incorrectly typed that shakes
    def __init__(self, position=(0, 0), letter="A"):
        super().__init__(position)
        self.letter = letter
        self.elapsed_time = 0
        self.duration = 0.5  # seconds
        font = pygame.font.Font(None, default_font_size)
        self.text_surface = font.render(self.letter, True, (255, 0, 0))
        surf_size = self.text_surface.get_size()
        self.screen_wh = (surf_size[0], surf_size[1])

    def draw(self, screen, camera):
        screen.blit(self.text_surface, self.position)

    def update(self, time_delta):
        self.elapsed_time += time_delta
        self.original_position = self.position
        # Shake effect
        if self.elapsed_time < self.duration:
            shake_amplitude = 2
            shake_frequency = 7
            offset_x = shake_amplitude * math.sin(shake_frequency * self.elapsed_time * 2 * math.pi)
            offset_y = shake_amplitude * math.cos(shake_frequency * self.elapsed_time * 2 * math.pi)
            self.position = (self.original_position[0] + offset_x, self.original_position[1] + offset_y)
        else:
            self.scheduled_for_removal = True
            self.position = self.original_position

class TargetTextWindow(ScreenSprite):
    def __init__(self, position=(0, 0), text=""):
        # This is a screen sprite
        # position is the top left of the screen coords
        super().__init__(position)
        self.margin = 10 # margin around text in pixels
        self.text = text
        self.progress = 0  # Number of characters correctly typed
        self.target_text_color = (0, 255, 0)
        self.correct_text_color = (255, 255, 255)
        # Generate the text surface
        font = pygame.font.Font(None, 36)
        self.text_surface = font.render(self.text, True, self.target_text_color)
        surf_size = self.text_surface.get_size()
        self.screen_wh = (surf_size[0] + 2 * self.margin, surf_size[1] + 2 * self.margin)
        self.visible = True
        self.animations = []  # List of HitLetter animations

    def set_screen_position(self, position):
        old_position = self.position
        delta_position = (position[0] - old_position[0], position[1] - old_position[1])
        super().set_screen_position(position)
        #update all animations by the same delta
        for anim in self.animations:
            anim.set_screen_position((anim.position[0] + delta_position[0], anim.position[1] + delta_position[1]))


    def correct_letter_typed(self):
        if self.progress < len(self.text):
            letter = self.text[self.progress]
            # Calculate position of the letter in screen coordinates
            font = pygame.font.Font(None, 36)
            letter_surface = font.render(self.text[:self.progress], True, self.target_text_color)
            letter_width = letter_surface.get_width()
            letter_x = self.position[0] + self.margin + letter_width
            letter_y = self.position[1] + self.margin
            # Create a HitLetter animation
            hit_letter = HitLetter(position=(letter_x, letter_y), letter=letter)
            self.animations.append(hit_letter)
            self.progress += 1

    def incorrect_letter_typed(self):
        if self.progress < len(self.text):
            letter = self.text[self.progress]
            # Calculate position of the letter in screen coordinates
            font = pygame.font.Font(None, 36)
            letter_surface = font.render(self.text[:self.progress], True, self.target_text_color)
            letter_width = letter_surface.get_width()
            letter_x = self.position[0] + self.margin + letter_width
            letter_y = self.position[1] + self.margin
            # Create a WrongLetter animation
            wrong_letter = WrongLetter(position=(letter_x, letter_y), letter=letter)
            self.animations.append(wrong_letter)

    def draw(self, screen, camera):
        if not self.visible:
            return
        rect=self.get_screen_rect(camera)
        # Don't draw if offscreen
        if rect[0]<0 or rect[1]<0 or rect[0]+rect[2]>screen.get_width() or rect[1]+rect[3]>screen.get_height():
            return


        # Draw the border and background of the text window
        border_color = (255, 255, 255)
        screen.fill((0, 0, 0), self.get_screen_rect(camera))
        pygame.draw.rect(screen, border_color, self.get_screen_rect(camera), 2)
        # Draw the text with progress indication
        screen.blit(self.text_surface, (self.position[0]+self.margin, self.position[1]+self.margin))
        font = pygame.font.Font(None, 36)
        # Highlight the correctly typed portion
        if self.progress > 0:
            correct_text = self.text[:self.progress]
            correct_surface = font.render(correct_text, True, self.correct_text_color)
            screen.blit(correct_surface, (self.position[0]+self.margin, self.position[1]+self.margin))
        # Draw any animations for correctly typed letters
        for anim in self.animations:
            anim.draw(screen, camera)

    def update(self, time_delta):
        if self.progress >= len(self.text):
            self.scheduled_for_removal = True
        # Update animations
        for anim in self.animations:
            anim.update(time_delta) 
        # Remove finished animations
        self.animations = [anim for anim in self.animations if not anim.should_remove()]