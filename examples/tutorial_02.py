from gamegridp_local.gamegridp import actor
from gamegridp_local.gamegridp import gamegrid
import logging
import sys

grid=gamegrid.GameGrid("My Grid", cell_size=64, columns=8, rows=8,margin=2,
                        img_path="water.jpg",img_action="crop")
grid.show()