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
                name="get_positions",
                description="Get the positions used in the league with their counts and types",
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
                name="get_settings",
                description="Get comprehensive league settings including scoring, playoff, waiver, and trade settings",
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
                name="get_stat_categories",
                description="Get the stat categories tracked in the league with their position types",
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
                name="get_teams",
                description="Get details of all teams in the league including roster management stats and managers",
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
                name="get_transactions",
                description="Get league transactions (adds, drops, trades, commish moves)",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "league_id": {
                            "type": "string",
                            "description": "The league ID to query"
                        },
                        "tran_types": {
                            "type": "string",
                            "description": "Comma-separated transaction types: add, drop, commish, trade"
                        },
                        "count": {
                            "type": "string",
                            "description": "Number of transactions to retrieve (optional, returns all if not specified)"
                        }
                    },
                    "required": ["league_id", "tran_types"]
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
                description="Get roster for a specific team for a given week or date",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "team_key": {
                            "type": "string",
                            "description": "The team key to query"
                        },
                        "week": {
                            "type": "integer",
                            "description": "Week number of the roster to get (optional)"
                        },
                        "day": {
                            "type": "string",
                            "description": "Day to get the roster (YYYY-MM-DD format, optional). If neither week nor day is specified, returns today's roster."
                        }
                    },
                    "required": ["team_key"]
                }
            ),
            Tool(
                name="get_team_details",
                description="Get detailed information about a specific team",
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
                name="get_team_matchup",
                description="Get the opponent team key for a team's matchup in a given week",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "team_key": {
                            "type": "string",
                            "description": "The team key to query"
                        },
                        "week": {
                            "type": "integer",
                            "description": "Week number to find the matchup for"
                        }
                    },
                    "required": ["team_key", "week"]
                }
            ),
            Tool(
                name="get_team_proposed_trades",
                description="Get proposed trades that include the team (both offered and received)",
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
                description="Get statistics for one or more players for a specified time period",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "league_id": {
                            "type": "string",
                            "description": "The league ID to query"
                        },
                        "player_ids": {
                            "type": "string",
                            "description": "Comma-separated list of Yahoo! player IDs"
                        },
                        "req_type": {
                            "type": "string",
                            "description": "Stats time range: 'season', 'average_season', 'lastweek', 'lastmonth', 'date', 'week'"
                        },
                        "date": {
                            "type": "string",
                            "description": "Date for stats (YYYY-MM-DD format, used with req_type='date')"
                        },
                        "week": {
                            "type": "integer",
                            "description": "Week number (used with req_type='week')"
                        },
                        "season": {
                            "type": "integer",
                            "description": "Season year (used with req_type='season')"
                        }
                    },
                    "required": ["league_id", "player_ids", "req_type"]
                }
            ),
            Tool(
                name="search_players",
                description="Search for players by name or get player details by ID",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "league_id": {
                            "type": "string",
                            "description": "The league ID to search in"
                        },
                        "player": {
                            "description": "Player search: string for name search (returns up to 25 matches), integer for single player ID, or comma-separated integers for multiple player IDs"
                        }
                    },
                    "required": ["league_id", "player"]
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
            Tool(
                name="get_waivers",
                description="Get players currently on waivers in the league",
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
            elif name == "get_positions":
                result = await tools.get_positions(arguments["league_id"])
            elif name == "get_settings":
                result = await tools.get_settings(arguments["league_id"])
            elif name == "get_stat_categories":
                result = await tools.get_stat_categories(arguments["league_id"])
            elif name == "get_teams":
                result = await tools.get_teams(arguments["league_id"])
            elif name == "get_transactions":
                result = await tools.get_transactions(
                    arguments["league_id"],
                    arguments["tran_types"],
                    arguments.get("count")
                )
            elif name == "get_league_standings":
                result = await tools.get_league_standings(arguments["league_id"])
            elif name == "get_team_roster":
                result = await tools.get_team_roster(
                    arguments["team_key"],
                    arguments.get("week"),
                    arguments.get("day")
                )
            elif name == "get_team_details":
                result = await tools.get_team_details(arguments["team_key"])
            elif name == "get_team_matchup":
                result = await tools.get_team_matchup(
                    arguments["team_key"],
                    arguments["week"]
                )
            elif name == "get_team_proposed_trades":
                result = await tools.get_team_proposed_trades(arguments["team_key"])
            elif name == "get_matchup_scores":
                result = await tools.get_matchup_scores(
                    arguments["team_key"],
                    arguments.get("week")
                )
            elif name == "get_player_stats":
                # Parse comma-separated player IDs into list of integers.
                player_ids_str = arguments["player_ids"]
                player_ids = [int(x.strip()) for x in player_ids_str.split(',')]
                result = await tools.get_player_stats(
                    arguments["league_id"],
                    player_ids,
                    arguments["req_type"],
                    arguments.get("date"),
                    arguments.get("week"),
                    arguments.get("season")
                )
            elif name == "search_players":
                # Handle player input: can be string (name), int (single ID), or comma-separated ints.
                player_input = arguments["player"]
                if isinstance(player_input, str):
                    # Check if it's a comma-separated list of integers.
                    if ',' in player_input:
                        try:
                            player = [int(x.strip()) for x in player_input.split(',')]
                        except ValueError:
                            # Not all integers, treat as name search.
                            player = player_input
                    else:
                        # Try to parse as single integer.
                        try:
                            player = int(player_input)
                        except ValueError:
                            # Not an integer, treat as name search.
                            player = player_input
                else:
                    player = player_input
                result = await tools.search_players(arguments["league_id"], player)
            elif name == "get_free_agents":
                result = await tools.get_free_agents(
                    arguments["league_id"],
                    arguments["position"]
                )
            elif name == "get_waivers":
                result = await tools.get_waivers(arguments["league_id"])
            else:
                raise ValueError(f"Unknown tool: {name}")

            return [TextContent(type="text", text=str(result))]

        except Exception as e:
            logger.error(f"Error calling tool {name}: {e}")
            return [TextContent(type="text", text=f"Error: {str(e)}")]

    return server
