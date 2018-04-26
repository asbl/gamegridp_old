import logging
import sys

from gamegridp import actor
from gamegridp import gamegrid
from gamegridp import keys


class MyGrid(gamegrid.GameGrid):
    """My Grid with custom setup method."""

    def setup(self):
        robo1 = Robot(grid=self, location=(20, 20), img_action="do_nothing", log=True)
        robo1.add_image("images/robo_green.png", "scale", (40, 40))


class Robot(actor.Actor):
    def setup(self):
        self.set_rotatable()
        self._logging.info("Actor: "+ self.title + "'s setup wird ausgeführt, rotatable:"+str(self.is_rotatable))

    def act(self):
        self.move(3)

    def listen(self, event, data):
        if event == "key":
            if data == keys.W:
                self.turn_left(10)
            elif data == keys.S:
                self.turn_right(10)

logging.basicConfig(stream=sys.stdout, level=logging.INFO)
module_logger = logging.getLogger('gglogger')
mygrid = MyGrid("My Grid", log=True, cell_size=1, columns=400, rows=400,
                margin=0, speed=60,
                background_color=(200, 0, 0),cell_color=(0, 0, 255), img_path="images/stone.jpg")
mygrid.show()
