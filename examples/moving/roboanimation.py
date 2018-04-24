import logging
import sys

from gamegridp import actor
from gamegridp import gamegrid


class MyGrid(gamegrid.GameGrid):
    """My Grid with custom setup method."""
    def setup(self):
        self.player1 = Robot("Player", grid=self, location=(50, 70))


class Robot(actor.Actor):

    def setup(self):
        self.image_add("images/robot_blue1.png", "do_nothing")
        self.image_add("images/robot_blue2.png", "do_nothing")
        self.animation_speed = 20
        self.animate()

    def act(self):
        if self.is_valid_move():
            self.move()
        else:
            self.flip_x()

logging.basicConfig(stream=sys.stdout, level=logging.INFO)
module_logger = logging.getLogger('gglogger')
mygrid = MyGrid("My Grid", log=True, cell_size=1, columns=200, rows=150,
                margin=0, speed=40,
                background_color=(200, 0, 0), cell_color=(0, 0, 255), img_path="images/water.png")
mygrid.show()
