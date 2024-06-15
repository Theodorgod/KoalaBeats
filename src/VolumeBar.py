import pygame as pg
from Buttons import Buttons
import VolumeBar as VolumeBar

# Classes for the volume button and volume bar
# Author Theodor Fritsch, Linus Rackner
# Version 24-04-24

class VolumeButton(Buttons):
    def __init__(self) -> None:
        super().__init__(700, 610, 40, 40, "assets/images/soundbutton.png")
        self.extended: bool = False

    #extends the volumebar
    def click(self, mouseX: int, mouseY: int) -> None:
            if self.Xpos <= mouseX <= self.Xpos + self.Width:
                if self.Ypos <= mouseY <= self.Ypos + self.Height:
                     self.extended = not self.extended

    #allows to mute the volume (defined in main class to be m button)
    def mute(self,  volumeBar: VolumeBar) -> None:
        if pg.mixer.music.get_volume() == 0:
            pg.mixer.music.set_volume(volumeBar.volume)
            self.img = pg.image.load("assets/images/soundbutton.png")
            self.img = pg.transform.scale(self.img, (self.Width, self.Height))
        else:
            pg.mixer.music.set_volume(0)
            self.img = pg.image.load("assets/images/mutebutton.png")
            self.img = pg.transform.scale(self.img, (self.Width, self.Height))



# Class for the volume slider on interface which allows the user to modifiy the volume in the app
# Author Theodor Fritsch, Linus Rackner
# Version 24-04-24

class VolumeBar():
    def __init__(self, scrHeight: int) -> None:
        self.width: int = 10
        self.height: int = scrHeight / 5

        self.x: int = 940
        self.y: int = 365

        self.volume: float = pg.mixer.music.get_volume() # inital volume
        self.muted: bool = False

        self.sliderRadius: int = self.width

        self.bgColor: pg.Color = pg.Color("cadetblue2")
        self.fillColor: pg.Color = pg.Color("cadetblue4")
        self.sliderColor: pg.Color = pg.Color("black")

    
    def draw(self, surf: pg.Surface, volumeButton: VolumeButton) -> None:
        if volumeButton.extended == True:
            pg.draw.rect(surf, self.bgColor, (self.x, self.y, self.width, self.height))
            pg.draw.rect(surf, self.fillColor, (self.x, self.y + self.height -(self.volume * self.height), self.width, self.volume * self.height))
            pg.draw.circle(surf, self.sliderColor, (self.x + self.width/2, self.y + self.height -(self.volume * self.height)), self.sliderRadius)

    #changes the volume by clicking on the bar
    def click(self, mouseX: int, mouseY: int, volumeButton: VolumeButton) -> None:
        if volumeButton.extended:
            if self.x <= mouseX <= self.x + self.width:
                if self.y <= mouseY <= self.y + self.height:
                    pos: float = (self.y + self.height - mouseY)/(self.height)
                    pg.mixer.music.set_volume(pos)
                    self.volume = pos
                    volumeButton.img = pg.image.load("assets/images/soundbutton.png")
                    volumeButton.img = pg.transform.scale(volumeButton.img, (volumeButton.Width, volumeButton.Height))