
class Scene():
    def __init__(self,game):
        self.game = game
        self.screen = self.game.temp_screen
    def update(self):
        pass
    def render(self):
        pass
    def onenter(self):
        pass
    def onexit(self):
        pass
    def enter(self):
        self.game.curr_scene = self
        self.onenter()
    def exit(self):
        self.game.prev_scene = self
        self.onexit()
