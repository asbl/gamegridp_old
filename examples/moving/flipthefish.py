from gamegridp import actor
from gamegridp import gamegrid


class MyGrid(gamegrid.GameGrid):
    """My Grid with custom setup method."""

    def setup(self):
        self.player1 = Player("Player", grid=self, location=(3, 3), img_path="images/fish.png",
                         img_action="do_nothing")


class Player(actor.Actor):

    def act(self):
        if self.is_valid_move():
            self.move()
        else:
            self.flip_x()



mygrid = MyGrid("My Grid", log=True, cell_size=20, columns=20, rows=20,
                margin=0, speed=120,
                background_color=(200, 0, 0),cell_color=(0, 0, 255),img_path="images/water.png")
mygrid.show()
