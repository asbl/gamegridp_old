from gamegridp import actor
from gamegridp import gamegrid
from gamegridp import keys

class MyGrid(gamegrid.GameGrid):
    """My Grid with custom setup method."""

    def setup(self):
        player1 = Player("Player", grid=self, location=(20, 20), img_action="do_nothing")
        player1.image_add("images/robo_green.png", "scale", (40, 40))


class Player(actor.Actor):
    is_rotatable = True
    def act(self):
        self.move(3)

    def listen(self, event, data):
        if event == "key":
            if data == keys.W:
                self.turn_left(10)
            elif data == keys.S:
                self.turn_right(10)


mygrid = MyGrid("My Grid", log=True, cell_size=1, columns=400, rows=400,
                margin=0, speed=60,
                background_color=(200, 0, 0),cell_color=(0, 0, 255), img_path="images/stone.jpg")
mygrid.show()
