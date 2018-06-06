GUI Elemente
------------

Du kannst GUI-Elemente hinzufügen, in dem dein Grid keine Kindklasse eines normalen Grids ist, sondern eine Kindklasse von
**gamegridp.GUIGrid**.

Beispiel:

.. code-block:: python
    :linenos:
   :emphasize-lines: 1

    class MyGrid(gamegridp.GUIGrid):
        """My Grid with custom setup method."""
        def setup(self):
            self.toolbar.add_button("Spin")

Anschließend kannst du über folgende Methoden Nachrichten senden:

* integer_box : Eine Box zum Eingeben von Integer-Zahlen.

* message_box : Eine Box, die eine Nachricht anzeigt

* button_box : Eine Box mit Buttons. Der ausgewählte Button wird als String zurückgegeben.

Beispiel:


.. code-block:: python
    :linenos:
   :emphasize-lines: 1

    message = "Die Tür ist geschlossen... möchtest du sie öffnen"
                choices = ["Ja", "Nein"]
                reply = self.grid.button_box(message, choices)