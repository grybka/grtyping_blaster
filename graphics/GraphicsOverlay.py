import pygame
#This is an overlay showing player health and score
#Health is shown as a health bar at the bottom and labeled "Health:"
#Score is shown as text at the top-left labeled "Score: <score>"

class GraphicsOverlay:
    def __init__(self):
        self.player_health=100
        self.player_score=0

    def draw(self,screen):
        screen_size=screen.get_size()
        #Draw health bar at bottom
        health_bar_width=200
        health_bar_height=20
        health_bar_x=20
        health_bar_y=screen_size[1]-health_bar_height-20
        pygame.draw.rect(screen,(255,0,0),(health_bar_x,health_bar_y,health_bar_width,health_bar_height))
        current_health_width=int((self.player_health/100)*health_bar_width)
        pygame.draw.rect(screen,(0,255,0),(health_bar_x,health_bar_y,current_health_width,health_bar_height))
        #Draw health label
        font=pygame.font.SysFont(None,24)
        health_label=font.render("Health:",True,(255,255,255))
        screen.blit(health_label,(health_bar_x-80,health_bar_y))
        #Draw score at top-left
        score_label=font.render(f"Score: {self.player_score}",True,(255,255,255))
        screen.blit(score_label,(20,20))