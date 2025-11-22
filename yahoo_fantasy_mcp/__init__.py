"""Yahoo Fantasy MCP Server.

A Model Context Protocol server for Yahoo Fantasy Sports data.
"""

__version__ = "0.1.0"

from .server import create_server

__all__ = ["create_server", "__version__"]
