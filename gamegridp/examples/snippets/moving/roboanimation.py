import gamegridp


class MyGrid(gamegridp.GameGrid):
    """My Grid with custom setup method."""
    def setup(self):
        self.player1 = Robot(grid=self, location=(50, 70))


class Robot(gamegridp.Actor):

    def setup(self):
        self.add_image("images/robot_blue1.png", "scale", size=(120,120))
        self.add_image("images/robot_blue2.png", "scale", size=(120,120))
        self.animation_speed = 30
        self.animate()


    def act(self):
        valid = self.move(1)
        if not valid:
            self.flip_x()

MyGrid.log()
mygrid = MyGrid("My Grid", cell_size=1, columns=500, rows=150,
                margin=0,  img_path="images/water.png")
mygrid.show()
