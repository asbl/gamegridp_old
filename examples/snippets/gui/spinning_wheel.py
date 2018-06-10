import gamegridp
import random

class MyGrid(gamegridp.GUIGrid):
    """My Grid with custom setup method."""
    def setup(self):
        self.toolbar.add_button("Spin")
        self.arrow=Arrow(grid=self, location=(1,1))
        self.chip=None
        self.placed = False
        self.set_image("images/greenfield.jpg")
        self.run()

    def listen(self, event, data):
        if event=="button":
            if data=="Spin":
                self.arrow.spin()
        if event=="mouse_left" and self.placed == False:
            print(data)
            if not data == (1, 1):
                self.chip=Chip(grid=self, location=(data[0],data[1]))
                self.placed = True

class Arrow(gamegridp.Actor):
    def setup(self):
        self.is_rotatable = True
        self.spinning = 0
        self.is_rotatable = True
        self.set_image("images/arrow.png")

    def act(self):
        if self.spinning > 0:
            self.turn_left((self.spinning/800)*20)
            self.spinning = self.spinning - 1
            if self.spinning == 0:
                if self.get_actor_in_front("Chip"):
                    print(self.get_actor_in_front("Chip"))
                    self.grid.message_box("Du hast gewonnen")
                else:
                    self.grid.message_box("Du hast verloren")
                if self.grid.chip:
                    self.grid.chip.remove()
                    self.placed=False


    def spin(self):
        self.spinning=random.randint(600,800)
        self.grid.places = False

class Chip(gamegridp.Actor):
    def setup(self):
        self.set_image("images/chip.png")

MyGrid.log()
mygrid = MyGrid("My Grid",    cell_size=100, columns=3, rows=3, margin=1,toolbar=True,actionbar=False)
mygrid.show()