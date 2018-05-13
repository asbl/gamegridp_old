import logging
import sys

import gamegridp
from gamegridp import keys


class MyGrid(gamegridp.GameGrid):
    """My Grid with custom setup method."""

    def setup(self):
        robo1 = Robot(grid=self, location=(20, 20), img_action="do_nothing")
        robo1.add_image("images/robo_green.png", "scale", (40, 40))


class Robot(gamegridp.Actor):
    def setup(self):
        self.set_rotatable()
        self._logging.info("Actor: "+ self.title + "'s setup wird ausgeführt, rotatable:"+str(self.is_rotatable))

    def act(self):
        self.move(3)

    def listen(self, event, data):
        if event == "key":
            if "W" in data :
                self.turn_left(10)
            if "S" in data:
                self.turn_right(10)

logging.basicConfig(stream=sys.stdout, level=logging.INFO)
mygrid = MyGrid("My Grid", cell_size=1, columns=400, rows=400,
                margin=0, speed=60,
                background_color=(200, 0, 0),cell_color=(0, 0, 255), img_path="images/stone.jpg")
mygrid.show()
