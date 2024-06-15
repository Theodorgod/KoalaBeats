import pygame as pg
import MusicPlayer

# Class for playlists
# Author Linus Rackner, Theodor Fritsch
# Version 25-04-2024

class Playlist:
    def __init__(self) -> None:
        self.allPlaylist: dict[str, list[int]] = {}
        self.playlistIndex: list[int] = []

        self.currentPlaylist: str = "All Songs"

        #This reades from the playlist.txt file and puts all the playlists with each respective songs in a dictionary
        #where the key is the playlist in string and the value is a list of ints with each int representing a song like an index.
        #This is also the reason to why the songs have the numbers in front of them
        self.file = open("assets/playlists.txt","r")
        while True:
            self.line = self.file.readline()
            if self.line == '':
                break
            self.list = list[str]
            self.list = self.line.split(";")
            self.list.pop()
            for i in range (len(self.list)):
                if i == 0:
                     self.allPlaylist[self.list[0]] = []
                else:
                    self.allPlaylist[self.list[0]].append((int(self.list[i])))
            self.playlistIndex.append(self.list[0])
        
        self.file.close()

        self.bgColor: pg.Color = pg.Color("slategrey")
        self.playlistColor: pg.Color = pg.Color("gray63")

        self.font: pg.font = pg.font.SysFont("segoeuiblack", 20)
        self.renderList: list[pg.Surface] = []
        self.rectList: list[pg.Rect] = []
        for i in range (0, len(self.allPlaylist)):
            self.renderList.append(self.font.render(self.playlistIndex[i], True, pg.Color("grey21"), pg.Color("gray63")))
            self.rectList.append(self.renderList[i].get_rect())
            self.rectList[i].x = 45
            self.rectList[i].y = 400 + 60 * i
    
    #this draws the available playlists
    def drawPlaylists(self, surf: pg.Surface) -> None:
        pg.draw.rect(surf, self.bgColor, (30, 380, 340, 310))
        for i in range (0, len(self.allPlaylist)):
            pg.draw.rect(surf, self.playlistColor, (40, 390 + 60 * i, 320 , 50))
            pg.draw.rect(surf, pg.Color("white"), self.rectList[i])
            surf.blit(self.renderList[i], self.rectList[i].topleft)
            if self.currentPlaylist == self.playlistIndex[i]:
                pg.draw.rect(surf, pg.Color("cyan2"), (320, 405 + 60 * i, 20, 20))


    #the def for changing playlist is in the Dashboard class