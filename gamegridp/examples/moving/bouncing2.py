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
        asteroids=[]
        a1 = Asteroid(grid=self, location=(100,60))
        a1.direction = 220
        a2 = Asteroid(grid=self, location=(20,60))
        a2.direction = 320
        a2.add_collision_partner(a1)

    def collision(self, partner1, partner2):
        self.bounce(partner1, partner2)
        partner1.move(2)
        partner2.move(2)

class Asteroid(gamegridp.Actor):
    def setup(self):
        self.set_image("images/asteroid.png","scale",(30,30))
        self.set_rotatable()

    def act(self):
        self.move(2)
        border=self.is_at_border()
        if border is not False:
            self.bounce_from_border(border)
            self.move(2)




logging.basicConfig(stream=sys.stdout, level=logging.INFO)
random.seed()
screen_x=400
screen_y=300
mygrid = MyGrid("My Grid", cell_size=1, columns=screen_x, rows=screen_y,
                margin=0, speed=10)
mygrid.show()
