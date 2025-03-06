import os
import time
import pygame
import curses
from abc import ABC, abstractmethod

class Playable(ABC):
    """Abstract base class for playable items."""

    @abstractmethod
    def play(self):
        """Play the item."""
        pass

    @abstractmethod
    def pause(self):
        """Pause the item."""
        pass

    @abstractmethod
    def stop(self):
        """Stop the item."""
        pass


class Song:
    """Represents a song."""
    def __init__(self, name: str, path: str):
        self.name = name
        self.path = path


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
        

def main(stdscr):
    """
    Terminal interface for the music player.
    
    Parameters:
    stdscr: The curses standard screen.
    """
    player = MusicPlayer()

    if not player.library.songs:
        stdscr.addstr(0, 0, "Nenhuma música encontrada! Adicione arquivos MP3 na pasta 'music'.")
        stdscr.refresh()
        time.sleep(3)
        return

    curses.curs_set(0)
    stdscr.nodelay(True)
    stdscr.timeout(100)

    index = 0
    player.play(index)

    while True:
        stdscr.clear()
        stdscr.addstr(0, 2, "🎵 CLI Music Player 🎵", curses.A_BOLD)
        stdscr.addstr(2, 2, "Use ↑/↓ para navegar | Enter para tocar | Espaço para pausar | q para sair | < / > proximo / anterior")

        # Lista de músicas
        for i, song in enumerate(player.library.get_songs()):
            if i == index:
                stdscr.addstr(4 + i, 2, f"👉 {song.name}", curses.A_REVERSE)
            else:
                stdscr.addstr(4 + i, 2, f"  {song.name}")

        # Informações do player
        elapsed = player.format_time(player.get_elapsed_time())
        stdscr.addstr(15, 2, f"Status: {'▶ Tocando' if player.playing else '⏸ Pausado'}")
        stdscr.addstr(16, 2, f"Volume 🔊: {'█' * int(player.volume * 10)}")
        stdscr.addstr(17, 2, f"Tempo  ⏳: {elapsed}")
       # stdscr.addstr(18, 2, f"Lyrics : {'█' * int(player.volume * 10)}")

        stdscr.refresh()

        key = stdscr.getch()

        if key == ord('q'):
            player.stop()
            break
        elif key == curses.KEY_UP and index > 0:
            index -= 1
        elif key == curses.KEY_DOWN and index < len(player.library.songs) - 1:
            index += 1
        elif key == ord('\n'):  # Enter
            player.play(index)
        elif key == ord(' '):  # Espaço
            player.pause()
        elif key == ord('+'):
            player.change_volume(True)
        elif key == ord('-'):
            player.change_volume(False)
        elif key == curses.KEY_RIGHT:  # >
            player.next_song()
        elif key == curses.KEY_LEFT:  # <
            player.previous_song()

if __name__ == "__main__":
    curses.wrapper(main)