Datenbankanbindung
==================

GameGridP verfügt über eine  sqllite-Anbindung. Folgendermaßen kannst du Daten in sqllite speichern:

Tabelle vorbereiten und in Python laden
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

1. Erstelle eine Datenbank und lege die Tabellenstruktur an.
 Du kannst dafür den `DB Browser for sqlite <http://sqlitebrowser.org/>`_ oder `Sqlite Studio <https://sqlitestudio.pl/index.rvt>`_ verwenden.

2. Deine Klasse muss eine Kindklasse der Klasse DatabaseGrid sein.

Beispiel:

.. code-block:: python
    :linenos:

    class MyGrid(gamegridp.DatabaseGrid, gamegridp.GUIGrid):

3. Öffne eine Verbindung zur Datenbank.

.. code-block:: python
    :linenos:

        self.connect("robodatabase.db")

Jetzt kannst du folgendermaßen Daten aus der Datenbank auslesen und in die Datenbank schreiben.

Daten auslesen
^^^^^^^^^^^^^^

Daten kannst du entweder mit der Anweisung self.select_single_row oder mit select_all_rows stellen.

self.select_single_row fragt eine einzelne Zeile aus der Datenbank ab:

.. code-block:: python
    :linenos:

row = self.select_single_row('SELECT id FROM Game ORDER BY id DESC LIMIT 1')

fragt z.B. aus der Tabelle GAME die GameID ab. Das Ergebnis wird in einer Liste gespeichert und kann z.B. über

.. code-block:: python
    :linenos:
        gameid = row[0]

abgefragt werden.

Mit self.select_all_rows können alle Werte einer Abfrage abgefragt werden.

.. code-block:: python
    :linenos:

    rows = self.select_single_row('SELECT id FROM Game ORDER BY id DESC')

Mit folgendem Code kannst du die einzelnen Werte dann weiterverarbeiten


Daten in die Tabelle schreiben
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Daten kannst du mit Hilfe der Methode self.insert(Tabelle, Dictionary) einfügen.
In dem Dictionary (Eine Datenstruktur vergleichbar mit einem Telefonbuch oder Wörterbuch)
werden die Zuordnungen spaltenname : wert gespeichert.

So soll z.B. in Spalte 4 und Zeile 4 der Actor vom Typ Wall mit der ID 1 gespeichert werden:

.. code-block:: python
    :linenos:

        dict = {"column":4,
                "row": 4,
                "GameID": 1,
                "Actor" : "Wall
                }
            self.insert("Actors", dict )

Daten übertragen und Verbindung schließen
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Zuletzt musst du die Daten in die Datenbank übertragen (committen) und die Verbindung schließen. Dies geht wie folgt:

.. code-block:: python
    :linenos:

        self.commit()
        self.close_connection()

