"""Unit tests for the MCP resource metadata helpers."""

from yahoo_fantasy_mcp import server


def test_league_resource_includes_configured_id():
    resources = server._list_league_resources("466.l.223398")
    assert len(resources) == 1

    resource = resources[0]
    assert str(resource.uri) == server._LEAGUE_RESOURCE_URI
    assert resource.name == "yahoo-league-id"
    assert "466.l.223398" in resource.description
    assert resource.mimeType == "application/json"
    assert resource.meta == {"league_id": "466.l.223398"}
    assert resource.size == len("466.l.223398")


def test_league_resource_handles_missing_env(monkeypatch):
    monkeypatch.delenv(server._YAHOO_LEAGUE_ENV, raising=False)
    resources = server._list_league_resources(None)
    assert len(resources) == 1

    resource = resources[0]
    assert str(resource.uri) == server._LEAGUE_RESOURCE_URI
    assert server._YAHOO_LEAGUE_ENV in resource.description
    assert resource.meta is None
    assert resource.size is None
