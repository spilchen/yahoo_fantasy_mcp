"""Entry point for running the Yahoo Fantasy MCP server."""

import asyncio
import os
import sys
import argparse
from pathlib import Path
from .server import create_server


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
        server = create_server(oauth2_file=str(oauth2_file))
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
        server = create_server(client_id=client_id, client_secret=client_secret)

    asyncio.run(server.run())


if __name__ == "__main__":
    main()
