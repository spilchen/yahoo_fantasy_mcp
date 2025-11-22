# Yahoo Fantasy MCP Server

A Model Context Protocol (MCP) server that provides access to Yahoo Fantasy Sports data. This server acts as a front-end for the [yahoo_fantasy_api](https://github.com/spilchen/yahoo_fantasy_api) library, allowing AI assistants and other MCP clients to query fantasy league information.

## Features

- Query fantasy league standings and team information
- Retrieve player statistics and projections
- Access matchup data and scoring details
- Get roster information for teams
- Search for players and free agents

## Installation

### From PyPI (when published)

```bash
pip install yahoo-fantasy-mcp
```

### From Source

```bash
git clone https://github.com/yourusername/yahoo_fantasy_mcp.git
cd yahoo_fantasy_mcp
pip install -e .
```

## Prerequisites

Before using this MCP server, you need to set up Yahoo Fantasy API credentials:

1. Register your application at [Yahoo Developer Network](https://developer.yahoo.com/apps/)
2. Obtain your `client_id` and `client_secret`
3. Set up OAuth2 authentication (see [yahoo_fantasy_api documentation](https://github.com/spilchen/yahoo_fantasy_api))

## Configuration

Create a configuration file with your Yahoo API credentials:

```json
{
  "yahoo_client_id": "your_client_id",
  "yahoo_client_secret": "your_client_secret"
}
```

## Usage

### As an MCP Server

Add to your MCP client configuration (e.g., Claude Desktop):

```json
{
  "mcpServers": {
    "yahoo-fantasy": {
      "command": "python",
      "args": ["-m", "yahoo_fantasy_mcp"],
      "env": {
        "YAHOO_CLIENT_ID": "your_client_id",
        "YAHOO_CLIENT_SECRET": "your_client_secret"
      }
    }
  }
}
```

### Standalone

```bash
python -m yahoo_fantasy_mcp
```

## Available Tools

The MCP server exposes the following tools:

- `get_league_standings` - Get current standings for a league
- `get_team_roster` - Get roster for a specific team
- `get_matchup_scores` - Get scores for current/specific matchup
- `get_player_stats` - Get statistics for a player
- `search_players` - Search for players by name
- `get_free_agents` - Get available free agents

## Development

### Setup Development Environment

```bash
# Clone the repository
git clone https://github.com/yourusername/yahoo_fantasy_mcp.git
cd yahoo_fantasy_mcp

# Install development dependencies
pip install -e ".[dev]"
```

### Running Tests

```bash
pytest
```

### Code Quality

```bash
# Run linter
flake8 yahoo_fantasy_mcp tests

# Run type checker
mypy yahoo_fantasy_mcp

# Format code
black yahoo_fantasy_mcp tests
```

## Project Structure

```
yahoo_fantasy_mcp/
├── yahoo_fantasy_mcp/
│   ├── __init__.py
│   ├── __main__.py
│   ├── server.py          # Main MCP server implementation
│   └── tools.py           # Tool implementations
├── tests/
│   ├── __init__.py
│   ├── test_server.py
│   └── test_tools.py
├── README.md
├── setup.py
├── requirements.txt
├── requirements-dev.txt
└── .gitignore
```

## License

MIT License - See LICENSE file for details

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Credits

Built on top of [yahoo_fantasy_api](https://github.com/spilchen/yahoo_fantasy_api) by spilchen.

## Support

For issues and questions:
- File an issue on GitHub
- Check the [yahoo_fantasy_api documentation](https://github.com/spilchen/yahoo_fantasy_api)
