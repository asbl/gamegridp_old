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
    play= False

    def grid_pane_size_x(self):
        return self.grid_width * self.grid_x + (self.grid_x+2) * self.margin                                        

    def grid_pane_size_y(self):
        return self.grid_height * self.grid_y + (self.grid_y+2) * self.margin
        
    def draw_actionbar(self):
        """ 
        Draws the action bar
        """
        myfont = pygame.font.SysFont("monospace", 15)
        path=os.path.join(os.path.dirname(__file__), 'play.png')
        image = pygame.image.load(path)
        image = pygame.transform.scale(image, (20, 20))
        pygame.screen.blit(image,(5,(self.grid_pane_size_y()+5)))
        label = myfont.render("Act", 1, (0,0,0))
        pygame.screen.blit(label, (30, (self.grid_pane_size_y()+5)))
        path=os.path.join(os.path.dirname(__file__), 'run.png')
        image = pygame.image.load(path)
        image = pygame.transform.scale(image, (20, 20))
        pygame.screen.blit(image,(60,self.grid_pane_size_y()+5))
        label = myfont.render("Run", 1, (0,0,0))
        pygame.screen.blit(label, (85, (self.grid_pane_size_y()+5)))
        path=os.path.join(os.path.dirname(__file__), 'reset.png')
        image = pygame.image.load(path)
        image = pygame.transform.scale(image, (20, 20))
        pygame.screen.blit(image,(120,self.grid_pane_size_y()+5))
        label = myfont.render("Reset", 1, (0,0,0))
        pygame.screen.blit(label, (145, (self.grid_pane_size_y()+5)))
        
    def draw_grid(self, grid):
        """ 
        Draws grid with all actors in it.
        """
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
                

    def add_actor(self, actor):
        """ 
        Adds an actor to the grid. 
        The method is called when a new actor is created.
        """
        logging.info("Actor hinzugefügt: "+ actor.title)
        self.actors.append(actor)
        logging.info(self.actors)

    def get_actors_at_location(self, location):
        """ 
        Get all actors at a specific location
        """
        actors_at_location = []
        for actor in self.actors:
            if actor.get_location() == location:
                actors_at_location.append(actor)
        return actors_at_location
    
    def get_actors_at_location_by_class(self, location,class_name):
        """ 
        Geta all actors of a specific class at a specific location
        """
        actors_at_location = ()
        for actor in self.actors:
            if actor.get_location == location and actor.__class__.__name__ == class_name:
                actors_at_location.append(actor)
        return actors_at_location

    def __init__(self, title, grid_x, grid_y,
                 grid_width, grid_height, margin=0):
        """ 
        Initialises the grid
        """
        
        # Init model
        self.margin = margin
        self.grid_width = grid_width
        self.grid_height = grid_height
        self.grid_x = grid_x
        self.grid_y = grid_y
        for row in range(grid_x):
            self.grid.append([])
            for column in range(grid_y):
                self.grid[row].append(0)
        # Init gui
        x_res = self.grid_pane_size_x()
        y_res = self.grid_pane_size_y()+30
        
        WINDOW_SIZE = [x_res, y_res]
        pygame.screen = pygame.display.set_mode(WINDOW_SIZE)
        pygame.display.set_caption(title)
        pygame.init()
        
    def act(self, key, click_location):
        """ 
        Should be overwritten in sub-classes
        """
        pass

    def go(self):
        """
        Starts the mainloop        
        """
        clock = pygame.time.Clock()

        while not self.done:
            for event in pygame.event.get():  # User did something
                key=None
                click_loc=None
                if event.type == pygame.QUIT:  # If user clicked close
                    self.done = True
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    if pos[0] < self.grid_pane_size_x() and pos[1] < self.grid_pane_size_y():
                        column = pos[0] // (self.grid_width + self.grid_margin)
                        row = pos[1] // (self.grid_height + self.grid_margin)
                        click_loc=[column,row]
                        logging.info("Mouseclick at grid-position:"+str(click_loc))
                    elif pos[1] >= self.grid_pane_size_y() and pos[0] >5 and pos[0]<30:
                        self.play=False
                        logging.info("Act")
                        if self.play:
                            self.act(key,click_loc)
                            for actor in self.actors:
                                actor.act(key,click_loc)
                    elif pos[1] >= self.grid_pane_size_y() and pos[0] >60 and pos[0]<120:
                         if self.play==True:
                            self.play=False
                            logging.info("Stop")
                         else:
                             self.play=True
                             logging.info("Play")
                    elif pos[1] >= self.grid_pane_size_y() and pos[0] >120 and pos[0]<180:
                        self.play=False
                        logging.info("Reset")
                elif event.type ==pygame.KEYDOWN:
                    key=event.key
                    logging.info("key pressed")
            if self.play:
                self.act(key,click_loc)
                for actor in self.actors:
                    actor.act(key,click_loc)
            self.draw_grid(self.grid)
            self.draw_actionbar()
            clock.tick(5)
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
        grid.add_actor(self)
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
    gg.go()
   


if __name__ == "__main__":
    main()
