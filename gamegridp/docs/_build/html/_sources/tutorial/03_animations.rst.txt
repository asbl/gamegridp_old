Animationen
---------------

Animationen kannst du erstellen, indem du einem Actor mehrere Bilder hinzufügst.
Anschließend kannst du mit der Methode animate() die Figur animieren, d.h. es wird ähnlich wie bei einem Daumenkino
schnell zwischen den einzelnen Bildern umgeschaltet.

.. code-block:: python
   :linenos:

    def setup(self):
        self.add_image("images/robot_blue1.png", "scale", size=(20,20))
        self.add_image("images/robot_blue2.png", "scale", size=(20,20))
        self._animation_speed = 2
        self.animate()

Siehe Beispiel **Roboanimation** auf `Github <https://github.com/asbl/gamegridp/blob/latest/examples/snippets/moving/roboanimation.py>`_

.. image:: /_images/roboanimation.gif

