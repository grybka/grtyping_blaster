from game_world.Procedure import Procedure
from sprite.ImageSprite import ShrinkingSprite
from sprite.TargetTextWindow import TargetTextWindow
from sprite.TestCircle import TestCircle
from sprite.SpriteWithTextWindow import SpriteWithTextWindow
from sprite.SpriteMotionScript import SMSE_ChangeTextboxVisibility, SMSE_Wait, SMSE_MoveToPosition, SMSE_MoveToPosition_Smooth,SMSE_MoveToSprite
from graphics.Graphics import Graphics
from sprite.SpriteFactory import get_sprite_factory
from sound.Sound import get_sound_store


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

class Target:
    # This is an object with text that can be typed
    def __init__(self, text, game_world,motion_script: Procedure=None,object_sprite=None):
        self.game_world=game_world
        self.graphics=game_world.graphics
        self.text=text
        self.on_char=0
        #self.text_window=TargetTextWindow(text=text)
        self.object_sprite=object_sprite or TestCircle(position=(0,0))
#        self.object_sprite=TestCircle(position=(0,0))
        self.sprite_with_window=SpriteWithTextWindow(position=(-200,-200), text=text, sprite=self.object_sprite,visibility=True)
        
        if motion_script is None:
            motion_script=Procedure()

        self.set_motion_script(motion_script)
       
        self.should_remove=False
        #These are scripts for things like explosions, letter hits, etc
        self.animations=[]
        self.is_alive=True #Used to see if it can shoot back at the player

    def start(self):
        self.graphics.add_sprite(self.sprite_with_window)

    def set_motion_script(self, motion_script: Procedure):
        self.motion_script=motion_script
        motion_script.set_property("target",self)
        motion_script.set_property("sprite",self.sprite_with_window)
        motion_script.set_property("game_world",self.game_world)


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
        get_sound_store().play_sound("laser")
        #Here is the shooting animation.  How to do this more generally?
        if self.on_char < len(self.text):
            shoot_anim=Animation()
            player_pos=self.game_world.get_player_world_position()
            shoot_anim.sprites.append(TestCircle(position=player_pos,radius=5))
            self.graphics.add_sprite(shoot_anim.sprites[0])
            shoot_anim.motion_script.add_step(SMSE_MoveToSprite(shoot_anim.sprites[0], target_sprite=self.object_sprite,duration=0.5))
            self.animations.append(shoot_anim)
        else: #finishing move
            self.is_alive=False
            shoot_anim=Animation()
            player_pos=self.game_world.get_player_world_position()
            shoot_anim.sprites.append(TestCircle(position=player_pos,radius=5))
            self.graphics.add_sprite(shoot_anim.sprites[0])
            shoot_anim.motion_script.add_step(SMSE_MoveToSprite(shoot_anim.sprites[0], target_sprite=self.object_sprite,duration=0.5))
            shoot_anim.finishing_move=True
            self.animations.append(shoot_anim)

    def incorrect_letter_typed(self):
        get_sound_store().play_sound("mistype")
        self.sprite_with_window.text_window.incorrect_letter_typed()

    def finalize(self):
        #called right before it will be removed
        self.sprite_with_window.scheduled_for_removal = True
        if not self.is_alive:
            #Death animation here        
            #same ship but shrinking
            shrinker=ShrinkingSprite(self.sprite_with_window.sprite.image,world_position=self.sprite_with_window.position,angle=0,shrink_rate=1.0)
            self.game_world.graphics.add_sprite(shrinker)
            #explosion animation
            exp_sprite=get_sprite_factory().create_animated_sprite("explosion1")
            exp_sprite.end_on_last_frame=True
            exp_sprite.position=self.sprite_with_window.position
            self.game_world.graphics.add_sprite(exp_sprite)
            #explosion sound
            get_sound_store().play_sound("explosion")

    def update(self, time_delta):
        self.motion_script.update(time_delta)
        for anim in self.animations:
            anim.update(time_delta)
            #make sure animation is finalized before removal
            if anim.is_done():
                anim.finalize()
                if anim.finishing_move: #I was waiting for this to complete before ending
                    self.should_remove=True
        self.animations=[a for a in self.animations if not a.is_done()]