import gamegridp


class MyGrid(gamegridp.GameGrid):
    """My Grid with custom setup method."""
    def setup(self):
        self.player1 = Robot(grid=self, location=(50, 70))


class Robot(gamegridp.Actor):

    def setup(self):
        self.add_image("images/robot_blue1.png", "scale", size=(20,20))
        self.add_image("images/robot_blue2.png", "scale", size=(20,20))
        self.animation_speed = 20
        self.animate()


    def act(self):
        valid = self.move()
        if not valid:
            self.flip_x()

mygrid = MyGrid("My Grid", cell_size=1, columns=200, rows=150,
                margin=0, speed=60,
                background_color=(200, 0, 0), cell_color=(0, 0, 255), img_path="images/water.png")
mygrid.show()
