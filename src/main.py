import time
import pygame
import curses
import os
from playable import Playable
from song import Song
from music_player import MusicPlayer

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