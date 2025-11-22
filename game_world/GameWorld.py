import copy
from graphics.Graphics import Graphics
#from game_world.Target import Target
from sprite.SpriteFactory import get_sprite_factory
from game_world.Procedure import Procedure
from game_world.WorldProcedures import WP_PlayerDead, WP_Wait, WP_PlayAnimation, WP_PlaySound
from sound.Sound import get_sound_store
import random

class WorldObject: #an object in the game world, usually drawn to the screen
    def __init__(self,position=(0,0)):
        self.motion_script=Procedure()
        self.position=position        
        self.should_remove=False
        #self.set_position(position)        

    def get_sprites(self):
        return []

    def set_position(self, position):
        self.position = position
        for sprite in self.get_sprites():  
            sprite.set_world_position(position)

    def get_position(self):
        return self.position

    def update(self, time_delta):
        self.motion_script.update(time_delta)        

    def set_motion_script(self, motion_script: Procedure):
        motion_script.set_property("object",self)
        self.motion_script = motion_script

    def schedule_for_removal(self):
        self.should_remove=True

    def check_should_remove(self):
        return self.should_remove    
    
    def finalize(self):
        #called before removal
        pass

    def is_targetable(self):
        return False
    
    def start(self):
        pass


class GameWorld:
    def __init__(self,graphics: Graphics):
        self.graphics=graphics
        self.player_object=None
        self.default_player_script=None
        self.world_objects=[]



        self.targets=[]
        
        self.on_target=None
        self.player_health=100
        self.player_score=0
        self.procedures=[]
        self.game_on=True
        self.player_alive=True
        self.player_sprite=None
        print("Game World initialized as ", self)
        self.wait_for_keypress=False
        #Stats for the level
        self.letters_hit=0
        self.letters_missed=0

    def add_player(self, player_object: WorldObject):
        self.player_object=player_object
        self.add_world_object(player_object)

    def set_default_player_script(self,motion_script: Procedure):
        self.default_player_script=motion_script

    def add_world_object(self, world_object: WorldObject):
        self.world_objects.append(world_object)
        for sprite in world_object.get_sprites():
            self.graphics.add_sprite(sprite)        

    def add_target(self,target):        
        self.add_world_object(target)

    #def set_player_sprite(self,sprite):
        #depricated        
        #self.player_sprite=sprite
        #print("screen position:", self.graphics.screen_size[0]//2, self.graphics.screen_size[1]-100)
        #self.player_sprite.set_screen_position((self.graphics.screen_size[0]//4, self.graphics.screen_size[1]//2),self.graphics.camera)
        #self.player_sprite.set_screen_position((self.graphics.screen_size[0]//2, self.graphics.screen_size[1]-100),self.graphics.camera)       
        #self.graphics.add_sprite(sprite)

    def get_targets(self,alive_only=True):
        if not alive_only:
            return [t for t in self.world_objects if t.is_targetable()]
        return [t for t in self.world_objects if t.is_targetable() and t.is_alive]

    def add_procedure(self,procedure):
        self.procedures.append(procedure)
        self.some_bool=True

    def text_typed(self,text):    
        if self.wait_for_keypress:
            self.wait_for_keypress=False
            return
        targets=[ t for t in self.world_objects if t.is_targetable() and t.is_alive ]            
        #print("n targets available:", len(targets))
        if self.on_target is None:
            #figure out which to target
            if len(targets)==1:
                self.on_target=targets[0]
            else:
                for target in targets:
                    if target.is_alive and target.accepts_text(text):
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
        #update world objects (including player and targets)
        for obj in self.world_objects:
            obj.update(time_delta)
        #check if player needs to be given default script
        if self.player_object is not None and self.default_player_script is not None:
            if self.player_object.motion_script.is_done():
                #give default script
                new_script=copy.deepcopy(self.default_player_script)
                self.player_object.set_motion_script(new_script)            

        #check objects for removal
        for obj in self.world_objects:
            if obj.check_should_remove():                
                obj.finalize()
        self.world_objects=[obj for obj in self.world_objects if not obj.check_should_remove()]
        
        #update procedures
        for procedure in self.procedures:
            procedure.update(time_delta)
        self.procedures=[p for p in self.procedures if not p.is_done()]
        #remove any completed objects            
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
        return self.player_object.get_position()
    
    def damage_player(self, damage_amount):
        self.player_health-=damage_amount
        if self.player_health<0:
            self.player_health=0
    
    def end_level(self):
        #Clean up the game world for ending the level
        for object in self.world_objects:
            object.finalize()        
        self.game_on=False
