class GlobalPlayerState:
    def __init__(self):
        self.unlocked_levels=set()
        self.unlocked_ships=set()
        self.selected_ship="ship1"
        self.total_letters=0
        self.all_levels_unlocked=False
 
    def unlock_level(self, level_name: str):
        self.unlocked_levels.add(level_name)
 
    def unlock_ship(self, ship_name: str):
        self.unlocked_ships.add(ship_name)
 
    def select_ship(self, ship_name: str):
        if ship_name in self.unlocked_ships:
            self.selected_ship=ship_name
 
    def add_score(self, score: int):
        self.total_score += score