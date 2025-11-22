"""Tests for the MCP server implementation."""

import pytest
from yahoo_fantasy_mcp.server import create_server


class TestServer:
    """Test cases for the MCP server."""

    def test_create_server(self):
        """Test that server can be created with valid credentials."""
        server = create_server("test_client_id", "test_client_secret")
        assert server is not None
        assert server.name == "yahoo-fantasy"

    @pytest.mark.asyncio
    async def test_list_tools(self):
        """Test that tools are properly listed."""
        server = create_server("test_client_id", "test_client_secret")
        # TODO(SPILLY): Add proper test implementation.
        assert server is not None

    @pytest.mark.asyncio
    async def test_call_tool_get_league_standings(self):
        """Test calling get_league_standings tool."""
        # TODO(SPILLY): Implement test with mock data.
        pass

    @pytest.mark.asyncio
    async def test_call_tool_get_team_roster(self):
        """Test calling get_team_roster tool."""
        # TODO(SPILLY): Implement test with mock data.
        pass

    @pytest.mark.asyncio
    async def test_call_tool_get_matchup_scores(self):
        """Test calling get_matchup_scores tool."""
        # TODO(SPILLY): Implement test with mock data.
        pass

    @pytest.mark.asyncio
    async def test_call_tool_get_player_stats(self):
        """Test calling get_player_stats tool."""
        # TODO(SPILLY): Implement test with mock data.
        pass

    @pytest.mark.asyncio
    async def test_call_tool_search_players(self):
        """Test calling search_players tool."""
        # TODO(SPILLY): Implement test with mock data.
        pass

    @pytest.mark.asyncio
    async def test_call_tool_get_free_agents(self):
        """Test calling get_free_agents tool."""
        # TODO(SPILLY): Implement test with mock data.
        pass

    @pytest.mark.asyncio
    async def test_call_tool_unknown(self):
        """Test calling an unknown tool returns an error."""
        # TODO(SPILLY): Implement test.
        pass
