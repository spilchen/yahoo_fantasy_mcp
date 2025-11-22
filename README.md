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
2. Obtain your `consumer_key` and `consumer_secret`
3. Set up OAuth2 authentication using one of the methods below

## Configuration

There are two ways to authenticate with Yahoo's API:

### Option 1: Using oauth2.json (Recommended)

Create an `oauth2.json` file with your Yahoo OAuth credentials. You can generate this file using the [yahoo_fantasy_api](https://github.com/spilchen/yahoo_fantasy_api) authentication flow:

```python
from yahoo_oauth import OAuth2

# This will prompt you to authorize via browser
sc = OAuth2(None, None, from_file='oauth2.json')
```

The `oauth2.json` file will look like:

```json
{
  "access_token": "...",
  "consumer_key": "your_consumer_key",
  "consumer_secret": "your_consumer_secret",
  "guid": "...",
  "refresh_token": "...",
  "token_time": 1234567890.123456,
  "token_type": "bearer"
}
```

### Option 2: Using Environment Variables

Set the following environment variables:

```bash
export YAHOO_CLIENT_ID="your_consumer_key"
export YAHOO_CLIENT_SECRET="your_consumer_secret"
```

## Usage

### As an MCP Server

#### With oauth2.json file (default)

Add to your MCP client configuration (e.g., Claude Desktop):

```json
{
  "mcpServers": {
    "yahoo-fantasy": {
      "command": "python",
      "args": ["-m", "yahoo_fantasy_mcp"],
      "cwd": "/path/to/directory/with/oauth2.json"
    }
  }
}
```

Or specify a custom path:

```json
{
  "mcpServers": {
    "yahoo-fantasy": {
      "command": "python",
      "args": ["-m", "yahoo_fantasy_mcp", "--oauth2-file", "/path/to/oauth2.json"]
    }
  }
}
```

#### With environment variables

```json
{
  "mcpServers": {
    "yahoo-fantasy": {
      "command": "python",
      "args": ["-m", "yahoo_fantasy_mcp"],
      "env": {
        "YAHOO_CLIENT_ID": "your_consumer_key",
        "YAHOO_CLIENT_SECRET": "your_consumer_secret"
      }
    }
  }
}
```

### Standalone

```bash
# Using oauth2.json in current directory (default)
python -m yahoo_fantasy_mcp

# Using oauth2.json from custom path
python -m yahoo_fantasy_mcp --oauth2-file /path/to/oauth2.json

# Using environment variables
YAHOO_CLIENT_ID=your_key YAHOO_CLIENT_SECRET=your_secret python -m yahoo_fantasy_mcp
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
