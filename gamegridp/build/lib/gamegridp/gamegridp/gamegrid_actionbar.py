import os

import pygame


class Actionbar(object):
    def __init__(self, grid):
        self.grid = grid
        self.height = 30
        self.posy = 0

    def set_width(self, width):
        self.width = width

    def set_posy(self, posy):
        self.posy = posy

    def draw(self):
        """
                Draws the action bar
                """
        package_directory = os.path.dirname(os.path.abspath(__file__))
        myfont = pygame.font.SysFont("monospace", 15)
        actionbar = pygame.Surface((self.width, 30))
        actionbar.fill((255, 255, 255))
        # Act Button:
        path = os.path.join(package_directory, "data", 'play.png')
        image = pygame.image.load(path)
        image = pygame.transform.scale(image, (20, 20))
        actionbar.blit(image, (5, 5))
        label = myfont.render("Act", 1, (0, 0, 0))
        actionbar.blit(label, (30, 5))
        # Run Button:
        if not self.grid.is_running:
            path = os.path.join(package_directory, "data", 'run.png')
            image = pygame.image.load(path)
            image = pygame.transform.scale(image, (20, 20))
            actionbar.blit(image, (60, 5))
            label = myfont.render("Run", 1, (0, 0, 0))
            actionbar.blit(label, (85, 5))
        if self.grid.is_running:
            path = os.path.join(package_directory, "data", 'pause.png')
            image = pygame.image.load(path)
            image = pygame.transform.scale(image, (20, 20))
            actionbar.blit(image, (60, 5))
            label = myfont.render("Pause", 1, (0, 0, 0))
            actionbar.blit(label, (85, 5))
        # Reset Button:
        path = os.path.join(package_directory, "data", 'reset.png')
        image = pygame.image.load(path)
        image = pygame.transform.scale(image, (20, 20))
        actionbar.blit(image, (140, 5))
        label = myfont.render("Reset", 1, (0, 0, 0))
        actionbar.blit(label, (165, 5))
        # Info-Button
        path = os.path.join(package_directory, "data", 'question.png')
        image = pygame.image.load(path)
        image = pygame.transform.scale(image, (20, 20))
        actionbar.blit(image, (225, 5))
        label = myfont.render("Info", 1, (0, 0, 0))
        actionbar.blit(label, (245, 5))
        # Info-Button
        path = os.path.join(package_directory, "data", 'left.png')
        image = pygame.image.load(path)
        image = pygame.transform.scale(image, (20, 20))
        actionbar.blit(image, (285, 5))
        label = myfont.render("Speed:" + str(self.grid.speed), 1, (0, 0, 0))
        actionbar.blit(label, (305, 5))
        path = os.path.join(package_directory, "data", 'right.png')
        image = pygame.image.load(path)
        image = pygame.transform.scale(image, (20, 20))
        actionbar.blit(image, (380, 5))
        pygame.screen.blit(actionbar, (0, self.posy, self.width, self.height))
