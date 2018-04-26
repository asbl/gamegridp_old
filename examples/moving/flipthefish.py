import logging
import sys

from gamegridp import actor
from gamegridp import gamegrid


class MyGrid(gamegrid.GameGrid):
    """My Grid with custom setup method."""
    def setup(self):
        self.player1 = Player(grid=self, location=(3, 3))
        self.player1.add_image(img_path="images/fish.png", img_action="scale", data=(80, 80))


class Player(actor.Actor):
    def act(self):
        if self.is_valid_move():
            self.move()
        else:
            self.flip_x()


logging.basicConfig(stream=sys.stdout, level=logging.INFO)
module_logger = logging.getLogger('gglogger')
mygrid = MyGrid("My Grid", log=True, cell_size=25, columns=40, rows=20,
                margin=0, speed=120,
                background_color=(200, 0, 0), cell_color=(0, 0, 255), img_path="images/water.png")
mygrid.show()
