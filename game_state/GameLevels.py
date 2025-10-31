from game_world.GameWorld import GameWorld
from game_world.LevelScripting import LSE_EndLevel, LSE_TargetShootPlayer, LSE_Wait, LSE_WaitForNoTargets, LSE_AddTarget, LSE_SetBackground, LSE_RemoveTarget
from sprite.SpriteMotionScript import SMSE_MoveToPosition, SMSE_SetPosition, SMSE_MoveToPosition_Smooth
from game_world.Procedure import Procedure
from sprite.TestCircle import TestCircle
from game_world.Target import Target
from sprite.Background import BackgroundStarField
from sprite.SpriteFactory import SpriteFactory
from game_state.TextFactory import TextFactory
from sprite.SpriteFactory import get_sprite_factory

def get_levelone_script(game_world: GameWorld):
    screen_size=game_world.graphics.screen_size
    offscreen=100
    #First, motion paths
    down_and_hold_left=Procedure([
        SMSE_SetPosition(None, position=(-offscreen,300)),
        #SMSE_MoveToPosition(None, end_position=(300,300), duration=2.0),
        SMSE_MoveToPosition_Smooth(None,initial_position=None,initial_velocity=(0,0),final_velocity=(0,0), final_position=(300,300), duration=2.0),

        LSE_Wait(None, duration=1.0),
        LSE_TargetShootPlayer(None, source_target=None, damage_amount=10),
        LSE_Wait(None, duration=1.0),
        SMSE_MoveToPosition_Smooth(None,initial_position=None,initial_velocity=(0,0),final_velocity=(0,0), final_position=(0,-offscreen), duration=2.0),
        LSE_RemoveTarget(None,None)
        ])
    down_and_hold_right=Procedure([
        SMSE_SetPosition(None, position=(screen_size[0]+offscreen,300)),
        SMSE_MoveToPosition_Smooth(None,initial_position=None,initial_velocity=(0,0),final_velocity=(0,0), final_position=(600,300), duration=2.0),

        LSE_Wait(None, duration=1.0),
        LSE_TargetShootPlayer(None, source_target=None, damage_amount=10,n_shots=5)
        ])
    #Next, some sprites
    sprite_factory=get_sprite_factory()
    game_world.set_player_sprite(sprite_factory.create_image_sprite("ship3"))

    #Then, the word factory
    text_factory=TextFactory()
    text_factory.load_text_category("simple", "data/1000words.txt")

    def add_target(textname,spritename,motionscript):
        return LSE_AddTarget(game_world, target=Target(text_factory.generate_random_text(textname), game_world=game_world,object_sprite=sprite_factory.create_image_sprite(spritename)), motion_script=motionscript)

    script=Procedure()
    script.add_step(LSE_SetBackground(game_world,BackgroundStarField(100,100)))
    script.add_step(LSE_Wait(game_world, duration=0.5))
    script.add_step(add_target("simple","ship2",down_and_hold_left))
    script.add_step(LSE_WaitForNoTargets(game_world))
    script.add_step(add_target("simple","ship2",down_and_hold_right))
    script.add_step(LSE_WaitForNoTargets(game_world))
    script.add_step(add_target("simple","ship2",down_and_hold_left))
    script.add_step(add_target("simple","ship2",down_and_hold_right))
    script.add_step(LSE_WaitForNoTargets(game_world))
    script.add_step(LSE_EndLevel(game_world))
    return script