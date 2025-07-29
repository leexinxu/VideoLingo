#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试真实的playlist_monitor.py中的函数
"""

import os
import sys
import json

# Add current directory to path for imports
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

# 导入真实的PlaylistMonitor类
from playlist_monitor import PlaylistMonitor

def test_real_functions():
    """测试真实的函数"""
    
    # 创建PlaylistMonitor实例
    print("创建PlaylistMonitor实例...")
    monitor = PlaylistMonitor()
    
    # 测试数据
    playlist_name = "中配"
    video_title = "Who Will Lead Europe's Space Future？ ESA Selects 5 Companies for Launcher Challenge"
    
    # 读取terminology.json中的theme
    terminology_file = "/Volumes/Data/AI/VideoLingo/history/中配/0Lj_YnaDqLQ_Who Will Lead Europes Space Future ESA Selects 5 C/log/terminology.json"
    
    try:
        with open(terminology_file, 'r', encoding='utf-8') as f:
            terminology_data = json.load(f)
            theme_title = terminology_data.get('theme', video_title)
            print(f"从terminology.json读取theme: {theme_title}")
    except Exception as e:
        print(f"读取terminology.json错误: {e}")
        theme_title = video_title
    
    print("=" * 100)
    print("🧪 测试真实的标题生成函数")
    print("=" * 100)
    print(f"播放列表名称: {playlist_name}")
    print(f"原始英文标题: {video_title}")
    print(f"主题描述: {theme_title[:50]}...")
    print("-" * 100)
    
    # 测试1: 翻译标题函数
    print("🔤 测试1: translate_title() 函数")
    try:
        translated_title = monitor.translate_title(video_title)
        print(f"   翻译结果: {translated_title}")
        print(f"   翻译成功: {'✅' if translated_title != video_title else '❌'}")
    except Exception as e:
        print(f"   翻译错误: {e}")
        translated_title = video_title
    
    print()
    
    # 测试2: 生成新标题函数
    print("🎯 测试2: generate_new_title() 函数")
    try:
        final_title = monitor.generate_new_title(playlist_name, video_title, theme_title)
        print(f"   最终标题: {final_title}")
        print(f"   标题长度: {len(final_title)} 字符")
        
        # 检查标题格式
        expected_parts = [f"【{playlist_name}】", "——"]
        format_check = all(part in final_title for part in expected_parts)
        print(f"   格式正确: {'✅' if format_check else '❌'}")
        
    except Exception as e:
        print(f"   生成标题错误: {e}")
        final_title = theme_title
    
    print("-" * 100)
    print("📊 最终结果对比:")
    print(f"   原始格式: {theme_title}")
    print(f"   新格式: {final_title}")
    print("   提升效果: 新格式包含播放列表标识和翻译后的英文标题")
    print("=" * 100)
    
    return final_title

if __name__ == "__main__":
    test_real_functions()