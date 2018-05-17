Die Konsole
------------------

Die Konsole kann z.B. in Rollenspielen dabei helfen, Informationen als Text auszugeben.

Du kannst eine Konsole zum GameGrid hinzufügen, in dem du beim Aufrufen des Konstruktors den Parameter console=True ergänzt.

Beispiel

.. code-block:: python
    :linenos:

    mygrid = MyGrid("My Grid", cell_size=20, columns=30, rows=20,
                margin=1, console = True)

Du kannst folgendermaßen Informationen auf die Konsole schreiben:

.. code-block:: python
    :linenos:

    self.grid.console.print("Information für die Konsole")