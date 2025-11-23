import pygame
from game_state.GameManagerBase import GameState,GameStatus
from graphics.Graphics import Graphics
from graphics.GraphicsBase import Camera

class TheStore(GameState):
    def __init__(self,screen, global_player_state=None):
        super().__init__(global_player_state)
        self.screen=screen
        self.font=pygame.font.Font(None,36)
        self.text=self.font.render("Welcome to the Store! Press Q to Quit.",True,(255,255,255))
        self.text_rect=self.text.get_rect(center=(screen.get_width()//2,screen.get_height()//2))
        self.should_quit=False

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_q:
            self.should_quit=True

    def update(self, time_delta):
        pass

    def draw(self,screen):
        screen.fill((0,0,0))
        screen.blit(self.text,self.text_rect)

    def get_status(self):
        if self.should_quit:
            return GameStatus(True, "ReturnToGame")
        return GameStatus(False)