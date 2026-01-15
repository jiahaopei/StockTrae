#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import argparse
from config import Config
from stock_fetcher import StockDataFetcher
from threshold_checker import ThresholdChecker
from report_generator import ReportGenerator
from scheduler import TaskScheduler


def main():
    parser = argparse.ArgumentParser(description='股票监控程序')
    parser.add_argument('--config', type=str, default='config.yaml', help='配置文件路径')
    parser.add_argument('--once', action='store_true', help='执行一次任务后退出')
    parser.add_argument('--schedule', action='store_true', help='启动定时任务')
    
    args = parser.parse_args()
    
    try:
        config = Config(args.config)
    except FileNotFoundError as e:
        print(f"错误: {e}")
        sys.exit(1)
    
    fetcher = StockDataFetcher()
    checker = ThresholdChecker(config)
    generator = ReportGenerator(config)
    
    def run_monitor():
        print("\n" + "=" * 80)
        print("开始执行股票监控任务...")
        print("=" * 80 + "\n")
        
        stocks = config.get_stocks()
        print(f"监控股票数量: {len(stocks)}")
        
        alerts = checker.check_all_stocks(stocks)
        
        if alerts:
            print(f"\n发现 {len(alerts)} 只股票触发阈值:\n")
            
            report = generator.generate_console_report(alerts)
            print(report)
            
            filepath = generator.generate_report(alerts)
            print(f"\n报告已保存至: {filepath}")
        else:
            print("\n没有股票触发阈值")
        
        print("\n" + "=" * 80)
        print("股票监控任务完成")
        print("=" * 80 + "\n")
    
    if args.once:
        run_monitor()
    elif args.schedule:
        if config.is_schedule_enabled():
            scheduler = TaskScheduler(config)
            scheduler.schedule_task(run_monitor)
            
            try:
                scheduler.run()
            except KeyboardInterrupt:
                print("\n收到中断信号，正在停止...")
                scheduler.stop()
        else:
            print("定时任务未启用，请在配置文件中启用 schedule.enabled")
            sys.exit(1)
    else:
        print("请指定运行模式:")
        print("  --once    : 执行一次任务后退出")
        print("  --schedule: 启动定时任务")
        print("\n示例:")
        print("  python main.py --once")
        print("  python main.py --schedule")


if __name__ == '__main__':
    main()
