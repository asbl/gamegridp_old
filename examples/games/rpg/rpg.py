import gamegridp

class MyGrid(gamegridp.GUIGrid, gamegridp.CellGrid):
    """My Grid with custom setup method."""
    def setup(self):
        for i in range(self.rows):
            for j in range(self.columns):
                Grass(self,(j,i))

        Wall(self,(0,4))
        Wall(self, (1, 4))
        Wall(self, (2, 4))
        Wall(self, (3, 4))
        Wall(self, (4, 4))
        Wall(self, (5, 4))
        Wall(self, (6, 4))
        Wall(self, (6, 0))
        Wall(self, (6, 1))
        #Wall(self, (6, 2))
        Wall(self, (6, 3))
        Torch(self, (10, 8))
        Fireplace(self, (10, 14))
        Door(self, (6, 2))
        Player(self, (8, 2))
        self.play_music("rpgsounds/bensound-betterdays.mp3")
        self.run()

class Player(gamegridp.Actor):
    def setup(self):
        self._is_rotatable = False
        self.set_image("rpgimages/knight.png")
        self.inventory=[]

    def act(self):
        pass


    def listen(self, event, data):
        if event == "key_down":
            if "W" in data:
                self.move_up()
            elif "S" in data:
                self.move_down()
            elif "A" in data:
                self.move_left()
            elif "D" in data:
                self.move_right()
        # Wird auf den Button Torch gedrückt?
        elif event == "button" and data=="Fackel":
            fireplace = self.get_actor_at_location("Fireplace")
            if fireplace:
                self.grid.console.print("Du zündest die Feuerstelle an.")
                fireplace.burn()
        # wird eine Fackel gefunden?
        torch = self.get_actor_at_location("Torch")
        if torch:
            message = "Du findest eine Fackel. Möchtest du sie aufheben?"
            choices = ["Ja", "Nein"]
            reply = self.grid.button_box(message, choices)
            if reply == "Ja":
                self.inventory.append("Torch")
                torch.remove()
                self.grid.console.print("Du hebst die Fackel auf.")
                self.grid.toolbar.add_button("Fackel", "rpgimages/torch.png")
        # Prallt der Held auf eine Tür?
        door = self.get_actor_in_front("Door")
        if door:
            if door.closed:
                message = "Die Tür ist geschlossen... möchtest du sie öffnen"
                choices = ["Ja", "Nein"]
                reply = self.grid.button_box(message, choices)
                if reply == "Ja":
                    door.open()
                    self.grid.console.print("Du hast das Tor geöffnet.")

class Wall(gamegridp.Actor):
    def setup(self):
        self.is_blocking = True
        self.set_image("rpgimages/wall.png")

class Grass(gamegridp.Actor):
    def setup(self):
        self.set_image("rpgimages/grass.png")

class Torch(gamegridp.Actor):
    def setup(self):
        self.set_image("rpgimages/torch.png")

class Fireplace(gamegridp.Actor):
    def setup(self):
        self.set_image("rpgimages/fireplace_0.png")
        self.burning = False
        self.is_static = True

    def burn(self):
        if self.burning == False:
            self.delete_images()
            self.add_image("rpgimages/fireplace_1.png")
            self.add_image("rpgimages/fireplace_2.png")
            self.grid.play_sound("rpgsounds/fireplace.wav")
            self.animate()
            self.burning = True

class Door(gamegridp.Actor):
    def setup(self):
        self.set_image("rpgimages/door_closed.png")
        self.is_blocking = True
        self.closed = True
        self.is_static = True

    def open(self):
        if self.closed == True:
            self.set_image("rpgimages/door_open.png")
            self.grid.play_sound("rpgsounds/olddoor.wav")
            self.closed = False
            self.is_blocking = False


MyGrid.log()
mygrid = MyGrid("My Grid", cell_size=20, columns=30, rows=20,
                margin=1, toolbar=True, console = True, actionbar = False)
mygrid.show()
