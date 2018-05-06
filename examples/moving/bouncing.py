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
        for i in range(5):
            new_asteroid = Asteroid(grid=self, location=(random.randint(35,screen_x-35),random.randint(35,screen_y-35)))
            for asteroid in asteroids:
                new_asteroid.add_collision_partner(asteroid)
            asteroids.append(new_asteroid)



    def collision(self, partner1, partner2):
        partner1.direction=partner1.direction+180
        partner2.direction=partner2.direction+180


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

logging.basicConfig(stream=sys.stdout, level=logging.INFO)
random.seed()
screen_x=400
screen_y=300
mygrid = MyGrid("My Grid", cell_size=1, columns=screen_x, rows=screen_y,
                margin=0, speed=120)
mygrid.show()
