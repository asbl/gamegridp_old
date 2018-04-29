import gamegridp
from gamegridp import keys
import random
import sys

class MyGrid(gamegridp.GameGrid):
    """My Grid with custom setup method."""

    def setup(self):
        self.set_image("images/galaxy.jpg","scale")
        player1 = Player(grid=self, location=(40, 40))
        for i in range(5):
            asteroid=Asteroid(grid=self, location=(random.randint(0,screen_x),random.randint(0,screen_y)))
            player1.add_collision_partner(asteroid)

    def collision(self, partner1, partner2):
        Explosion(grid=self, location=partner1.location)
        partner1.remove()
        partner2.remove()
        self.stop()


class Player(gamegridp.Actor):

    def setup(self):
        self.set_image("images/ship.png","scale",(30,30))
        self.set_rotatable()


    def listen(self,event,data):
        if event == "key":
            if data == keys.W:
                self.turn_left(10)
            elif data == keys.S:
                self.turn_right(10)

    def act(self):
        self.move(3)


class Asteroid(gamegridp.Actor):
    def setup(self):
        self.set_image("images/asteroid.png","scale",(30,30))
        self.set_rotatable()
        self.direction = random.randint(0, 360)

    def act(self):
        if self.is_valid_move():
            self.move(1)
        else:
            self.turn_left(180)

class Explosion(gamegridp.Actor):
    def setup(self):
        self.add_image("images/explosion.png", "do_nothing")

random.seed()
screen_x=400
screen_y=300
mygrid = MyGrid("My Grid", log=True, cell_size=1, columns=screen_x, rows=screen_y,
                margin=0, speed=120)
mygrid.show()
