import gamegridp
from gamegridp import keys
import random
import sys

class MyGrid(gamegridp.PixelGrid):
    """My Grid with custom setup method."""

    def setup(self):
        self.set_image("images/galaxy.jpg","scale")
        asteroids=[]
        for i in range(5):
            new_asteroid = Asteroid(grid=self, location=(random.randint(35,self.columns-35),random.randint(35,self.rows-35)))
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

def main(argv):
    random.seed()
    MyGrid.log()
    mygrid = MyGrid("My Grid", cell_size=1, columns=400, rows=300,
                margin=0)
    mygrid.log()
    mygrid.show()


if __name__ == "__main__":
    main(sys.argv[1:])