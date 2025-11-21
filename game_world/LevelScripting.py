import copy
from game_world.GameWorld import GameWorld
from game_world.ObjectScripting import MoveObjectToPosition_Smooth, WobbleObject
from game_world.Procedure import Procedure, ProcedureStep
from game_world.WorldProcedures import WP_DamagePlayer
from sprite.SpriteMotionScript import SMSE_MoveToPosition, SMSE_MoveToPosition_Smooth, SMSE_MoveToSprite, SMSE_RemoveSprite, SMSE_SetPosition
from sprite.TestCircle import TestCircle
from sprite.CutsceneCommunication import CutsceneCommunication
from sound.Sound import get_sound_store

lev_debug=True

class LevelScriptElement(ProcedureStep):
    def __init__(self, game_world):
        self.game_world = game_world

    def start_step(self):
        if lev_debug:
            print(f"Starting level script element: {self.__class__.__name__}")

    def update(self, time_delta):
        pass

    def set_property(self, property_name, value):
        if property_name == "game_world":
            self.game_world = value
            return True
        return super().set_property(property_name, value)
    
    def step_done(self):
        return True
    
#Elements to make
#Wait for time
#Wait until target gone
#Wait until animation finished
#Add new target
#Modify Background

class LSE_Wait(LevelScriptElement):
    def __init__(self, game_world,duration: float):
        super().__init__(game_world)
        self.duration = duration
        self.elapsed_time = 0

    def update(self, time_delta):
        self.elapsed_time += time_delta

    def step_done(self):
        return self.elapsed_time >= self.duration
    
class LSE_WaitForNoTargets(LevelScriptElement):
    def __init__(self, game_world):
        super().__init__(game_world)

    def update(self, time_delta):
        pass

    def step_done(self):
        #alive_only=False to wait for all targets to be gone, there may be non alive targets finishing death animations
        return len(self.game_world.get_targets(alive_only=False)) == 0

class LSE_AddTarget(LevelScriptElement):
    def __init__(self, game_world, target, motion_script):
        super().__init__(game_world)
        self.target = target
        self.target.set_motion_script(copy.deepcopy(motion_script))
        self.is_done=False

    def start_step(self):
        self.target.start()
        return super().start_step()

    def update(self, time_delta):
        self.game_world.add_target(self.target)
        self.is_done=True

    def step_done(self):
        return self.is_done
    
class LSE_AddObject(LevelScriptElement):
    def __init__(self, game_world, object, motion_script):
        super().__init__(game_world)
        self.object = object
        self.object.set_motion_script(motion_script)
        self.is_done=False

    def start_step(self):
        self.object.start()
        return super().start_step()

    def update(self, time_delta):
        self.game_world.add_world_object(self.object)
        self.is_done=True

    def step_done(self):
        return self.is_done

class LSE_AddTarget(LevelScriptElement):
    def __init__(self, game_world, object, motion_script):
        super().__init__(game_world)
        self.object = object
        self.object.set_motion_script(copy.deepcopy(motion_script))
        self.is_done=False

    def start_step(self):
        self.object.start()
        return super().start_step()

    def update(self, time_delta):
        self.game_world.add_target(self.object)
        self.is_done=True

    def step_done(self):
        return self.is_done

class LSE_AddBackgroundSprite(LevelScriptElement):
    def __init__(self, game_world, background):
        super().__init__(game_world)
        self.background = background
        self.is_done = False

    def update(self, time_delta):
        self.game_world.set_background(self.background)
        self.is_done = True

    def step_done(self):
        return self.is_done
    
class LSE_SetBackground(LevelScriptElement):
    def __init__(self, game_world, background):
        super().__init__(game_world)
        self.background = background
        self.is_done = False

    def update(self, time_delta):
        self.game_world.graphics.add_background(self.background)
        self.is_done = True

    def step_done(self):
        return self.is_done
    
