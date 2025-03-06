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
