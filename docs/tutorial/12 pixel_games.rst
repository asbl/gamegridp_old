Pixel-Games
------------

Pixel-Games sind Spiele bei denen die einzelnen Felder des Spielfeldes eine Größe von genau einem Pixel haben.
Pixel-Games unterscheiden sich durch einige Besonderheiten:

  * Da die Akteure **größer** sind als die Zelle auf der sie sich befinden, funktioniert die Kollisionsabfrage anders (Siehe Kollisionen).


Das PixelGrid
^^^^^^^^^^^^^^

Die Klasse gamegridp.PixelGrid ist eine Kindklasse von GameGridp. Ein PixelGrid bietet einige spezielle Funktionen,
die nur für Pixel-Spiele von besonderer Bedeutung sind. Dies sind aktuell:

  * bounce(self, actor1, actor2): Berechnet die Winkel zweier aufeinander zufliegenden Actors neu, so dass Einfalsswinkel=Ausfallswinkel
  * bounce_against_line(self, actor1, line_axis): Berechnet den Winkel neu, wenn ein Actor auf die Linie mit dem Neigungswinkel line_axis aufprallt.
  * bounce_from_border(self,actor, border : Berechnet den Winkel neu wenn der Actor gegen den Rand prallt.