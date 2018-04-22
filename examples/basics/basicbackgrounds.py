from gamegridp import gamegrid

class MyGrid(gamegrid.GameGrid):
    """My Grid with custom setup method."""


grid = MyGrid("My Grid", cell_size=64, columns=8, rows=8, margin=2,
                        img_path="images/water.jpg",img_action="crop")
grid.show()
