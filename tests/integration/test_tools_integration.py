"""Integration tests for Yahoo Fantasy API tools.

These tests require actual Yahoo API credentials and a valid YAHOO_LEAGUE_ID.
They will be skipped if credentials are not available.

To run these tests:
    pytest tests/integration/ -v
"""

import os
import pytest
from yahoo_fantasy_mcp.tools import YahooFantasyTools


@pytest.fixture
def skip_if_no_credentials():
    """Skip test if credentials are not available."""
    league_id = os.getenv("YAHOO_LEAGUE_ID")
    oauth2_file = os.path.exists("oauth2.json")
    has_env_vars = os.getenv("YAHOO_CLIENT_ID") and os.getenv("YAHOO_CLIENT_SECRET")

    if not league_id:
        pytest.skip("YAHOO_LEAGUE_ID environment variable not set")
    if not oauth2_file and not has_env_vars:
        pytest.skip("No credentials available (oauth2.json or env vars)")


@pytest.fixture
def tools():
    """Create a tools instance for testing with real credentials."""
    oauth2_file = "oauth2.json" if os.path.exists("oauth2.json") else None
    client_id = os.getenv("YAHOO_CLIENT_ID")
    client_secret = os.getenv("YAHOO_CLIENT_SECRET")

    if oauth2_file:
        return YahooFantasyTools(oauth2_file=oauth2_file)
    elif client_id and client_secret:
        return YahooFantasyTools(client_id=client_id, client_secret=client_secret)
    else:
        pytest.skip("No credentials available")


@pytest.fixture
def league_id():
    """Get the league ID from environment."""
    return os.getenv("YAHOO_LEAGUE_ID")


