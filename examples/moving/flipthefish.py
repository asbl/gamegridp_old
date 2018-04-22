import sys
import gamegridp


class MyGrid(gamegridp.GameGrid):
    """My Grid with custom setup method."""

    def setup(self):
        self.player1 = Player("Player", grid=self, location=(3, 3), img_path="images/fish.png",
                         img_action="do_nothing")



class Player(gamegridp.Actor):
    def __init(self):
        super().__init()


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
                if not self.is_flipped:
                    self.flip_x()
            elif data == keys.D:
                self.move_right()
                if self.is_flipped:
                    self.flip_x()


mygrid = MyGrid("My Grid", log=True, cell_size=20, columns=20, rows=20,
                margin=0, speed=120,
                background_color=(200, 0, 0),cell_color=(0, 0, 255),img_path="images/water.png")
mygrid.show()
