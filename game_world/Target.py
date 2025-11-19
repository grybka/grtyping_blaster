from game_world.ObjectScripting import DamagePlayer, DespawnSelfObject, MoveObjectToPosition, MoveObjectToPosition_Smooth, MoveObjectToObject, SpawnSpriteAtObject
from game_world.Procedure import Procedure
from sprite.ImageSprite import ShrinkingSprite
from sprite.TargetTextWindow import TargetTextWindow
from sprite.TestCircle import TestCircle
from sprite.SpriteWithTextWindow import SpriteWithTextWindow
from sprite.SpriteMotionScript import SMSE_ChangeTextboxVisibility, SMSE_Wait, SMSE_MoveToPosition, SMSE_MoveToPosition_Smooth,SMSE_MoveToSprite
from graphics.Graphics import Graphics
from sprite.CutsceneCommunication import CutsceneCommunication
from sprite.SpriteFactory import get_sprite_factory
from sound.Sound import get_sound_store
from game_world.GameWorld import WorldObject
import random


class Animation:
    # I need to decide whether this lives in graphics or world
    # as it stands I could potentially update it twice
    # thinking now it should live in graphics
    def __init__(self):
        self.sprites = []
        self.motion_script=Procedure()
        self.finishing_move=False

    def update(self, time_delta):
#        for sprite in self.sprites:
#            sprite.update(time_delta)
        self.motion_script.update(time_delta)

    def draw(self, screen, camera):
        for sprite in self.sprites:
            sprite.draw(screen, camera)

    def is_done(self):
        # Determine if the animation is done
        return self.motion_script.is_done()
    
    def finalize(self):
        # Clean up any resources or finalize the animation
        for sprite in self.sprites:
            sprite.scheduled_for_removal = True
    
#There is quite a lot to a target.  It has:
# - text to be typed, and a tracker of progress
# - a text window showing the text
# - an object sprite in the world
# - a motion script to move the object sprite around
# - a sprite animation to play on a correct letter typed
# - a sprite animation to play on an incorrect letter typed
# - a sprite animation to play on completion (not yet implemented)

class Target(WorldObject):
    # This is an object with text that can be typed
    # TODO Needs a timeout
    def __init__(self, text, game_world,motion_script: Procedure=None,object_sprite=None,attack_on_error=True):
        super().__init__()
        self.game_world=game_world
        self.graphics=game_world.graphics
        self.text=text
        self.on_char=0
        #self.text_window=TargetTextWindow(text=text)
        self.object_sprite=object_sprite or TestCircle(position=(0,0))
#        self.object_sprite=TestCircle(position=(0,0))
        self.sprite_with_window=SpriteWithTextWindow(position=(-200,-200), text=text, sprite=self.object_sprite,visibility=True)                
       
        self.should_remove=False
        #These are scripts for things like explosions, letter hits, etc
        self.animations=[]
        self.is_alive=True #Used to see if it can shoot back at the player
        #
        self.attack_on_error=attack_on_error

    def start(self):
        self.graphics.add_sprite(self.sprite_with_window)

    def get_sprites(self):
        return [self.sprite_with_window]
    
    def set_position(self, position):
        self.position = position
        #print("target set position called: {}".format(position))
        for sprite in self.get_sprites():  
            sprite.set_position(position)

    def text_typed(self, char):
        if self.on_char < len(self.text):
            if self.text[self.on_char] == char:
                self.correct_letter_typed()
                #print("correct letter typed")
                return True
            else:
                self.incorrect_letter_typed()
                #print("incorrect letter typed")
                return False
        
        return True
            
    def correct_letter_typed(self):
        self.on_char += 1
        self.sprite_with_window.text_window.correct_letter_typed()
        if self.on_char < len(self.text):
            ...
        else:
            self.successful_completion()
            #execute defeated script here


        
#        get_sound_store().play_sound("laser")
        #Here is the shooting animation.  How to do this more generally?
