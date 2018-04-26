import logging
import sys
import sqlite3 as lite
from gamegridp import actor
from gamegridp import gamegrid


class MyGrid(gamegrid.GameGrid):
    """My Grid with custom setup method."""

    def listen(self, event=None, data=None):
        self._logging.info(event)
        if event == "mouse_left":
            if self.is_empty((data[0], data[1])):
                Wall(self, (data[0], data[1]))
                self._logging.info("Wall created at: " + str(data[0]) + "," + str(data[1]))
            else:
                self.remove_actor(cell=(data[0], data[1]))
        elif event == "mouse_right":
            if self.is_empty((data[0], data[1])):
                Robot(self, (data[0], data[1]))
                self._logging.info("Robo created at: " + str(data[0]) + "," + str(data[1]))
            else:
                self.remove_actor(cell=(data[0], data[1]))
        elif event == "button":
            if data=="Speichern":
                self._logging.info("Button " + str(data) + " pressed")
                self.save()

    def save(self):
        #try:
            connection = lite.connect('robodatabase.db')
            cursor = connection.cursor()
            cursor.execute('SELECT id FROM Game ORDER BY id DESC LIMIT 1')
            gameid = cursor.fetchone()
            gameid=int(gameid[0])+1
            for actor in self.actors:
                cursor.execute('INSERT INTO Actors(row,column,GameID,Actor) VALUES ('+str(actor.location[0])+","+str(actor.location[1])+","+str(gameid)+",'"+str(actor.title)+"')")
                self._logging.info("...values inserted")

            cursor.execute('INSERT INTO Game Values('+gameid+')')
            connection.commit()

    def load(self,gameid):
        #try:
            connection = lite.connect('robodatabase.db')
            cursor = connection.cursor()
            cursor.execute('SELECT id FROM Game ORDER BY id DESC LIMIT 1')
            gameid = cursor.fetchone()
            gameid=int(gameid[0])+1
            for actor in self.actors:
                cursor.execute('SELECT * from Actors WHERE game='+str(gameid))
                self._logging.info("...values loaded")


            cursor.execute('INSERT INTO Game Values('+gameid+')')
            connection.commit()

class Robot(actor.Actor):
    def setup(self):
        self.title="Robot"
        self.set_rotatable()
        self.add_image("images/robo_green.png", "scale", (40, 40))

    def act(self):
        self.move(1)


class Wall(actor.Actor):
    def setup(self):
        self.title="Wall"
        self.set_blocked()
        self.add_image("images/rock.png", img_action="scale")


logging.basicConfig(stream=sys.stdout, level=logging.INFO)
module_logger = logging.getLogger('gglogger')
mygrid = MyGrid("My Grid", log=True, cell_size=60, columns=10, rows=10,
                margin=0, speed=120,
                background_color=(200, 0, 0), cell_color=(0, 0, 255), img_path="images/stone.jpg", toolbar=True)
mygrid.add_toolbar_button("images/rock.png", "Speichern")
mygrid.show()
