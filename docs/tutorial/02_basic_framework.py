Akteure im Grid
---------------

Als nächstes geht es dazu

import gamegridp
import logging
import sys

import gamegridp

.. code-block:: python
   :linenos:
    class MyGrid(gamegridp.GameGrid):
        """My Grid with custom setup method."""
        def setup(self):
            self.set_image(img_path="images/soccer_green.jpg")
            Player(grid=self, location=(3, 3))
            Player(grid=self, location=(8, 2))
    class Player(gamegridp.Actor):
        def setup(self):
            self.set_image(img_path="images/char_blue.png")
        def act(self):
            self.move()
            if not self.is_valid_move():
                self.turn_left()
    my_grid = MyGrid("My Grid", cell_size=12, columns=16, rows=16, margin=5, speed=60)
    my_grid.show()

Was macht der Code?
--------------------

  * In Zeile 1-6 wird ein Bauplan für ein neues Grid mit dem Namen MyGrid
    erstellt:

  * In Zeile 7-13 wird ein Bauplan für einen Akteur mit dem Namen Player
    erstellt.

  * In Zeile 3 ist die setup-Methode angegeben, die das Spielfeld einrichtet.
    Darin werden zwei Player Objekte an unterschiedlichen Positionen erzeugt.

  * In Zeile 10-13 wird die act()-Methode des Akteurs festgelegt. Sobald man auf den Button
    run klickt wird diese Methode immer wieder aufgerufen und sorgt dafür, dass die beiden Player-Objekte
    immer weiterlaufen, bis sie auf ein Hindernis stoßen und sich dann nach links drehen.

  * Am Ende wird wieder das MyGrid-Objekt erzeugt, welches wiederum nach seinem Bauplan die beiden Player-Objekte mit erzeugt.