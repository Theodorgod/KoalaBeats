import pygame as pg
from Buttons import Buttons
import random

# Class for changing the fonts of the text
# Author Theodor Fritsch
# Version: 2024-05-15

class Font(Buttons):
    def __init__(self) -> None:
        super().__init__(1200, 0, 80, 80, "assets/images/fontknapp.png")
        #self.img.set_colorkey((255, 255, 255))
        
        self.currentFont: str = "segoeuiblack"
        self.allFonts: list[str] = []

        self.file = open("assets/fonts.txt","r")
        while True:
            self.line = self.file.readline()
            if self.line == '':
                break
            self.list: list[str] = self.line.split(";")
            self.list.pop()
            for i in self.list:
                self.allFonts.append(i)
        
        self.file.close()

    def click(self, mouseX: int, mouseY: int) -> bool:
        if self.Xpos <= mouseX <= self.Xpos + self.Width:
            if self.Ypos <= mouseY <= self.Ypos + self.Height:
                self.fontIndex: int = random.randint(0, (len(self.allFonts) - 1))
                self.currentFont = self.allFonts[self.fontIndex]
                return True