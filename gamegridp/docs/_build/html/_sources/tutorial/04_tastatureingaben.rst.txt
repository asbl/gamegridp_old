Tastatureingaben
----------------

Tastatureingaben kannst du über Events abfangen. Dazu kannst du sowohl in deiner Grid-Klasse als auch in der Actor-Klasse
die Methode listen überschreiben.

Genau wie die Act-Methode wird auch die Listen-Methode bei jedem Durchlauf der Mainloop einmal ausgeführt und
überprüft ob in der Zwischenzeit Events (Tastatureingaben, Mausaktionen oder Drücken auf Buttons) gesendet wurden.

Die Methode hat zwei Parameter:

.. code-block:: python

    def listen(self, event, data):
        pass

Argumente:
  * **event** liefert in einem Text die Art des Events mit, das gesendet wurde. Bei einer Tastatureingabe gibt es hier zwei Varianten:
    * key bzw. key_pressed liefert die gerade gedrückte Taste. Wenn du eine Taste gedrückt hälst, wird das Event immer wieder gefeuert.
    * key_down wird nur gesendet, wenn die Taste heruntergedrückt wird.
    In Zellbasierten Spielen ist meist key_down die bessere Wahl, da sonst die Eingabe zu überempfindlich wird. In Pixelbasierten Spielen ist hingegen
    key bzw. key_pressed die bessere Alternative, da hier exaktere Eingaben abgeprüft werden können.
  * **data** liefert zusätzliche Informationen. Bei einer Tastatureingabe enthält data eine Liste aller zur Zeit gedrückten Tasten.

So kann die Methode aussehen, wenn bei einem Tastendruck in die entsprechende Richtung gelaufen werden soll:

.. code-block:: python
   :linenos:

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
