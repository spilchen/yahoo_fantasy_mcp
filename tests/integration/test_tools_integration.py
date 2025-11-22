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
