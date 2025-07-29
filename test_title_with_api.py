#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
使用真实API测试新的标题生成功能
"""

import os
import sys
import json

# Add current directory to path for imports
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

from core.utils.ask_gpt import ask_gpt

class TitleTester:
    def __init__(self):
        pass
    
    def translate_title(self, text_to_translate: str) -> str:
        """将英文标题翻译成中文"""
        try:
            prompt = f"""请将以下英文文本翻译成中文，保持原意的同时使其符合中文表达习惯。

英文标题："{text_to_translate}"

要求：
1. 只返回中文翻译结果
2. 不要包含任何解释、注释或思考过程
3. 确保翻译准确且符合中文表达习惯

中文翻译："""
            
            translated = ask_gpt(prompt, log_title="translate_title")
            # 清理可能的多余内容，只保留翻译结果
            cleaned_translation = translated.strip()
            # 如果包含换行符，只取第一行
            if '\n' in cleaned_translation:
                cleaned_translation = cleaned_translation.split('\n')[0].strip()
            
            print(f"Title translation: '{text_to_translate}' -> '{cleaned_translation}'")
            return cleaned_translation
        except Exception as e:
            print(f"Error translating title: {e}")
            # 翻译失败时返回原文
            return text_to_translate
    
    def generate_new_title(self, playlist_name: str, video_title: str, theme_title: str) -> str:
        """生成新的标题格式：【{playlist_name}】{video_title}——{theme_title}"""
        try:
            # 翻译英文标题
            translated_title = self.translate_title(video_title)
            
            # 生成新标题
            new_title = f"【{playlist_name}】{translated_title}——{theme_title}"
            
            print(f"Generated new title: {new_title}")
            return new_title
        except Exception as e:
            print(f"Error generating new title: {e}")
            # 出错时返回原theme_title
            return theme_title

def test_with_real_api():
    """使用真实API测试标题生成"""
    
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
    tester = TitleTester()
    
    print("=" * 80)
    print("使用真实API测试新的标题生成功能")
    print("=" * 80)
    print(f"播放列表名称: {playlist_name}")
    print(f"原始英文标题: {video_title}")
    print(f"主题描述: {theme_title[:100]}...")
    print("-" * 80)
    
    # 生成新标题
    final_title = tester.generate_new_title(playlist_name, video_title, theme_title)
    
    print("-" * 80)
    print("最终生成的标题:")
    print(f"{final_title}")
    print(f"标题长度: {len(final_title)} 字符")
    print()
    print("对比:")
    print(f"原格式（仅theme）: {theme_title}")
    print(f"新格式（完整）: {final_title}")
    print("=" * 80)
    
    return final_title

if __name__ == "__main__":
    test_with_real_api()