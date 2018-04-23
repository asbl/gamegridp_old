from gamegridp import actor
from gamegridp import keys
from gamegridp import gamegrid
import logging
import sys

class MyGrid(gamegrid.GameGrid):
    """My Grid with custom setup method."""
    def setup(self):
        self.player1 = Robot("Player", grid=self, location=(1, 0))


class Robot(actor.Actor):

    def setup(self):
        self.image_add("images/robot_blue1.png", "do_nothing")
        self.image_add("images/robot_blue2.png", "do_nothing")
        self.animation_speed = 10

    def act(self):
        self.animated = True
        self.move()

logging.basicConfig(stream=sys.stdout, level=logging.INFO)
module_logger = logging.getLogger('gglogger')
mygrid = MyGrid("My Grid", log=True, cell_size=150, columns=6, rows=1,
                margin=0, speed=20,
                background_color=(200, 0, 0),cell_color=(0, 0, 255),img_path="images/water.png")
mygrid.show()
