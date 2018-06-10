import gamegridp
from gamegridp import keys
import logging
import sys

class MyGrid(gamegridp.GameGrid):
    """My Grid with custom setup method."""


    def setup(self):
        self.player1 = Player(grid=self, location=(3, 3), img_path="images/char_blue.png",
                              img_action="center")



class Player(gamegridp.Actor):

    def setup(self):
        self._is_rotatable = True

    def act(self):
        self.move()

    def listen(self, event, data):
        if event == "key_down":
            if "W" in data:
                self.direction = "up"
                self.move()
            elif "S" in data:
                self.direction = "down"
                self.move()
            elif "A" in data:
                self.direction = "left"
                self.move()
            elif "D" in data:
                self.direction = "right"
                self.move()


MyGrid.log()
mygrid = MyGrid("My Grid",    cell_size=40, columns=15, rows=5,
                margin=1, speed=60,
                background_color=(200, 0, 0),cell_color=(0, 0, 255), img_path="images/soccer_green.jpg")
mygrid.show()
