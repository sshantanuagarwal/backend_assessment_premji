import requests
import json
from datetime import datetime, timedelta
import time
import uuid

BASE_URL = "http://localhost:8000"
TEST_USER_ID = str(uuid.uuid4())  # Generate a unique user ID
HEADERS = {"X-User-ID": TEST_USER_ID}  # Headers for authentication
STOCKS = ["RELIANCE", "ICICIBANK", "HDFCBANK", "TATAMOTORS"]


def print_response(response, message):
    print(f"\n{message}")
    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        print(json.dumps(response.json(), indent=2))
    else:
        print(response.text)


def wait_for_server():
    """Wait for the server to be ready"""
    while True:
        try:
            response = requests.get(f"{BASE_URL}/stocks", headers=HEADERS)
            if response.status_code == 200:
                print("Server is ready!")
                break
        except requests.exceptions.ConnectionError:
            print("Waiting for server to start...")
            time.sleep(1)


def get_available_stocks():
    """Get list of available stocks"""
    response = requests.get(f"{BASE_URL}/stocks", headers=HEADERS)
    print_response(response, "Available Stocks:")
    if response.status_code == 200:
        return response.json()
    return None


def get_market_data(stock_symbol: str):
    """Get market data for a stock"""
    # Use a timestamp that exists in our data (with time component)
    current_ts = datetime(2023, 7, 19, 0, 0, 0)
    payload = {
        "stock_symbol": stock_symbol,
        "current_ts": current_ts.isoformat()
    }
    response = requests.post(f"{BASE_URL}/market/data/tick", json=payload, headers=HEADERS)
    print_response(response, f"Market Data for {stock_symbol}:")
    if response.status_code == 200:
        return response.json()
    return None


def create_portfolio(user_id: str):
    """Create a new portfolio"""
    payload = {
        "initial_capital": 100000.0,
        "user_id": user_id
    }
    response = requests.post(f"{BASE_URL}/portfolio", json=payload, headers=HEADERS)
    print_response(response, "Portfolio Creation:")
    if response.status_code == 200:
        return response.json()
    return None


def update_portfolio_timestamp(portfolio_id: str, new_ts: datetime):
    """Update portfolio timestamp"""
    response = requests.put(
        f"{BASE_URL}/portfolio/{portfolio_id}/timestamp",
        json={"new_ts": new_ts.isoformat()},
        headers=HEADERS
    )
    print_response(response, "Portfolio Timestamp Update:")
    if response.status_code == 200:
        return response.json()
    print("Failed to update portfolio timestamp")
    return None


def execute_trade(portfolio_id: str, stock_symbol: str, quantity: int, trade_type: str):
    """Execute a trade"""
    # Use a timestamp that exists in our data (with time component)
    current_ts = datetime(2023, 7, 19, 0, 0, 0)
    # Get current market price
    market_data = get_market_data(stock_symbol)
    if market_data:
        current_price = (market_data["open_price"] + market_data["close_price"]) / 2
        payload = {
            "stock_symbol": stock_symbol,
            "quantity": quantity,
            "price": current_price,
            "trade_type": trade_type,
            "execution_ts": current_ts.isoformat()
        }
        response = requests.post(f"{BASE_URL}/market/trade", json=payload, headers=HEADERS)
        print_response(response, "Trade Execution:")
        if response.status_code == 200:
            return response.json()
    return None


def get_portfolio_net_worth(portfolio_id: str):
    """Get portfolio net worth"""
    response = requests.get(f"{BASE_URL}/portfolio-net-worth", headers=HEADERS)
    print_response(response, "Portfolio Net Worth:")
    if response.status_code == 200:
        return response.json()
    print("Failed to get portfolio net worth")
    return None


def get_stock_analysis(stock_symbol: str):
    """Get stock analysis"""
    # Use a timestamp that exists in our data (with time component)
    end_ts = datetime(2023, 7, 19, 0, 0, 0)
    start_ts = end_ts - timedelta(days=30)
    params = {
        "stock_symbol": stock_symbol,
        "start_ts": start_ts.isoformat(),
        "end_ts": end_ts.isoformat()
    }
    response = requests.get(
        f"{BASE_URL}/analysis/estimate_returns/stock",
        params=params,
        headers=HEADERS
    )
    print_response(response, f"Stock Analysis for {stock_symbol}:")
    if response.status_code == 200:
        return response.json()
    return None


def get_portfolio_analysis(portfolio_id: str):
    """Get portfolio analysis"""
    # Use a timestamp that exists in our data (with time component)
    end_ts = datetime(2023, 7, 19, 0, 0, 0)
    start_ts = end_ts - timedelta(days=30)
    params = {
        "start_ts": start_ts.isoformat(),
        "end_ts": end_ts.isoformat(),
        "portfolio_id": portfolio_id
    }
    response = requests.get(
        f"{BASE_URL}/analysis/estimate_returns/portfolio",
        params=params,
        headers=HEADERS
    )
    print_response(response, "Portfolio Analysis:")
    if response.status_code == 200:
        return response.json()
    return None


def main():
    print("Starting Stock Market Simulator Demo...")
    print(f"Using test user ID: {TEST_USER_ID}")

    # Wait for server to be ready
    wait_for_server()

    params = {
        "name": "my-task-2",
        "group_id": "group-2",
        "start_date": "2025-06-03",
        "end_date": "2025-06-07",
        "estimated_effort": 8.0,
        "weekdays": [1, 2, 3, 4]
    }
    response = requests.post(f"{BASE_URL}/tasks",
                             params=params,
                             headers=HEADERS)
    print_response(response, "Portfolio Analysis:")

    return
    # Get available stocks
    stocks = get_available_stocks()
    if not stocks:
        print("Failed to get available stocks")
        return

    # Get market data for RELIANCE
    for stock in STOCKS:
        market_data = get_market_data(stock)
        if not market_data:
            print("Failed to get market data")
            return

    # Create a new portfolio
    portfolio = create_portfolio(TEST_USER_ID)
    if not portfolio:
        print("Failed to create portfolio")
        return

    portfolio_id = portfolio["id"]

    # Update portfolio timestamp
    new_ts = datetime(2023, 7, 19, 0, 0, 0)
    if not update_portfolio_timestamp(portfolio_id, new_ts):
        print("Failed to update portfolio timestamp")
        return

    # Execute a trade
    for stock in STOCKS:
        trade = execute_trade(portfolio_id, stock, 10, "BUY")
        if not trade:
            print("Failed to execute trade")
            return

    # Get portfolio net worth
    net_worth = get_portfolio_net_worth(portfolio_id)
    if not net_worth:
        print("Failed to get portfolio net worth")
        return

    # Get stock analysis
    for stock in STOCKS:
        stock_analysis = get_stock_analysis(stock)
        if not stock_analysis:
            print("Failed to get stock analysis")
            return

    # Get portfolio analysis
    portfolio_analysis = get_portfolio_analysis(portfolio_id)
    if not portfolio_analysis:
        print("Failed to get portfolio analysis")
        return

    print("\nDemo completed successfully!")


if __name__ == "__main__":
    main()
