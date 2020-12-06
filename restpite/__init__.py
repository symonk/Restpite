"""Top-level package for Restpite."""

__author__ = """Simon Kerr"""
__email__ = "jackofspaces@gmail.com"
__version__ = "0.1.0"


from .configuration.config import RestpiteConfig
from .http.request import given

__all__ = ["given", "RestpiteConfig"]
