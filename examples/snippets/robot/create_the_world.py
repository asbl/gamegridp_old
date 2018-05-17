import logging
import sys
import sqlite3 as lite
import gamegridp


class MyGrid(gamegridp.DatabaseGrid, gamegridp.GUIGrid):
    """My Grid with custom setup method."""

    def setup(self):
        self.toolbar.add_button("Speichern", "images/save.png")
        self.toolbar.add_button("Laden", "images/save.png")
        self.toolbar.add_button("wall", "images/rock.png")
        self.toolbar.add_button("robot", "images/robo_green.png")
        self.toolbar.add_button("gold", "images/stone_gold.png")
        self.toolbar.add_button("diamond", "images/stone_blue.png")
        self.toolbar.add_button("emerald", "images/stone_green.png")

    def listen(self, event=None, data=None):
        self._logging.info(event)
        if event == "mouse_left":
            if self.is_empty_cell((data[0], data[1])):
                if self.state=="wall":
                    Wall(self, (data[0], data[1]))
                if self.state=="robot":
                    Robot(self, (data[0], data[1]))
                if self.state=="gold":
                    Gold(self, (data[0], data[1]))
                if self.state=="diamond":
                    Diamond(self, (data[0], data[1]))
                if self.state=="emerald":
                    Emerald(self, (data[0], data[1]))
            else:
                self.remove_actor(cell=(data[0], data[1]))
        elif event == "button":
            if data == "robot":
                self.state="robot"
            elif data == "wall":
                self.state="wall"
            elif data == "gold":
                self.state="gold"
            elif data == "emerald":
                self.state="emerald"
            elif data == "diamond":
                self.state="diamond"
            elif data=="Speichern":
                self._logging.info("Create the World: event -save")
                game_id = self.save()
                self.messageBox("Neues Spiel mit id "+str(game_id)+" erstellt")
            if data=="Laden":
                self._logging.info("Create the World: event - load")
                game_id=self.integer_box("Gebe das Spiel ein, das geladen werden soll")
                if game_id:
                    self.remove_all_actors()
                    self.load(game_id)

    def save(self) -> int:
        self.connect("robodatabase.db")
        row = self.select_single_row('SELECT id FROM Game ORDER BY id DESC LIMIT 1')
        gameid = row[0]
        gameid=gameid+1
        for actor in self.actors:
            dict = {"column":actor.location[0],
                                  "row": actor.location[1],
                                  "GameID": gameid,
                                  "Actor" : actor.title}
            self.insert("Actors", dict )
        self.insert("Game",{"ID": gameid})
        self.commit()
        self.close_connection()
        self._logging.info("Game "+str(gameid)+" saved")
        return gameid

    def load(self, game_id):
        connection = lite.connect('robodatabase.db')
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM Actors WHERE GameID=' + str(game_id))
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
        self.is_rotatable = True
        self.add_image("images/robo_green.png", "scale", (40, 40))


    def act(self):
        self.move(1)


class Wall(gamegridp.Actor):
    def setup(self):
        self.title="Wall"
        self.is_blocking = True
        self.add_image("images/rock.png", img_action="scale")

class Gold(gamegridp.Actor):
    def setup(self):
        self.title="Wall"
        self.add_image("images/stone_gold.png", img_action="scale")

class Diamond(gamegridp.Actor):
    def setup(self):
        self.title="Wall"
        self.add_image("images/stone_blue.png", img_action="scale")

class Emerald(gamegridp.Actor):
    def setup(self):
        self.title="Wall"
        self.add_image("images/stone_green.png", img_action="scale")


logging.basicConfig(stream=sys.stdout, level=logging.INFO)
mygrid = MyGrid("My Grid", cell_size=60, columns=10, rows=10,
                margin=0, speed=120,
                background_color=(200, 0, 0), cell_color=(0, 0, 255), img_path="images/stone.jpg", toolbar=True)
mygrid.show()
