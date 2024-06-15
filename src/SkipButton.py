import pygame as pg
from Buttons import Buttons
from MusicPlayer import MusicPlayer
from ProgressBar import ProgressBar
from Playback import Playback

# Class for the buttons to skip and reset song on ui
# Author Linus Rackner, Theodor Fritsch
# Version 2024-05-25
class SkipButton(Buttons):
    # button that skipps current song
    def __init__(self) -> None:
        super().__init__(660, 610, 40, 40, "assets/images/forwardbutton.png")
    
    def click(self, mouseX: int, mouseY: int, mode: str, progressBar: ProgressBar, musicPlayer: MusicPlayer, playbackbutt: Playback) -> None:
        if self.Xpos <= mouseX <= self.Xpos + self.Width:
            if self.Ypos <= mouseY <= self.Ypos + self.Height:
                musicPlayer.next(mode, progressBar)
                playbackbutt.img = pg.image.load("assets/images/playbutton.png")
                playbackbutt.img = pg.transform.scale(playbackbutt.img, (60, 60))


class ReverseButton(Buttons):
    # button that restarts the song or goes back a song
    def __init__(self) -> None:
        super().__init__(560, 610, 40, 40, "assets/images/backbutton.png")

    def click(self,  mouseX: int, mouseY: int, progressBar: ProgressBar, musicPlayer: MusicPlayer, playbackbutt: Playback) -> None:
        if self.Xpos <= mouseX <= self.Xpos + self.Width:
            if self.Ypos <= mouseY <= self.Ypos + self.Height:
                musicPlayer.back(progressBar)
                musicPlayer.realSongPos = 0
                playbackbutt.img = pg.image.load("assets/images/playbutton.png")
                playbackbutt.img = pg.transform.scale(playbackbutt.img, (60,60))