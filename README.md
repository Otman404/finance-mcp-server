# yfinance MCP Server

[![smithery badge](https://smithery.ai/badge/@Otman404/finance-mcp-server)](https://smithery.ai/server/@Otman404/finance-mcp-server)
[Model Context Protocol](https://modelcontextprotocol.io/introduction) server that allows LLMs to get accurate and up-to-date prices and news about stock/cryptocurrencies tickers.

## Available Tools

- `get_price_tool`: Get the price of a stock/cryptocurrency ticker
  - Arguments:
    - `ticker` (string): Required - Ticker name or alias (e.g., "BTC-USD", "AAPL")
    - `period` (string): Optional - Time period (e.g., "1d", "5d", "1mo"). Defaults to "1d"
- `get_news_tool`: Get the news of a stock/cryptocurrency ticker.
  - Required arguments:
    - `ticker` (string): Required
    - `count` (string): Optional - Number of articles to retrieve (default: 5)

## Installation

### Installing via Smithery

To install yfinance-mcp-server for Claude Desktop automatically via [Smithery](https://smithery.ai/server/@Otman404/finance-mcp-server):

```bash
npx -y @smithery/cli install @Otman404/finance-mcp-server --client claude
```

### Using uv

Install the package locally

```bash
uv pip install -e .
```

Run the server

```bash
finance-mcp-server
```

Using docker

```bash
# build the container
docker build -t finance-server .

# run the container
docker run -it finance-server
```

## Configuration

## Usage for Claude Desktop

Add the following to [claude_desktop_config.json](https://modelcontextprotocol.io/quickstart/user)

### uvx

```json
"mcpServers": {
  "finance": {
    "command": "uvx",
    "args": ["finance-mcp-server"]
  }
}
```

### docker

```json
{
  "mcpServers": {
    "finance": {
      "command": "docker",
      "args": ["run", "-i", "--rm", "finance-server"]
    }
  }
}
```

## Usage for [5ire](https://github.com/nanbingxyz/5ire)

### uvx

```json
{
  "key": "finance",
  "command": "uvx",
  "args": ["finance-mcp-server"]
}
```

### docker

```json
{
  "key": "finance-server",
  "command": "docker",
  "args": ["run", "-i", "--rm", "finance-server"]
}
```

## Example Interactions

![example](img/example.png)
