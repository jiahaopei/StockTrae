from typing import Dict, List, Optional
from stock_fetcher import StockDataFetcher
from config import Config


class ThresholdChecker:
    def __init__(self, config: Config):
        self.config = config
        self.fetcher = StockDataFetcher()
    
    def check_stock(self, stock_code: str, stock_name: str) -> Optional[Dict]:
        alerts = []
        
        realtime_data = self.fetcher.get_stock_realtime(stock_code)
        if not realtime_data:
            return None
        
        price = realtime_data['price']
        change_percent = realtime_data['change_percent']
        
        if self.config.is_daily_change_enabled():
            rise_threshold = self.config.get_rise_percent_threshold()
            fall_threshold = self.config.get_fall_percent_threshold()
            
            if change_percent >= rise_threshold:
                alerts.append({
                    'type': 'daily_rise',
                    'description': f'单日涨幅达到{rise_threshold}%'
                })
            elif change_percent <= fall_threshold:
                alerts.append({
                    'type': 'daily_fall',
                    'description': f'单日跌幅达到{abs(fall_threshold)}%'
                })
        
        if self.config.is_consecutive_days_enabled():
            consecutive_data = self.fetcher.get_consecutive_days(stock_code)
            rise_days_threshold = self.config.get_rise_days_threshold()
            fall_days_threshold = self.config.get_fall_days_threshold()
            
            if consecutive_data['consecutive_rise'] >= rise_days_threshold:
                alerts.append({
                    'type': 'consecutive_rise',
                    'description': f'连续{consecutive_data["consecutive_rise"]}天上涨（阈值：{rise_days_threshold}天）'
                })
            
            if consecutive_data['consecutive_fall'] >= fall_days_threshold:
                alerts.append({
                    'type': 'consecutive_fall',
                    'description': f'连续{consecutive_data["consecutive_fall"]}天下跌（阈值：{fall_days_threshold}天）'
                })
        
        if alerts:
            return {
                'code': stock_code,
                'name': stock_name,
                'price': price,
                'change_percent': change_percent,
                'alerts': alerts
            }
        
        return None
    
    def check_all_stocks(self, stocks: List[Dict]) -> List[Dict]:
        results = []
        for stock in stocks:
            code = stock['code']
            name = stock['name']
            
            alert = self.check_stock(code, name)
            if alert:
                results.append(alert)
        
        return results