class LSE_UpdateBackground(LevelScriptElement):
    def __init__(self, game_world, property_name, property_value):
        super().__init__(game_world)
        self.property_name = property_name
        self.property_value = property_value
        self.is_done = False

    def update(self, time_delta):
        #print("LSE_UpdateBackground: updating", self.property_name, "to", self.property_value)
        self.game_world.graphics.update_background_property(self.property_name, self.property_value)
        self.is_done = True

    def step_done(self):
        return self.is_done
    

class LSE_TargetShootPlayer(LevelScriptElement):
    def __init__(self, game_world, source_target, damage_amount,n_shots=1, time_between_shots=1):
        super().__init__(game_world)
        self.source = source_target
        self.damage_amount = damage_amount
        self.n_shots = n_shots
        self.time_between_shots = time_between_shots
        self.is_done = False
        self.elapsed_time = 0
        self.shots_fired = 0

    def set_property(self, property_name, value):
        if property_name == "target":
            self.source = value
            return True
        return super().set_property(property_name, value)


    def update(self, time_delta):
        if not self.source.is_alive:
            self.is_done = True
            return
        self.elapsed_time += time_delta
        if self.elapsed_time <= self.time_between_shots:
            return
        self.elapsed_time=0
        #generate a script that shoots the player from the source
        source_pos=self.source.sprite_with_window.get_world_position(None)
        bullet=TestCircle(radius=5)
        #Play the shooting sound (Should I move this to the bullet procedure?  Maybe)
        get_sound_store().play_sound("enemy_laser")

        #print("source pos:", source_pos, "player pos:", player_pos)
        self.game_world.graphics.add_sprite(bullet)
        to_do=Procedure([
            SMSE_SetPosition(bullet, position=source_pos),
            SMSE_MoveToSprite(bullet, target_sprite=self.game_world.get_player_sprite(), duration=0.5),
            WP_DamagePlayer(self.game_world, self.damage_amount),
            SMSE_RemoveSprite(bullet)
        ])
        self.game_world.add_procedure(to_do)
        self.shots_fired+=1
        if self.shots_fired>=self.n_shots:
            self.is_done = True

    def step_done(self):
        return self.is_done
    

class LSE_EndLevel(LevelScriptElement):
    def __init__(self, game_world):
        super().__init__(game_world)
        self.is_done = False

    def update(self, time_delta):
        self.game_world.end_level()
        self.is_done = True

    def step_done(self):
        return self.is_done
    
class LSE_SetPlayerMotionScript(LevelScriptElement):
    def __init__(self, game_world, motion_script: Procedure):
        super().__init__(game_world)
        self.motion_script = motion_script
        self.is_done = False

    def update(self, time_delta):
        self.game_world.player_object.set_motion_script(self.motion_script)
        self.is_done = True

    def step_done(self):
        return self.is_done
    
class LSE_PlayerWarpsAway(LSE_SetPlayerMotionScript):
    def __init__(self, game_world):
        self.warp_position = (int(1.1 * game_world.graphics.screen_size[0]), game_world.graphics.screen_size[1] // 2)
        self.motion_script = Procedure([MoveObjectToPosition_Smooth(end_position=self.warp_position,duration=2.0),WobbleObject(duration=10.0)])
        super().__init__(game_world,motion_script=self.motion_script)
            
class LSE_RemoveTarget(LevelScriptElement):
    def __init__(self,game_world,target):
        super().__init__(game_world)
        self.target=target
        self.is_done = False

    def update(self, time_delta):
        self.target.should_remove=True
        self.is_done = True

    def set_property(self, property_name, value):
        if property_name == "target":
            self.target = value
            return True
        return super().set_property(property_name, value)

    def step_done(self):
        return self.is_done
    
class LSE_ChangeTextBoxVisibility(LevelScriptElement):
    def __init__(self, game_world, target, visible: bool):
        super().__init__(game_world)
        self.target = target
        self.visible = visible
        self.is_done = False

    def set_property(self, property_name, value):
        if property_name == "target":
            self.target = value
            return True
        return super().set_property(property_name, value)

    def update(self, time_delta):
        self.target.sprite_with_window.set_text_window_visibility(self.visible)        
        self.is_done = True

    def step_done(self):
        return self.is_done