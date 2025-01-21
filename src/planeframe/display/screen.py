"""E-ink display management module."""

import logging
from typing import Optional, Dict, Any
from inky.auto import auto
from PIL import Image

class Display:
    """Manages the e-ink display interface."""
    
    def __init__(self):
        """Initialize the display."""
        self.display = auto()
        self._current_origin: Optional[str] = None
        self._current_destination: Optional[str] = None
    
    def needs_update(self, origin: str, destination: str) -> bool:
        """Check if the display needs to be updated with new flight info."""
        return (self._current_origin != origin or 
                self._current_destination != destination)
    
    def update(self, image: Image.Image) -> None:
        """Update the display with a new image."""
        try:
            # Rotate image to landscape
            rotated_image = image.rotate(90, expand=True)
            self.display.set_image(rotated_image)
            self.display.show()
        except Exception as e:
            logging.error(f'Display refresh failed: {e}')
            raise
    
    def set_current_flight(self, origin: str, destination: str) -> None:
        """Update the current flight information."""
        self._current_origin = origin
        self._current_destination = destination
    
    def clear(self) -> None:
        """Clear the display."""
        try:
            blank_image = Image.new('RGB', self.display.resolution, 'white')
            self.display.set_image(blank_image)
            self.display.show()
            self._current_origin = None
            self._current_destination = None
        except Exception as e:
            logging.error(f'Failed to clear display: {e}')
            raise

# Create a singleton display instance
display = Display() 