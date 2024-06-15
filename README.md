### Koala beats


# Project description

This project is a music app. You will be able to play songs, create playlists and shuffle them.

# How to get started

Clone down this repo and make sure you have python and the python library pygame installed. 

# How to use the app

The app functions like any other music playing app. On the left side of the app you can find all of your playlists and choose which song to play from that playlist by clicking on the songs name. In the middle of the screen you have your controls, you can pause/ unpause the music, skip to the next or previous song and control the applications volume. By clicking on the progressbar you can jump to different times in the song.

# How to add a song

The music file needs to be a .mp3 file. First place the file in the ``assets\music`` folder and add "xx - " to the beginning of the files name. The xx part is the index of the song, simply take the index of the last song already in the folder and add 1. The you need to update the data.txt file in ``assets``, add a ne line on the format Filename;Name of the song;Name of the artist;Image filename (not necessary). Lastly you need to update the playlists.txt file, add the song index to the All Songs playlist and then to any other playlist you like or create a new playlist.  
