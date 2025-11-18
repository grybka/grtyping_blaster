from game_state.GameManagerBase import GameState, GameManagerBase, GameStatus
from game_state.PlayGameLevel import LevelDoneState, PlayGameLevel, GameOverState
from game_state.LevelSelect import LevelSelectState
import pygame

class FadeCutState(GameState):
    def __init__(self,screen,next_state):
        self.screen=screen
        self.alpha=0
        self.fade_in=True
        self.fade_out=False
        self.done=False
        self.fade_surface=pygame.Surface(screen.get_size())
        self.next_state=next_state        
        self.fade_surface.fill((0,0,0))
        self.old_background=pygame.display.get_surface().copy()

    def handle_event(self, event):
        ...

    def update(self, time_delta):
        #A good spot to put asynchronous loading of next state resources
        max_alpha=150
        if self.fade_in:
            self.alpha+=200*time_delta
            if self.alpha>=max_alpha:
                self.alpha=255
                self.fade_in=False
                self.fade_out=True
                self.next_state.update(time_delta)  #ensure next state gets updated at least once
        elif self.fade_out:
            self.next_state.update(time_delta)
            self.alpha-=200*time_delta
            if self.alpha<=0:                
                self.alpha=0
                self.fade_out=False
                self.done=True

    def draw(self,screen):
        if self.fade_in:   
            self.old_background.blit(self.screen,(0,0))         
            self.fade_surface.set_alpha(int(self.alpha))
            screen.blit(self.fade_surface,(0,0))
        elif self.fade_out:
            self.next_state.draw(screen)
            self.fade_surface.set_alpha(int(self.alpha))
            screen.blit(self.fade_surface,(0,0))

    def get_status(self):
        if self.done:
            return GameStatus(True, "fadecut",self.next_state)
        return GameStatus(False)


class GameManager(GameManagerBase):
    def __init__(self,screen,on_game_state=None):
        super().__init__(on_game_state)
        self.screen=screen

    def next_state(self, status):
        if status.change_state:
            if status.new_state=="fadecut":
                self.on_game_state=status.data
                return
            if status.new_state=="PlayGameLevel":
                #TODO get level name
                #self.on_game_state=PlayGameLevel(self.screen,level_name=status.data)
                self.on_game_state=FadeCutState(self.screen,PlayGameLevel(self.screen,level_name=status.data))
            if status.new_state=="LevelDoneState":
                score=status.data
                #self.on_game_state=LevelDoneState(self.screen,score)
                self.on_game_state=FadeCutState(self.screen,LevelDoneState(self.screen,score))
            if status.new_state=="GameOverState":
                score=status.data
                #self.on_game_state=GameOverState(self.screen,score)
                self.on_game_state=FadeCutState(self.screen,GameOverState(self.screen,score))
            if status.new_state=="Quit":
                pygame.quit()
                exit()
            if status.new_state=="LevelSelectState":
                #self.on_game_state=LevelSelectState(self.screen)                                
                self.on_game_state=FadeCutState(self.screen,LevelSelectState(self.screen))

        #if status=="LevelDone":
        ##    score=self.on_game_state.world.player_score
            #self.on_game_state.world.end_level()
        #    self.on_game_state=LevelDoneState(self.screen,score)
        #elif status=="GameOver":
        #    score=self.on_game_state.world.player_score
            #self.on_game_state.world.end_level()
        #    self.on_game_state=GameOverState(self.screen,score)