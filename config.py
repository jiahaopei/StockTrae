import yaml
from pathlib import Path
from typing import List, Dict, Any


class Config:
    def __init__(self, config_path: str = "config.yaml"):
        self.config_path = config_path
        self.config = self._load_config()
    
    def _load_config(self) -> Dict[str, Any]:
        config_file = Path(self.config_path)
        if not config_file.exists():
            raise FileNotFoundError(f"配置文件 {self.config_path} 不存在")
        
        with open(config_file, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    
    def get_stocks(self) -> List[Dict[str, str]]:
        return self.config.get('stocks', [])
    
    def get_thresholds(self) -> Dict[str, Any]:
        return self.config.get('thresholds', {})
    
    def get_schedule(self) -> Dict[str, Any]:
        return self.config.get('schedule', {})
    
    def get_output_config(self) -> Dict[str, str]:
        return self.config.get('output', {})
    
    def is_consecutive_days_enabled(self) -> bool:
        return self.config.get('thresholds', {}).get('consecutive_days', {}).get('enabled', False)
    
    def get_rise_days_threshold(self) -> int:
        return self.config.get('thresholds', {}).get('consecutive_days', {}).get('rise_days', 3)
    
    def get_fall_days_threshold(self) -> int:
        return self.config.get('thresholds', {}).get('consecutive_days', {}).get('fall_days', 3)
    
    def is_daily_change_enabled(self) -> bool:
        return self.config.get('thresholds', {}).get('daily_change', {}).get('enabled', False)
    
    def get_rise_percent_threshold(self) -> float:
        return self.config.get('thresholds', {}).get('daily_change', {}).get('rise_percent', 5.0)
    
    def get_fall_percent_threshold(self) -> float:
        return self.config.get('thresholds', {}).get('daily_change', {}).get('fall_percent', -5.0)
    
    def is_schedule_enabled(self) -> bool:
        return self.config.get('schedule', {}).get('enabled', False)
    
    def get_schedule_time(self) -> str:
        return self.config.get('schedule', {}).get('time', '15:00')
