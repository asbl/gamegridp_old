import logging
import sys

from gamegridp import actor
from gamegridp import gamegrid


class MyGrid(gamegrid.GameGrid):
    """My Grid with custom setup method."""
    def setup(self):
        self.robot1 = Robot("Player", grid=self, location=(50, 70),img_path="images/robo_green.png")
        self.robot2 = Robot("Player", grid=self, location=(50, 70), img_path="images/robo_yellow_png")

class Robot(actor.Actor):
    direction="right"

    def setup(self):
        if self.direction=="left":
            self.turn_left(180)


    def act(self):
        self.move()


logging.basicConfig(stream=sys.stdout, level=logging.INFO)
module_logger = logging.getLogger('gglogger')
mygrid = MyGrid("My Grid", log=True, cell_size=1, columns=200, rows=150,
                margin=0, speed=40,
                background_color=(200, 0, 0), cell_color=(0, 0, 255), img_path="images/water.png")
mygrid.show()
