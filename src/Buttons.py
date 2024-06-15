import pygame as pg

# Class for buttons on UI, other classes inherit from this class to prevent duplicate code
# Authors: Linus Rackner, Theodor Fritsch
# Version: 2024-04-22

class Buttons :
    # values needed for the button
    def __init__ (self, Xpos: int, Ypos: int, Width: int, Height: int, imgSource: str) -> None:
        self.img: pg.image = pg.image.load(imgSource)
        self.img = pg.transform.scale(self.img, (Width, Height))
        self.img = self.img.convert_alpha()
        self.img.set_colorkey((0, 0, 0))
        self.Ypos: int = Ypos
        self.Xpos: int = Xpos
        self.Width: int = Width
        self.Height: int = Height

    def draw (self, surf: pg.Surface) -> None: # draws the button
        surf.blit(self.img, (self.Xpos, self.Ypos))