import game_world
from game_world.GameWorld import GameWorld
from game_world.LevelScripting import LSE_AddObject, LSE_ChangeTextBoxVisibility, LSE_EndLevel, LSE_PlayerWarpsAway, LSE_SetPlayerMotionScript, LSE_TargetShootPlayer, LSE_UpdateBackground, LSE_Wait, LSE_WaitForNoTargets, LSE_AddTarget, LSE_SetBackground, LSE_RemoveTarget
from sprite.BackgroundParallax import BackgroundParallax, BackgroundParallaxStarField,load_background
from sprite.SpriteMotionScript import SMSE_MoveToPosition, SMSE_SetPosition, SMSE_MoveToPosition_Smooth, SMSE_Wobble
from game_world.Procedure import Procedure, SimultaneousProcedureStep
from sprite.TestCircle import TestCircle
from game_world.Target import ChargingTarget, Target, CutsceneTargetComms
from sprite.Background import BackgroundStarField
from sprite.SpriteFactory import SpriteFactory
from game_state.TextFactory import TextFactory
from sprite.SpriteFactory import get_sprite_factory
from sprite.TextSprite import TextSprite
from game_world.PlayerObject import PlayerObject
from game_world.ObjectScripting import *
from game_world.SceneObjects import SceneObject

import random

#Shared word factory
text_factory=TextFactory()
text_factory.load_text_category("letters","data/words/letters.txt")
text_factory.load_text_category("short", "data/short_words.txt")
text_factory.load_text_category("medium", "data/medium_words.txt")
text_factory.load_text_category("long", "data/long_words.txt")

def add_n_targets(n_targets,textname,spritenames,target_type=ChargingTarget,time_limit=-1,entry_points=[],hold_points=[]):                            
    steps=[]
    entry_motions=get_n_entry_motion_procedures(n_targets,entry_points=entry_points, hold_points=hold_points,time_limit=time_limit)        
    for i in range(n_targets):
        if isinstance(spritenames,str):
            spritename=spritenames[0]
        else:
            spritename=random.choice(spritenames)
        text=text_factory.generate_random_text(textname)            
        steps.append( LSE_AddTarget(game_world, object=target_type(text=text, game_world=game_world,object_sprite=sprite_factory.create_image_sprite(spritename)), motion_script=entry_motions[i]) )
    return steps

