# Integration Tests

This directory contains integration tests that interact with the real Yahoo Fantasy API.

## Requirements

- Valid Yahoo API credentials (either `oauth2.json` or environment variables)
- `YAHOO_LEAGUE_ID` environment variable set to a valid league ID

## Running Integration Tests

Integration tests are **not** run as part of the regular test suite to avoid requiring credentials during CI/CD.

To run integration tests:

```bash
# Run all integration tests
pytest tests/integration/ -v

# Run a specific integration test
pytest tests/integration/test_tools_integration.py::TestYahooFantasyToolsIntegration::test_get_league_standings -v
```

## Notes

- Tests will be automatically skipped if credentials are not available
- These tests make real API calls and may be subject to rate limiting
- Results depend on actual league data and may vary over time
