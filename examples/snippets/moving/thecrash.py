from gamegridp import actor
from gamegridp import gamegrid


class MyGrid(gamegrid.GameGrid):
    """My Grid with custom setup method."""
    def setup(self):
        self.robot1 = Robot(grid=self, location=(0, 0), img_path="images/robo_green.png", img_action="scale")
        self.robot2 = Robot(grid=self, location=(28, 0), img_path="images/robo_yellow.png", img_action="scale")
        self.robot1.add_collision_partner(self.robot2)
        self.robot2.turn_left(180)
        self.set_image(img_path = "images/water.png", img_action = "fill")

    def act(self):
        pass

    def collision(self, partner1, partner2):
        location = self.robot1.get_location()
        explosion = Explosion(title="boom", grid=self, location=self.robot1.location)
        self.remove_actor(self.robot1)
        self.remove_actor(self.robot2)
        self.add_actor(explosion)

class Explosion(actor.Actor):
    def setup(self):
        self.add_image("images/explosion.png", "do_nothing")


class Robot(actor.Actor):
    def setup(self):
        self.set_rotatable()

    def act(self):
        self.move()

MyGrid.log()
mygrid = MyGrid("My Grid", cell_size=40, columns=29, rows=1,
                margin=0,)
mygrid.show()
