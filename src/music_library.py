import time
import pygame
import curses
import os
from playable import Playable
from song import Song

class MusicLibrary:
    """Manages the music library."""
    def __init__(self, music_dir="music"):
        self.music_dir = music_dir
        self.songs = self._load_songs()

    def _load_songs(self):
        """Loads songs from the directory."""
        if not os.path.exists(self.music_dir):
            os.makedirs(self.music_dir)

        songs = []
        for file in os.listdir(self.music_dir):
            if file.endswith(".mp3"):
                songs.append(Song(file, os.path.join(self.music_dir, file)))
        return songs

    def get_songs(self):
        """Returns the list of loaded songs."""
        return self.songs
