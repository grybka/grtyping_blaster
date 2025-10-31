from game_world.Procedure import ProcedureStep

class WP_DamagePlayer(ProcedureStep):
    def __init__(self, game_world, damage_amount):
        super().__init__()
        self.game_world = game_world
        self.damage_amount = damage_amount
        self.done = False

    def update(self, time_delta):
        print("WPDAMAGEPLACE: Damaging player by", self.damage_amount)
        self.game_world.player_health -= self.damage_amount
        self.done = True

    def step_done(self):
        return self.done