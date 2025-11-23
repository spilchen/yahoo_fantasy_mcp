"""Tool implementations for Yahoo Fantasy API operations."""

import json
from typing import Optional, Dict, Any, Union, List
import logging

from yahoo_oauth import OAuth2
import yahoo_fantasy_api as yfa

logger = logging.getLogger(__name__)


class YahooFantasyTools:
    """Tools for interacting with Yahoo Fantasy API."""

    def __init__(
        self,
        client_id: Optional[str] = None,
        client_secret: Optional[str] = None,
        oauth2_file: Optional[str] = None
    ):
        """Initialize the tools with Yahoo API credentials.

        Args:
            client_id: Yahoo API client ID (for env var auth)
            client_secret: Yahoo API client secret (for env var auth)
            oauth2_file: Path to oauth2.json file (alternative auth method)
        """
        self.client_id = client_id
        self.client_secret = client_secret
        self.oauth2_file = oauth2_file

        # Initialize OAuth2 client.
        if oauth2_file:
            # Use oauth2.json file for authentication.
            logger.info(f"Initializing OAuth2 from file: {oauth2_file}")
            self._oauth = OAuth2(None, None, from_file=oauth2_file)
        elif client_id and client_secret:
            # Use environment variables for authentication.
            logger.info("Initializing OAuth2 from environment variables")
            self._oauth = OAuth2(client_id, client_secret)
        else:
            raise ValueError(
                "Either oauth2_file or both client_id and client_secret must be provided"
            )

    def get_all_leagues(self, game_code: str = 'nfl', year: Optional[int] = None) -> Dict[str, Any]:
        """Get all leagues the user is part of for a specific game and year.

        Args:
            game_code: Game code (e.g., 'nfl', 'mlb', 'nba', 'nhl')
            year: Year to query (defaults to current year)

        Returns:
            Dictionary containing league information
        """
        import datetime

        if year is None:
            year = datetime.datetime.now().year

        try:
            game = yfa.Game(self._oauth, game_code)
            league_ids = game.league_ids(year=year)

            leagues = []
            for league_id in league_ids:
                try:
                    league = game.to_league(league_id)
                    league_name = league.settings().get('name', 'Unknown')
                    leagues.append({
                        'league_id': league_id,
                        'name': league_name,
                        'game_code': game_code,
                        'year': year
                    })
                except Exception as e:
                    logger.warning(f"Could not get details for league {league_id}: {e}")
                    leagues.append({
                        'league_id': league_id,
                        'name': 'Unknown',
                        'game_code': game_code,
                        'year': year
                    })

            return {
                'game_code': game_code,
                'year': year,
                'leagues': leagues
            }
        except Exception as e:
            logger.error(f"Error getting leagues for {game_code} {year}: {e}")
            return {
                'game_code': game_code,
                'year': year,
                'leagues': [],
                'error': str(e)
            }

    async def get_team_key(self, league_id: str) -> Dict[str, Any]:
        """Get the team key for the logged in user's team in a league.

        Args:
            league_id: The league ID to query

        Returns:
            Dictionary containing the team_key for the logged in user's team.
        """
        logger.info(f"Getting team key for league: {league_id}")
        try:
            league = yfa.League(self._oauth, league_id)
            team_key = league.team_key()

            return {
                "league_id": league_id,
                "team_key": team_key
            }
        except Exception as e:
            logger.error(f"Error getting team key for league {league_id}: {e}")
            return {
                "league_id": league_id,
                "team_key": None,
                "error": str(e)
            }

    async def get_current_week(self, league_id: str) -> Dict[str, Any]:
        """Get the current week number of the league.

        Args:
            league_id: The league ID to query

        Returns:
            Dictionary containing the current week number.
        """
        logger.info(f"Getting current week for league: {league_id}")
        try:
            league = yfa.League(self._oauth, league_id)
            current_week = league.current_week()

            return {
                "league_id": league_id,
                "current_week": current_week
            }
        except Exception as e:
            logger.error(f"Error getting current week for league {league_id}: {e}")
            return {
                "league_id": league_id,
                "current_week": None,
                "error": str(e)
            }

    async def get_edit_date(self, league_id: str) -> Dict[str, Any]:
        """Get the next date when lineups can be edited.

        Args:
            league_id: The league ID to query

        Returns:
            Dictionary containing the edit date (roster deadline).
        """
        logger.info(f"Getting edit date for league: {league_id}")
        try:
            league = yfa.League(self._oauth, league_id)
            edit_date = league.edit_date()

            return {
                "league_id": league_id,
                "edit_date": edit_date.isoformat()
            }
        except Exception as e:
            logger.error(f"Error getting edit date for league {league_id}: {e}")
            return {
                "league_id": league_id,
                "edit_date": None,
                "error": str(e)
            }

    async def get_end_week(self, league_id: str) -> Dict[str, Any]:
        """Get the ending week number of the league season.

        Args:
            league_id: The league ID to query

        Returns:
            Dictionary containing the ending week number.
        """
        logger.info(f"Getting end week for league: {league_id}")
        try:
            league = yfa.League(self._oauth, league_id)
            end_week = league.end_week()

            return {
                "league_id": league_id,
                "end_week": end_week
            }
        except Exception as e:
            logger.error(f"Error getting end week for league {league_id}: {e}")
            return {
                "league_id": league_id,
                "end_week": None,
                "error": str(e)
            }

    async def get_matchups(self, league_id: str, week: Optional[int] = None) -> Dict[str, Any]:
        """Get matchup data for a given week.

        Args:
            league_id: The league ID to query
            week: Week number to query (optional, defaults to current week)

        Returns:
            Dictionary containing matchup details as key/value pairs.
        """
        logger.info(f"Getting matchups for league: {league_id}, week: {week}")
        try:
            league = yfa.League(self._oauth, league_id)
            matchups = league.matchups(week=week)

            return {
                "league_id": league_id,
                "week": week,
                "matchups": matchups
            }
        except Exception as e:
            logger.error(f"Error getting matchups for league {league_id}, week {week}: {e}")
            return {
                "league_id": league_id,
                "week": week,
                "matchups": None,
                "error": str(e)
            }

    async def get_positions(self, league_id: str) -> Dict[str, Any]:
        """Get the positions used in the league.

        Args:
            league_id: The league ID to query

        Returns:
            Dictionary containing positions used in the league. Each key is a
            position, with count and position_type as the values.
        """
        logger.info(f"Getting positions for league: {league_id}")
        try:
            league = yfa.League(self._oauth, league_id)
            positions = league.positions()

            return {
                "league_id": league_id,
                "positions": positions
            }
        except Exception as e:
            logger.error(f"Error getting positions for league {league_id}: {e}")
            return {
                "league_id": league_id,
                "positions": None,
                "error": str(e)
            }

    async def get_settings(self, league_id: str) -> Dict[str, Any]:
        """Get the league settings.

        Args:
            league_id: The league ID to query

        Returns:
            Dictionary containing comprehensive league settings including league_key,
            name, draft_status, num_teams, scoring_type, playoff settings, waiver
            settings, trade settings, and more.
        """
        logger.info(f"Getting settings for league: {league_id}")
        try:
            league = yfa.League(self._oauth, league_id)
            settings = league.settings()

            return {
                "league_id": league_id,
                "settings": settings
            }
        except Exception as e:
            logger.error(f"Error getting settings for league {league_id}: {e}")
            return {
                "league_id": league_id,
                "settings": None,
                "error": str(e)
            }

    async def get_stat_categories(self, league_id: str) -> Dict[str, Any]:
        """Get the stat categories tracked in the league.

        Args:
            league_id: The league ID to query

        Returns:
            Dictionary containing a list of stat categories. Each entry has
            display_name (e.g., 'R', 'HR', 'W') and position_type (e.g., 'B' for
            batter, 'P' for pitcher).
        """
        logger.info(f"Getting stat categories for league: {league_id}")
        try:
            league = yfa.League(self._oauth, league_id)
            stat_categories = league.stat_categories()

            return {
                "league_id": league_id,
                "stat_categories": stat_categories
            }
        except Exception as e:
            logger.error(f"Error getting stat categories for league {league_id}: {e}")
            return {
                "league_id": league_id,
                "stat_categories": [],
                "error": str(e)
            }

    async def get_teams(self, league_id: str) -> Dict[str, Any]:
        """Get details of all teams in the league.

        Args:
            league_id: The league ID to query

        Returns:
            Dictionary containing teams data. Each team key maps to team details
            including team_key, team_id, name, is_owned_by_current_login, url,
            waiver_priority, number_of_moves, number_of_trades, roster_adds,
            clinched_playoffs, managers, and more.
        """
        logger.info(f"Getting teams for league: {league_id}")
        try:
            league = yfa.League(self._oauth, league_id)
            teams = league.teams()

            return {
                "league_id": league_id,
                "teams": teams
            }
        except Exception as e:
            logger.error(f"Error getting teams for league {league_id}: {e}")
            return {
                "league_id": league_id,
                "teams": {},
                "error": str(e)
            }

    async def get_transactions(
        self, league_id: str, tran_types: str, count: Optional[str] = None
    ) -> Dict[str, Any]:
        """Get transactions for the league.

        Args:
            league_id: The league ID to query
            tran_types: Comma-separated transaction types to retrieve. Valid values:
                       add, drop, commish, trade
            count: Number of transactions to retrieve (optional, returns all if not specified)

        Returns:
            Dictionary containing a list of transactions with details including players,
            status, timestamp, team keys/names, transaction_id, and transaction_key.
        """
        logger.info(f"Getting transactions for league: {league_id}, types: {tran_types}, count: {count}")
        try:
            league = yfa.League(self._oauth, league_id)
            transactions = league.transactions(tran_types, count)

            return {
                "league_id": league_id,
                "tran_types": tran_types,
                "count": count,
                "transactions": transactions
            }
        except Exception as e:
            logger.error(f"Error getting transactions for league {league_id}: {e}")
            return {
                "league_id": league_id,
                "tran_types": tran_types,
                "count": count,
                "transactions": [],
                "error": str(e)
            }

    async def get_league_standings(self, league_id: str) -> Dict[str, Any]:
        """Get current standings for a fantasy league.

        Args:
            league_id: The league ID to query

        Returns:
            Dictionary containing league standings data with teams ordered by rank.
            Each team includes: team_key, name, rank, playoff_seed, outcome_totals
            (wins, losses, ties, percentage), and games_back.
        """
        logger.info(f"Getting standings for league: {league_id}")
        try:
            league = yfa.League(self._oauth, league_id)
            standings = league.standings()

            return {
                "league_id": league_id,
                "standings": standings
            }
        except Exception as e:
            logger.error(f"Error getting standings for league {league_id}: {e}")
            return {
                "league_id": league_id,
                "standings": [],
                "error": str(e)
            }

    async def get_team_roster(self, team_key: str) -> Dict[str, Any]:
        """Get roster for a specific team.

        Args:
            team_key: The team key to query

        Returns:
            Dictionary containing team roster data
        """
        # TODO(SPILLY): Implement using yahoo_fantasy_api.
        logger.info(f"Getting roster for team: {team_key}")
        return {"team_key": team_key, "roster": []}

    async def get_matchup_scores(
        self, team_key: str, week: Optional[int] = None
    ) -> Dict[str, Any]:
        """Get scores for current or specific matchup.

        Args:
            team_key: The team key to query
            week: Week number (optional, defaults to current week)

        Returns:
            Dictionary containing matchup score data
        """
        # TODO(SPILLY): Implement using yahoo_fantasy_api.
        logger.info(f"Getting matchup scores for team: {team_key}, week: {week}")
        return {"team_key": team_key, "week": week, "matchup": {}}

    async def get_player_stats(self, player_key: str) -> Dict[str, Any]:
        """Get statistics for a specific player.

        Args:
            player_key: The player key to query

        Returns:
            Dictionary containing player statistics
        """
        # TODO(SPILLY): Implement using yahoo_fantasy_api.
        logger.info(f"Getting stats for player: {player_key}")
        return {"player_key": player_key, "stats": {}}

    async def search_players(
        self, league_id: str, search_term: str
    ) -> Dict[str, Any]:
        """Search for players by name.

        Args:
            league_id: The league ID to search in
            search_term: Player name to search for

        Returns:
            Dictionary containing search results
        """
        # TODO(SPILLY): Implement using yahoo_fantasy_api.
        logger.info(f"Searching for players: {search_term} in league: {league_id}")
        return {"league_id": league_id, "search_term": search_term, "results": []}

    async def get_free_agents(
        self, league_id: str, position: str
    ) -> Dict[str, Any]:
        """Get available free agents in a league for a specific position.

        Args:
            league_id: The league ID to query
            position: Position filter (required). Use position codes like 'QB', 'RB',
                     'WR', 'TE', etc., or position types like 'O' for offense, 'D' for defense.

        Returns:
            Dictionary containing free agent data including player_id, name,
            position_type, and eligible_positions for each player.
        """
        logger.info(f"Getting free agents for league: {league_id}, position: {position}")
        try:
            league = yfa.League(self._oauth, league_id)
            free_agents = league.free_agents(position)

            return {
                "league_id": league_id,
                "position": position,
                "free_agents": free_agents
            }
        except Exception as e:
            logger.error(f"Error getting free agents for league {league_id}, position {position}: {e}")
            return {
                "league_id": league_id,
                "position": position,
                "free_agents": [],
                "error": str(e)
            }

    async def get_waivers(self, league_id: str) -> Dict[str, Any]:
        """Get players currently on waivers in the league.

        Args:
            league_id: The league ID to query

        Returns:
            Dictionary containing waiver data including player_id, name,
            position_type, eligible_positions, percent_owned, and status
            for each player.
        """
        logger.info(f"Getting waivers for league: {league_id}")
        try:
            league = yfa.League(self._oauth, league_id)
            waivers = league.waivers()

            return {
                "league_id": league_id,
                "waivers": waivers
            }
        except Exception as e:
            logger.error(f"Error getting waivers for league {league_id}: {e}")
            return {
                "league_id": league_id,
                "waivers": [],
                "error": str(e)
            }

    async def get_player_details(
        self, league_id: str, player: Union[str, int, List[int]]
    ) -> Dict[str, Any]:
        """Get detailed information about one or more players.

        Args:
            league_id: The league ID to query
            player: If a string, searches for players by name (returns up to 25 matches).
                   If an int, looks up a single player by ID.
                   If a list of ints, looks up multiple players by their IDs.

        Returns:
            Dictionary containing player details including player_key, player_id, name,
            position_type, eligible_positions, editorial team info, and more.
            For name searches, returns a list of matching players.
            For ID lookups, returns a list of player details.
        """
        logger.info(f"Getting player details for league: {league_id}, player: {player}")
        try:
            league = yfa.League(self._oauth, league_id)
            player_details = league.player_details(player)

            return {
                "league_id": league_id,
                "player": player,
                "players": player_details
            }
        except Exception as e:
            logger.error(f"Error getting player details for league {league_id}, player {player}: {e}")
            return {
                "league_id": league_id,
                "player": player,
                "players": [],
                "error": str(e)
            }
