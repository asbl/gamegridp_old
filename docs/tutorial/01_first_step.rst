Das Spielfenster
------------------
Die wichtigsten beiden Klassen der Bibliothek gamegridp sind GameGrid und Actor.

    Die Klasse GameGrid erzeugt das Spielfenster
    Actors sind alle sich bewegenden Figuren und Objekte, die im Spielfenster erscheinen

GameGrid stellt ein Spielfenster (GameGrid) zur Verfügung.
Das Spielfenster besteht aus einzelnen, quadratischen Zellen, die in Zeilen und Spalten angeordnet sind.
Die Zellengröße, Anzahl der Zeilen, Spalten, Abstände zwischen den Zellen (und vieles mehr) ist frei wählbar.

.. code-block:: python
   :linenos:

   class MyGrid(gamegrid.GameGrid):
        """My Grid with custom setup method."""

Zuletzt erstellst du ein konkretes Grid nach diesem Bauplan -
Hier mit 8 Zeilen, 8 Spalten, der Zellgröße 64 und dem Abstand 1 zwischen den einzelnen Zellen:

.. code-block:: python
   :linenos:

    grid=MyGrid("My Grid", cell_size=64, columns=8, rows=8, margin=1)
        grid.show()


Komplettes Programm:

.. code-block:: python
   :linenos:

   import gamegridp

   class MyGrid(gamegridp.GameGrid):
       """My Grid with custom setup method."""

   grid=MyGrid("My Grid", cell_size=64, columns=8, rows=8,margin=1)
   grid.show()
