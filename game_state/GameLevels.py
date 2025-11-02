from game_world.GameWorld import GameWorld
from game_world.LevelScripting import LSE_ChangeTextBoxVisibility, LSE_EndLevel, LSE_PlayerWarpsAway, LSE_TargetShootPlayer, LSE_UpdateBackground, LSE_Wait, LSE_WaitForNoTargets, LSE_AddTarget, LSE_SetBackground, LSE_RemoveTarget
from sprite.SpriteMotionScript import SMSE_MoveToPosition, SMSE_SetPosition, SMSE_MoveToPosition_Smooth, SMSE_Wobble
from game_world.Procedure import Procedure, SimultaneousProcedureStep
from sprite.TestCircle import TestCircle
from game_world.Target import Target
from sprite.Background import BackgroundStarField
from sprite.SpriteFactory import SpriteFactory
from game_state.TextFactory import TextFactory
from sprite.SpriteFactory import get_sprite_factory
from sprite.TextSprite import TextSprite
import random

def get_levelone_script(game_world: GameWorld):
    screen_size=game_world.graphics.screen_size
    offscreen=100
    #First, motion paths
    # Entry and exit positions
    left_low=(-offscreen,screen_size[1]//3)
    left_high=(-2*offscreen,screen_size[1]//2)
    right_low=(screen_size[0]+offscreen,screen_size[1]//3)
    right_high=(screen_size[0]+2*offscreen,screen_size[1]//2)
    top_left=(screen_size[0]//3, -offscreen)
    top_mid=(screen_size[0]//2, -offscreen)
    top_right=(2*screen_size[0]//3, -offscreen)
    bottom_left=(screen_size[0]//3, screen_size[1]+offscreen)
    bottom_mid=(screen_size[0]//2, screen_size[1]+offscreen)
    bottom_right=(2*screen_size[0]//3, screen_size[1]+offscreen)    
    #hover positions
    hover_left_mid=(screen_size[0]//4, screen_size[1]//2)
    hover_mid_mid=(screen_size[0]//2, screen_size[1]//2)
    hover_right_mid=(3*screen_size[0]//4, screen_size[1]//2)
    hover_left_high=(screen_size[0]//4, screen_size[1]//3)
    hover_mid_high=(screen_size[0]//2, screen_size[1]//3)
    hover_right_high=(3*screen_size[0]//4, screen_size[1]//3)
    def generate_motion_path(start_pos=None,hover_pos=None,leave_pos=None):
        start_pos=start_pos or random.choice([left_low,left_high,right_low,right_high,top_left,top_mid,top_right,bottom_left,bottom_mid,bottom_right])
        hover_pos=hover_pos or random.choice([hover_left_mid,hover_mid_mid,hover_right_mid,hover_left_high,hover_mid_high,hover_right_high])
        leave_pos=leave_pos or random.choice([left_low,left_high,right_low,right_high,top_left,top_mid,top_right,bottom_left,bottom_mid,bottom_right])
        entry_duration=2.0
        exit_duration=2.0
        hover_duration=2.0        
        n_shots=4
        return Procedure([
            SMSE_SetPosition(None, position=start_pos),
            LSE_ChangeTextBoxVisibility(None, None,visible=False),
            SMSE_MoveToPosition_Smooth(None,initial_position=start_pos,initial_velocity=(0,0),final_velocity=(0,0), final_position=hover_pos, duration=entry_duration),
            LSE_ChangeTextBoxVisibility(None, None, visible=True),            
            SMSE_Wobble(None, amplitude_x=10, amplitude_y=10, frequency_x=1.0, frequency_y=0.2, duration=hover_duration),
            SimultaneousProcedureStep([LSE_TargetShootPlayer(None, source_target=None, damage_amount=10,n_shots=n_shots),
                                       SMSE_Wobble(None, amplitude_x=10, amplitude_y=10, frequency_x=1.0, frequency_y=0.2, duration=hover_duration)]),
            SMSE_MoveToPosition_Smooth(None,initial_position=hover_pos,initial_velocity=(0,0),final_velocity=(0,0), final_position=leave_pos, duration=exit_duration),
            LSE_RemoveTarget(None,None)
        ])
    
    down_and_hold_left=Procedure([
        SMSE_SetPosition(None, position=(-offscreen,300)),
        LSE_ChangeTextBoxVisibility(None, None,visible=False),
        #SMSE_MoveToPosition(None, end_position=(300,300), duration=2.0),
        SMSE_MoveToPosition_Smooth(None,initial_position=None,initial_velocity=(0,0),final_velocity=(0,0), final_position=(300,300), duration=2.0),
        LSE_ChangeTextBoxVisibility(None, None, visible=True),
        LSE_Wait(None, duration=1.0),
        LSE_TargetShootPlayer(None, source_target=None, damage_amount=40),
        LSE_Wait(None, duration=1.0),
        SMSE_MoveToPosition_Smooth(None,initial_position=None,initial_velocity=(0,0),final_velocity=(0,0), final_position=(0,-offscreen), duration=2.0),
        LSE_RemoveTarget(None,None)
        ])

    #Next, some sprites
    sprite_factory=get_sprite_factory()
    game_world.set_player_sprite(sprite_factory.create_image_sprite("ship3"))

    #Then, the word factory
    text_factory=TextFactory()
    text_factory.load_text_category("short", "data/short_words.txt")
    text_factory.load_text_category("medium", "data/medium_words.txt")
    text_factory.load_text_category("long", "data/long_words.txt")

    def add_target(textname,spritename,motionscript):
        return LSE_AddTarget(game_world, target=Target(text_factory.generate_random_text(textname), game_world=game_world,object_sprite=sprite_factory.create_image_sprite(spritename)), motion_script=motionscript)

    script=Procedure()
    script.add_step(LSE_SetBackground(game_world,BackgroundStarField(100,100)))
    script.add_step(LSE_AddTarget(game_world,target=Target("start",game_world=game_world,object_sprite=TextSprite("Type start to begin",)), motion_script=Procedure([SMSE_SetPosition(None, position=(screen_size[0]//2,screen_size[1]//2))])))
    script.add_step(LSE_WaitForNoTargets(game_world))
    script.add_step(LSE_Wait(game_world, duration=0.5))    
    
    for i in range(5):
        script.add_step(add_target("short","ship2",generate_motion_path()))
        script.add_step(LSE_WaitForNoTargets(game_world))
    for i in range(5):
        script.add_step(add_target("medium","ship2",generate_motion_path()))
        script.add_step(LSE_WaitForNoTargets(game_world))
    for i in range(2):
        script.add_step(add_target("medium","ship2",generate_motion_path()))
    script.add_step(LSE_WaitForNoTargets(game_world))
        
    script.add_step(LSE_UpdateBackground(game_world, property_name="velocity", property_value=500))
    script.add_step(LSE_Wait(game_world, duration=0.25))
    script.add_step(LSE_UpdateBackground(game_world, property_name="velocity", property_value=1000))
    script.add_step(LSE_Wait(game_world, duration=0.25))
    script.add_step(LSE_PlayerWarpsAway(game_world, warp_position=(screen_size[0]//2, -200)))
    #script.add_step(LSE_EndLevel(game_world))
    return script