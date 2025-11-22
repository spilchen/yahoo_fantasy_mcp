"""Main MCP server implementation for Yahoo Fantasy API."""

from typing import Any, Optional
from mcp.server import Server
from mcp.types import Tool, TextContent
import logging

from .tools import YahooFantasyTools

logger = logging.getLogger(__name__)


def create_server(
    client_id: Optional[str] = None,
    client_secret: Optional[str] = None,
    oauth2_file: Optional[str] = None
) -> Server:
    """Create and configure the MCP server.

    Args:
        client_id: Yahoo API client ID (for env var auth)
        client_secret: Yahoo API client secret (for env var auth)
        oauth2_file: Path to oauth2.json file (alternative auth method)

    Returns:
        Configured MCP Server instance
    """
    server = Server("yahoo-fantasy")
    tools = YahooFantasyTools(
        client_id=client_id,
        client_secret=client_secret,
        oauth2_file=oauth2_file
    )

    @server.list_tools()
    async def list_tools() -> list[Tool]:
        """List available tools."""
        return [
            Tool(
                name="get_team_key",
                description="Get the team key for the logged in user's team in a league",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "league_id": {
                            "type": "string",
                            "description": "The league ID to query"
                        }
                    },
                    "required": ["league_id"]
                }
            ),
            Tool(
                name="get_current_week",
                description="Get the current week number of the league",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "league_id": {
                            "type": "string",
                            "description": "The league ID to query"
                        }
                    },
                    "required": ["league_id"]
                }
            ),
            Tool(
                name="get_edit_date",
                description="Get the next date when lineups can be edited (roster deadline)",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "league_id": {
                            "type": "string",
                            "description": "The league ID to query"
                        }
                    },
                    "required": ["league_id"]
                }
            ),
            Tool(
                name="get_end_week",
                description="Get the ending week number of the league season",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "league_id": {
                            "type": "string",
                            "description": "The league ID to query"
                        }
                    },
                    "required": ["league_id"]
                }
            ),
            Tool(
                name="get_matchups",
                description="Get matchup data for a given week (defaults to current week)",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "league_id": {
                            "type": "string",
                            "description": "The league ID to query"
                        },
                        "week": {
                            "type": "integer",
                            "description": "Week number (optional, defaults to current week)"
                        }
                    },
                    "required": ["league_id"]
                }
            ),
            Tool(
                name="get_league_standings",
                description="Get current standings for a fantasy league",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "league_id": {
                            "type": "string",
                            "description": "The league ID to query"
                        }
                    },
                    "required": ["league_id"]
                }
            ),
            Tool(
                name="get_team_roster",
                description="Get roster for a specific team",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "team_key": {
                            "type": "string",
                            "description": "The team key to query"
                        }
                    },
                    "required": ["team_key"]
                }
            ),
            Tool(
                name="get_matchup_scores",
                description="Get scores for current or specific matchup",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "team_key": {
                            "type": "string",
                            "description": "The team key to query"
                        },
                        "week": {
                            "type": "integer",
                            "description": "Week number (optional)"
                        }
                    },
                    "required": ["team_key"]
                }
            ),
            Tool(
                name="get_player_stats",
                description="Get statistics for a specific player",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "player_key": {
                            "type": "string",
                            "description": "The player key to query"
                        }
                    },
                    "required": ["player_key"]
                }
            ),
            Tool(
                name="search_players",
                description="Search for players by name",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "league_id": {
                            "type": "string",
                            "description": "The league ID to search in"
                        },
                        "search_term": {
                            "type": "string",
                            "description": "Player name to search for"
                        }
                    },
                    "required": ["league_id", "search_term"]
                }
            ),
            Tool(
                name="get_free_agents",
                description="Get available free agents in a league for a specific position",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "league_id": {
                            "type": "string",
                            "description": "The league ID to query"
                        },
                        "position": {
                            "type": "string",
                            "description": "Position filter (required). Use position codes like 'QB', 'RB', 'WR', 'TE', etc."
                        }
                    },
                    "required": ["league_id", "position"]
                }
            ),
        ]

    @server.call_tool()
    async def call_tool(name: str, arguments: Any) -> list[TextContent]:
        """Handle tool calls.

        Args:
            name: Name of the tool to call
            arguments: Tool arguments

        Returns:
            List of text content results
        """
        try:
            if name == "get_team_key":
                result = await tools.get_team_key(arguments["league_id"])
            elif name == "get_current_week":
                result = await tools.get_current_week(arguments["league_id"])
            elif name == "get_edit_date":
                result = await tools.get_edit_date(arguments["league_id"])
            elif name == "get_end_week":
                result = await tools.get_end_week(arguments["league_id"])
            elif name == "get_matchups":
                result = await tools.get_matchups(
                    arguments["league_id"],
                    arguments.get("week")
                )
            elif name == "get_league_standings":
                result = await tools.get_league_standings(arguments["league_id"])
            elif name == "get_team_roster":
                result = await tools.get_team_roster(arguments["team_key"])
            elif name == "get_matchup_scores":
                result = await tools.get_matchup_scores(
                    arguments["team_key"],
                    arguments.get("week")
                )
            elif name == "get_player_stats":
                result = await tools.get_player_stats(arguments["player_key"])
            elif name == "search_players":
                result = await tools.search_players(
                    arguments["league_id"],
                    arguments["search_term"]
                )
            elif name == "get_free_agents":
                result = await tools.get_free_agents(
                    arguments["league_id"],
                    arguments["position"]
                )
            else:
                raise ValueError(f"Unknown tool: {name}")

            return [TextContent(type="text", text=str(result))]

        except Exception as e:
            logger.error(f"Error calling tool {name}: {e}")
            return [TextContent(type="text", text=f"Error: {str(e)}")]

    return server
