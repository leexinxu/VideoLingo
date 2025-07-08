#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
# ------------
# Log Cleanup Script
# ------------
# Clean up old log files and keep only the main log file
# ------------
"""

import os
import glob
from datetime import datetime

def cleanup_logs():
    """清理旧的日志文件"""
    logs_dir = "logs"
    
    if not os.path.exists(logs_dir):
        print("Logs directory not found")
        return
    
    # 要保留的主日志文件
    main_log = "playlist_monitor.log"
    
    # 获取所有日志文件
    log_files = glob.glob(os.path.join(logs_dir, "*.log"))
    
    print(f"Found {len(log_files)} log files:")
    for log_file in log_files:
        file_size = os.path.getsize(log_file)
        file_name = os.path.basename(log_file)
        print(f"  - {file_name}: {file_size / 1024:.1f}KB")
    
    # 删除除了主日志文件之外的所有文件
    deleted_count = 0
    for log_file in log_files:
        file_name = os.path.basename(log_file)
        if file_name != main_log:
            try:
                os.remove(log_file)
                print(f"Deleted: {file_name}")
                deleted_count += 1
            except Exception as e:
                print(f"Error deleting {file_name}: {e}")
    
    print(f"\nCleanup completed: {deleted_count} files deleted")
    
    # 显示剩余文件
    remaining_files = glob.glob(os.path.join(logs_dir, "*.log"))
    if remaining_files:
        print(f"\nRemaining log files:")
        for log_file in remaining_files:
            file_size = os.path.getsize(log_file)
            file_name = os.path.basename(log_file)
            print(f"  - {file_name}: {file_size / 1024:.1f}KB")
    else:
        print("\nNo log files remaining")

if __name__ == "__main__":
    cleanup_logs() 