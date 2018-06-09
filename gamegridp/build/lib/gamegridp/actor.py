# -*- coding: utf-8 -*-
"""
Created on Mon Apr 16 21:50:48 2018

@author: asieb
"""

import logging
import math
import cProfile
import pygame


class Actor(pygame.sprite.Sprite):
    """ Ein Actor ist eine Spielfigur oder ein Objekt in der Welt,
            z.B. ein Auto, eine Wand, ein Untergrund.


        Attributes
        ----------
        grid: Grid
            Das Spielfeld in dem der Actor sich befindet.
        color: (r,g,b)
            Die Farbe des Actors (falls dieser über k
            ein Hintergrundbild verfügt.
        title: str
            Der Name des Actors
        size: (x,y):
            Die größe des Actors in Pixeln (x und y)
        direction: int
            Die Richtung als int-Wert zwischen 0° und 360°
            0° bezeichnet dabei einen Blick nach rechts und der Winkel verläuft
            gegen den Uhrzeigersinn.
        is_blocking: bool
            Legt fest, ob der Akteur das Feld für andere Akteure blockiert. Wenn die Variable wahr ist,
            ist es nicht möglich sich über das Feld des Akteurs zu bewegen.
        image_rect: Rect
            Das Rechteck (Rectangle), welches das Objekt umschließt.
        is_rotatable: bool
            Wahr, wenn sich das Bild mit der Richtung mitdrehen soll.
        class_name
            Der Typ des Akteurs - entspricht dem Klassennamen.
        actor_id
            Jeder Akteur hat eine eindeutige ID.

        Methoden
        --------
        """

    # Konstruktor
    def __init__(self, grid, location: tuple = (0, 0), color: tuple = (0, 0, 255), title: str = "Actor",
                 img_path: str = None, size: tuple = (40, 40), img_action: str = None):
        pygame.sprite.Sprite.__init__(self)
        # define instance variables
        self.title = title
        self._actor_id = 0
        self._logging = logging.getLogger('Actor:')
        # Define instance variables
        self._original_images = []  # All images stores for actor
        self._image = None
        self._is_static = False
        self._image_index = 0
        self._is_rotatable = False
        self._is_flipped = False
        self.__grid__ = grid
        self._location = location
        self._direction = 0
        self.color = color
        self.size = size
        self.animation_speed = self.grid.speed/2
        self._animated = False
        self._is_blocking = False
        self._collision_partners = pygame.sprite.Group()
        # Set Actor image
        self._logging.debug("actor.__init__() : Target-Location:" + str(self.location))
        self._has_image = False
        # Add image to actor
        if img_path is not None:
            self.add_image(img_path, img_action, size)
        else:
            self.delete_images()
        self._logging.debug(
            "actor.__init__() : Actor: " + str(title) + "'s setup wurde ausgeführt" + str(self._is_rotatable))
        # Add actor to grid
        grid.add_actor(self, location)
        # set the bounding-box style (cell for cell-based games, image for pixel-based games
        if self.grid.cell_size == 1:
            self._bounding_box_type = "image"
        else:
            self._bounding_box_type = "cell"
        self.__bounding_box_size__ = None
        self.setup()
        self._logging.debug("actor.__init__() : Actor " + str(title) + " wurde initialisiert")

    # Properties
    @property
    def is_blocking(self):
        """bool: Legt fest, ob der Akteur das Feld "blockt", d.h. für
        andere Akteure unpassierbar macht.
        """
        return self._is_blocking

    @is_blocking.setter
    def is_blocking(self, value: bool):
        self._is_blocking = value

    @property
    def direction(self) -> int:
        """int: Legt die Richtung fest, in die der Akteur "schaut"
            0° bezeichnet dabei nach Osten, andere Winkel werden gegen den Uhrzeigersinn angegeben.
            Die Direction kann alternativ auch als String ("left", "right", "top", "bottom"  festgelegt werden.
        """
        return self._direction

    @property
    def is_static(self):
        return self._is_static

    @is_static.setter
    def is_static(self, value: bool):
        self._is_static = True
        self.grid.update_actor(self, "is_static", value)

    @direction.setter
    def direction(self, value: int):
        if value == "right":
            value = 0
        if value == "left":
            value = 180
        if value == "up":
            value = 90
        if value == "down":
            value = 270
        self._logging.debug(
            "actor.rotation() : rotated by " + str(value) + " degrees. Is rotatable?: " + str(self._is_rotatable))
        self.__rotate__(value)
        self._direction = value
        # if value < 0:
        #    self.direction = 360 + value
        # if value > 360:
        self._direction = value % 360

    @property
    def image_rect(self):
        """
            :return: The surrounding Rectangle used for redrawing and image manipulation
        """
        try:
            left, top = self.__get_image_coordinates_in_pixels__()
            width = self._image.get_width()
            height = self._image.get_height()
        except AttributeError:
            left, top, width, height = 0, 0, 0, 0
        return pygame.Rect(left, top, width, height)


    @property
    def image(self):
        """
        Gets the actual image of the actor.
        """
        return self._image

    @image.setter
    def image(self, value: str):
        """
        sets the actual image
        :param value: the path to the image
        """
        self._image = value

    @property
    def is_rotatable(self):
        """
        : return true if actor-image is rotatable, else false
         """
        return self._is_rotatable

    @is_rotatable.setter
    def is_rotatable(self, value: bool):
        """
        sets the actual image
        :param value: the path to the image
        """
        self._is_rotatable = value

    @property
    def grid(self):
        return self.__grid__

    @property
    def location(self) -> tuple:
        """
        returns the location of object
        """
        return self._location

    @location.setter
    def location(self, value: tuple):
        """
        Sets the location
        :type value: tuple with x and y-coordinate
        """
        self._logging.debug("actor.location: Location set")
        self.__grid__.repaint_area(pygame.Rect(self.image_rect))
        self._location = value
        self.__grid__.repaint_area(pygame.Rect(self.image_rect))
        self.__grid__.__update__(no_logic=True)

    @property
    def has_image(self):
        """
        Checks if actor has an image
        :return: true if actor has an image, else false
        """
        return self._has_image

    @has_image.setter
    def has_image(self, value):
        self._has_image = value

    @property
    def class_name(self) -> str:
        return self.__class__.__name__

    @property
    def actor_id(self) -> int:
        return self._actor_id

    @actor_id.setter
    def actor_id(self, value:int):
        self._actor_id = value

    @property
    def rect(self,):
        """
        Gibt die umgebene Bounding-Box um den Akteur zurück.

        :return: Die umgebende Bounding-Box.
        """
        if self._bounding_box_type == "image":
            rect = self.__image_rect__()
            return rect
        else:
            return self.__cell_rect__()

    # Methoden
    def act(self):
        """
        Überschreibe diese Methode in deinen eigenen Actor-Klassen
        """
        pass

    def set_image(self, img_path: str, img_action: str = None, size=None):
        """

        Fügt ein einzelnes Bild zu einem Actor hinzu.

        :param img_path: Der Pfad des Bildes relativ zum eigenen Dateipfad.
        :param img_action: Die Aktion die durchgeführt werden soll: *scale*, *crop*, *do_nothing*
        :param size: scale/crop : Die Größe des veränderten Bildes as 2-Tupel
        """

        if self.has_image:
            self.delete_images()
        self.add_image(img_path, img_action, size)

    def add_image(self, img_path: str, img_action: str = None, size=None):
        """
        Ergänzt ein einzelnes Bild zu einem Actor. Auf diese Weise können mehrere Bilder hinzugefügt werden.
        Die Animation kann dann mit *animate()* gestartet werdeb

        :param img_path: Der Pfad des Bildes relativ zum eigenen Dateipfad.
        :param img_action: Die Aktion die durchgeführt werden soll: *scale*, *crop*, *do_nothing*
        :param size: scale/crop : Die Größe des veränderten Bildes as 2-Tupel
        """
        self._logging.info("add_image(): Start add image")
        self.__grid__.repaint_area(pygame.Rect(self.image_rect))
        if img_action is None and self.grid.cell_size == 1:
            img_action = "do_nothing"
        if img_action is None and self.grid.cell_size > 1:
            img_action = "scale"
        self._logging.info(
            "img_action:" + str(img_action))
        if not self.has_image:
            self._original_images = []
            self._logging.info("add_image(): list was cleared:" + str(self._original_images.__len__()))
        self._logging.info("add_image(): Has image:" + str(self.has_image))
        if img_path in self.grid.images_dict:
            _image = self.grid.images_dict[img_path]
        else :
            _image = pygame.image.load(img_path).convert_alpha()
            self.grid.images_dict[img_path] = _image
        self._original_images.append(_image)
        self._logging.info("actor.add_image() : Number of Actor images:" + str(self._original_images.__len__()))
        self.__image_transform__(-1, img_action, size)
        self.image = self._original_images[0]  # overwrite image
        self.__grid__.repaint_area(pygame.Rect(self.image_rect))
        self.has_image = True

    def delete_images(self):
        """
        Löscht alle Bilder eines Akteurs. Dies kann z.B. sinnvoll sein,
        wenn eine neue Animation festgelegt werden soll und dafür die alte
        Animation zuvor gelöscht werden muss.
        """
        self._original_images = []
        self._image = pygame.Surface(self.size)
        self._image.fill(self.color)
        self._original_images.append(self._image)
        self.has_image = False

    def animate(self):
        """
        Startet eine Animation.
        """
        if not self._animated:
            self._animated = True

    def add_collision_partner(self, partner):
        """
        .. deprecated:: 0.4.0
          `add_collision_partner` wird in GameGrid 0.6 ersetzt werden.
        """
        self._collision_partners.add(partner)

    def stop(self):
        """
        Stopt die Animation eines Akteurs.
        """
        self._animated = False

    def _next_sprite(self):
        """
        Läd das nächste Sprite in einer Animation.
        """
        if self._animated:
            if self.grid.frame % self.animation_speed == 0:
                # every n-th frame (n: animation speed) do:
                self.grid.repaint_area(pygame.Rect(self.image_rect))
                if self._image_index < self._original_images.__len__() - 1:
                    self._image_index = self._image_index + 1
                else:
                    self._image_index = 0
                self.image = self._original_images[self._image_index]
                self.draw()
                self.grid.repaint_area(pygame.Rect(self.image_rect))
                self._logging.info("actor.image_next() : Image Index:" + str(self._image_index) + "/" + str(
                self._original_images.__len__() - 1))


    def __rotate__(self, direction: int):
        """
        rotates the actor by _direction_ degrees

        :param direction:
        """
        if self.is_rotatable:
            self.__grid__.repaint_area(pygame.Rect(self.image_rect))
            # rotate the original image to new direction
            self._logging.debug("actor.__rotate: rotate Image" + str(dir(self._original_images)) + ", Image: " + str(
                self._image) + "Index:" + str(self._image_index))
            self.image = pygame.transform.rotate(self._original_images[self._image_index], direction)
            self.__grid__.repaint_area(pygame.Rect(self.image_rect))

    def is_in_grid(self, target: tuple = None) -> bool:
        """
        Überprüft ob ein Akteur (bzw. eine gegebene Zellen-Koordinate im Grid ist.

        :param target Überprüft eine beliebige Zellen-Koordinate, ob diese in Grid liegt
        (Falls kein Ziel angegeben ist, wird die Zellen-Koordinate des Akteurs selbst verwendet)
        """
        if target == None:
            target = self.location
        if self.grid.is_location_in_grid(target):
            return True
        return False

    def is_at_border(self) -> str:
        """
        Überprüft, ob der Akteur an der Grenze zum Rand ist.

        :return: Die zugehörige Grenze als String ("left", "right", "top" oder "bottom")
        """
        if self.is_at_left_border():
            return "left"
        elif self.is_at_right_border():
            return "right"
        elif self.is_at_bottom_border():
            return "bottom"
        elif self.is_at_top_border():
            return "top"
        else:
            return False

    def is_at_left_border(self) -> bool:
        """
        Überprüft, ob der Akteur an der Grenze zum linken Rand ist.

        :return: True oder False
        """
        if self.grid.is_at_left_border(self.rect):
            return True
        else:
            return False

    def is_at_bottom_border(self) -> bool:
        """
        Überprüft, ob der Akteur an der Grenze zum unteren Rand ist.

        :return: True oder False
        """
        if self.grid.is_at_bottom_border(self.rect):
            return True
        else:
            return False

    def is_at_right_border(self) -> bool:
        """
        Überprüft, ob der Akteur an der Grenze zum rechten Rand ist.

        :return: True oder False
        """
        if self.grid.is_at_right_border(self.rect):
            return True
        else:
            return False

    def is_at_top_border(self) -> bool:
        """
        Überprüft, ob der Akteur an der Grenze zum oberen Rand ist.

        :return: True oder False
        """
        if self.grid.is_at_top_border(self.rect):
            return True
        else:
            return False

    def bounding_box_is_in_grid(self, target: tuple = None) -> bool:
        """
        Überprüft, ob die Bounding-Box eines Akteurs (komplett) im Grid ist.

        :return: True oder False
        """
        if target == None:
            box = self.rect
        else:
            box = self.rect(target)
        if self.grid.is_rectangle_in_grid(box):
            return True
        else:
            return False

    def get_bounding_box_collision(self, actor, class_name : str = None):
        self.grid.get_all_collisions_for_actor(actor, class_name)

    def get_all_bounding_box_collisions(self, actor, class_name : str = None):
        self.grid.get_all_bounding_box_collisions(actor, class_name)

    def flip_x(self):
        """
        Spiegelt das Bild des Akteurs über die y-Achse.
        Der Akteur selbst wird dabei um 180° gedreht.
        """
        if not self._is_flipped:
            self._is_flipped = True
        else:
            self._is_flipped = False
        self.__flip_x__()
        self.turn_left(180)

    def __flip_x__(self):
        """
        Flipped das Element in x-Richtung
        """
        try:
            if not self._is_flipped:
                self.__grid__.repaint_area(pygame.Rect(self.image_rect))
                self._logging.debug(
                    "actor.flip_x() : Flipping " + self.title + " image number " + str(self._image_index))
                self.image = pygame.transform.flip(self._original_images[self._image_index], False, False)
                self.__grid__.repaint_area(pygame.Rect(self.image_rect))
            else:
                self.__grid__.repaint_area(pygame.Rect(self.image_rect))
                self.image = pygame.transform.flip(self._original_images[self._image_index], True, False)
                self.__grid__.repaint_area(pygame.Rect(self.image_rect))
        except IndexError:
            self._logging.warning("actor.flip_x : Index Error in __flip_x__() in: Image Index is out of bounds")


    def set_rotatable(self):
        """
        DEPRECATED / VERALTET Achtung: Verwende stattdessen das Attribut: is_rotatable
        """
        self._is_rotatable = True

    def set_text(self, text, size):
        myfont = pygame.font.SysFont("monospace", size)
        label = myfont.render(text, 1, (0, 0, 0))
        self.image.blit(label, (0, 0))
        self._original_images[0] = self._image
        self.__grid__.repaint_area(pygame.Rect(self.image_rect))

    def get_all_actors_at_location(self, class_name, location=None) -> list:
        """
        Gibt *alle* Akteure einer bestimmten Klasse an der selben Position
        wie der aktuelle Akteur zurück
        (Alternativ kann auch eine beliebige Position abgefragt werden).

        :param class_name: Der Klassenname nachdem gesucht werden soll als String
            (z.B. alle Akteure vom Typ "Wall").
        :param location: Optional kann eine andere Zellen-Koordinate als
            Tupel (x,y) angegeben werden.
        :return: Eine Liste aller Akteure vom angegebenen Typ
        """
        if location == None:
            location = self.location
        actors = self.grid.get_all_actors_at_location(location, class_name)
        if self in actors:
            actors.remove(self)
        return actors

    def get_actor_at_location(self, class_name, location=None) -> list:
        """
        Gibt *einen* Akteur  an der Position zurück.

        :param class_name: Der Klassenname nachdem gesucht werden soll als String
            (z.B. alle Akteure vom Typ "Wall").
        :param location: Optional kann eine andere Zellen-Koordinate als
            Tupel (x,y) angegeben werden.
        :return: Der erste Akteur vom angegegebenen Typ.
        """
        if location == None:
            location = self.location
        actors_at_location = self.get_all_actors_at_location(class_name, location)
        if actors_at_location:
            return actors_at_location[0]
        else:
            return None

    def get_actor_in_front(self, class_name, distance=1) -> list:
        """
        Gibt einen Akteur in x-Feldern Entfernung vor dem aktuellen Akteur zurück.
        (Alternativ kann auch eine beliebige Position abgefragt werden).

        :param class_name: Der Klassenname nachdem gesucht werden soll als String
            (z.B. alle Akteure vom Typ "Wall").
        :param distance: Anzahl an Feldern, die nach vorne geschaut werden soll.
        :return: Eine Liste aller Akteure vom angegebenen Typ
        """
        location = self.look_forward(distance)
        actors_at_location = self.get_all_actors_at_location(class_name, location)
        if actors_at_location:
            return actors_at_location[0]




    def __image_transform__(self, index: int, img_action: str, size: str = None):
        """
        Should be called before main-loop
        :param size: img_acton : "scale" -> data : location
        """
        img_action = str.lower(img_action)
        cell_size = self.grid.cell_size
        if img_action == "scale":
            if size is None:
                size = (cell_size, cell_size)
            self._original_images[index] = pygame.transform.scale(self._original_images[index],
                                                                  (size[0], size[1]))
        elif img_action == "center":
            cropped_surface = pygame.Surface((cell_size, cell_size), pygame.SRCALPHA, 32)
            width = self._original_images[self._image_index].get_width()
            height = self._original_images[self._image_index].get_height()
            x_pos = (self.grid.cell_size - width) / 2
            y_pos = (self.grid.cell_size - height) / 2
            cropped_surface.blit(self._original_images[self._image_index], (x_pos, y_pos),
                                 (0, 0, cell_size, cell_size))
            self._original_images[self._image_index] = cropped_surface
        elif img_action == "do_nothing":
            self._original_images[self._image_index] = self._original_images[self._image_index]



    def __image_rect__(self, location=None):
        """
        the image rect when drawn to another location
        """
        if location == None:
            location = self.location
        try:
            width = self._image.get_width()
            height = self._image.get_height()
            left, top = self.__get_image_coordinates_in_pixels__(location)
        except AttributeError:
            left, top, width, height = 0, 0, 0, 0
        return pygame.Rect(left, top, width, height)

    def __cell_rect__(self, location: tuple = None):
        if location == None:
            location = self.location
        return self.grid.cell_rect(location)

    def set_bounding_box_size(self, value):
        """
        Legt die Größe der umgebenen Bounding-Box fest.

        :param value: Eine Größe (width, height) als Tupel.
        """
        self.__bounding_box_size__ = value

    def __get_image_coordinates_in_pixels__(self, location: tuple = None):
        """
        Gibt die Bildkoordinaten der oberen linken Recke des Akteur-Bildes zurück.

        :return: Tupel (x,y) mit Pixelkoordinaten der linken oberen Ecke
        """
        if location == None:
            column = self.location[0]
            row = self.location[1]
        else:
            column = location[0]
            row = location[1]
        cell_margin = self.__grid__.cell_margin
        cell_size = self.__grid__.cell_size
        if self._image.get_width() > cell_size:
            overlapping_x = (self._image.get_width() - cell_size) / 2
        else:
            overlapping_x = 0

        if self._image.get_height() > cell_size:
            overlapping_y = (self._image.get_height() - cell_size) / 2
        else:
            overlapping_y = 0

        cell_left = cell_margin + (cell_margin + cell_size) * column - overlapping_x
        cell_top = cell_margin + (cell_margin + cell_size) * row - overlapping_y
        return cell_left, cell_top

    def get_neighbour_cells(self) -> list:
        """
        Gibt alle 8 umgebenen Zellen zurück.

        :return: Alle Nachbarzellen als Liste.
        """
        locations = []
        y_pos = self.location[0]
        x_pos = self.location[1]
        locations.append([x_pos + 1, y_pos])
        locations.append([x_pos + 1, y_pos + 1])
        locations.append([x_pos, y_pos + 1])
        locations.append([x_pos - 1, y_pos + 1])
        locations.append([x_pos - 1, y_pos])
        locations.append([x_pos - 1, y_pos - 1])
        locations.append([x_pos, y_pos - 1])
        locations.append([x_pos + 1, y_pos - 1])
        return locations

    def listen(self, key, data):
        """
        Diese Methode sollte in deiner Kind-Klasse überschrieben werden.
        """
        pass

    def get_location(self) -> tuple:
        """
        Gibt die aktuelle Position des Akteurs zurück

        :return: the location as tuple
        """
        return self.location



    def set_x(self, x):
        """
        Setzt die x-Koordinate der Akteurs.
        :param x: Die x-Koordinate die gesetzt werden soll.
        """
        self.location = (x, self.location[1])

    def set_y(self, y):
        """
        Setzt die y-Koordinate der Akteurs.
        :param y: Die y-Koordinate die gesetzt werden soll.
        """

        self.location = (self.location[0], y)

    def get_x(self):
        """
        Gibt die x-Koordinate des Akteuers zurück.

        :param x: Gibt die x-Koordinate des Akteurs zurück.
        """
        return self.location[0]

    def get_y(self):
        """
        Gibt die y-Koordinate des Akteuers zurück.

        :param y: Gibt die y-Koordinate des Akteurs zurück
        """
        return self.location[1]

    def setup(self):
        """
        Sollte in deiner Kind-Klasse überschrieben werden.
        """
        pass

    def turn_left(self, degrees: int = 90):
        """
        Dreht den Akteur um degrees Grad nach links.

        :param degrees: Die Gradzahl um die der Akteur gedreht wird.

        :return: Die neue Richtung in Grad.
        """
        direction = self.direction + degrees
        self.direction = direction
        self._logging.debug("Richtung:" + str(self.direction))
        return self.direction

    def turn_right(self, degrees: int = 90):
        """
        Dreht den Akteur um degrees Grad nach links.

        :param degrees: Die Gradzahl um die der Akteur gedreht wird.

        :return: Die neue Richtung in Grad.
        """
        direction = self.direction - degrees
        self.direction = direction
        self._logging.debug("Richtung:" + str(self.direction))
        return self.direction

    def move(self, distance: int = 1, move: bool = True):
        """
        Bewegt den Akteur **distance** Schritte vorwärts. Wenn der Zug nicht valide ist, wird er nicht durchgeführt.

        :param distance: Die Anzahl an Schritten die der Akteur vorgehen soll
        :param move: Wenn der Parameter False ist, wird nur überprüft, ob der Zug legal ist.

        :return: Ist der Zug ein valider Zug? True/False
        """
        target = self.look_forward(distance)
        self._logging.debug(
            "actor" + str(self) + ".move(): ...try to move from" + str(self.location) + " to target" + str(
                target) + " direction:" + str(self.direction))
        return self.move_to(target, move)

    def move_to(self, target: tuple, move: bool = True):
        """
        Bewegt den Akteur an die angegebene Position. Wenn der Zug nicht valide ist wird er nicht durchgeführt.

        :param target: Die Ziel Zellenkoordinaten
        :param move: Wenn der Parameter False ist, wird nur überprüft, ob der Zug legal ist.

        :return: Ist der Zug ein valider Zug? True/False
        """
        if self.is_valid_target(target):
            if move is True:
                self.location = target
            return True
        else:
            return False

    def move_back(self, distance: int = 1, move: bool = True):
        """
        Bewegt den Akteur **distance** Schritte rückwärts. Wenn der Zug nicht valide ist, wird er nicht durchgeführt.

        :param distance: Die Anzahl an Schritten die der Akteur vorgehen soll
        :param move: Wenn der Parameter False ist, wird nur überprüft, ob der Zug legal ist.

        :return: Ist der Zug ein valider Zug? True/False
        """
        target = self.look_back(distance)
        return self.move_to(target, move)

    def move_right(self, distance=1, move: bool = True):
        """
        Bewegt den Akteur **distance** Schritte nach rechts. Wenn der Zug nicht valide ist, wird er nicht durchgeführt.

        :param distance: Die Anzahl an Schritten die der Akteur vorgehen soll
        :param move: Wenn der Parameter False ist, wird nur überprüft, ob der Zug legal ist.

        :return: Ist der Zug ein valider Zug? True/False
        """
        self.direction = 0
        return self.move(distance, move)

    def move_left(self, distance=1, move: bool = True):
        """
        Bewegt den Akteur **distance** Schritte nach links. Wenn der Zug nicht valide ist, wird er nicht durchgeführt.

        :param distance: Die Anzahl an Schritten die der Akteur vorgehen soll
        :param move: Wenn der Parameter False ist, wird nur überprüft, ob der Zug legal ist.

        :return: Ist der Zug ein valider Zug? True/False
        """
        self.direction = 180
        self.move(distance, move)

    def move_down(self, distance=1, move: bool = True):
        """
        Bewegt den Akteur **distance** Schritte nach unten. Wenn der Zug nicht valide ist, wird er nicht durchgeführt.

        :param distance: Die Anzahl an Schritten die der Akteur vorgehen soll
        :param move: Wenn der Parameter False ist, wird nur überprüft, ob der Zug legal ist.

        :return: Ist der Zug ein valider Zug? True/False
        """
        self.direction = 270
        return self.move(distance, move)

    def move_up(self, distance=1, move: bool = True):
        """
        Bewegt den Akteur **distance** Schritte nach oben. Wenn der Zug nicht valide ist, wird er nicht durchgeführt.

        :param distance: Die Anzahl an Schritten die der Akteur vorgehen soll
        :param move: Wenn der Parameter False ist, wird nur überprüft, ob der Zug legal ist.

        :return: Ist der Zug ein valider Zug? True/False
        """
        self.direction = 90
        return self.move(distance, move)

    def look_forward(self, distance: int = 1) -> tuple:
        """
        Schaut *distance* Felder nach vorne und gibt die zugehörige Koordinate zurück.

        :param distance : Anzahl an Felder die voraus geschaut wird.

        :return location : Zellenkoordinate als Tuple (x,y)
        """
        self._logging.debug("actor.look_forward() : Location:" + str(self.location) + "Direction" + str(self.direction))
        loc_x = round(self.location[0] + math.cos(math.radians(self.direction)) * distance)
        loc_y = round(self.location[1] - math.sin(math.radians(self.direction)) * distance)
        return loc_x, loc_y

    def look_back(self, distance: int = 1) -> tuple:
        """
        Schaut *distance* Felder nach hinten und gibt die zugehörige Koordinate zurück.

        :param distance : Anzahl an Felder die voraus geschaut wird.

        :return location : Zellenkoordinate als Tuple (x,y)
        """
        self._logging.debug("actor.look_forward() : Location:" + str(self.location) + "Direction" + str(self.direction))
        loc_x = round(self.location[0] - math.cos(math.radians(self.direction)) * distance)
        loc_y = round(self.location[1] + math.sin(math.radians(self.direction)) * distance)
        return loc_x, loc_y

    def look_up(self, distance: int = 1) -> tuple:
        """
        Schaut *distance* Felder nach oben und gibt die zugehörige Koordinate zurück.

        :param distance : Anzahl an Felder die voraus geschaut wird.

        :return location : Zellenkoordinate als Tuple (x,y)
        """
        self._logging.debug("actor.look_forward() : Location:" + str(self.location) + "Direction" + str(self.direction))
        loc_x = self.location[0]
        loc_y = self.location[1] - distance
        return loc_x, loc_y

    def look_down(self, distance: int = 1) -> tuple:
        """
        Schaut *distance* Felder nach unten und gibt die zugehörige Koordinate zurück.

        :param distance : Anzahl an Felder die voraus geschaut wird.

        :return location : Zellenkoordinate als Tuple (x,y)
        """
        self._logging.debug("actor.look_forward() : Location:" + str(self.location) + "Direction" + str(self.direction))
        loc_x = self.location[0]
        loc_y = self.location[1] + distance
        return loc_x, loc_y

    def look_left(self, distance: int = 1) -> tuple:
        """
        Schaut *distance* Felder nach links und gibt die zugehörige Koordinate zurück.

        :param distance : Anzahl an Felder die voraus geschaut wird.

        :return location : Zellenkoordinate als Tuple (x,y)
        """
        self._logging.debug("actor.look_forward() : Location:" + str(self.location) + "Direction" + str(self.direction))
        loc_x = self.location[0] - distance
        loc_y = self.location[1]
        return loc_x, loc_y

    def look_right(self, distance: int = 1) -> tuple:
        """
        Schaut *distance* Felder nach rechts und gibt die zugehörige Koordinate zurück.

        :param distance : Anzahl an Felder die voraus geschaut wird.

        :return location : Zellenkoordinate als Tuple (x,y)
        """
        self._logging.debug("actor.look_forward() : Location:" + str(self.location) + "Direction" + str(self.direction))
        loc_x = self.location[0] + distance
        loc_y = self.location[1]
        return loc_x, loc_y

    def is_valid_move(self, move_func=None, distance=1):
        """
        Überprüft, ob ein Zug legal ist.

        :param move_func: Eine move-Funktion, z.B. move, move_back, move_left,...
        :param distance: Die Anzahl an Schritten, die der move-Funktion als Parameter übergeben werden sollen.

        :return: True falls Zug legal ist, ansonsten False.
        """
        if move_func == None:
            move_func = self.move
        return move_func(distance, False)

    def is_valid_target(self, target: tuple = None):
        """
        Gibt zurück, ob die angegebene Position einen legalen Zug erlaubt.

        :param target: Das zu überprüfende Ziel als (x,y)-Tupel
            Wenn kein Ziel angegeben wird, schaut der Akteur ein Feld nach vorne.

        :return True, falls Zug legal ist, ansonsten False
        """
        valid = False
        if target is None:
            target = self.look_forward()
        if self.is_in_grid(target):
            self._logging.debug("actor.is_valid_target() : target:" + str(target) + ",true")
            valid = True
        else:
            self._logging.debug("actor.is_valid_target() : target:" + str(target) + ",false")
            valid = False
        # check if target is not blocked
        actors_at_position = self.__grid__.get_all_actors_at_location(target)
        for actor in actors_at_position:
            if actor: #list is not none?
                if actor.is_blocking:
                    valid = False
        return valid



    def draw(self):
        """
        Zeichnet den Akteur auf das Spielfeld.
        """
        if self.has_image:
            cell_left, cell_top = self.__get_image_coordinates_in_pixels__()
            self.__flip_x__()
            self.__rotate__(self.direction)
            if self.grid._show_bounding_boxes:
                pygame.draw.rect(self._image, (255, 0, 0),
                                 (0, 0, self.rect.width, self.rect.height), 2)
            if self.grid._show_direction_marker:
                # self._logging.debug("actor.draw() - Draw line from"+str(self._image.get_rect().center)+" to "+str(self._image.get_rect().topleft))
                x = round(
                    self.rect.width / 2 + math.cos(math.radians(self.direction)) * self.rect.width)
                y = round(self.rect.height / 2 - math.sin(
                    math.radians(self.direction)) * self.rect.height)
                pygame.draw.line(self.image, (255, 0, 0), (self.rect.width / 2,
                                                           self.rect.height / 2), (x, y), 2)
            self.grid.grid_surface.blit(self._image, (cell_left, cell_top))

    def remove(self):
        """
        Entfernt den Akteur vom Grid.
        """
        self.grid.remove_actor(self)
        del (self)



