import os
from datetime import datetime
from typing import List, Optional

import pandas as pd

from assessment_app.models.models import Trade, TickData, StockInfo


class MarketService:
    def __init__(self):
        self.data_dir = "assessment_app/data"

    def get_stock_data(self, stock_symbol: str, timestamp: datetime) -> pd.DataFrame:
        """Get stock data for a specific timestamp"""
        file_path = os.path.join(self.data_dir, f"{stock_symbol}.csv")
        if not os.path.exists(file_path):
            return pd.DataFrame()
        
        df = pd.read_csv(file_path)
        df['Date'] = pd.to_datetime(df['Date'])
        df = df[df['Date'].dt.date == timestamp.date()]
        return df

    def get_stock_data_range(self, stock_symbol: str, start_ts: datetime, end_ts: datetime) -> pd.DataFrame:
        """Get stock data for a date range"""
        file_path = os.path.join(self.data_dir, f"{stock_symbol}.csv")
        if not os.path.exists(file_path):
            return pd.DataFrame()
        
        df = pd.read_csv(file_path)
        df['Date'] = pd.to_datetime(df['Date'])
        df = df[(df['Date'].dt.date >= start_ts.date()) & (df['Date'].dt.date <= end_ts.date())]
        return df

    def validate_trade(self, trade: Trade) -> bool:
        """Validate if a trade can be executed"""
        df = self.get_stock_data(trade.stock_symbol, trade.execution_ts)
        if df.empty:
            return False
        
        row = df.iloc[0]
        return row['Low'] <= trade.price <= row['High']

    def get_current_price(self, stock_symbol: str, timestamp: datetime) -> float:
        """Get current price for a stock"""
        df = self.get_stock_data(stock_symbol, timestamp)
        if df.empty:
            return 0.0
        
        row = df.iloc[0]
        return (row['Open'] + row['Close']) / 2

    def get_tick_data(self, stock_symbol: str, timestamp: datetime) -> Optional[TickData]:
        """Get tick data for a stock"""
        df = self.get_stock_data(stock_symbol, timestamp)
        if df.empty:
            return None
        
        row = df.iloc[0]
        return TickData(
            stock_symbol=stock_symbol,
            timestamp=timestamp,
            price=(row['Open'] + row['Close']) / 2,
            open_price=row['Open'],
            high_price=row['High'],
            low_price=row['Low'],
            close_price=row['Close'],
            volume=row['Volume']
        )

    def get_available_stocks(self) -> List[StockInfo]:
        """Get list of available stocks"""
        stocks = []
        for file_name in os.listdir(self.data_dir):
            if file_name.endswith(".csv"):
                stock_symbol = file_name[:-4]  # Remove .csv extension
                stocks.append(StockInfo(
                    stock_symbol=stock_symbol,
                    name=stock_symbol  # Using symbol as name for simplicity
                ))
        return stocks 