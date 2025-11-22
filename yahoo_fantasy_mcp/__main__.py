"""Entry point for running the Yahoo Fantasy MCP server."""

import asyncio
import os
import sys
from .server import create_server


def main():
    """Run the MCP server."""
    # Check for required environment variables.
    client_id = os.getenv("YAHOO_CLIENT_ID")
    client_secret = os.getenv("YAHOO_CLIENT_SECRET")

    if not client_id or not client_secret:
        print("Error: YAHOO_CLIENT_ID and YAHOO_CLIENT_SECRET environment variables must be set", file=sys.stderr)
        sys.exit(1)

    # Create and run the server.
    server = create_server(client_id, client_secret)
    asyncio.run(server.run())


if __name__ == "__main__":
    main()
