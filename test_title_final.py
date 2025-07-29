#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
最终测试：演示标题生成功能（使用预定义翻译避免API问题）
"""

import os
import sys
import json

# Add current directory to path for imports
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

class FinalTitleTester:
    def __init__(self):
        # 预定义的翻译结果，避免API问题
        self.translation_dict = {
            "Who Will Lead Europe's Space Future？ ESA Selects 5 Companies for Launcher Challenge": "谁将引领欧洲的太空未来？欧空局选定5家公司参与运载火箭挑战"
        }
    
    def translate_title(self, text_to_translate: str) -> str:
        """将英文标题翻译成中文（使用预定义翻译）"""
        translated = self.translation_dict.get(text_to_translate, text_to_translate)
        print(f"Title translation: '{text_to_translate}' -> '{translated}'")
        return translated
    
    def generate_new_title(self, playlist_name: str, video_title: str, theme_title: str) -> str:
        """生成新的标题格式：【{playlist_name}】{video_title}——{theme_title}"""
        # 翻译英文标题
        translated_title = self.translate_title(video_title)
        
        # 生成新标题
        new_title = f"【{playlist_name}】{translated_title}——{theme_title}"
        
        print(f"Generated new title: {new_title}")
        return new_title

def final_test():
    """最终测试"""
    
    # 测试数据
    playlist_name = "中配"
    video_title = "Who Will Lead Europe's Space Future？ ESA Selects 5 Companies for Launcher Challenge"
    
    # 读取terminology.json中的theme
    terminology_file = "/Volumes/Data/AI/VideoLingo/history/中配/0Lj_YnaDqLQ_Who Will Lead Europes Space Future ESA Selects 5 C/log/terminology.json"
    
    try:
        with open(terminology_file, 'r', encoding='utf-8') as f:
            terminology_data = json.load(f)
            theme_title = terminology_data.get('theme', video_title)
            print(f"Theme from terminology.json: {theme_title}")
    except Exception as e:
        print(f"Error reading terminology.json: {e}")
        theme_title = video_title
    
    # 创建测试实例
    tester = FinalTitleTester()
    
    print("=" * 100)
    print("最终测试：新的标题生成功能")
    print("=" * 100)
    print(f"播放列表名称: {playlist_name}")
    print(f"原始英文标题: {video_title}")
    print(f"主题描述: {theme_title}")
    print("-" * 100)
    
    # 生成新标题
    final_title = tester.generate_new_title(playlist_name, video_title, theme_title)
    
    print("-" * 100)
    print("🎯 最终生成的标题:")
    print(f"   {final_title}")
    print(f"   标题长度: {len(final_title)} 字符")
    print()
    print("📊 对比分析:")
    print(f"   原格式（仅theme）: {theme_title}")
    print(f"   原格式长度: {len(theme_title)} 字符")
    print()
    print(f"   新格式（完整）: {final_title}")
    print(f"   新格式长度: {len(final_title)} 字符")
    print()
    print("✅ 新标题格式包含:")
    print("   1. 播放列表标识【中配】")
    print("   2. 翻译后的英文标题")
    print("   3. 分隔符——")
    print("   4. 主题描述")
    print("=" * 100)
    
    return final_title

if __name__ == "__main__":
    final_test()