#        if self.on_char < len(self.text):
#            shoot_anim=Animation()
#            player_pos=self.game_world.get_player_world_position()
#            shoot_anim.sprites.append(TestCircle(position=player_pos,radius=5))
#            self.graphics.add_sprite(shoot_anim.sprites[0])
#            shoot_anim.motion_script.add_step(SMSE_MoveToSprite(shoot_anim.sprites[0], target_sprite=self.object_sprite,duration=0.5))
#            self.animations.append(shoot_anim)
#        else: #finishing move
#            self.is_alive=False
#            shoot_anim=Animation()
#            player_pos=self.game_world.get_player_world_position()
#            shoot_anim.sprites.append(TestCircle(position=player_pos,radius=5))
#            self.graphics.add_sprite(shoot_anim.sprites[0])
#            shoot_anim.motion_script.add_step(SMSE_MoveToSprite(shoot_anim.sprites[0], target_sprite=self.object_sprite,duration=0.5))
#            shoot_anim.finishing_move=True
#            self.animations.append(shoot_anim)

    def successful_completion(self):
        print("Successful completion")

        
    def unsuccessful_completion(self):
        print("Unsuccessful completion")
        ...

    def incorrect_letter_typed(self):
        get_sound_store().play_sound("mistype")
        self.sprite_with_window.text_window.incorrect_letter_typed()
        if self.attack_on_error:
            self.unsuccessful_completion()
        #execute incorrect letters script here

    def schedule_for_removal(self):
        self.should_remove=True

    def check_should_remove(self):
        return self.should_remove

    def finalize(self):
        #called right before it will be removed
        self.sprite_with_window.scheduled_for_removal = True        

    def update(self, time_delta):
        super().update(time_delta)
        #self.motion_script.update(time_delta)
        #for anim in self.animations:
        #    anim.update(time_delta)
        #    #make sure animation is finalized before removal
        #    if anim.is_done():
        #        anim.finalize()
        #        if anim.finishing_move: #I was waiting for this to complete before ending
        #            self.should_remove=True
        #self.animations=[a for a in self.animations if not a.is_done()]

    def is_targetable(self):
        return True


