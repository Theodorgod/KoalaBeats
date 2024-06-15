import pygame as pg
from Buttons import Buttons
from MusicPlayer import MusicPlayer
from ProgressBar import ProgressBar

# Class for the buttons which plays and pauses the music
# Autor Linus Racker, Theodor Fritsch
# Version 23-04-2024

class Playback(Buttons):
    def __init__ (self) -> None:
        super().__init__(600, 600, 60, 60, "assets/images/pausebutton.png")#initiates a button from the buttons class

    # plays music, continues it and pauses it
    def activatePlayback(self, musicPlayer: MusicPlayer, progressBar: ProgressBar) -> None:
        if pg.mixer.music.get_busy(): #if music is aleady playing
            self.img = pg.image.load("assets/images/pausebutton.png")
            self.img = pg.transform.scale(self.img, (60, 60))
            musicPlayer.pause()
        
        else: #if music is currently not playing
            self.img = pg.image.load("assets/images/playbutton.png")
            self.img = pg.transform.scale(self.img, (60, 60))
            musicPlayer.play(progressBar)
        
    def click(self, mouseX: int, mouseY: int, progressBar: ProgressBar, musicPlayer: MusicPlayer) -> None:
        if self.Xpos <= mouseX <= self.Xpos + self.Width:
            if self.Ypos <= mouseY <= self.Ypos + self.Height:
                self.activatePlayback(musicPlayer, progressBar)