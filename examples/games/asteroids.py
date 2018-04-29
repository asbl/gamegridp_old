import gamegridp
from gamegridp import keys

class MyGrid(gamegridp.GameGrid):
    """My Grid with custom setup method."""

    def setup(self):
        self.set_image("images/galaxy.jpg")
        player1 = Player(grid=self, location=(80, 80))


class Player(gamegridp.Actor):

    def listen(self,event,data):
        if event == "key":
            if data == keys.W:
                self.move_up()
            elif data == keys.S:
                self.move_down()
            elif data == keys.A:
                self.move_left()
            elif data == keys.D:
                self.move_right()



mygrid = MyGrid("My Grid", log=True, cell_size=1, columns=200, rows=200,
                margin=0, speed=60)
mygrid.show()
