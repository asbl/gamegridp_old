from gamegridp import actor
from gamegridp import gamegrid


class MyGrid(gamegrid.GameGrid):
    """My Grid with custom setup method."""

    def setup(self):
        player1 = Player("Player", grid=self, location=(3, 3), img_path="images/char_blue.png",
                         img_action="do_nothing")
        player2 = Player("Player", grid=self, location=(8, 2), img_path="images/char_blue.png",
                         img_action="do_nothing")


class Player(actor.Actor):
    def act(self):
        self.move()
        if not self.is_valid_move():
            self.turn_left()


mygrid = MyGrid("My Grid", log=True, cell_size=12, columns=16, rows=16,
                margin=5, img_path="images/soccer_green.jpg", speed=60)
mygrid.show()
