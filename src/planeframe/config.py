"""Configuration management for the Plane Frame application."""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Application configuration."""
    
    LATITUDE = float(os.getenv('LATITUDE', '0'))
    LONGITUDE = float(os.getenv('LONGITUDE', '0'))
    RADIUS = int(os.getenv('RADIUS', '10'))
    
    # Display settings
    REFRESH_INTERVAL = int(os.getenv('REFRESH_INTERVAL', '30'))
    
    @classmethod
    def validate(cls) -> bool:
        """Validate that all required configuration is present."""
        required_vars = ['LATITUDE', 'LONGITUDE', 'RADIUS']
        return all(getattr(cls, var) for var in required_vars)

# Create a config instance
config = Config() 