import pygame as pg
from MusicPlayer import MusicPlayer
from ProgressBar import ProgressBar
from Playlist import Playlist
from Font import Font
from Playback import Playback
import os


# Class for displaying all available songs, moderated by currenlty selected playlist
# Authors Linus Rackner, Theodor Fritsch
# Version: 2024-05-14

class Dashboard:
    def __init__(self, width: int) -> None:
        self.font: pg.font = pg.font.SysFont("segoeuiblack", 20)

        self.padding: int = 30

        self.songs: list[self.Song] = []

        #this loads all the songs with the information from the "Data.txt" file
        with open("assets/data.txt") as file:
            for i, line in enumerate(file):
                line = line.split(";")

                self.songs.append(self.Song(line[0], line[1], line[2], i, self.font, self.padding, width, line[3].strip()))

        self.surf: pg.Surface = pg.Surface((width, self.songs[len(self.songs) - 1].artistRect.bottom))
        self.surf.set_colorkey(pg.Color("black"))

        self.yOffset: int = 0

        self.currentSong: self.Song = None

    #this is to change song by clicking on it on the interface
    def click(self, mouseX: int, mouseY: int, surf: pg.Surface, musicPlayer: MusicPlayer, progressBar: ProgressBar) -> None:
        if 0 <= mouseX <= self.surf.get_width():
            if 0 <= mouseY <= surf.get_height() / 2:
                localY: int = mouseY + self.yOffset
                for song in self.songs:
                    if song.songRect.x <= mouseX <= song.songRect.right:
                        if song.songRect.y <= localY <= song.artistRect.bottom:
                            musicPlayer.next("SPECIFIC", progressBar, musicPlayer.songs.index(song.path))

    #this changes color of currently selected song
    def update(self, songPlaying: str) -> None:
        for song in self.songs:
            if song.path == songPlaying:
                song.update(True)
            else:
                song.update(False)

        if self.currentSong != None and not self.currentSong.isPlaying:
            self.songs.remove(self.currentSong)
            self.currentSong = None

    #this changes the playlist by mouseclick and lets you play songs from selected playlist
    def changePlaylist(self, mouseX: int, mouseY: int, pl: Playlist, mp: MusicPlayer, pb: ProgressBar, pbb: Playback) -> None:
        for i, rect in enumerate(pl.rectList):
            if pl.rectList[i].x <= mouseX <= (pl.rectList[i].width + pl.rectList[i].x):
                if pl.rectList[i].y <= mouseY <= (pl.rectList[i].height + pl.rectList[i].y):
                    pl.currentPlaylist = list(pl.allPlaylist.keys())[i]

                    # Make sure we dont lose track of the current song playing even if we switch playlist
                    for song in self.songs:
                        if song.isPlaying:
                            self.currentSong = song

                    self.songs.clear()
                    self.yOffset = 0
                    with open("assets/data.txt") as file:
                         j: int = 0
                         for i, line in enumerate(file):
                              for k in pl.allPlaylist[pl.currentPlaylist]:
                                 if (i + 10) == k:
                                    lines = line.split(";")
                                    self.songs.append(self.Song(lines[0], lines[1], lines[2], j, self.font, self.padding, 400, lines[3].strip()))
                                    j += 1

                    mp.update(pb, pl.allPlaylist[pl.currentPlaylist])
                    mp.next("SHUFFLE", pb, -1)
                    mp.songIndexHistory.clear()
                    pbb.img = pg.image.load("assets/images/playbutton.png")
                    pbb.img = pg.transform.scale(pbb.img, (60, 60))

                    if self.currentSong not in self.songs:
                        self.songs.append(self.currentSong)
                    else:
                        self.currentSong = None

    #lets you scroll trough the list of songs
    def scroll(self, keysPressed: list[bool], surf: pg.Surface) -> None:
        if keysPressed[pg.K_UP]:
            if self.yOffset - 1 >= 0:
                self.yOffset -= 2
        if keysPressed[pg.K_DOWN]:
            if self.yOffset + 1 <= self.surf.get_height() - (surf.get_height() / 2):
                self.yOffset += 2

    def draw(self, surf: pg.Surface, font: Font) -> None:
        self.surf.fill(pg.Color("black"))
        for song in self.songs:
            if song != self.currentSong:
                song.draw(self.surf)

            if song.isPlaying and song.img != None:
                song.drawImg(surf)

        surf.blit(self.surf, (0, 0), (0, self.yOffset, self.surf.get_width(), surf.get_height() / 2))


    def updateFont(self, mouseX: int, mouseY:int, font: Font, pl: Playlist) -> None:
        if font.click(mouseX, mouseY):
            self.font: pg.font = pg.font.SysFont(font.currentFont, 20)
            self.songs.clear()
            with open("assets/data.txt") as file:
                             j: int = 0
                             for i, line in enumerate(file):
                                  for k in pl.allPlaylist[pl.currentPlaylist]:
                                     if (i + 10) == k:
                                        lines = line.split(";")
                                        self.songs.append(self.Song(lines[0], lines[1], lines[2], j, self.font, self.padding, 400, lines[3].strip()))
                                        j += 1


    # A helper class that contains the information about the song
    class Song:
        def __init__(self, path: str, song: str, artist: str, i: int, font: pg.font, padding: int, width: int, img: str) -> None:
            self.color: pg.Color = pg.Color("green")
            self.song: str = song
            self.artist: str = artist
            self.i: int = i

            self.path: str = path

            self.font: pg.font = font

            self.songRender: pg.Surface = self.font.render(self.song, True, self.color, pg.Color("white"))
            self.artistRender: pg.Surface = self.font.render(self.artist, True, self.color, pg.Color("white"))

            self.songRect: pg.Rect = self.songRender.get_rect()
            self.songRect.x = padding
            self.songRect.y = self.i * (self.songRect.height * 2) + (self.i + 1) * padding
            self.songRect.width = width - 2 * padding

            self.artistRect: pg.Rect = self.artistRender.get_rect()
            self.artistRect.x = padding
            self.artistRect.y = self.songRect.y + self.artistRect.height
            self.artistRect.width = width - 2 * padding

            self.img: pg.image = None

            self.songBgColor: pg.Color = pg.Color("plum4")

            if img != "":
                self.img = pg.image.load(os.path.join("assets/images/", img))
                self.img = pg.transform.scale(self.img, (400, 400))

            self.isPlaying: bool = False

        def drawImg(self, surf: pg.Surface) -> None:
            imgRect: pg.Rect = self.img.get_rect()
            imgRect.x = (surf.get_width() / 2) - imgRect.width / 2
            imgRect.y = 20

            surf.blit(self.img, imgRect.topleft)

        def update(self, isPlaying: bool) -> None:
            if isPlaying:
                self.color = pg.Color("cyan")
                self.isPlaying = True
            else:
                self.color = pg.Color("cyan3")
                self.isPlaying = False

            self.songRender: pg.Surface = self.font.render(self.song, True, self.color, pg.Color(self.songBgColor))
            self.artistRender: pg.Surface = self.font.render(self.artist, True, self.color, pg.Color(self.songBgColor))

        def draw(self, surf: pg.Surface) -> None:
            pg.draw.rect(surf, pg.Color(self.songBgColor), self.songRect)
            pg.draw.rect(surf, pg.Color(self.songBgColor), self.artistRect)
            surf.blit(self.songRender, self.songRect.topleft)
            surf.blit(self.artistRender, self.artistRect.topleft)
