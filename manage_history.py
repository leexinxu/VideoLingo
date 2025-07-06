#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
# ------------
# Simple History Manager
# ------------
# Simplified history management tool
# ------------
"""

import os
import sys
from history_manager import HistoryManager

def show_menu():
    """显示菜单"""
    print("\n📁 VideoLingo History Manager")
    print("=" * 40)
    print("1. 查看所有存档视频")
    print("2. 查看中字播放列表")
    print("3. 查看中配播放列表")
    print("4. 清理旧文件")
    print("5. 导出摘要")
    print("0. 退出")
    print("=" * 40)

def main():
    """主函数"""
    manager = HistoryManager()
    
    while True:
        show_menu()
        choice = input("请选择操作 (0-5): ").strip()
        
        if choice == "0":
            print("👋 再见!")
            break
        elif choice == "1":
            print("\n📁 所有存档视频:")
            manager.list_archived_videos()
        elif choice == "2":
            print("\n📁 中字播放列表:")
            manager.list_archived_videos("中字")
        elif choice == "3":
            print("\n📁 中配播放列表:")
            manager.list_archived_videos("中配")
        elif choice == "4":
            days = input("清理多少天前的文件? (默认30天): ").strip()
            if not days:
                days = 30
            else:
                try:
                    days = int(days)
                except ValueError:
                    print("❌ 请输入有效的天数")
                    continue
            
            confirm = input(f"确定要清理{days}天前的文件吗? (y/N): ").strip().lower()
            if confirm == 'y':
                manager.clean_history(days)
            else:
                print("❌ 操作已取消")
        elif choice == "5":
            try:
                filename = input("导出文件名 (默认: history_summary.json): ").strip()
                if not filename:
                    filename = "history_summary.json"
                manager.export_summary(filename)
            except EOFError:
                print("❌ 输入错误")
                continue
        else:
            print("❌ 无效选择，请重试")
        
        input("\n按回车键继续...")

if __name__ == "__main__":
    main() 