import pygame as pg

# A class that draws a progress bar that shows how far into a song you have listened and enables you to skip forwards and backwards by pressing on the bar
# Authors: Theodor Fritsch
# Version 24-04-2024
class ProgressBar:
    def __init__(self, scrWidth: int) -> None:
        self.width: int = scrWidth / 3
        self.height: int = 10

        self.x: int = self.width
        self.y: int = 500

        self.progress: int = 0

        self.sliderRadius: int = self.height

        self.bgColor: pg.Color = pg.Color("azure2")
        self.fillColor: pg.Color = pg.Color("azure4")
        self.sliderColor: pg.Color = pg.Color("azure3")

        self.font: pg.font = pg.font.SysFont("segoeuiblack", 13)

    # Checks if a click hit the prograssbar and if true changes where we are att in the music based on the mouse position
    def click(self, mouseX: int, mouseY: int, musicplayer) -> None:
        if self.x <= mouseX <= self.x + self.width and pg.mixer.music.get_busy():
            if self.y <= mouseY <= self.y + self.height:
                musicplayer.realSongPos = 0

                pos: float = (abs(mouseX - self.x) / self.width) * musicplayer.getSoundLength()
                pg.mixer.music.rewind()
                pg.mixer.music.set_pos(pos)

                musicplayer.realSongPos += pos
    
    # Updates how long the progrssbar should be based on how much of the song has elapsed
    def update(self, songLength: float, currentPos: int) -> None:
        self.progress = int((currentPos / songLength) * self.width)

    def reset(self) -> None:
        self.progress = 0

    # Renders and draws time text next to the progress bar
    def renderText(self, currentPos: int, surf: pg.Surface) -> None:
        text: str =  "%02d:%02d" % (currentPos // 60, currentPos % 60)
        textRendered: pg.Surface = self.font.render(text, False, pg.Color("black"), pg.Color("pink"))
        textRect: pg.Rect = textRendered.get_rect()
        textRect.centery = self.y + self.height / 2
        textRect.x = self.x - textRect.width - 5

        surf.blit(textRendered, (textRect.topleft))
        
    # Draws the progressbar to screen
    def draw(self, surf: pg.Surface, currentPos: int) -> None:
        pg.draw.rect(surf, self.bgColor, (self.x, self.y, self.width, self.height))
        pg.draw.rect(surf, self.fillColor, (self.x, self.y, self.progress, self.height))
        self.renderText(currentPos, surf)