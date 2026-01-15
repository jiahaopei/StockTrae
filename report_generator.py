from pathlib import Path
from datetime import datetime
from typing import List, Dict
from config import Config


class ReportGenerator:
    def __init__(self, config: Config):
        self.config = config
    
    def generate_report(self, alerts: List[Dict]) -> str:
        if not alerts:
            return ""
        
        output_config = self.config.get_output_config()
        directory = Path(output_config.get('directory', 'output'))
        directory.mkdir(exist_ok=True)
        
        date_str = datetime.now().strftime('%Y%m%d')
        filename = output_config.get('filename', 'stock_alert_{date}.txt').format(date=date_str)
        filepath = directory / filename
        
        content = self._format_report(alerts)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return str(filepath)
    
    def _format_report(self, alerts: List[Dict]) -> str:
        lines = []
        lines.append("=" * 80)
        lines.append("股票监控报告")
        lines.append(f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        lines.append("=" * 80)
        lines.append("")
        
        for idx, alert in enumerate(alerts, 1):
            lines.append(f"【{idx}】股票代码: {alert['code']}")
            lines.append(f"股票名称: {alert['name']}")
            lines.append(f"当前价格: {alert['price']:.2f} 元")
            lines.append(f"当日涨跌: {alert['change_percent']:.2f}%")
            lines.append("")
            lines.append("触发阈值:")
            
            for alert_item in alert['alerts']:
                lines.append(f"  - {alert_item['description']}")
            
            lines.append("")
            lines.append("-" * 80)
            lines.append("")
        
        lines.append(f"总计: {len(alerts)} 只股票触发阈值")
        lines.append("=" * 80)
        
        return '\n'.join(lines)
    
    def generate_console_report(self, alerts: List[Dict]) -> str:
        return self._format_report(alerts)
