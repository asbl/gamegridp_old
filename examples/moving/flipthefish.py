import logging
import sys
import gamegridp


class MyGrid(gamegridp.GameGrid):
    """My Grid with custom setup method."""
    def setup(self):
        self.player1 = Player(grid=self, location=(3, 3))
        self.player1.add_image(img_path="images/fish.png", size=(80, 80))


class Player(gamegridp.Actor):
    def act(self):
        if self.is_valid_move():
            self.move()
        else:
            self.flip_x()


logging.basicConfig(stream=sys.stdout, level=logging.INFO)
mygrid = MyGrid("My Grid", cell_size=25, columns=40, rows=20,
                margin=1, speed=120,
                background_color=(200, 0, 0), cell_color=(0, 0, 255), img_path="images/water.png")
mygrid.show()
