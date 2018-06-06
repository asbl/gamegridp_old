import sys
sys.path.insert(0, "D:\\Code\\gamegridp\\gamegridp")
sys.path.insert(0, "D:\\Code\\gamegridp\\actor")
from gamegridp import actor
from gamegridp import gamegrid
from gamegridp import keys
import logging
import sys

class MyGrid(gamegrid.GameGrid):
    """My Grid with custom setup method."""

    def setup(self):
        self.player1 = Player(grid=self, location=(3, 3), img_path="images/char_blue.png",
                              img_action="do_nothing")



class Player(actor.Actor):
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
module_logger = logging.getLogger('gglogger')
mygrid = MyGrid("My Grid", log=True, cell_size=1, columns=200, rows=200,
                margin=0, speed=120,
                background_color=(200, 0, 0),cell_color=(0, 0, 255), img_path="images/soccer_green.jpg")
mygrid.show()
