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

### Setting Your League ID

The server requires a `YAHOO_LEAGUE_ID` environment variable to know which league to query.

**Finding your League ID:**

If you don't know your league ID, simply run the server without setting `YAHOO_LEAGUE_ID`:

```bash
python -m yahoo_fantasy_mcp
```

The server will list all leagues you're part of and then exit. Example output:

```
============================================================
YAHOO_LEAGUE_ID not set - Listing available leagues
============================================================

Checking NFL leagues...
Checking MLB leagues...

Found the following leagues:

1. [NFL 2024] My Fantasy League
   League ID: 423.l.123456

2. [MLB 2024] Baseball League
   League ID: 412.l.789012

To use one of these leagues, set the YAHOO_LEAGUE_ID environment variable:

  export YAHOO_LEAGUE_ID=<league_id>

For example:
  export YAHOO_LEAGUE_ID=423.l.123456
```

Then set the environment variable:

```bash
export YAHOO_LEAGUE_ID=423.l.123456
```

## Usage

### As an MCP Server

This server uses the **stdio transport** protocol, communicating via standard input/output streams. It does not listen on any network port.

#### Transport Type

- **Type**: stdio (standard input/output)
- **Protocol**: The server reads JSON-RPC messages from stdin and writes responses to stdout
- **Connection**: Invoked as a subprocess by the MCP client

#### Required Environment Variables

The server requires the following environment variable to be set:

- `YAHOO_LEAGUE_ID` - The ID of your Yahoo Fantasy league (e.g., "423.l.123456")

#### Optional Environment Variables

Depending on your authentication method, you may need:

- `YAHOO_CLIENT_ID` - Your Yahoo API consumer key (if not using oauth2.json)
- `YAHOO_CLIENT_SECRET` - Your Yahoo API consumer secret (if not using oauth2.json)

#### Command-Line Arguments

- `--oauth2-file <path>` - Path to oauth2.json file (default: "oauth2.json" in current directory)

#### MCP Client Configuration

The server should be configured in your MCP client as a stdio server. Below are example configurations for common MCP clients.

##### With oauth2.json file (recommended)

The server will automatically look for `oauth2.json` in the current working directory.

```json
{
  "mcpServers": {
    "yahoo-fantasy": {
      "command": "python",
      "args": ["-m", "yahoo_fantasy_mcp"],
      "cwd": "/path/to/directory/with/oauth2.json",
      "env": {
        "YAHOO_LEAGUE_ID": "423.l.123456"
      }
    }
  }
}
```

Or specify a custom path to the oauth2.json file:

```json
{
  "mcpServers": {
    "yahoo-fantasy": {
      "command": "python",
      "args": ["-m", "yahoo_fantasy_mcp", "--oauth2-file", "/path/to/oauth2.json"],
      "env": {
        "YAHOO_LEAGUE_ID": "423.l.123456"
      }
    }
  }
}
```

##### With environment variables

If you don't have an oauth2.json file, you can provide credentials via environment variables:

```json
{
  "mcpServers": {
    "yahoo-fantasy": {
      "command": "python",
      "args": ["-m", "yahoo_fantasy_mcp"],
      "env": {
        "YAHOO_CLIENT_ID": "your_consumer_key",
        "YAHOO_CLIENT_SECRET": "your_consumer_secret",
        "YAHOO_LEAGUE_ID": "423.l.123456"
      }
    }
  }
}
```

#### Important Notes

- The server must be able to find either the `oauth2.json` file or the environment variables for authentication.
- If using `oauth2.json`, ensure the `cwd` (current working directory) is set to the directory containing the file, or use the `--oauth2-file` argument to specify the full path.
- The server will automatically refresh OAuth tokens as needed.
- On first run with environment variables, you'll need to complete the OAuth flow via browser.

### Standalone Testing

You can test the server standalone to verify it's working correctly:

```bash
# Using oauth2.json in current directory (default)
export YAHOO_LEAGUE_ID=423.l.123456
python -m yahoo_fantasy_mcp

# Using oauth2.json from custom path
export YAHOO_LEAGUE_ID=423.l.123456
python -m yahoo_fantasy_mcp --oauth2-file /path/to/oauth2.json

# Using environment variables
export YAHOO_LEAGUE_ID=423.l.123456
YAHOO_CLIENT_ID=your_key YAHOO_CLIENT_SECRET=your_secret python -m yahoo_fantasy_mcp
```

Note: When run standalone without an MCP client, the server will wait for JSON-RPC messages on stdin. This is primarily useful for testing that the server starts correctly and authentication works.

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
