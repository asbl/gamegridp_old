Die Toolbar
------------------

Ein Toolbar hinzufügen
"""""""""""""""""""""""

Die Toolbar ist der Platz für GUI-Elemente, z.B. Buttons oder Labels.


.. code-block:: python
    :linenos:

    mygrid = MyGrid("My Grid", cell_size=20, columns=30, rows=20,
                margin=1, toolbar = True)

GUI-Elemente zur Toolbar hinzufügen
"""""""""""""""""""""""""""""""""""

In die Toolbar können GUI-Elemente hinzugefügt werden. Zum jetzigen Zeitpunkt ist es nur möglich, Buttons hinzuzufügen:

.. code-block:: python
    :linenos:

    grid.toolbar.add_button("Button", "button_image.png")


Auf Toolbar-Events reagieren
""""""""""""""""""""""""""""

Die Toolbar wirft auch selbst Events. Ein Button Event sendet zum Beispiel ein Event mit den Paramtern

* event: "button"

* data: Der Name des Buttons als String

Das Event kann in der listen()-Methode wie jedes andere Element abgefangen und interpretiert werden.