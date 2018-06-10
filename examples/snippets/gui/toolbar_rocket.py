import gamegridp

class MyGrid(gamegridp.GUIGrid):
    """My Grid with custom setup method."""
    def setup(self):
        self.toolbar.add_button("Start Rocket", "images/ship.png", color=(200,200,200), border=(50,50,50))
        self.rocket=Rocket(grid=self, location=(100,180))
        self.run()
        self.set_image("images/galaxy.jpg")

    def listen(self, event, data):
        if event=="button":
            if data=="Start Rocket":
                self.rocket.started = True


class Rocket(gamegridp.Actor):
    def setup(self):
        self.set_image("images/ship.png")
        self.started=False
        self.turn_left(90)

    def act(self):
        if self.started:
            self.move(1)
        if not self.is_valid_move():
            self.remove()


mygrid = MyGrid("My Grid",    cell_size=1, columns=200, rows=240, margin=0, toolbar=True, actionbar = False)
mygrid.show()
