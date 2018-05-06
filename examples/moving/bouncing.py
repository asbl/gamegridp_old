import gamegridp
from gamegridp import keys
import random
import sys
import logging
import sys

class MyGrid(gamegridp.GameGrid):
    """My Grid with custom setup method."""

    def setup(self):
        self.set_image("images/galaxy.jpg","scale")
        for i in range(1):
            asteroid=Asteroid(grid=self, location=(random.randint(0,screen_x),random.randint(0,screen_y)))

    def collision(self, partner1, partner2):
        Explosion(grid=self, location= partner1.location)
        partner1.remove()
        partner2.remove()
        self.stop()


class Asteroid(gamegridp.Actor):
    def setup(self):
        self.set_image("images/asteroid.png","scale",(30,30))
        self.set_rotatable()
        self.direction = random.randint(0, 360)

    def act(self):
        valid = self.move(4)
        if not valid:
            print("not valid")
            self.turn_left(180)
            self.move(4)

class Explosion(gamegridp.Actor):
    def setup(self):
        self.add_image("images/explosion.png", "do_nothing")

logging.basicConfig(stream=sys.stdout, level=logging.INFO)
random.seed()
screen_x=400
screen_y=300
mygrid = MyGrid("My Grid", cell_size=1, columns=screen_x, rows=screen_y,
                margin=0, speed=120)
mygrid.show()
