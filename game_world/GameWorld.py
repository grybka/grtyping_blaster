from graphics.Graphics import Graphics
from game_world.Target import Target
from sprite.SpriteFactory import get_sprite_factory
from game_world.Procedure import Procedure
from game_world.WorldProcedures import WP_PlayerDead, WP_Wait, WP_PlayAnimation, WP_PlaySound
from sound.Sound import get_sound_store
import random
class GameWorld:
    def __init__(self,graphics: Graphics):
        self.graphics=graphics
        self.targets=[]
        self.on_target=None
        self.player_health=100
        self.player_score=0
        self.procedures=[]
        self.game_on=True
        self.player_alive=True
        self.player_sprite=None
        print("Game World initialized as ", self)

    def get_player_sprite(self):
        return self.player_sprite

    def set_player_sprite(self,sprite):
        self.player_sprite=sprite
        print("screen position:", self.graphics.screen_size[0]//2, self.graphics.screen_size[1]-100)
        self.player_sprite.set_screen_position((self.graphics.screen_size[0]//2, self.graphics.screen_size[1]-100),self.graphics.camera)       
        self.graphics.add_sprite(sprite)

    def add_target(self,target: Target):
        self.targets.append(target)

    def add_procedure(self,procedure):
        self.procedures.append(procedure)
        self.some_bool=True

    def text_typed(self,text):
        if self.on_target is None:
            #figure out which to target
            if len(self.targets)==1:
                self.on_target=self.targets[0]
            else:
                for target in self.targets:
                    if target.is_alive and target.text.startswith(text):
                        self.on_target=target
                        break
                if self.on_target is None:
                    #no target found
                    return
        self.on_target.text_typed(text)
        
        #The target can take a while to disappear, so immediately switch target if it is dead
        if not self.on_target.is_alive:
            self.on_target=None

    def update(self, time_delta):
        for target in self.targets:
            target.update(time_delta)
            if target.should_remove:
                if self.on_target==target:
                    self.on_target=None
                target.finalize()
                self.player_score+=len(target.text)
        #update procedures
        for procedure in self.procedures:
            procedure.update(time_delta)
        self.procedures=[p for p in self.procedures if not p.is_done()]
        #remove any completed targets
        self.targets=[t for t in self.targets if not t.should_remove]
        self.graphics.overlay.player_health=self.player_health
        self.graphics.overlay.player_score=self.player_score
        #Make player explode if out of health
        if self.player_health<=0 and self.game_on and self.player_alive:            
            blowup_procedure=Procedure()
            player_position=self.get_player_world_position()
            for i in range(5):
                exp_sprite=get_sprite_factory().create_animated_sprite("explosion1")
                exp_sprite.end_on_last_frame=False                
                exp_sprite.position=(player_position[0]+random.randint(-30,30),player_position[1]+random.randint(-30,30))
                blowup_procedure.add_step(WP_PlayAnimation(self.graphics,exp_sprite))
                blowup_procedure.add_step(WP_PlaySound("explosion"))
                blowup_procedure.add_step(WP_Wait(0.2))      
            blowup_procedure.add_step(WP_Wait(1.0))
            blowup_procedure.add_step(WP_PlayerDead(self,exp_sprite))          
            self.procedures.append(blowup_procedure)
            self.player_alive=False

    def get_player_world_position(self):
        return self.get_player_sprite().get_world_position(None)
    
    def end_level(self):
        #Clean up the game world for ending the level
        for target in self.targets:
            target.finalize()
        self.targets=[]
        self.game_on=False
