import time
import pygame
import curses
from playable import Playable
from music_library import MusicLibrary

class MusicPlayer(Playable):
    """Manages music playback using composition with MusicLibrary."""

    def __init__(self):
        """
        Initializes the MusicPlayer.
        """
        pygame.mixer.init()
        self.library = MusicLibrary()
        self.current_index = 0
        self.playing = False
        self.volume = 0.5
        self.start_time = None
        self.elapsed_time = 0
        self.queue = []  # Initialize the queue

   #  def collect_image():


    def play(self, index=None):
        """
        Plays a song.
        
        Parameters:
        index (int, optional): The index of the song to play. If None, plays the current song.
        """
        if index is not None:
            self.current_index = index

        if self.queue:
            song = self.queue.pop(0)  # Get the next song from the queue
        else:
            if self.library.songs:
                song = self.library.songs[self.current_index]
            else:
                return

        try:
            pygame.mixer.music.load(song.path)
            pygame.mixer.music.set_volume(self.volume)
            pygame.mixer.music.play()
            self.start_time = time.time()
            self.playing = True
        except pygame.error as e:
            print(f"Erro ao carregar a música: {e}")

    def add_to_queue(self, song_index):
        """
        Adds a song to the queue.
        
        Parameters:
        song_index (int): The index of the song to add to the queue.
        """
        if 0 <= song_index < len(self.library.songs):
            self.queue.append(self.library.songs[song_index])

    def sound_indicator():
        print("")

    def pause(self):
        """
        Pauses or resumes the song.
        """
        if self.playing:
            pygame.mixer.music.pause()
            self.elapsed_time += time.time() - self.start_time
            self.start_time = None
            self.playing = False
        else:
            pygame.mixer.music.unpause()
            self.start_time = time.time()
            self.playing = True

    def stop(self):
        """
        Stops the song.
        """
        pygame.mixer.music.stop()
        self.elapsed_time = 0
        self.start_time = None
        self.playing = False

    def next_song(self):
        """
        Advances to the next song.
        """
        self.stop()
        if self.queue:
            self.play()
        else:
            self.current_index = (self.current_index + 1) % len(self.library.songs)
            self.play()

    def previous_song(self):
        """
        Goes back to the previous song.
        """
        self.stop()
        self.current_index = (self.current_index - 1) % len(self.library.songs)
        self.play()

    def change_volume(self, increase=True):
        """
        Adjusts the volume.
        
        Parameters:
        increase (bool): If True, increases the volume. If False, decreases the volume.
        """
        self.volume = min(1.0, self.volume + 0.1) if increase else max(0.0, self.volume - 0.1)
        pygame.mixer.music.set_volume(self.volume)

    def get_elapsed_time(self):
        """
        Returns the elapsed time.
        
        Returns:
        float: Elapsed time in seconds.
        """
        if self.start_time is None:
            return self.elapsed_time
        return self.elapsed_time + (time.time() - self.start_time if self.playing else 0)

    @staticmethod
    def format_time(seconds):
        """
        Static method to format time.
        
        Parameters:
        seconds (float): Time in seconds.
        
        Returns:
        str: Time formatted as MM:SS.
        """
        return time.strftime('%M:%S', time.gmtime(seconds))

   # def lyrics(self, song):
       # "letra da musica"
        
