from gamegridp import actor
from gamegridp import gamegrid
from gamegridp import keys
#import logging
#import sys

class MyGrid(gamegrid.GameGrid):
    """My Grid with custom setup method."""


    def setup(self):
        self.player1 = Player(grid=self, location=(3, 3), img_path="images/char_blue.png",
                              img_action="do_nothing")



class Player(actor.Actor):

    def setup(self):
        self._is_rotatable = True

    def act(self):
        self.move()

    def listen(self, event, data):
        if event == "key":
            if "W" in data:
                self.move_up()
            elif "S" in data:
                self.move_down()
            elif "A" in data:
                self.move_left()
            if "D" in data:
                self.move_right()

#logging.basicConfig(stream=sys.stdout, level=logging.INFO)
mygrid = MyGrid("My Grid", cell_size=1, columns=200, rows=200,
                margin=0,img_path="images/soccer_green.jpg")
mygrid.show()
