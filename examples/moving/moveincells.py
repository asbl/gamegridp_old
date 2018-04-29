import gamegridp
from gamegridp import keys
import logging
import sys

class MyGrid(gamegridp.GameGrid):
    """My Grid with custom setup method."""


    def setup(self):
        self.player1 = Player(grid=self, location=(3, 3), img_path="images/char_blue.png",
                              img_action="do_nothing")



class Player(gamegridp.Actor):

    def setup(self):
        self._is_rotatable = True

    def act(self):
        self.move()

    def listen(self, event, data):
        if event == "key":
            if data == keys.W:
                self.move_up()
            elif data == keys.S:
                self.move_down()
            elif data == keys.A:
                self.move_left()
            elif data == keys.D:
                self.move_right()

logging.basicConfig(stream=sys.stdout, level=logging.INFO)
mygrid = MyGrid("My Grid", cell_size=40, columns=5, rows=5,
                margin=1, speed=60,
                background_color=(200, 0, 0),cell_color=(0, 0, 255), img_path="images/soccer_green.jpg")
mygrid.show()
