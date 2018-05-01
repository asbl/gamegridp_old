import logging
import sys
import sqlite3 as lite
import gamegridp


class MyGrid(gamegridp.GameGrid):
    """My Grid with custom setup method."""

    def setup(self):
        self.load(2)

    def listen(self, event=None, data=None):
        self._logging.info(event)
        if event == "mouse_left":
            if self.is_empty_cell((data[0], data[1])):
                Wall(self, (data[0], data[1]))
                self._logging.info("Wall created at: " + str(data[0]) + "," + str(data[1]))
            else:
                self.remove_actor(cell=(data[0], data[1]))
        elif event == "mouse_right":
            if self.is_empty_cell((data[0], data[1])):
                Robot(self, (data[0], data[1]))
                self._logging.info("Robo created at: " + str(data[0]) + "," + str(data[1]))
            else:
                self.remove_actor(cell=(data[0], data[1]))
        elif event == "button":
            if data=="Speichern":
                self._logging.info("Button " + str(data) + " pressed")
                self.save()

    def save(self):
        connection = lite.connect('robodatabase.db')
        cursor = connection.cursor()
        cursor.execute('SELECT id FROM Game ORDER BY id DESC LIMIT 1')
        gameid = cursor.fetchone()
        gameid = gameid[0]
        gameid=gameid+1
        for actor in self.actors:
            cursor.execute('INSERT INTO Actors(row,column,GameID,Actor) VALUES ('+str(actor.location[0])+","+str(actor.location[1])+","+str(gameid)+",'"+str(actor.title)+"')")
            self._logging.info("...values inserted")
        self._logging.info("Game " + str(gameid) + " saved")
        cursor.execute('INSERT INTO Game (ID) Values('+str(gameid)+')')
        self._logging.info("...game id")
        connection.commit()
        connection.close()
        self._logging.info("Game "+str(gameid)+" saved")

    def load(self,gameid):
        connection = lite.connect('robodatabase.db')
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM Actors')
        for actordata in cursor.fetchall():
            if actordata[4]=="Wall":
                Wall(grid=self, location=(actordata[1],actordata[2]))
            elif actordata[4]=="Robot":
                Robot(grid=self, location=(actordata[1], actordata[2]))
        actors=cursor.fetchall()
        print("Load Actors: "+str(actors))

class Robot(gamegridp.Actor):
    def setup(self):
        self.title="Robot"
        self.set_rotatable()
        self.add_image("images/robo_green.png", "scale", (40, 40))


    def act(self):
        self.move(1)


class Wall(gamegridp.Actor):
    def setup(self):
        self.title="Wall"
        self.set_blocked()
        self.add_image("images/rock.png", img_action="scale")


logging.basicConfig(stream=sys.stdout, level=logging.INFO)
mygrid = MyGrid("My Grid", cell_size=60, columns=10, rows=10,
                margin=0, speed=120,
                background_color=(200, 0, 0), cell_color=(0, 0, 255), img_path="images/stone.jpg", toolbar=True)
mygrid.add_toolbar_button("images/rock.png", "Speichern")
mygrid.show()
