"""Entry point for running the Yahoo Fantasy MCP server."""

import asyncio
import os
import sys
import argparse
from pathlib import Path
from mcp.server.stdio import stdio_server
from .server import create_server


async def run_server(
    client_id: str = None,
    client_secret: str = None,
    oauth2_file: str = None
):
    """Run the MCP server with stdio transport.

    Args:
        client_id: Yahoo API client ID (for env var auth)
        client_secret: Yahoo API client secret (for env var auth)
        oauth2_file: Path to oauth2.json file (alternative auth method)
    """
    async with stdio_server() as (read_stream, write_stream):
        server = create_server(
            client_id=client_id,
            client_secret=client_secret,
            oauth2_file=oauth2_file
        )
        await server.run(
            read_stream,
            write_stream,
            server.create_initialization_options()
        )


def main():
    """Run the MCP server."""
    parser = argparse.ArgumentParser(description="Yahoo Fantasy MCP Server")
    parser.add_argument(
        "--oauth2-file",
        type=str,
        default="oauth2.json",
        help="Path to oauth2.json file (default: oauth2.json)"
    )
    args = parser.parse_args()

    # Check if oauth2.json file exists.
    oauth2_file = Path(args.oauth2_file)

    # Try oauth2.json file first, then fall back to environment variables.
    if oauth2_file.exists():
        print(f"Using OAuth credentials from {oauth2_file}", file=sys.stderr)
        asyncio.run(run_server(oauth2_file=str(oauth2_file)))
    else:
        # Check for environment variables.
        client_id = os.getenv("YAHOO_CLIENT_ID")
        client_secret = os.getenv("YAHOO_CLIENT_SECRET")

        if not client_id or not client_secret:
            print(
                f"Error: {oauth2_file} not found and YAHOO_CLIENT_ID/YAHOO_CLIENT_SECRET "
                "environment variables are not set",
                file=sys.stderr
            )
            print("\nPlease either:", file=sys.stderr)
            print(f"  1. Create {oauth2_file} with Yahoo OAuth credentials", file=sys.stderr)
            print("  2. Set YAHOO_CLIENT_ID and YAHOO_CLIENT_SECRET environment variables", file=sys.stderr)
            sys.exit(1)

        print("Using OAuth credentials from environment variables", file=sys.stderr)
        asyncio.run(run_server(client_id=client_id, client_secret=client_secret))


if __name__ == "__main__":
    main()
