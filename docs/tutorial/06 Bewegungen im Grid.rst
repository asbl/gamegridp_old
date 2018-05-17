Bewegungen im Grid
------------------

Prinzipiell kann die Bewegung an unterschiedlichen Stellen des Programmcodes stattfinden:

Bewegung in der act-Methode:
  * In der act()-Methode: Hier macht die Bewegung vor allem dann Sinn, wenn der Akteur sich permanent fortbewegen soll.
   Immer wenn Bewegungen in Echtzeit stattfinden sollen, sollte hier auch deine Bewegung stattfinden.

.. code-block:: python
    :linenos:
    :emphasize-lines: 2
    :caption: Beispiel für Bewegung in der act-Methode

    def act(self):
        self.move(3)

    def listen(self, event, data):
        if event == "key":
            if "W" in data :
                self.turn_left(10)
            if "S" in data:
                self.turn_right(10)


Bewegung in der listen-Methode
  * In der listen()-Methode: Vor allem in rundenbasierten Spielen kann es sinnvoll sein, hier die Bewegung zu steuern.

.. code-block:: python
   :linenos:
   :emphasize-lines: 5,8,11,14
   :caption: Beispiel für Bewegung in der listen-Methode

    def listen(self, event, data):
        if event == "key_down":
            if "W" in data:
                self.direction = "up"
                self.move()
            elif "S" in data:
                self.direction = "down"
                self.move()
            elif "A" in data:
                self.direction = "left"
                self.move()
            elif "D" in data:
                self.direction = "right"
                self.move()