class TestYahooFantasyToolsIntegration:
    """Integration tests for Yahoo Fantasy API tools."""

    @pytest.mark.asyncio
    async def test_get_team_key(self, skip_if_no_credentials, tools, league_id):
        """Test get_team_key with real API."""
        result = await tools.get_team_key(league_id)

        assert "league_id" in result
        assert result["league_id"] == league_id
        assert "team_key" in result

        # If no error, we should have a team key.
        if "error" not in result:
            team_key = result["team_key"]
            assert team_key is not None
            assert isinstance(team_key, str)

            # Team key should start with the league_id.
            assert team_key.startswith(league_id)

            # Team key format should be: <game#>.l.<league#>.t.<team#>.
            assert ".t." in team_key

            print(f"\nSuccessfully retrieved team key: {team_key}")

    @pytest.mark.asyncio
    async def test_get_current_week(self, skip_if_no_credentials, tools, league_id):
        """Test get_current_week with real API."""
        result = await tools.get_current_week(league_id)

        assert "league_id" in result
        assert result["league_id"] == league_id
        assert "current_week" in result

        # If no error, we should have a current week number.
        if "error" not in result:
            current_week = result["current_week"]
            assert current_week is not None
            assert isinstance(current_week, int)

            # Week number should be positive and reasonable (1-18 for most leagues).
            assert current_week > 0
            assert current_week <= 20

            print(f"\nSuccessfully retrieved current week: {current_week}")

    @pytest.mark.asyncio
    async def test_get_edit_date(self, skip_if_no_credentials, tools, league_id):
        """Test get_edit_date with real API."""
        result = await tools.get_edit_date(league_id)

        assert "league_id" in result
        assert result["league_id"] == league_id
        assert "edit_date" in result

        # If no error, we should have an edit date.
        if "error" not in result:
            edit_date = result["edit_date"]
            assert edit_date is not None
            assert isinstance(edit_date, str)

            # Edit date should be in ISO format (YYYY-MM-DD).
            import datetime
            parsed_date = datetime.date.fromisoformat(edit_date)
            assert parsed_date is not None

            # Edit date should be a reasonable date (within a year from now).
            today = datetime.date.today()
            one_year_from_now = today + datetime.timedelta(days=365)
            assert today <= parsed_date <= one_year_from_now

            print(f"\nSuccessfully retrieved edit date: {edit_date}")

    @pytest.mark.asyncio
    async def test_get_end_week(self, skip_if_no_credentials, tools, league_id):
        """Test get_end_week with real API."""
        result = await tools.get_end_week(league_id)

        assert "league_id" in result
        assert result["league_id"] == league_id
        assert "end_week" in result

        # If no error, we should have an end week number.
        if "error" not in result:
            end_week = result["end_week"]
            assert end_week is not None
            assert isinstance(end_week, int)

            # End week should be positive and reasonable (typically 14-24 for most leagues).
            assert end_week > 0
            assert end_week <= 30

            print(f"\nSuccessfully retrieved end week: {end_week}")

    @pytest.mark.asyncio
    async def test_get_matchups(self, skip_if_no_credentials, tools, league_id):
        """Test get_matchups with real API."""
        # Test without specifying week (should default to current week).
        result = await tools.get_matchups(league_id)

        assert "league_id" in result
        assert result["league_id"] == league_id
        assert "week" in result
        assert "matchups" in result

        # If no error, we should have matchups data.
        if "error" not in result:
            matchups = result["matchups"]
            assert matchups is not None
            assert isinstance(matchups, dict)

            print(f"\nSuccessfully retrieved matchups for week {result.get('week', 'current')}")

        # Test with specific week.
        result_week_1 = await tools.get_matchups(league_id, week=1)
        assert "league_id" in result_week_1
        assert result_week_1["week"] == 1
        assert "matchups" in result_week_1

        if "error" not in result_week_1:
            print(f"Successfully retrieved matchups for week 1")

    @pytest.mark.asyncio
    async def test_get_positions(self, skip_if_no_credentials, tools, league_id):
        """Test get_positions with real API."""
        result = await tools.get_positions(league_id)

        assert "league_id" in result
        assert result["league_id"] == league_id
        assert "positions" in result

        # If no error, we should have positions data.
        if "error" not in result:
            positions = result["positions"]
            assert positions is not None
            assert isinstance(positions, dict)

            # Verify that at least one position exists.
            assert len(positions) > 0

            # Verify structure of positions - each should have a count.
            for position, details in positions.items():
                assert isinstance(details, dict)
                assert "count" in details
                # position_type is optional (e.g., BN and IR don't have it).

            print(f"\nSuccessfully retrieved {len(positions)} positions")
            print(f"Sample positions: {list(positions.keys())[:5]}")

    @pytest.mark.asyncio
    async def test_get_settings(self, skip_if_no_credentials, tools, league_id):
        """Test get_settings with real API."""
        result = await tools.get_settings(league_id)

        assert "league_id" in result
        assert result["league_id"] == league_id
        assert "settings" in result

        # If no error, we should have settings data.
        if "error" not in result:
            settings = result["settings"]
            assert settings is not None
            assert isinstance(settings, dict)

            # Verify common settings fields exist.
            assert "league_key" in settings
            assert "name" in settings
            assert "num_teams" in settings
            assert "scoring_type" in settings
            assert "game_code" in settings
            assert "season" in settings

            print(f"\nSuccessfully retrieved league settings")
            print(f"League name: {settings.get('name')}")
            print(f"Number of teams: {settings.get('num_teams')}")
            print(f"Scoring type: {settings.get('scoring_type')}")

    @pytest.mark.asyncio
    async def test_get_stat_categories(self, skip_if_no_credentials, tools, league_id):
        """Test get_stat_categories with real API."""
        result = await tools.get_stat_categories(league_id)

        assert "league_id" in result
        assert result["league_id"] == league_id
        assert "stat_categories" in result

        # If no error, we should have stat categories data.
        if "error" not in result:
            stat_categories = result["stat_categories"]
            assert stat_categories is not None
            assert isinstance(stat_categories, list)

            # Verify that at least one stat category exists.
            assert len(stat_categories) > 0

            # Verify structure of stat categories.
            for stat in stat_categories:
                assert isinstance(stat, dict)
                assert "display_name" in stat
                assert "position_type" in stat

            print(f"\nSuccessfully retrieved {len(stat_categories)} stat categories")
            print(f"Sample stats: {[s['display_name'] for s in stat_categories[:5]]}")

    @pytest.mark.asyncio
    async def test_get_free_agents(self, skip_if_no_credentials, tools, league_id):
        """Test get_free_agents with real API."""
        # Test with QB position.
        result = await tools.get_free_agents(league_id, "QB")

        assert "league_id" in result
        assert result["league_id"] == league_id
        assert "position" in result
        assert result["position"] == "QB"
        assert "free_agents" in result

        # If no error, we should have free agents data.
        if "error" not in result:
            free_agents = result["free_agents"]
            assert isinstance(free_agents, list)

            # If there are free agents, verify the structure.
            if len(free_agents) > 0:
                first_agent = free_agents[0]
                assert "player_id" in first_agent
                assert "name" in first_agent
                assert "position_type" in first_agent
                assert "eligible_positions" in first_agent

                print(f"\nSuccessfully retrieved {len(free_agents)} QB free agents")
                print(f"First free agent: {first_agent['name']}")

    @pytest.mark.asyncio
    async def test_get_league_standings(self, skip_if_no_credentials, tools, league_id):
        """Test get_league_standings with real API."""
        result = await tools.get_league_standings(league_id)

        assert "league_id" in result
        assert result["league_id"] == league_id
        assert "standings" in result

        # If no error, we should have standings data.
        if "error" not in result:
            standings = result["standings"]
            assert isinstance(standings, list)
            assert len(standings) > 0

            # Verify structure of first team.
            first_team = standings[0]
            assert "team_key" in first_team
            assert "name" in first_team
            assert "rank" in first_team
            assert "outcome_totals" in first_team
            assert "wins" in first_team["outcome_totals"]
            assert "losses" in first_team["outcome_totals"]

            # First team should have rank 1 (returned as string).
            assert first_team["rank"] == "1" or first_team["rank"] == 1

            print(f"\nSuccessfully retrieved {len(standings)} teams")
            print(f"First place: {first_team['name']}")
