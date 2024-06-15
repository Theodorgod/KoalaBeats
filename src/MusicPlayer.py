import pygame as pg
import os
import random
import sys
from ProgressBar import ProgressBar
import time
from Playlist import Playlist


# A class that handles the music playback and loads all of the available music
# Author Linus Rackner, Theodor Fritsch
# Version 24-04-2024

class MusicPlayer:
    def __init__(self) -> None:
        self.path: str = "assets/music/"

        #Loads all songs into a dictionary
        self.songs: list[str] = []
        self.availableIndexes: list[int] = []
        self.currentSongIndex: int = 0
        self.songIndexHistory: list[int] = []

        for (dirpath, dirnames, filenames) in os.walk(self.path):
            self.songs.extend(filenames)

        self.currentSongLength: int = sys.maxsize
        self.currentlyPlaying: bool = False
        self.isPaused: bool = True

        self.realSongPos: int = 0
        self.oldGetPos: int = 0

    def update(self, progressBar: ProgressBar, songsIndex: list[int]):
        if not self.isPaused:
            deltaTime: int = time.time() - self.oldGetPos
            self.realSongPos += deltaTime
            self.oldGetPos = time.time()

        if self.realSongPos > int(self.getSoundLength()):
            self.next("SHUFFLE", progressBar)

        self.availableIndexes = []
        for i in songsIndex:
            self.availableIndexes.append(int(i) - 10)

    # returns the length of the current song
    def getSoundLength(self) -> float:
        return self.currentSongLength
    
    # plays music, either from beginnig or continuing if current music is paused
    def play(self, progressBar: ProgressBar):
        self.isPaused = False
        if not self.currentlyPlaying:
            pg.mixer.music.load(os.path.join(self.path, self.songs[self.currentSongIndex]))
            sound: pg.mixer.Sound = pg.mixer.Sound(os.path.join(self.path, self.songs[self.currentSongIndex]))
            self.currentSongLength: float = sound.get_length()
            self.currentlyPlaying = True

            self.oldGetPos = time.time()

            progressBar.reset()

            pg.mixer.music.play()
        else:
            pg.mixer.music.unpause()

    # pauses music
    def pause(self) -> None:
        self.isPaused = True
        if pg.mixer.music.get_busy():
            pg.mixer.music.pause()


    # plays next song, either shuffle in current playlist or specific if chosen by user with eg.mouseclick
    def next(self, mode: str, progressBar: ProgressBar, index: int = -1):
        self.songIndexHistory.append(self.currentSongIndex)
        match mode:
            case "SHUFFLE":
                self.currentSongIndex = random.choice(self.availableIndexes)
                self.currentlyPlaying = False

                self.realSongPos = 0               

                self.play(progressBar)
            case "SPECIFIC":
                self.currentSongIndex = index

                if not self.isPaused:
                    self.currentlyPlaying = False

                    self.realSongPos = 0

                    self.play(progressBar)
                else:
                    self.currentlyPlaying = False
                    self.realSongPos = 0

                

    # restarts song or goes back one song if pressed within first 5 seconds of song
    def back(self, progressBar: ProgressBar) -> None:
        currentPos: int = pg.mixer.music.get_pos() / 1000
        if currentPos <= 5 and self.songIndexHistory:
            self.next("SPECIFIC", progressBar, self.songIndexHistory.pop())
            self.songIndexHistory.pop()
        else:
            self.currentlyPlaying = False
            self.play(progressBar)
    #Note: Going back one song plays the last one played and can remeber all songs till the first one, once back at the first one, it wont go back anymore