import logging
import sys

import gamegridp
from gamegridp import keys


class MyGrid(gamegridp.GameGrid):
    """My Grid with custom setup method."""

    def setup(self):
        self.set_image(img_path = "images/stone.jpg", img_action = "fill", size = (10,10))
        robo1 = Robot(grid=self, location=(20, 20), img_action="do_nothing")
        robo1.add_image("images/robo_green.png", "scale", (40, 40))



class Robot(gamegridp.Actor):
    def setup(self):
        self.set_rotatable()
        self._logging.info("Actor: "+ self.title + "'s setup wird ausgeführt, rotatable:"+str(self.is_rotatable))

    def act(self):
        pass

    def listen(self, event, data):
        self._logging.info("data:"+str(data))
        if event == "key":
            if "A" in data:
                self.turn_left(10)
            if "D" in data:
                self.turn_right(10)
            if "W" in data:
                self.move(3)


logging.basicConfig(stream=sys.stdout, level=logging.INFO)
mygrid = MyGrid("My Grid", cell_size=1, columns=200, rows=400,
                margin=2, speed=40,
                background_color=(200, 0, 0),cell_color=(0, 0, 255))
mygrid.show()
