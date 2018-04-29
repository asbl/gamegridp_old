import logging
import sys

import gamegridp


class MyGrid(gamegridp.GameGrid):
    """My Grid with custom setup method."""

    def setup(self):
        robo1 = Robot(grid=self, location=(1, 1), img_action="scale")

    def listen(self, event=None, data=None):
        if event == "mouse_left":
            if self.is_empty((data[0], data[1])):
                Wall(self, (data[0], data[1]))
                self._logging.info("Wall created at: " + str(data[0]) + "," + str(data[1]))
            else:
                self.remove_actor(cell=(data[0], data[1]))


class Robot(gamegridp.Actor):
    def setup(self):
        self.set_rotatable()

    def act(self):
        self.move(1)


class Wall(gamegridp.Actor):
    def setup(self):
        self.set_blocked()
        self.add_image("images/rock.png", img_action="scale")


logging.basicConfig(stream=sys.stdout, level=logging.INFO)
mygrid = MyGrid("My Grid", cell_size=60, columns=10, rows=10,
                margin=0, speed=120,
                background_color=(200, 0, 0), cell_color=(0, 0, 255), img_path="images/stone.jpg")
mygrid.show()
