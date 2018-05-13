import gamegridp
from gamegridp import keys
import random
import sys
import logging
import sys

class MyGrid(gamegridp.PixelGrid):
    """My Grid with custom setup method."""

    def setup(self):
        self.set_image("images/galaxy.jpg","scale")
        asteroids=[]
        for i in range(5):
            new_asteroid = Asteroid(grid=self, location=(random.randint(35,screen_x-35),random.randint(35,screen_y-35)))
            for asteroid in asteroids:
                new_asteroid.add_collision_partner(asteroid)
            asteroids.append(new_asteroid)

    def collision(self, partner1, partner2):
        self.bounce(partner1, partner2)


class Asteroid(gamegridp.Actor):
    def setup(self):
        self.set_image("images/asteroid.png","scale",(30,30))
        self.set_rotatable()
        self.direction = random.randint(0, 360)
        self.set_bounding_box_size((30, 30))

    def act(self):
        self.move(2)
        border=self.is_at_border()
        if border is not False:
            self.grid.bounce_from_border(self, border)
            self.move(2)


logging.basicConfig(stream=sys.stdout, level=logging.INFO)
random.seed()
screen_x=400
screen_y=300
mygrid = MyGrid("My Grid", cell_size=1, columns=screen_x, rows=screen_y,
                margin=0, speed=120)
mygrid.show()