class ChargingTarget(Target):
    # A target that charges the player on completion
    def __init__(self, text, game_world,motion_script: Procedure=None,object_sprite=None):
        super().__init__(text, game_world,motion_script,object_sprite)
        self.hit_player=False
        self.is_alive=True #willing to accept input
        self.has_timer=False
        self.elapsed_time=0
        self.time_limit=5.0
        self.timer_started=False

    def start_timer(self,time_limit):
        self.has_timer=True
        self.timer_started=True
        self.elapsed_time=0
        self.time_limit=time_limit

    def update(self, time_delta):
        super().update(time_delta)
        if self.has_timer and self.timer_started:
            self.elapsed_time += time_delta
            self.sprite_with_window.text_window.update_timer(self.time_limit - self.elapsed_time, self.time_limit)
            if self.elapsed_time > self.time_limit:
                #time's up
                self.unsuccessful_completion()
                self.timer_started=False


    def finalize(self):
        #called right before it will be removed
        ...
        #remove sprite
        self.sprite_with_window.schedule_for_removal()

        if self.hit_player:
            #replace ship with shrinking version
            shrinker=ShrinkingSprite(self.sprite_with_window.sprite.image,world_position=self.sprite_with_window.position,angle=0,shrink_duration=0.5)
            self.game_world.graphics.add_sprite(shrinker)
            #explode and damage player
            exp_sprite=get_sprite_factory().create_animated_sprite("explosion1")
            exp_sprite.end_on_last_frame=True
            exp_sprite.position=self.sprite_with_window.position
            self.game_world.graphics.add_sprite(exp_sprite)
            #make explosion sound
            get_sound_store().play_sound("explosion")
            #TODO damage player



    def successful_completion(self):        
        #player dodges, misses player
        self.is_alive=False
        impact_time=1.0
        object_position=self.get_position()        
        player_position=self.game_world.get_player_world_position()
        exit_x=-60
        dodge_by=150
        exit_y=(player_position[1]-object_position[1])/(player_position[0]-object_position[0])*(exit_x-object_position[0])+object_position[1]        
        impact_vel=((player_position[0]-object_position[0])/impact_time,(player_position[1]-object_position[1])/impact_time)
        exit_loc=(exit_x,exit_y)
        
        if random.choice([True,False]):
            dodge_loc=(player_position[0],player_position[1]+dodge_by)
        else:
            dodge_loc=(player_position[0],player_position[1]-dodge_by)
        if dodge_loc[1]<50:
            dodge_loc=(player_position[0],player_position[1]+dodge_by)
        if dodge_loc[1]>self.game_world.graphics.screen_size[1]-50:
            dodge_loc=(player_position[0],player_position[1]-dodge_by)
        print("Impact loc: {}, Dodge loc: {}, Target exit loc: {}".format(player_position, dodge_loc, exit_loc))
        #set player motion script to dodge
        dodge_script=Procedure([MoveObjectToPosition_Smooth(end_position=dodge_loc,duration=impact_time)])
        self.game_world.player_object.set_motion_script(dodge_script)
        #set self motion script to move offscreen        
        target_script=Procedure([MoveObjectToPosition_Smooth(end_position=player_position,object=self.object_sprite,duration=impact_time,final_velocity=impact_vel),
                                 MoveObjectToPosition(end_position=exit_loc,object=self.object_sprite,duration=0.2),
                                 DespawnSelfObject()
                                 ])
        self.set_motion_script(target_script)

    def unsuccessful_completion(self):
        #player hit, reduce health
        self.hit_player=True
        self.is_alive=False

        #same ship but shrinking
        shrinker=ShrinkingSprite(self.sprite_with_window.sprite.image,world_position=self.sprite_with_window.position,angle=0,shrink_duration=0.5)       
        target_script=Procedure([MoveObjectToObject(target_object=self.game_world.player_object,duration=1.0),
                                 DamagePlayer(damage_amount=10, object=self),                                 
                                 DespawnSelfObject()])
        self.set_motion_script(target_script)        
        
class ShootingTarget(Target):
    # A target that shoots at the player on incorrect letter
    def __init__(self, text, game_world,motion_script: Procedure=None,object_sprite=None):
        super().__init__(text, game_world,motion_script,object_sprite)
        self.is_alive=True #willing to accept input

    def unsuccessful_completion(self):
        #shoot at player
        shoot_anim=Animation()
        player_pos=self.game_world.get_player_world_position()
        shoot_anim.sprites.append(TestCircle(position=self.get_position(),radius=5))
        self.graphics.add_sprite(shoot_anim.sprites[0])
        shoot_anim.motion_script.add_step(SMSE_MoveToSprite(shoot_anim.sprites[0], target_sprite=self.game_world.player_object.object_sprite,duration=0.5))
        self.animations.append(shoot_anim)
        #damage player
        self.game_world.damage_player(5)

class CutsceneTargetComms(Target):
    # A window that displayes a cutscene communication and closes on keypress
    def __init__(self, text, game_world,motion_script: Procedure=None,object_sprite=None,character_image=None):
        super().__init__(text, game_world,motion_script,object_sprite,attack_on_error=False)        
        self.is_alive=True #willing to accept input
        self.sprite_with_window=CutsceneCommunication(character_image,text)
        self.set_position( (200,200))
        self.sprite_with_window.set_text(text)

    def start(self):
        self.graphics.add_sprite(self.sprite_with_window)

    def text_typed(self, char):
        self.successful_completion()
        return True
    
    def successful_completion(self):
        #just remove self
        self.is_alive=False
        self.schedule_for_removal()