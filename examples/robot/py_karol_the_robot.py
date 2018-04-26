import logging
import sys

from gamegridp import actor
from gamegridp import gamegrid


class MyGrid(gamegrid.GameGrid):
    """My Grid with custom setup method."""

    def setup(self):
        robo1 = Robot(grid=self, location=(1, 1), img_action="scale", log=True)

        # Draw border
        for i in range(self._grid_rows):
            Wall(grid=self, location=(0, i))
        for i in range(self._grid_rows):
            Wall(grid=self, location=(self._grid_rows - 1, i))
        for i in range(self._grid_columns):
            Wall(grid=self, location=(i, 0))
        for i in range(self._grid_columns - 1):
            Wall(grid=self, location=(i, self._grid_columns - 1))


class Robot(actor.Actor):
    def setup(self):
        self.set_rotatable()
        self.add_image("images/robo_green.png", "scale", (40, 40))

    def act(self):
        self.move(1)


class Wall(actor.Actor):
    def setup(self):
        self.set_blocked()
        self.add_image("images/rock.png", img_action="scale")


logging.basicConfig(stream=sys.stdout, level=logging.INFO)
module_logger = logging.getLogger('gglogger')
mygrid = MyGrid("My Grid", log=True, cell_size=60, columns=10, rows=10,
                margin=0, speed=120,
                background_color=(200, 0, 0), cell_color=(0, 0, 255), img_path="images/stone.jpg")
mygrid.show()
