"""Integration test for get_team_roster API."""

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


@pytest.mark.asyncio
async def test_get_team_roster_current(skip_if_no_credentials, tools, league_id):
    """Test get_team_roster without parameters (current roster)."""
    # First, get team_key for the logged in user's team.
    team_key_result = await tools.get_team_key(league_id)

    if "error" in team_key_result or not team_key_result.get("team_key"):
        pytest.skip("Could not get team_key for testing")

    team_key = team_key_result["team_key"]

    # Test get_team_roster without week or day (should return today's roster).
    result = await tools.get_team_roster(team_key)

    assert "team_key" in result
    assert result["team_key"] == team_key
    assert "roster" in result

    # If no error, we should have roster data.
    if "error" not in result:
        roster = result["roster"]
        assert isinstance(roster, list)

        # Should have at least one player.
        if len(roster) > 0:
            first_player = roster[0]
            assert "player_id" in first_player
            assert "name" in first_player
            assert "position_type" in first_player
            assert "eligible_positions" in first_player
            # selected_position and status are optional but commonly present.

            print(f"\nSuccessfully retrieved current roster for team {team_key}")
            print(f"Roster size: {len(roster)} players")
            print(f"First player: {first_player['name']} ({first_player['position_type']})")


@pytest.mark.asyncio
async def test_get_team_roster_by_week(skip_if_no_credentials, tools, league_id):
    """Test get_team_roster with week parameter."""
    # First, get team_key for the logged in user's team.
    team_key_result = await tools.get_team_key(league_id)

    if "error" in team_key_result or not team_key_result.get("team_key"):
        pytest.skip("Could not get team_key for testing")

    team_key = team_key_result["team_key"]

    # Test with week 1 roster.
    result = await tools.get_team_roster(team_key, week=1)

    assert "team_key" in result
    assert result["team_key"] == team_key
    assert "week" in result
    assert result["week"] == 1
    assert "roster" in result

    # If no error, we should have roster data.
    if "error" not in result:
        roster = result["roster"]
        assert isinstance(roster, list)

        # Should have at least one player.
        if len(roster) > 0:
            first_player = roster[0]
            assert "player_id" in first_player
            assert "name" in first_player

            print(f"\nSuccessfully retrieved week 1 roster for team {team_key}")
            print(f"Roster size: {len(roster)} players")
