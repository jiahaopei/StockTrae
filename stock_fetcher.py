import akshare as ak
import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, List, Optional


class StockDataFetcher:
    def __init__(self):
        pass
    
    def get_stock_realtime(self, stock_code: str) -> Optional[Dict[str, float]]:
        try:
            df = ak.stock_zh_a_spot_em()
            stock_data = df[df['代码'] == stock_code]
            
            if stock_data.empty:
                return None
            
            row = stock_data.iloc[0]
            return {
                'code': row['代码'],
                'name': row['名称'],
                'price': float(row['最新价']),
                'change_percent': float(row['涨跌幅'])
            }
        except Exception as e:
            print(f"获取股票 {stock_code} 实时数据失败: {e}")
            return None
    
    def get_stock_history(self, stock_code: str, days: int = 30) -> Optional[pd.DataFrame]:
        try:
            end_date = datetime.now().strftime('%Y%m%d')
            start_date = (datetime.now() - timedelta(days=days * 2)).strftime('%Y%m%d')
            
            df = ak.stock_zh_a_hist(symbol=stock_code, period="daily", 
                                   start_date=start_date, end_date=end_date, adjust="qfq")
            
            if df.empty:
                return None
            
            df['涨跌幅'] = df['涨跌幅'].astype(float)
            df['收盘'] = df['收盘'].astype(float)
            df['日期'] = pd.to_datetime(df['日期'])
            
            return df.tail(days)
        except Exception as e:
            print(f"获取股票 {stock_code} 历史数据失败: {e}")
            return None
    
    def get_consecutive_days(self, stock_code: str, days: int = 30) -> Dict[str, int]:
        df = self.get_stock_history(stock_code, days)
        
        if df is None or df.empty:
            return {'consecutive_rise': 0, 'consecutive_fall': 0}
        
        consecutive_rise = 0
        consecutive_fall = 0
        
        for _, row in df.iterrows():
            if row['涨跌幅'] > 0:
                consecutive_rise += 1
                consecutive_fall = 0
            elif row['涨跌幅'] < 0:
                consecutive_fall += 1
                consecutive_rise = 0
            else:
                consecutive_rise = 0
                consecutive_fall = 0
        
        return {
            'consecutive_rise': consecutive_rise,
            'consecutive_fall': consecutive_fall
        }
    
    def get_multiple_stocks_data(self, stock_codes: List[str]) -> List[Dict]:
        results = []
        for code in stock_codes:
            data = self.get_stock_realtime(code)
            if data:
                results.append(data)
        return results
