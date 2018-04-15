import pygame
import logging
import importlib
importlib.reload(logging)
import sys
import os
import math


class Gamegrid(object):
    grid = []
    actors = []
    done = False
    grid_width = 16
    grid_height = 16
    grid_x = 10
    grid_y = 10
    grid_margin = 0

    def grid_pane_size_x(self):
        return self.grid_width * self.grid_x + (self.grid_x+2) * self.margin                                        

    def grid_pane_size_y(self):
        return self.grid_height * self.grid_y + (self.grid_y+2) * self.margin
        
    def drawCommandos(self):
        path=os.path.join(os.path.dirname(__file__), 'play.png')
        image = pygame.image.load(path)
        image = pygame.transform.scale(image, (20, 20))
        pygame.screen.blit(image,(0,(self.grid_pane_size_y())))
        path=os.path.join(os.path.dirname(__file__), 'pause.png')
        image = pygame.image.load(path)
        image = pygame.transform.scale(image, (20, 20))
        pygame.screen.blit(image,(20,self.grid_pane_size_y()))
        
    def drawGrid(self, grid):
        pygame.screen.fill((255,255,255))
        # Draw the grid
        for row in range(self.grid_x):
            for column in range(self.grid_y):
                grid_location=[column,row]
                cell_left = (self.grid_margin + self.grid_width) * column
                cell_top = (self.grid_margin + self.grid_height) * row + self.grid_margin
                cell_width = self.grid_width
                cell_height = self.grid_height
                pygame.draw.rect(pygame.screen,(255,255,255),
                                [cell_left, cell_top,cell_height,cell_width])
                # Draw Actors at actual position
                actors_at_location = self.get_actors_at_location(grid_location)
                for actor in actors_at_location:
                    if actor.hasImage():
                        pygame.screen.blit(actor.image,(cell_left,cell_top))
                

    def addActor(self, actor):
        logging.info("Actor hinzugefügt: "+ actor.title)
        self.actors.append(actor)
        logging.info(self.actors)

    def get_actors_at_location(self, location):
        actors_at_location = []
        for actor in self.actors:
            if actor.get_location() == location:
                actors_at_location.append(actor)
        return actors_at_location
    
    def get_actors_at_location_by_class(self, location,class_name):
        actors_at_location = ()
        for actor in self.actors:
            if actor.get_location == location and actor.__class__.__name__ == class_name:
                actors_at_location.append(actor)
        return actors_at_location

    def __init__(self, title, grid_x, grid_y,
                 grid_width, grid_height, margin=0):
        self.margin = margin
        self.grid_width = grid_width
        self.grid_height = grid_height
        self.grid_x = grid_x
        self.grid_y = grid_y
        """
        Initialisiert das Programm
        """
        # Erstelle das Modell
        for row in range(grid_x):
            self.grid.append([])
            for column in range(grid_y):
                self.grid[row].append(0)
        # Erstelle die GUI
        x_res = self.grid_pane_size_x()
        y_res = self.grid_pane_size_y()+20

        WINDOW_SIZE = [x_res, y_res]
        pygame.screen = pygame.display.set_mode(WINDOW_SIZE)
        pygame.display.set_caption(title)
        
    def act(self, key, click_location):
        pass

    def go(self):
        """
        Startet die Mainloop
        """
        clock = pygame.time.Clock()

        while not self.done:
            for event in pygame.event.get():  # User did something
                key=None
                click_loc=None
                if event.type == pygame.QUIT:  # If user clicked close
                    self.done = True
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    if pos[0] < self.grid_pane_size_x() and pos[1] < self.grid_pane_size_y():
                        column = pos[0] // (self.grid_width + self.grid_margin)
                        row = pos[1] // (self.grid_height + self.grid_margin)
                        click_loc=[column,row]
                        logging.info("Mouseclick at grid-position:"+str(click_loc))
                    elif pos[0] >= self.grid_pane_size_x() and pos[1] < 20:
                        self.play=True
                        logging.info("Play")
                    else:
                        self.play=False
                        logging.info("Pause")
                if event.type ==pygame.KEYDOWN:
                    key=event.key
                    logging.info("key pressed")
                self.act(key,click_loc)
                for actor in self.actors:
                    actor.act(key,click_loc)
                self.drawGrid(self.grid)
                self.drawCommandos()
                clock.tick(60)
                pygame.display.flip()
        pygame.quit()


class Actor(object):
    title = ""
    location = [0, 0]
    direction = 0
    grid = None
    image=None
    img_path=None

    def __init__(self, title, x_pos, y_pos, grid):
        self.location=[x_pos,y_pos]
        self.title = title
        grid.addActor(self)
        self.grid = grid
        if self.img_path!= None:
            image = pygame.image.load(self.img_path)
            self.image = pygame.transform.scale(image, (grid.grid_width, grid.grid_height))
        logging.info("Target-Location:" + str(self.location))

        
        
    def act(self, key, click_location):
        pass

    def setX(self, x):
        self.location[0] = x

    def setY(self, y):
        self.location[1] = y

    def turn_left(self):
        if (self.direction < 270):
            self.direction = self.direction+90
        else:
            self.direction = 0
        logging.info("Richtung:"+str(self.direction))

    def turn_right(self):
        if (self.direction > 0):
            self.direction = self.direction-90
        else:
            self.direction = 270
        logging.info("Richtung:"+str(self.direction))

    def move_forward(self):
        target=self.get_target_location()
        if  (self.is_location_in_grid(target)):
            self.location = target
        logging.info("self"+str(self.location)+", target"+str(target))

    def move_up(self):
        self.direction=90
        self.move_forward()

    def move_right(self):
        self.direction=0
        self.move_forward()

    def move_left(self):
        self.direction=180
        self.move_forward()

    def move_down(self):
        self.direction=270
        self.move_forward()
        
    def get_target_location(self):
        loc_x=round(self.location[0]+math.cos(math.radians(self.direction)))
        loc_y=round(self.location[1]-math.sin(math.radians(self.direction)))
        return  [loc_x,loc_y]
        
    def is_location_in_grid(self,location):
        if location[0]>self.grid.grid_x-1:
            return False
        elif location[1]>self.grid.grid_y-1:
            return False
        elif location[0]<0 or location[1]<0:
            return False
        else :
            return True
        
    def get_location(self):
        return self.location

    def get_neighbours(self):
        locations = []
        y_pos = self.y_pos
        x_pos = self.x_pos
        locations.append([x_pos+1, y_pos])
        locations.append([x_pos+1, y_pos+1])
        locations.append([x_pos, y_pos+1])
        locations.append([x_pos-1, y_pos+1])
        locations.append([x_pos-1, y_pos])
        locations.append([x_pos-1, y_pos-1])
        locations.append([x_pos, y_pos-1])
        locations.append([x_pos+1, y_pos-1])
        return locations

    def hasImage(self):
        if self.image==None:
            return False
        else:
            return True
        
    def mouse_pressed(self,location):
        pass

def main():
    logging.basicConfig(format="%(message)s",level=logging.DEBUG,stream=sys.stdout)
    gg = Gamegrid("First Game", 16, 16, 16, 16)
    gg.addActor(Actor("test", 4, 4, gg))
    gg.go()
   


if __name__ == "__main__":
    main()
