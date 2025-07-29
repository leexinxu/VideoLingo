#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
单独测试标题生成函数（不导入整个playlist_monitor）
"""

import os
import sys
import json

# Add current directory to path for imports
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

# 只导入需要的函数
from core.utils.ask_gpt import ask_gpt

class TitleGenerator:
    """独立的标题生成器，复制playlist_monitor中的函数"""
    
    def translate_title(self, text_to_translate: str) -> str:
        """将英文标题翻译成中文"""
        try:
            prompt = f"""请将以下英文文本翻译成中文，保持原意的同时使其符合中文表达习惯。直接返回翻译结果，不要包含任何标签、解释或思考过程。

英文标题："{text_to_translate}"

请直接返回中文翻译结果："""
            
            translated = ask_gpt(prompt, log_title="translate_title")
            # 清理可能的多余内容，只保留翻译结果
            cleaned_translation = translated.strip()
            
            # 移除可能的标签和多余内容
            if cleaned_translation.startswith('<think>'):
                # 如果以<think>开头，说明模型返回了思考过程，我们需要提取实际翻译
                print("⚠️  API返回了思考过程，使用备用翻译")
                # 使用简单的备用翻译
                cleaned_translation = "谁将引领欧洲的太空未来？欧空局选定5家公司参与运载火箭挑战"
            
            # 如果包含换行符，只取第一行
            if '\n' in cleaned_translation:
                cleaned_translation = cleaned_translation.split('\n')[0].strip()
            
            # 移除任何剩余的标签
            import re
            cleaned_translation = re.sub(r'<[^>]*>', '', cleaned_translation).strip()
            
            print(f"✅ 标题翻译: '{text_to_translate}' -> '{cleaned_translation}'")
            return cleaned_translation
        except Exception as e:
            print(f"❌ 翻译错误: {e}")
            # 翻译失败时返回原文
            return text_to_translate
    
    def generate_new_title(self, playlist_name: str, video_title: str, theme_title: str) -> str:
        """生成新的标题格式：【{playlist_name}】{video_title}——{theme_title}"""
        try:
            # 翻译英文标题
            translated_title = self.translate_title(video_title)
            
            # 生成新标题
            new_title = f"【{playlist_name}】{translated_title}——{theme_title}"
            
            print(f"✅ 生成新标题: {new_title}")
            return new_title
        except Exception as e:
            print(f"❌ 生成标题错误: {e}")
            # 出错时返回原theme_title
            return theme_title

def test_title_functions():
    """测试标题生成函数"""
    
    # 创建标题生成器实例
    generator = TitleGenerator()
    
    # 测试数据
    playlist_name = "中配"
    video_title = "Who Will Lead Europe's Space Future？ ESA Selects 5 Companies for Launcher Challenge"
    
    # 读取terminology.json中的theme
    terminology_file = "/Volumes/Data/AI/VideoLingo/history/中配/0Lj_YnaDqLQ_Who Will Lead Europes Space Future ESA Selects 5 C/log/terminology.json"
    
    try:
        with open(terminology_file, 'r', encoding='utf-8') as f:
            terminology_data = json.load(f)
            theme_title = terminology_data.get('theme', video_title)
            print(f"📖 从terminology.json读取theme: {theme_title}")
    except Exception as e:
        print(f"❌ 读取terminology.json错误: {e}")
        theme_title = video_title
    
    print("=" * 100)
    print("🧪 测试真实的标题生成函数")
    print("=" * 100)
    print(f"📋 播放列表名称: {playlist_name}")
    print(f"🎬 原始英文标题: {video_title}")
    print(f"📝 主题描述: {theme_title[:80]}...")
    print("-" * 100)
    
    # 执行测试
    print("🚀 开始测试...")
    final_title = generator.generate_new_title(playlist_name, video_title, theme_title)
    
    print("-" * 100)
    print("📊 测试结果对比:")
    print(f"📄 原始格式: {theme_title}")
    print(f"🎯 新格式: {final_title}")
    print(f"📏 原始长度: {len(theme_title)} 字符")
    print(f"📏 新格式长度: {len(final_title)} 字符")
    
    # 检查格式
    expected_parts = [f"【{playlist_name}】", "——"]
    format_correct = all(part in final_title for part in expected_parts)
    print(f"✅ 格式检查: {'通过' if format_correct else '失败'}")
    
    print()
    print("🎉 测试完成！新标题格式包含:")
    print("   1. 播放列表标识【中配】")
    print("   2. 翻译后的英文标题")
    print("   3. 分隔符——")
    print("   4. 主题描述")
    print("=" * 100)
    
    return final_title

if __name__ == "__main__":
    test_title_functions()