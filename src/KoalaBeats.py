import pygame as pg
from MusicPlayer import MusicPlayer 
from Buttons import Buttons
from ProgressBar import ProgressBar
from Playback import Playback
from SkipButton import SkipButton, ReverseButton
from Dashboard import Dashboard
from VolumeBar import VolumeBar, VolumeButton
from Playlist import Playlist
from Font import Font

# Main class of the application
# Authors: Theodor Fritsch
# Version: 2024-04-22

class KoalaBeats:
    def __init__(self) -> None:

        # Initialize pygame and our window
        pg.mixer.pre_init(44100, -16, 2, 2048)
        pg.mixer.init()
        pg.init()

        icon: pg.Surface = pg.image.load("assets\images\Designer.jpeg")

        pg.display.set_icon(icon)
        self.win: pg.Surface = pg.display.set_mode((1280, 720))
        pg.display.set_caption("Koala Beats")

        self.running: bool = True
        self.clock: pg.time.Clock = pg.time.Clock()

        #initializing an object of each class we've created
        self.musicPlayer: MusicPlayer = MusicPlayer()
        self.dashboard: Dashboard = Dashboard(400)
        self.playlist: Playlist = Playlist()
        self.progressBar: ProgressBar = ProgressBar(pg.display.get_surface().get_width())
        self.playback: Playback = Playback()
        self.skipButton: SkipButton = SkipButton()
        self.reverseButton: ReverseButton = ReverseButton()
        self.volumeButton: VolumeButton = VolumeButton()
        self.volumeBar: VolumeBar = VolumeBar(pg.display.get_surface().get_height())
        self.font: Font = Font()


    #this draws all the objects on the interface
    def draw(self) -> None:
        self.win.fill(pg.Color("plum1"))

        self.progressBar.draw(self.win, self.musicPlayer.realSongPos)
        self.playback.draw(self.win)
        self.skipButton.draw(self.win)
        self.reverseButton.draw(self.win)
        self.dashboard.draw(self.win, self.font)
        self.volumeButton.draw(self.win)
        self.volumeBar.draw(self.win, self.volumeButton)
        self.playlist.drawPlaylists(self.win)
        self.font.draw(self.win)
        

        pg.display.update()

    def update(self) -> None:
        self.progressBar.update(self.musicPlayer.getSoundLength(), self.musicPlayer.realSongPos)

        self.musicPlayer.update(self.progressBar, self.playlist.allPlaylist[self.playlist.currentPlaylist])

        self.dashboard.update(self.musicPlayer.songs[self.musicPlayer.currentSongIndex])

    # Handles all of the UI events/interactions
    def eventHandler(self) -> None:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running = False
            if event.type == pg.MOUSEBUTTONDOWN:
                mousePos: tuple[int, int] = pg.mouse.get_pos()

                self.progressBar.click(mousePos[0], mousePos[1], self.musicPlayer)

                self.skipButton.click(mousePos[0], mousePos[1], "SHUFFLE", self.progressBar, self.musicPlayer, self.playback)
                self.reverseButton.click(mousePos[0], mousePos[1], self.progressBar, self.musicPlayer, self.playback)
                self.playback.click(mousePos[0], mousePos[1], self.progressBar, self.musicPlayer)

                self.dashboard.click(mousePos[0], mousePos[1], self.win, self.musicPlayer, self.progressBar)
                self.volumeButton.click(mousePos[0], mousePos[1])
                self.volumeBar.click(mousePos[0], mousePos[1], self.volumeButton)
                self.dashboard.changePlaylist(mousePos[0], mousePos[1], self.playlist, self.musicPlayer, self.progressBar, self.playback)
                self.font.click(mousePos[0], mousePos[1])
                self.dashboard.updateFont(mousePos[0], mousePos[1], self.font, self.playlist)
                
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    self.playback.activatePlayback(self.musicPlayer, self.progressBar)
                if event.key == pg.K_b:
                    self.musicPlayer.next("SHUFFLE", self.progressBar)
                    self.playback.activatePlayback(self.musicPlayer, self.progressBar)
                    self.playback.activatePlayback(self.musicPlayer, self.progressBar)
                if event.key == pg.K_m:
                    self.volumeButton.mute(self.volumeBar)

        self.dashboard.scroll(pg.key.get_pressed(), self.win)

    def mainLoop(self) -> None:
        while self.running:
            self.clock.tick(144)

            self.draw()
            self.update()
            self.eventHandler()

        pg.quit()

    
if __name__ == "__main__":
    kb: KoalaBeats = KoalaBeats()
    kb.mainLoop()