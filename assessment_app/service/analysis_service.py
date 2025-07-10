from datetime import datetime
import numpy as np
from typing import List, Optional
from assessment_app.models.models import Portfolio, PortfolioHolding, PortfolioAnalysis

class AnalysisService:
    def compute_cagr(self, start_price: float, end_price: float, start_date: datetime, end_date: datetime) -> float:
        """Compute Compound Annual Growth Rate (CAGR)"""
        years = (end_date - start_date).days / 365.0
        if years <= 0 or start_price <= 0:
            return 0.0
        return ((end_price / start_price) ** (1 / years)) - 1

    def compute_portfolio_returns(self, portfolio: Portfolio, holdings: List[PortfolioHolding], start_ts: datetime, end_ts: datetime) -> PortfolioAnalysis:
        """Compute portfolio returns"""
        total_investment = sum(h.average_price * h.quantity for h in holdings)
        current_value = sum(h.current_value for h in holdings)
        returns = current_value - total_investment
        returns_percentage = (returns / total_investment * 100) if total_investment > 0 else 0.0
        
        return PortfolioAnalysis(
            portfolio_id=portfolio.portfolio_id,
            user_id=portfolio.user_id,
            initial_capital=portfolio.initial_capital,
            current_capital=portfolio.current_capital,
            holdings=holdings,
            returns=returns,
            returns_percentage=returns_percentage
        )

    def compute_stock_returns(self, start_price: float, end_price: float, start_ts: datetime, end_ts: datetime) -> float:
        """Compute stock returns"""
        if start_price <= 0:
            return 0.0
        return (end_price - start_price) / start_price * 100

    def compute_portfolio_net_worth(self, portfolio: Portfolio, holdings: List[PortfolioHolding]) -> float:
        """Compute portfolio net worth"""
        holdings_value = sum(h.current_value for h in holdings)
        return portfolio.cash_balance + holdings_value

    def compute_holding_returns(self, holding: PortfolioHolding, start_ts: datetime, end_ts: datetime) -> float:
        """Compute returns for a single holding"""
        investment = holding.average_price * holding.quantity
        if investment <= 0:
            return 0.0
        return (holding.current_value - investment) / investment * 100

    def compute_portfolio_risk_metrics(self, portfolio: Portfolio, holdings: List[PortfolioHolding], start_ts: datetime, end_ts: datetime) -> PortfolioAnalysis:
        """Compute portfolio risk metrics"""
        # Calculate daily returns for each holding
        daily_returns = []
        for holding in holdings:
            daily_return = self.compute_holding_returns(holding, start_ts, end_ts)
            daily_returns.append(daily_return)
        
        if not daily_returns:
            return PortfolioAnalysis(
                portfolio_id=portfolio.portfolio_id,
                user_id=portfolio.user_id,
                initial_capital=portfolio.initial_capital,
                current_capital=portfolio.current_capital,
                holdings=holdings,
                volatility=0.0,
                sharpe_ratio=0.0,
                max_drawdown=0.0
            )
        
        # Calculate risk metrics
        volatility = np.std(daily_returns) if len(daily_returns) > 1 else 0.0
        avg_return = np.mean(daily_returns)
        risk_free_rate = 0.02  # Assuming 2% risk-free rate
        sharpe_ratio = (avg_return - risk_free_rate) / volatility if volatility > 0 else 0.0
        max_drawdown = self._calculate_max_drawdown(daily_returns)
        
        return PortfolioAnalysis(
            portfolio_id=portfolio.portfolio_id,
            user_id=portfolio.user_id,
            initial_capital=portfolio.initial_capital,
            current_capital=portfolio.current_capital,
            holdings=holdings,
            volatility=volatility,
            sharpe_ratio=sharpe_ratio,
            max_drawdown=max_drawdown
        )

    def compute_stock_risk_metrics(self, prices: List[float], start_ts: datetime, end_ts: datetime) -> PortfolioAnalysis:
        """Compute risk metrics for a single stock"""
        if len(prices) < 2:
            return PortfolioAnalysis(
                volatility=0.0,
                sharpe_ratio=0.0,
                max_drawdown=0.0
            )
        
        # Calculate daily returns
        daily_returns = [(prices[i] - prices[i-1]) / prices[i-1] * 100 for i in range(1, len(prices))]
        
        # Calculate risk metrics
        volatility = np.std(daily_returns)
        avg_return = np.mean(daily_returns)
        risk_free_rate = 0.02  # Assuming 2% risk-free rate
        sharpe_ratio = (avg_return - risk_free_rate) / volatility if volatility > 0 else 0.0
        max_drawdown = self._calculate_max_drawdown(prices)
        
        return PortfolioAnalysis(
            volatility=volatility,
            sharpe_ratio=sharpe_ratio,
            max_drawdown=max_drawdown
        )

    def _calculate_max_drawdown(self, prices: List[float]) -> float:
        """Calculate maximum drawdown from a list of prices"""
        if len(prices) < 2:
            return 0.0
        
        peak = prices[0]
        max_drawdown = 0.0
        
        for price in prices[1:]:
            if price > peak:
                peak = price
            drawdown = (peak - price) / peak
            max_drawdown = max(max_drawdown, drawdown)
        
        return max_drawdown * 100 