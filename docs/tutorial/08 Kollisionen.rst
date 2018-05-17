Kollisionen
------------------

Bei Kollisionen muss man unterscheiden zwischen unterschiedlichen Arten von Kollisionen:

* **Zellen-Kollisionen**: Wenn dein Spiel Zellenbasiert ist,
dann bedeutet eine  Zellen-Kollision, das zwei Akteure in der selben Zelle stehen.

* **Bounding-Box-Kollisionen**: Wenn zwei Akteure auf einem Grid mit Zellgröße 1 kollidieren,
ist die erste Art der Abfrage natürlich ungeeignet. Hier müsste man theoretisch Pixel für Pixel
auf eine Kollision miteinander vergleichen.
Daher überorüft das Grid die umgebenden Bounding-Boxen, ob diese sich schneiden
(In der ersten Version handelt es sich dabei immer um Rechtecke). Diese Variante ist zwar etwas ungenau,
ist aber effizent berechenbar.

Zellen-Kollisionen
^^^^^^^^^^^^^^^^^^

Es gibt zwar mehrere Arten, Kollisionen in zellbasierten Spielen zu verwalten. Die einfachste Methode ist abet oft folgende:

* In der *act* oder *listen*-Methode der Klasse *GameGrid* kann eine Kollision mit Hilfe der Funktion
**get_all_actors_at_location()** überprüft werden.
(siehe auch: :py:meth:`gamegridp.gamegrid.GameGrid.get_all_actors_at_location`)

* Alternativ können auch die Akteure selbst überprüfen, ob eine Kollision vorliegt.
    Jeder Akteur verfügt über die Methode **get_all_actors_at_location()**
    (siehe auch: :py:meth:`gamegridp.gamegrid.Actor.get_all_actors_at_location`).

Beide Methoden geben jeweils eine Liste an Akteuren zurück. Man kann auch direkt nach Klassen filtern;

.. code-block:: python
    :linenos:

    gegenstand = self.get_all_actor_at_location("Gegenstand")
    # gegenstand ist eine Liste mit allen an der Position gefundenen Gegenständen.
        if gegenstand: # Abkürzung für if gegenstand is not None:
            #... tue etwas

Pixel-Kollisionen
^^^^^^^^^^^^^^^^^^

Da es aufwendig ist, alle Kollisionen pixelgenau zu überprüfen, werden jeweils Rechtecke miteinander verglichen.
Dazu sind zwei Schritte notwendig:

* In der setup()-Methode des jeweiligen Akteurs wird festgelegt, mit welchem Akteur der Akteur kollidieren kann.
Dafür ist die Methode actor.add_collision_partner() von Bedeutung.

**Beispiel 1**: Ein Schiff (player1 soll mit Asteroiden kollidieren können:

.. code-block:: python
    :linenos:
    :emphasize-lines: 4

        player1 = Player(grid=self, location=(40, 40))
        for i in range(5):
            asteroid=Asteroid(grid=self, location=(random.randint(30,screen_x-30),random.randint(0+30,screen_y-30)))
            player1.add_collision_partner(asteroid)


* Für alle Objekte wird in jedem Durchlauf überprüft, ob diese Kollidieren.
Wenn diese kollidieren, wird die collision(self, partner1, partner2)-Methode aufgerufen. Du kannst diese Methode
aufrufen, um dein gewünschtes Verhalten zu programmieren.

Beispiel: Das Schiff aus Beispiel 1 soll mit den Asteroiden kollidieren

.. code-block:: python
    :linenos:
    :emphasize-lines: 4

    def collision(self, partner1, partner2):
        Explosion(grid=self, location= partner1.location)
        partner1.remove()
        partner2.remove()
        self.stop()

Alternative
"""""""""""

Alternativ dazu ist es auch möglich Kollisionen manuell z.B. in der act() oder in der listen()-Methode abzufragen.
Hierfür kannst du entweder in der Klasse **Grid** folgende Methoden benutzen:

* get_all_bounding_box_collisions(actor, class_name: str = None): py:meth:`gamegridp.get_all_bounding_box_collisions`-
  Gibt alle Kollisionen eines Actors gefiltert nach Klassennamen zurück.


* get_bounding_box_collision :py:meth:`gamegridp.get_bounding_box_collision` -
  Gibt eine einzelne Kollision eines Actors gefiltert nach Klassennamen zurück.

In der Klasse **Actor** kannst du folgende Methoden verwenden:

* get_all_bounding_box_collisions(actor, class_name: str = None): py:meth:`gamegridp.get_all_bounding_box_collisions`- Gibt alle Kollisionen eines Actors gefiltert nach Klassennamen zurück.

* get_bounding_box_collision : py:meth:`gamegridp.get_bounding_box_collision` - Gibt eine einzelne Kollision eines Actors gefiltert nach Klassennamen zurück.




