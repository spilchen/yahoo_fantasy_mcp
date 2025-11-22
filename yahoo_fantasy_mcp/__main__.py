"""Entry point for running the Yahoo Fantasy MCP server."""

import asyncio
import os
import sys
import argparse
from pathlib import Path
from mcp.server.stdio import stdio_server
from .server import create_server
from .tools import YahooFantasyTools


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


def list_available_leagues(
    client_id: str = None,
    client_secret: str = None,
    oauth2_file: str = None
):
    """List all leagues the user is part of to help with setup.

    Args:
        client_id: Yahoo API client ID (for env var auth)
        client_secret: Yahoo API client secret (for env var auth)
        oauth2_file: Path to oauth2.json file (alternative auth method)
    """
    print("\n" + "="*60, file=sys.stderr)
    print("YAHOO_LEAGUE_ID not set - Listing available leagues", file=sys.stderr)
    print("="*60 + "\n", file=sys.stderr)

    try:
        tools = YahooFantasyTools(
            client_id=client_id,
            client_secret=client_secret,
            oauth2_file=oauth2_file
        )

        game_codes = ['nfl', 'mlb', 'nba', 'nhl']
        all_leagues = []

        for game_code in game_codes:
            print(f"Checking {game_code.upper()} leagues...", file=sys.stderr)
            result = tools.get_all_leagues(game_code=game_code)

            if result.get('leagues'):
                all_leagues.extend(result['leagues'])

        if all_leagues:
            print("\nFound the following leagues:\n", file=sys.stderr)
            for i, league in enumerate(all_leagues, 1):
                print(f"{i}. [{league['game_code'].upper()} {league['year']}] {league['name']}", file=sys.stderr)
                print(f"   League ID: {league['league_id']}", file=sys.stderr)
                print("", file=sys.stderr)

            print("\nTo use one of these leagues, set the YAHOO_LEAGUE_ID environment variable:", file=sys.stderr)
            print("\n  export YAHOO_LEAGUE_ID=<league_id>", file=sys.stderr)
            print("\nFor example:", file=sys.stderr)
            if all_leagues:
                print(f"  export YAHOO_LEAGUE_ID={all_leagues[0]['league_id']}", file=sys.stderr)
        else:
            print("\nNo leagues found. You may not be part of any active leagues.", file=sys.stderr)
            print("Please join a league on Yahoo Fantasy Sports first.", file=sys.stderr)

        print("\n" + "="*60 + "\n", file=sys.stderr)

    except Exception as e:
        print(f"\nError listing leagues: {e}", file=sys.stderr)
        print("Please check your credentials and try again.\n", file=sys.stderr)


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

    # Determine authentication method.
    if oauth2_file.exists():
        print(f"Using OAuth credentials from {oauth2_file}", file=sys.stderr)
        auth_kwargs = {"oauth2_file": str(oauth2_file)}
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
        auth_kwargs = {"client_id": client_id, "client_secret": client_secret}

    # Check if league ID is set.
    league_id = os.getenv("YAHOO_LEAGUE_ID")
    if not league_id:
        list_available_leagues(**auth_kwargs)
        sys.exit(0)

    print(f"Using league ID: {league_id}", file=sys.stderr)
    asyncio.run(run_server(**auth_kwargs))


if __name__ == "__main__":
    main()
