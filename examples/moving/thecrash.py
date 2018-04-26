import logging
import sys

from gamegridp import actor
from gamegridp import gamegrid


class MyGrid(gamegrid.GameGrid):
    """My Grid with custom setup method."""
    def setup(self):
        self.robot1 = Robot(grid=self, location=(0, 0), img_path="images/robo_green.png", img_action="scale")
        self.robot2 = Robot(grid=self, location=(28, 0), img_path="images/robo_yellow.png", img_action="scale",
                            img_heading="W")

    def act(self):
        module_logger.info("MyGrid - Act")
        if self.colliding(self.robot1, self.robot2):
            module_logger.info("Collision")
            location=self.robot1.get_location()
            explosion = Explosion(title="boom", grid=self, location=self.robot1.location)
            self.remove_actor(self.robot1)
            self.remove_actor(self.robot2)
            self.add_actor(explosion)


class Explosion(actor.Actor):
    def setup(self):
        self.add_image("images/explosion.png", "do_nothing")

class Robot(actor.Actor):

    def act(self):
        self.move()


logging.basicConfig(stream=sys.stdout, level=logging.INFO)
module_logger = logging.getLogger('gglogger')
mygrid = MyGrid("My Grid", log=True, cell_size=40, columns=29, rows=1,
                margin=0, speed=40,
                background_color=(200, 0, 0), cell_color=(0, 0, 255), img_path="images/water.png")
mygrid.show()
