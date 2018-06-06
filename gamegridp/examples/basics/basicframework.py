import gamegridp

class MyGrid(gamegridp.GameGrid):
    """My Grid with custom setup method."""

    def setup(self):
        self.set_image(img_path="images/soccer_green.jpg")
        player1 = Player(grid=self, location=(3, 3))
        player2 = Player(grid=self, location=(8, 2))


class Player(gamegridp.Actor):
    def setup(self):
        self.set_image(img_path="images/char_blue.png")

    def act(self):
        self.move()
        if not self.is_valid_move():
            self.turn_left()
MyGrid.log()
my_grid = MyGrid("My Grid", cell_size=16, columns=40, rows=16, margin=1, speed=60)
my_grid.show()
