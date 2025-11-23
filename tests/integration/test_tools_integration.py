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
    async def test_get_teams(self, skip_if_no_credentials, tools, league_id):
        """Test get_teams with real API."""
        result = await tools.get_teams(league_id)

        assert "league_id" in result
        assert result["league_id"] == league_id
        assert "teams" in result

        # If no error, we should have teams data.
        if "error" not in result:
            teams = result["teams"]
            assert teams is not None
            assert isinstance(teams, dict)

            # Verify that at least one team exists.
            assert len(teams) > 0

            # Verify structure of teams - get first team.
            first_team_key = list(teams.keys())[0]
            first_team = teams[first_team_key]

            assert isinstance(first_team, dict)
            assert "team_key" in first_team
            assert "team_id" in first_team
            assert "name" in first_team
            # is_owned_by_current_login is optional.

            print(f"\nSuccessfully retrieved {len(teams)} teams")
            print(f"Sample team: {first_team.get('name')} (key: {first_team_key})")

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

    @pytest.mark.asyncio
    async def test_get_transactions(self, skip_if_no_credentials, tools, league_id):
        """Test get_transactions with real API."""
        # Test with trade transactions.
        result = await tools.get_transactions(league_id, "trade", "5")

        assert "league_id" in result
        assert result["league_id"] == league_id
        assert "tran_types" in result
        assert result["tran_types"] == "trade"
        assert "count" in result
        assert result["count"] == "5"
        assert "transactions" in result

        # If no error, we should have transactions data.
        if "error" not in result:
            transactions = result["transactions"]
            assert isinstance(transactions, list)

            # If there are transactions, verify the structure.
            if len(transactions) > 0:
                first_txn = transactions[0]
                assert "status" in first_txn
                assert "timestamp" in first_txn
                # Transaction should have transaction_id or transaction_key.
                assert "transaction_id" in first_txn or "transaction_key" in first_txn

                print(f"\nSuccessfully retrieved {len(transactions)} trade transactions")
                print(f"First transaction status: {first_txn['status']}")
            else:
                print("\nNo trade transactions found in league.")

    @pytest.mark.asyncio
    async def test_get_waivers(self, skip_if_no_credentials, tools, league_id):
        """Test get_waivers with real API."""
        result = await tools.get_waivers(league_id)

        assert "league_id" in result
        assert result["league_id"] == league_id
        assert "waivers" in result

        # If no error, we should have waivers data.
        if "error" not in result:
            waivers = result["waivers"]
            assert isinstance(waivers, list)

            # If there are players on waivers, verify the structure.
            if len(waivers) > 0:
                first_waiver = waivers[0]
                assert "player_id" in first_waiver
                assert "name" in first_waiver
                assert "position_type" in first_waiver
                assert "eligible_positions" in first_waiver
                # percent_owned and status are optional but commonly present.

                print(f"\nSuccessfully retrieved {len(waivers)} players on waivers")
                print(f"First player on waivers: {first_waiver['name']}")
            else:
                print("\nNo players currently on waivers.")

    @pytest.mark.asyncio
    async def test_get_player_details_by_name(self, skip_if_no_credentials, tools, league_id):
        """Test get_player_details with name search."""
        # Search for a common name that should return results.
        result = await tools.get_player_details(league_id, "Smith")

        assert "league_id" in result
        assert result["league_id"] == league_id
        assert "player" in result
        assert result["player"] == "Smith"
        assert "players" in result

        # If no error, we should have player details.
        if "error" not in result:
            players = result["players"]
            assert isinstance(players, list)

            # Should find at least one player with "Smith" in their name.
            if len(players) > 0:
                first_player = players[0]
                assert "player_id" in first_player
                assert "name" in first_player
                assert isinstance(first_player["name"], dict)
                assert "full" in first_player["name"]
                assert "player_key" in first_player
                assert "position_type" in first_player

                print(f"\nSuccessfully found {len(players)} players matching 'Smith'")
                print(f"First match: {first_player['name']['full']}")
            else:
                print("\nNo players found matching 'Smith'")

    @pytest.mark.asyncio
    async def test_get_player_details_by_id(self, skip_if_no_credentials, tools, league_id):
        """Test get_player_details with player ID lookup."""
        # First, get free agents to find a valid player ID.
        fa_result = await tools.get_free_agents(league_id, "QB")

        if "error" in fa_result or len(fa_result.get("free_agents", [])) == 0:
            pytest.skip("No free agents available to test with")

        # Get the first free agent's player_id.
        test_player_id = fa_result["free_agents"][0]["player_id"]

        # Now test get_player_details with this ID.
        result = await tools.get_player_details(league_id, test_player_id)

        assert "league_id" in result
        assert result["league_id"] == league_id
        assert "player" in result
        assert result["player"] == test_player_id
        assert "players" in result

        # If no error, we should have exactly one player.
        if "error" not in result:
            players = result["players"]
            assert isinstance(players, list)
            assert len(players) == 1

            player = players[0]
            assert "player_id" in player
            assert int(player["player_id"]) == test_player_id
            assert "name" in player
            assert "player_key" in player

            print(f"\nSuccessfully retrieved details for player ID {test_player_id}")
            print(f"Player name: {player['name']['full']}")

    @pytest.mark.asyncio
    async def test_get_player_stats(self, skip_if_no_credentials, tools, league_id):
        """Test get_player_stats with real API."""
        # First, get free agents to find a valid player ID.
        fa_result = await tools.get_free_agents(league_id, "G")

        if "error" in fa_result or len(fa_result.get("free_agents", [])) == 0:
            pytest.skip("No free agents available to test with")

        # Get the first free agent's player_id.
        test_player_id = fa_result["free_agents"][0]["player_id"]

        # Test with season stats.
        result = await tools.get_player_stats(league_id, [test_player_id], "season")

        assert "league_id" in result
        assert result["league_id"] == league_id
        assert "player_ids" in result
        assert result["player_ids"] == [test_player_id]
        assert "req_type" in result
        assert result["req_type"] == "season"
        assert "stats" in result

        # If no error, we should have stats data.
        if "error" not in result:
            stats = result["stats"]
            assert isinstance(stats, list)

            # Should have stats for the one player we requested.
            if len(stats) > 0:
                player_stat = stats[0]
                assert "player_id" in player_stat
                assert player_stat["player_id"] == test_player_id
                assert "name" in player_stat
                assert "position_type" in player_stat
                # Stats will vary by sport, but should have some statistical fields.

                print(f"\nSuccessfully retrieved season stats for player ID {test_player_id}")
                print(f"Player name: {player_stat['name']}")
                print(f"Position: {player_stat['position_type']}")
                # Print a few sample stat fields if available.
                stat_keys = [k for k in player_stat.keys() if k not in ['player_id', 'name', 'position_type']]
                if stat_keys:
                    print(f"Sample stats: {stat_keys[:5]}")
            else:
                print(f"\nNo stats available for player ID {test_player_id}")
