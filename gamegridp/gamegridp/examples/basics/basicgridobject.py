import gamegridp

class MyGrid(gamegridp.GameGrid):
    """My Grid with custom setup method."""


grid=MyGrid("My Grid", cell_size=64, columns=8, rows=8,margin=1)
grid.show()