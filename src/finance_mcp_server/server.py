import yfinance as yf
from typing import Any
from mcp.server.fastmcp import FastMCP
from datetime import datetime

mcp = FastMCP("finance")


ticker_map = {
    # Cryptocurrencies (Mapping names and symbols to SYMBOL-USD format)
    "bitcoin": "BTC-USD",
    "btc usd": "BTC-USD",
    "btc-usd": "BTC-USD",
    "btc": "BTC-USD",
    "ethereum": "ETH-USD",
    "eth": "ETH-USD",
    "ripple": "XRP-USD",
    "xrp": "XRP-USD",
    "cardano": "ADA-USD",
    "ada": "ADA-USD",
    "solana": "SOL-USD",
    "sol": "SOL-USD",
    "dogecoin": "DOGE-USD",
    "doge": "DOGE-USD",
    "polkadot": "DOT-USD",
    "dot": "DOT-USD",
    "litecoin": "LTC-USD",
    "ltc": "LTC-USD",
    "chainlink": "LINK-USD",
    "link": "LINK-USD",
    "bitcoin cash": "BCH-USD",
    "bch": "BCH-USD",
    "stellar": "XLM-USD",
    "xlm": "XLM-USD",
    "binance coin": "BNB-USD",
    "bnb": "BNB-USD",
    "shiba inu": "SHIB-USD",
    "shib": "SHIB-USD",
    "tron": "TRX-USD",
    "trx": "TRX-USD",
    "avalanche": "AVAX-USD",
    "avax": "AVAX-USD",
    "polygon": "MATIC-USD",
    "matic": "MATIC-USD",
    # Major US Stocks (Mapping common names/variations to Ticker)
    "apple": "AAPL",
    "apple stock": "AAPL",
    "microsoft": "MSFT",
    "microsoft stock": "MSFT",
    "google": "GOOGL",  # Often refers to Class A
    "alphabet": "GOOGL",
    "alphabet class a": "GOOGL",
    "alphabet class c": "GOOG",
    "amazon": "AMZN",
    "amazon stock": "AMZN",
    "meta": "META",
    "meta platforms": "META",
    "facebook": "META",  # Common old name
    "tesla": "TSLA",
    "tesla stock": "TSLA",
    "nvidia": "NVDA",
    "nvidia stock": "NVDA",
    "berkshire hathaway": "BRK-B",  # Class B is more commonly traded
    "berkshire hathaway class b": "BRK-B",
    "berkshire hathaway class a": "BRK-A",
    "jpmorgan chase": "JPM",
    "jpmorgan": "JPM",
    "jp morgan": "JPM",
    "johnson & johnson": "JNJ",
    "johnson and johnson": "JNJ",
    "visa": "V",
    "mastercard": "MA",
    "bank of america": "BAC",
    "home depot": "HD",
    "procter & gamble": "PG",
    "procter and gamble": "PG",
    "netflix": "NFLX",
    "disney": "DIS",
    "walt disney": "DIS",
    "intel": "INTC",
    "cisco": "CSCO",
    "verizon": "VZ",
    "at&t": "T",
    "boeing": "BA",
    "ford": "F",
    "general motors": "GM",
    # Major Indices (Mapping names to yfinance symbol)
    "s&p 500": "^GSPC",
    "s&p500": "^GSPC",
    "sp500": "^GSPC",
    "spx": "^GSPC",  # Common short name
    "nasdaq": "^IXIC",
    "nasdaq composite": "^IXIC",
    "dow jones": "^DJI",
    "dow jones industrial average": "^DJI",
    "the dow": "^DJI",
    "dji": "^DJI",
    "russell 2000": "^RUT",
    "vix": "^VIX",  # Volatility Index
    # Forex (Mapping common pairs to SYMBOLA-SYMBOLB=X format)
    "eurusd": "EURUSD=X",
    "euro dollar": "EURUSD=X",
    "usdjpy": "JPY=X",  # Note: yfinance uses JPY=X for USD/JPY
    "dollar yen": "JPY=X",
    "gbpusd": "GBPUSD=X",
    "pound dollar": "GBPUSD=X",
    "audusd": "AUDUSD=X",
    "aussie dollar": "AUDUSD=X",
    "usdcad": "CAD=X",  # USD/CAD
    "dollar loonie": "CAD=X",
    "usdchf": "CHF=X",  # USD/Swiss Franc
    "dollar swiss": "CHF=X",
    # Commodities/Futures (Mapping names to yfinance symbol, often =F)
    "gold": "GC=F",
    "gold futures": "GC=F",
    "crude oil": "CL=F",
    "oil": "CL=F",
    "wti crude": "CL=F",
    "brent crude": "BZ=F",
    "silver": "SI=F",
    "silver futures": "SI=F",
    "natural gas": "NG=F",
    "corn": "ZC=F",
    "wheat": "ZW=F",
    "soybeans": "ZS=F",
    # Major ETFs (Mapping names/symbols)
    "spy": "SPY",  # S&P 500 ETF
    "qqq": "QQQ",  # Nasdaq 100 ETF
    "dia": "DIA",  # Dow Jones ETF
    "gld": "GLD",  # Gold ETF
    "slv": "SLV",  # Silver ETF
    "uso": "USO",  # Oil ETF
    "vti": "VTI",  # Vanguard Total Stock Market ETF
    "agg": "AGG",  # iShares Core U.S. Aggregate Bond ETF
}


def ticker_mapper(ticker: str) -> str:
    """
    Validate and map the ticker symbol to its yfinance format.
    """
    ticker = ticker.lower().strip()
    mapped_ticker = ticker_map.get(ticker)
    if mapped_ticker:
        return mapped_ticker
    return ticker.upper()


async def get_price(ticker: str, perdiod: str) -> Any:
    return yf.Ticker(ticker).history(period=perdiod)


async def get_news(ticker: str, count: int) -> Any:
    ticker = yf.Ticker(ticker)
    return ticker.get_news(count=count, tab="news")


@mcp.tool(name="get_price", description="Get the price of a stock/crypto ticker.")
async def get_price_tool(ticker: str, period: str = "1d") -> str:

    ticker = ticker_mapper(ticker)
    try:
        response = await get_price(ticker, period)
        response.index = response.index.strftime("%B %d, %Y %I:%M")
        text = ""
        for index, row in response.iterrows():
            text += f"Open: ${row['Open']:.3f}, High: ${row['High']:.3f}, Low: ${row['Low']:.3f}, Close: ${row['Close']:.3f}, Volume: ${row['Volume']:.3f}\n "
        return text
    except KeyError:
        return f"{ticker} symbol not found"


@mcp.tool(name="get_news", description="Get the news of a stock/crypto ticker.")
async def get_news_tool(ticker: str, count: int = 5) -> str:

    ticker = ticker_mapper(ticker)
    try:
        response = await get_news(ticker, count)

        text = ""
        for news in response:
            publication_date = datetime.fromisoformat(
                news["content"]["pubDate"].replace("Z", "+00:00")
            ).strftime("%Y-%m-%d %H:%M:%S")
            article_link = news["content"]["provider"]["url"]
            article_title = news["content"]["title"]
            article_publisher = news["content"]["provider"]["displayName"]
            article_summary = news["content"]["summary"]
            text += f"Date: {publication_date}, Title: {article_title}, Publisher: {article_publisher}, Link: {article_link}, Summary: {article_summary}\n"
        return text
    except KeyError:
        return f"{ticker} symbol not found"

def main() -> None:
    print("Starting Finance MCP server")
    mcp.run(transport="stdio")

if __name__ == "__main__":
    main()