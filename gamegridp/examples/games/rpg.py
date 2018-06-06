import gamegridp
import logging
import sys

class MyGrid(gamegridp.GameGrid):
    """My Grid with custom setup method."""
    def setup(self):
        for i in range(ROWS):
            for j in range(COLUMNS):
                self.add_cell_image("rpgimages/stone.png",(j,i))



class Player(gamegridp.Actor):

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
            elif "D" in data:
                self.move_right()

logging.basicConfig(stream=sys.stdout, level=logging.INFO)
ROWS=20
COLUMNS=40
mygrid = MyGrid("My Grid",    cell_size=16, columns=40, rows=20,
                margin=0, speed=10)
mygrid.show()