def get_levelzero_script(game_world: GameWorld):
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
    def generate_path_positions(banned_positions=[]):
        # Generate start, hover, and leave positions avoiding banned positions
        start_choices=[left_low,left_high,right_low,right_high,top_left,top_mid,top_right,bottom_left,bottom_mid,bottom_right]
        hover_choices=[hover_left_mid,hover_mid_mid,hover_right_mid,hover_left_high,hover_mid_high,hover_right_high]
        leave_choices=[left_low,left_high,right_low,right_high,top_left,top_mid,top_right,bottom_left,bottom_mid,bottom_right]
        start_pos=random.choice([pos for pos in start_choices if pos not in banned_positions])
        hover_pos=random.choice([pos for pos in hover_choices if pos not in banned_positions])
        leave_pos=random.choice([pos for pos in leave_choices if pos not in banned_positions])
        return [start_pos, hover_pos, leave_pos]

    def generate_multiple_path_positions(n_paths=1):
        all_positions=[]
        for _ in range(n_paths):
            path_positions=generate_path_positions(banned_positions=[pos for sublist in all_positions for pos in sublist])
            all_positions.append(path_positions)
        return all_positions

    def generate_motion_path(position=None,banned_positions=[]):
        if position is None:
            start_pos,hover_pos,leave_pos=generate_path_positions(banned_positions)        
        else:
            start_pos,hover_pos,leave_pos=position
         #Now, create the motion script
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
    for i in range(4):
        script.add_step(add_target("medium","ship2",generate_motion_path()))
        script.add_step(LSE_WaitForNoTargets(game_world))
    paths=generate_multiple_path_positions(n_paths=2)
    for path in paths:
        script.add_step(add_target("medium","ship2",generate_motion_path(position=path)))
    script.add_step(LSE_WaitForNoTargets(game_world))
        
    script.add_step(LSE_UpdateBackground(game_world, property_name="velocity", property_value=500))
    script.add_step(LSE_Wait(game_world, duration=0.25))
    script.add_step(LSE_UpdateBackground(game_world, property_name="velocity", property_value=1000))
    script.add_step(LSE_Wait(game_world, duration=0.25))
    script.add_step(LSE_PlayerWarpsAway(game_world, warp_position=(screen_size[0]//2, -200)))
    #script.add_step(LSE_EndLevel(game_world))
    return script

#Entry motions for enemies
def get_n_entry_motion_procedures(n_procs,entry_points=None, hold_points=None,time_limit=-1):
    procs=[]
    used_entry_points=[]
    used_hold_points=[]
    for _ in range(n_procs):
        #select entry point
        entry_point=random.choice([pt for pt in entry_points if pt not in used_entry_points])
        used_entry_points.append(entry_point)
        #select hold point
        hold_point=random.choice([pt for pt in hold_points if pt not in used_hold_points])
        used_hold_points.append(hold_point)
        #create motion procedure
        proc=Procedure([
            SetObjectPosition(object=None, position=entry_point),
            MoveObjectToPosition_Smooth(object=None, end_position=hold_point, duration=2.0),
            StartTimer(time_amount=time_limit, object=None),
            WobbleObject(object=None, amplitude_x=10, amplitude_y=10, frequency_x=1.0, frequency_y=0.2, duration=-1.0)
        ])
        procs.append(proc)
    return procs    

def get_space_entry_points(graphics):
    return get_entry_points(graphics,angle_max=math.pi*0.5, angle_min=-math.pi*0.5)

def get_atmosphere_entry_points(graphics):
    return get_entry_points(graphics,angle_max=math.pi*0.5, angle_min=-math.pi*0.25)

def get_entry_points(graphics,angle_max,angle_min)
    #Space entry points are anywhere from a 180 degree arc from the right of the screen
    n_points=10
    space_entry_points=[]
    for i in range(n_points):
        theta=angle_min[i] + (angle_max-angle_min)*(i/(n_points-1))
        #theta=math.pi*(i/(n_points-1)) - math.pi*0.5
        x=0.5+0.6*math.cos(theta)
        y=0.5+0.6*math.sin(theta)
        space_entry_points.append( graphics.frac_to_screen((x,y)) )
    #Space hold points are m rows and n columns in the center right of the screen
    space_hold_points=[]
    n_rows=3
    n_columns=4
    y_spacing=1.0/(n_rows+1)
    for i in range(n_rows):
        for j in range(n_columns):
            x=0.5 + j*(0.9-0.5)/(n_columns-1)
            y=y_spacing*(i+1)
            space_hold_points.append( graphics.frac_to_screen((x,y)) )
    return space_entry_points, space_hold_points

#Level zero: Cutscene.  Your ship is destroyed by the alphabeticons
def get_levelzero_script(game_world: GameWorld):
    screen_size=game_world.graphics.screen_size
    helm_text_position=(screen_size[0]//4, screen_size[1]//4)
    alien_text_position=(2*screen_size[0]//3, screen_size[1]//4)
    captain_text_position=(screen_size[0]//4, 3*screen_size[1]//4)
    script=Procedure()
    script.add_step(LSE_SetBackground(game_world,load_background("space",velocity=200)))
    # Narrator: Somewhere in deep space
    script.add_step(LSE_AddTarget(game_world,object=CutsceneTargetComms(game_world=game_world,text="Somewhere in deep space...",character_image="hdf1",typing_speed=10),motion_script=Procedure()))
    # Enter: a big ship
    ship=SceneObject(sprite=get_sprite_factory().create_image_sprite("ship_carrier"), position=(game_world.graphics.screen_size[0]//2, -200))

    ship_script=Procedure([
        SetObjectPosition(object=None, position=(-100, screen_size[1]//2)),
        MoveObjectToPosition_Smooth(object=None, end_position=(screen_size[0]//3, screen_size[1]//2), duration=2.0),
        WobbleObject(object=None, amplitude_x=5, amplitude_y=5, frequency_x=1.0, frequency_y=0.5, duration=-1.0)
    ])
    script.add_step(LSE_AddObject(game_world, object=ship, motion_script=ship_script))
    script.add_step(LSE_WaitForNoTargets(game_world))
    # Enter: alphabeticons
    ship2=SceneObject(sprite=get_sprite_factory().create_image_sprite("ship_a1"))
    script.add_step(LSE_AddTarget(game_world,object=CutsceneTargetComms(position=helm_text_position,game_world=game_world,text="There is something on our scanners...",character_image="portrait2",typing_speed=10,speaker_name="Helm Officer"),motion_script=Procedure()))
    ship2_script=Procedure([
        SetObjectPosition(object=None, position=(screen_size[0]+100, screen_size[1]//2)),
        MoveObjectToPosition_Smooth(object=None, end_position=(screen_size[0]*2//3, screen_size[1]//2), duration=2.0),
        WobbleObject(object=None, amplitude_x=5, amplitude_y=5, frequency_x=1.0, frequency_y=0.5, duration=-1.0)
    ])
    script.add_step(LSE_AddObject(game_world, object=ship2, motion_script=ship2_script))
    script.add_step(LSE_WaitForNoTargets(game_world))
    # Alphabeticons:  We are the alphabeticons.  You have no chance to survive.
    script.add_step(LSE_AddTarget(game_world,object=CutsceneTargetComms(position=alien_text_position, game_world=game_world,text="We are the alphabeticons.  Earth is doomed.  We will hack autocorrect to make your text messages unreadable.",character_image="alphabet",typing_speed=10),motion_script=Procedure()))    
    script.add_step(LSE_WaitForNoTargets(game_world))
    # alphabeticons start shooting
    for i in range(4):
        shot=SceneObject(sprite=get_sprite_factory().create_composite_sprite("shot1"))    
        shot_script=Procedure([
            SetObjectPositionToOtherObject(object=None, target=ship2),
            MoveObjectToObject(target_object=ship, duration=2.0),
            SpawnSpriteAtObject(sprite=get_sprite_factory().create_animated_sprite("explosion1"), graphics=game_world.graphics),
            DespawnSelfObject()
        ])
        script.add_step(LSE_AddObject(game_world, object=shot, motion_script=shot_script))
        script.add_step(LSE_Wait(game_world, duration=0.5))
    # Captain: Alphabeticons?? What you say?
    script.add_step(LSE_AddTarget(game_world,object=CutsceneTargetComms(position=captain_text_position,game_world=game_world,text="Never!  Fire back!",character_image="portrait1",typing_speed=10),motion_script=Procedure()))
    script.add_step(LSE_WaitForNoTargets(game_world))
    script.add_step(LSE_AddTarget(game_world,object=CutsceneTargetComms(position=helm_text_position,game_world=game_world,text="Oh No!  I spilled soda on the keyboard.  We're helpless!",character_image="portrait2",typing_speed=7,typing_error_rate=0.15),motion_script=Procedure()))
    script.add_step(LSE_WaitForNoTargets(game_world))
    script.add_step(LSE_AddTarget(game_world,object=CutsceneTargetComms(position=captain_text_position,game_world=game_world,text="Abandon ship!  Captain Theo, you must escape and save Earth!",character_image="portrait1",typing_speed=10),motion_script=Procedure()))
    script.add_step(LSE_WaitForNoTargets(game_world))
    # Captain: To the escape pods!
    pod=SceneObject(sprite=get_sprite_factory().create_composite_sprite("ship1"), position=(game_world.graphics.screen_size[0]//2, screen_size[1]+200))
    pod_script=Procedure([
        SetObjectPositionToOtherObject(target=ship),
        MoveObjectToPosition_Smooth(object=None, end_position=(screen_size[0]*2//3, int(screen_size[1]*1.05)), duration=2.0),
        ])
    script.add_step(LSE_AddObject(game_world, object=pod, motion_script=pod_script))
    script.add_step(SpawnSpriteAtObject(object=ship,sprite=get_sprite_factory().create_animated_sprite("explosion1"), graphics=game_world.graphics))    
    script.add_step(LSE_Wait(game_world, duration=2.0))
    script.add_step(LSE_EndLevel(game_world))
    return script

#Level one: dodge debris
def get_levelone_script(game_world: GameWorld):
    screen_size=game_world.graphics.screen_size
    space_entry_points, space_hold_points = get_space_entry_points(game_world.graphics)

    sprite_factory=get_sprite_factory()


    #TODO make default ship movement script
    #game_world.set_player_sprite(sprite_factory.create_composite_sprite("ship6"))
    playerobject=PlayerObject(sprite_factory.create_composite_sprite("ship1"), position=(100, 100))
    playerscript=Procedure([
        MoveObjectToPosition_Smooth(end_position=(200,200),duration=2.0),
        MoveObjectToPosition_Smooth(end_position=(300,300),duration=2.0)
    ],is_loop=True)
    game_world.add_player(playerobject)
    game_world.set_default_player_script(playerscript)
    

    #Then, the word factory
    text_factory=TextFactory()
    text_factory.load_text_category("letters","data/words/letters.txt")
    text_factory.load_text_category("short", "data/short_words.txt")
    text_factory.load_text_category("medium", "data/medium_words.txt")
    text_factory.load_text_category("long", "data/long_words.txt")

    def add_n_targets(n_targets,textname,spritenames,time_limit=-1):                            
        steps=[]
        entry_motions=get_n_entry_motion_procedures(n_targets,entry_points=space_entry_points, hold_points=space_hold_points,time_limit=time_limit)        
        for i in range(n_targets):
            if isinstance(spritenames,str):
                spritename=spritenames[0]
            else:
                spritename=random.choice(spritenames)
            text=text_factory.generate_random_text(textname)            
            steps.append( LSE_AddTarget(game_world, object=ChargingTarget(text=text, game_world=game_world,object_sprite=sprite_factory.create_image_sprite(spritename)), motion_script=entry_motions[i]) )
        return steps

    debris_sprites=["debris1","debris2","debris3","debris4","debris5","debris6","debris7","debris8","debris9"]
    script=Procedure()
    #script.add_step(LSE_SetBackground(game_world,load_background("forest",velocity=500)))
    script.add_step(LSE_SetBackground(game_world,load_background("space",velocity=250)))
    #script.add_step(LSE_SetBackground(game_world,load_background("skies",velocity=500)))
    script.add_step(LSE_AddTarget(game_world,object=CutsceneTargetComms(game_world=game_world,text="Theo, you need to avoid the space debris!  If they knock out your shields, you're doomed",character_image="portrait1"),motion_script=Procedure()))
    script.add_step(LSE_WaitForNoTargets(game_world))
    script.add_step(LSE_Wait(game_world, duration=1.0))
    for i in range(4):
        script.add_step(add_n_targets(1,"letters",debris_sprites)[0])
        script.add_step(LSE_WaitForNoTargets(game_world))
    for i in range(2):
        steps=add_n_targets(2,"letters",debris_sprites)
        for step in steps:
            script.add_step(step)
        script.add_step(LSE_WaitForNoTargets(game_world))
    script.add_step(LSE_AddTarget(game_world,object=CutsceneTargetComms(game_world=game_world,text="They're coming faster!  You'll have to type quickly!",character_image="portrait1"),motion_script=Procedure()))
    script.add_step(LSE_UpdateBackground(game_world, property_name="velocity", property_value=500))

    script.add_step(LSE_WaitForNoTargets(game_world))    
    steps=add_n_targets(2,"letters",debris_sprites,time_limit=5.0)
    for step in steps:
        script.add_step(step)
    script.add_step(LSE_WaitForNoTargets(game_world))
    steps=add_n_targets(2,"letters",debris_sprites,time_limit=4.0)
    for step in steps:
        script.add_step(step)
    script.add_step(LSE_WaitForNoTargets(game_world))
    steps=add_n_targets(3,"letters",debris_sprites,time_limit=4.0)
    for step in steps:
        script.add_step(step)
    script.add_step(LSE_WaitForNoTargets(game_world))
    script.add_step(LSE_UpdateBackground(game_world, property_name="velocity", property_value=800))
    script.add_step(LSE_Wait(game_world, duration=1.0))
    steps=add_n_targets(3,"letters",debris_sprites,time_limit=2.0)
    for step in steps:
        script.add_step(step)
    script.add_step(LSE_WaitForNoTargets(game_world))    
    steps=add_n_targets(3,"letters",debris_sprites,time_limit=2.0)
    for step in steps:
        script.add_step(step)
    script.add_step(LSE_WaitForNoTargets(game_world))    
    steps=add_n_targets(3,"letters",debris_sprites,time_limit=1.0)
    for step in steps:
        script.add_step(step)
    script.add_step(LSE_WaitForNoTargets(game_world))
    #Players ship crashes on moon
    moon_sprite=sprite_factory.create_image_sprite("planet_moon")
    moon_object=SceneObject(sprite=moon_sprite)
    moon_script=Procedure([
        SetObjectPosition(object=None, position=(screen_size[0]//2, screen_size[1]//2 + 200)),
        MoveObjectToPosition(object=None, end_position=(screen_size[0]//2, screen_size[1]//2), duration=2.0),
    ])
    script.add_step(LSE_AddObject(game_world, object=moon_object, motion_script=moon_script))
    script.add_step(LSE_Wait(game_world, duration=2.0))
    #player crashes
    playerscript2=Procedure([
        MoveObjectToObject(target_object=moon_object, duration=2.0),
        SpawnSpriteAtObject(sprite=sprite_factory.create_animated_sprite("explosion1"), graphics=game_world.graphics)    
    ],is_loop=True)    
    script.add_step(LSE_SetPlayerMotionScript(game_world, motion_script=playerscript2))
    #Need a script that sets another player motion script
    #game_world.player_object.set_motion_script(playerscript2)


#    script.add_step(LSE_PlayerWarpsAway(game_world))
    script.add_step(LSE_Wait(game_world, duration=2.0))
    script.add_step(LSE_EndLevel(game_world))
    
    
    return script

#Level two: shoot down asteroids
def get_leveltwo_script(game_world: GameWorld):
    screen_size=game_world.graphics.screen_size
    entry_points, hold_points = get_atmosphere_entry_points(game_world.graphics)
    asteroid_sprites=["asteroid1"]
    
    sprite_factory=get_sprite_factory()

    #TODO make default ship movement script
    playerobject=PlayerObject(sprite_factory.create_composite_sprite("ship2"), position=(100, 100))
    playerscript=Procedure([
        MoveObjectToPosition_Smooth(end_position=(300,300),duration=2.0),
        WobbleObject(amplitude_x=10, amplitude_y=10, frequency_x=1.0, frequency_y=0.2, duration=-1.0)
    ],is_loop=True)
    game_world.add_player(playerobject)
    game_world.set_default_player_script(playerscript)
    script=Procedure()
    script.add_step(LSE_SetBackground(game_world,load_background("moon",velocity=500)))
    script.add_step(LSE_Wait(game_world, duration=1.0))
    steps=add_n_targets(3,"short",asteroid_sprites,time_limit=2.0)
    for step in steps:
        script.add_step(step)
    script.add_step(LSE_WaitForNoTargets(game_world))
    script.add_step(LSE_PlayerWarpsAway(game_world))
    script.add_step(LSE_Wait(game_world, duration=2.0))
    script.add_step(LSE_EndLevel(game_world))
    return script


