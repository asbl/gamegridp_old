import logging
import sys

from gamegridp import actor
from gamegridp import gamegrid


class MyGrid(gamegrid.GameGrid):
    """My Grid with custom setup method."""
    def setup(self):
        self.robot1 = Robot("Player", grid=self, location=(0, 0),img_path="images/robo_green.png",img_action="scale")
        self.robot2 = Robot("Player", grid=self, location=(29, 0), img_path="images/robo_yellow.png",img_action="scale",img_heading="W")

    def act(self):
        if self.colliding(robot1, robot2):
            location=self.robot1.get_location()
            self.remove(self.robot1)
            self.remove(self.robot2)
            

class Robot(actor.Actor):
    direction="right"

    def setup(self):
        self.move()


    def act(self):
        self.move()


logging.basicConfig(stream=sys.stdout, level=logging.INFO)
module_logger = logging.getLogger('gglogger')
mygrid = MyGrid("My Grid", log=True, cell_size=40, columns=30, rows=1,
                margin=0, speed=40,
                background_color=(200, 0, 0), cell_color=(0, 0, 255), img_path="images/water.png")
mygrid.show()
