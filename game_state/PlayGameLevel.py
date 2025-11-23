import pygame
from game_state.GameManagerBase import GameState, GameManagerBase, GameStatus
from game_world.GameWorld import GameWorld
from graphics.Graphics import Graphics
from game_state.GameLevels import *
from sound.Sound import get_sound_store

class LevelScore:
    def __init__(self,letters_hit, letters_missed):
        self.letters_hit=letters_hit
        self.letters_missed=letters_missed
        self.letters_typed=0
        self.letter_timing=0
        self.letters_collected=0

    def get_score(self):
        return self.letters_hit*10 - self.letters_missed*5

class PlayGameLevel(GameState):
    def __init__(self,screen,level_name={}, global_player_state=None):
        super().__init__(global_player_state)
        # Initialize graphics first and pass to world
        self.graphics = Graphics(screen)
        get_sound_store().load_sounds()
        self.world = GameWorld(self.graphics)
        if level_name["name"]=="Introduction":
            self.level_script=get_levelzero_script(self.world)
        elif level_name["name"]=="LevelOne":        
            self.level_script = get_levelone_script(self.world)
        elif level_name["name"]=="LevelTwo":        
            self.level_script = get_leveltwo_script(self.world)


    def start(self):
        self.graphics.show_overlay=True

    def handle_event(self, event):
        if event.type==pygame.TEXTINPUT:
            #event.text contains the character typed
            self.world.text_typed(event.text)
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            self.world.text_typed('\n')
        ...

    def update(self, time_delta):
        self.world.update(time_delta)
        self.graphics.update(time_delta)
        self.level_script.update(time_delta)

    def draw(self,screen):
        self.graphics.draw(screen)

    def get_status(self):
        if self.world.game_on==False:   
            score = LevelScore(self.world.letters_hit, self.world.letters_missed)
            score.letters_typed=self.world.letters_timed
            score.letter_timing=self.world.letter_timing
            score.letters_collected=self.world.letters_collected
            if self.world.player_alive==True:
                return GameStatus(True, "LevelDoneState", data=score)
            else:
                return GameStatus(True, "GameOverState", data=score)
        return GameStatus(False)
        #if self.world.game_on==False:   
        ##    if self.world.player_alive==False:
        #        return "GameOver"
        #    else:
        #        return "LevelDone"
        #return "PlayingLevel"



class LevelDoneState(GameState):
    def __init__(self,screen,score: LevelScore, global_player_state=None):
        super().__init__(global_player_state)
        self.screen=screen
        self.font=pygame.font.Font(None,48)
        self.text=self.font.render(f"Level Complete!\n",True,(255,255,255))
        self.text_rect=self.text.get_rect(center=(screen.get_width()//2,screen.get_height()//2))
        #make a text rect that shows letters hit, letters missed, and score
        self.letters_hit_text=self.font.render(f"Letters Hit: {score.letters_hit}", True, (255,255,255))
        self.letters_missed_text=self.font.render(f"Letters Missed: {score.letters_missed}", True, (255,255,255))
        self.score_text=self.font.render(f"Score: {score.get_score()}", True, (255,255,255))
        self.letters_hit_rect=self.letters_hit_text.get_rect(center=(screen.get_width()//2,screen.get_height()//2 + 50))
        self.letters_missed_rect=self.letters_missed_text.get_rect(center=(screen.get_width()//2,screen.get_height()//2 + 100))
        self.score_rect=self.score_text.get_rect(center=(screen.get_width()//2,screen.get_height()//2 + 150))
        #if letters_timed >0 show wpm
        if score.letters_typed >0 and score.letter_timing>0:
            wpm = (score.letters_typed / 5) / (score.letter_timing / 60)
            self.wpm_text=self.font.render(f"WPM: {wpm:.2f}", True, (255,255,255))
            self.wpm_rect=self.wpm_text.get_rect(center=(screen.get_width()//2,screen.get_height()//2 + 200))
        #if letters collected > 0 show letters collected
        if score.letters_collected >0:
            self.collected_text=self.font.render(f"Letters Collected: {score.letters_collected}", True, (255,255,255))
            self.collected_rect=self.collected_text.get_rect(center=(screen.get_width()//2,screen.get_height()//2 + 250))
        self.score=score
        self.should_quit=False

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            self.should_quit=True        

    def update(self, time_delta):
        ...

    def draw(self,screen):
        screen.fill((0,0,0))
        screen.blit(self.text,self.text_rect)
        screen.blit(self.letters_hit_text,self.letters_hit_rect)
        screen.blit(self.letters_missed_text,self.letters_missed_rect)
        screen.blit(self.score_text,self.score_rect)
        if hasattr(self, 'wpm_text'):
            screen.blit(self.wpm_text, self.wpm_rect)
        if hasattr(self, 'collected_text'):
            screen.blit(self.collected_text, self.collected_rect)
    def get_status(self):
        if self.should_quit:
            return GameStatus(True, "LevelSelectState")
        return GameStatus(False)

class GameOverState(GameState):
    def __init__(self,screen,score, global_player_state=None):
        super().__init__(global_player_state)
        self.screen=screen
        self.font=pygame.font.Font(None,48)
        self.text=self.font.render(f"You Got Exploded!",True,(255,0,0))
        self.text_rect=self.text.get_rect(center=(screen.get_width()//2,screen.get_height()//2))
        #make a text rect that shows letters hit, letters missed, and score
        self.letters_hit_text=self.font.render(f"Letters Hit: {score.letters_hit}", True, (255,255,255))
        self.letters_missed_text=self.font.render(f"Letters Missed: {score.letters_missed}", True, (255,255,255))
        self.score_text=self.font.render(f"Score: {score.get_score()}", True, (255,255,255))
        self.letters_hit_rect=self.letters_hit_text.get_rect(center=(screen.get_width()//2,screen.get_height()//2 + 50))
        self.letters_missed_rect=self.letters_missed_text.get_rect(center=(screen.get_width()//2,screen.get_height()//2 + 100))
        self.score_rect=self.score_text.get_rect(center=(screen.get_width()//2,screen.get_height()//2 + 150))
        self.score=score
        self.should_quit=False

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            self.should_quit=True            

    def update(self, time_delta):
        ...

    def draw(self,screen):
        screen.fill((0,0,0))
        screen.blit(self.text,self.text_rect)
        screen.blit(self.letters_hit_text,self.letters_hit_rect)
        screen.blit(self.letters_missed_text,self.letters_missed_rect)
        screen.blit(self.score_text,self.score_rect)

    def get_status(self):
        if self.should_quit:
            return GameStatus(True, "LevelSelectState")
        return GameStatus(False)
