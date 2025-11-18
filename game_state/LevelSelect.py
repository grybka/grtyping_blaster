import pygame
from game_state.GameManagerBase import GameState,GameStatus
from graphics.Graphics import Graphics
from graphics.GraphicsBase import Camera
from sprite.ImageSprite import ImageSprite, ScreenImageSprite
from sprite.SpriteFactory import get_sprite_factory
from sprite.TextBox import TextBox
import yaml


#This shows a map to select levels
#on the left will be a number of planets connected by lines that can be switched between
#on the right will be info about the selected level and a "start level" button


class GameMapEntry:
    def __init__(self):
        self.screen_position = (0, 0)  # position on the level select screen (in screen fraction)        
        self.level_name = ""
        self.level_description = "" 
        self.image_name="planet1"  # name of the sprite image to use for this level
        self.sprite_selected=None
        self.sprite_unselected=None

    def set_selected(self, selected: bool):
        if selected:
            if self.sprite_unselected:
                self.sprite_unselected.set_hidden(True)
            if self.sprite_selected:
                self.sprite_selected.set_hidden(False)
        else:
            if self.sprite_unselected:
                self.sprite_unselected.set_hidden(False)
            if self.sprite_selected:
                self.sprite_selected.set_hidden(True)

    def get_sprites(self):
        if not self.sprite_selected:
            self.sprite_unselected = get_sprite_factory().create_screen_image_sprite(self.image_name,position=self.screen_position)
            self.sprite_selected = ScreenImageSprite(self.sprite_unselected.image.copy(),screen_position=self.screen_position)            
            out_size=self.sprite_selected.image.get_size()
            pygame.draw.rect(self.sprite_selected.image,(255,255,0),(0,0,out_size[0],out_size[1]),5)
            self.sprite_selected.set_hidden(True)
            self.sprite_unselected.set_hidden(False)

        return self.sprite_selected, self.sprite_unselected

#The game map contains information about what levels are available
#each level is represented by a GameMapEntry
class GameMap:
    def __init__(self):
        self.entries = []
        self.connections = []        
        self.descript_box=None

    def update(self, time_delta):
        ...

    def set_selected_level(self, level_index: int):
        for i in range(len(self.entries)):
            if i==level_index:
                self.entries[level_index].set_selected(True)
            else:
                self.entries[i].set_selected(False)
        self.descript_box.set_text(self.entries[level_index].level_description)

        
    def build_graphics(self, graphics: Graphics):
        #this loops through the entries and creates:
        # - sprites for each level entry
        # - lines connecting the entries based on self.connections

        map_to_x=graphics.screen_size[0]*0.75

        #create the surface I want to draw the map on
        map_size_x=int(map_to_x)
        map_size_y=graphics.screen_size[1]
        for entry in self.entries:
            level_sprites=entry.get_sprites()            
            for level_sprite in level_sprites:
                level_sprite.set_screen_position( (int(entry.screen_position[0] * map_size_x), int(entry.screen_position[1] * map_size_y) )                )
                graphics.add_sprite(level_sprite)                  

        #build the description box
        lots_of_text="Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."
        self.descript_box=TextBox(position=(map_to_x,50),size=(graphics.screen_size[0]-map_to_x,graphics.screen_size[1]-100),
                                  font_size=32,text=lots_of_text,text_color=(255,255,255),bg_color=(0,0,0))
        graphics.add_sprite(self.descript_box)

class LevelSelectState(GameState):
    def __init__(self, screen):
        self.graphics = Graphics(screen)        
        sprite_factory=get_sprite_factory()
        self.level_map = GameMap()
        #load level info from yaml here
        with open("data/levels.yaml", 'r') as file:
            self.level_info_data = yaml.safe_load(file)
        for level_key, level_info in self.level_info_data.items():
            entry = GameMapEntry()
            entry.level_name = level_info.get("name", "Unknown")
            entry.level_description = level_info.get("description", "No description available.")
            entry.screen_position = level_info.get("map_position", (0.5, 0.5))
            entry.image_name = level_info.get("sprite_image", "planet1")
            self.level_map.entries.append(entry)
        
        self.graphics_built=False

        self.selected_level_index=0
        self.play_level=False

    def build_graphics(self):
        self.level_map.build_graphics(self.graphics)
        self.graphics_built=True
        self.level_map.entries[self.selected_level_index].set_selected(True)


    def update(self, time_delta):
        if not self.graphics_built:
            self.build_graphics()            
        self.graphics.update(time_delta)

    def draw(self, screen):
        self.graphics.draw(screen)

    def handle_event(self, event):        
        # handle arrows to move between selected planets
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                self.selected_level_index = (self.selected_level_index + 1) % len(self.level_map.entries)
                self.level_map.set_selected_level(self.selected_level_index)
            elif event.key == pygame.K_LEFT:                
                self.selected_level_index = (self.selected_level_index - 1) % len(self.level_map.entries)
                self.level_map.set_selected_level(self.selected_level_index)                
            elif event.key == pygame.K_RETURN:
                # Start the selected level
                selected_level = self.level_map.entries[self.selected_level_index]
                self.play_level=True
                print(f"Starting level: {selected_level.level_name}")
                # Here you would typically notify the GameManager to switch states

    def get_status(self):
        if self.play_level:
            return GameStatus(True, "PlayGameLevel", data=self.level_map.entries[self.selected_level_index])
        return GameStatus(False)