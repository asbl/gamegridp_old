import gamegridp
import logging
import sys

class MyGrid(gamegridp.GameGrid):
    """My Grid with custom setup method."""

    def setup(self):
        self.set_image(img_path="images/soccer_green.jpg")
        player1 = Player(grid=self, location=(3, 3), img_path="images/char_blue.png",
                         img_action="do_nothing")
        player2 = Player(grid=self, location=(8, 2), img_path="images/char_blue.png",
                         img_action="do_nothing")


class Player(gamegridp.Actor):
    def setup(self):
        pass

    def act(self):
        self.move()
        if not self.is_valid_move():
            self.turn_left()

logging.basicConfig(stream=sys.stdout, level=logging.INFO)
my_grid = MyGrid("My Grid", log=True, cell_size=12, columns=16, rows=16, margin=5, speed=60)
my_grid.show()
