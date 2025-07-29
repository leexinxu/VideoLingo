#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试修复后的翻译功能
"""

import os
import sys
import json

# Add current directory to path for imports
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

# 只导入需要的模块避免依赖问题
from core.utils.ask_gpt import ask_gpt
import re

def test_translate_title(text_to_translate: str) -> str:
    """测试修复后的翻译函数"""
    try:
        # 更简洁明确的prompt
        prompt = f"""Translate this English title to Chinese. Only return the Chinese translation, no explanations:

{text_to_translate}

Chinese translation:"""
        
        translated = ask_gpt(prompt, log_title="translate_title")
        cleaned_translation = translated.strip()
        
        print(f"原始API响应: {repr(translated)}")
        
        # 处理各种可能的问题格式
        # 如果包含thinking标签，尝试提取内容
        if '<think>' in cleaned_translation:
            print("⚠️  API返回了thinking过程，尝试提取翻译...")
            # 查找thinking标签后的内容
            match = re.search(r'</think>\s*(.+)', cleaned_translation, re.DOTALL)
            if match:
                cleaned_translation = match.group(1).strip()
                print(f"✅ 提取到翻译: {cleaned_translation}")
            else:
                # 如果没有找到，直接返回原英文标题
                print("❌ 无法从thinking过程中提取翻译，使用原英文标题")
                cleaned_translation = text_to_translate
        
        # 移除任何剩余的标签
        cleaned_translation = re.sub(r'<[^>]*>', '', cleaned_translation).strip()
        
        # 如果包含换行符，只取第一行
        if '\n' in cleaned_translation:
            lines = cleaned_translation.split('\n')
            # 找到第一个非空行
            for line in lines:
                if line.strip():
                    cleaned_translation = line.strip()
                    break
        
        # 如果翻译结果为空，直接返回原英文标题
        if not cleaned_translation or len(cleaned_translation.strip()) == 0:
            print("⚠️  翻译结果为空，使用原英文标题")
            cleaned_translation = text_to_translate
        
        print(f"✅ 最终翻译结果: '{text_to_translate}' -> '{cleaned_translation}'")
        return cleaned_translation
        
    except Exception as e:
        print(f"❌ 翻译错误: {e}")
        # 翻译失败时直接返回原英文标题
        print("🔄 使用原英文标题作为备用")
        return text_to_translate

def generate_new_title(playlist_name: str, video_title: str, theme_title: str) -> str:
    """生成新的标题格式"""
    try:
        # 翻译英文标题
        translated_title = test_translate_title(video_title)
        
        # 生成新标题
        new_title = f"【{playlist_name}】{translated_title}——{theme_title}"
        
        print(f"🎯 生成最终标题: {new_title}")
        return new_title
    except Exception as e:
        print(f"❌ 生成标题错误: {e}")
        # 出错时返回原theme_title
        return theme_title

def main():
    """主测试函数"""
    # 测试数据
    playlist_name = "中配"
    video_title = "Who Will Lead Europe's Space Future？ ESA Selects 5 Companies for Launcher Challenge"
    
    # 读取terminology.json中的theme
    terminology_file = "/Volumes/Data/AI/VideoLingo/history/中配/0Lj_YnaDqLQ_Who Will Lead Europes Space Future ESA Selects 5 C/log/terminology.json"
    
    try:
        with open(terminology_file, 'r', encoding='utf-8') as f:
            terminology_data = json.load(f)
            theme_title = terminology_data.get('theme', video_title)
    except Exception as e:
        print(f"❌ 读取terminology.json错误: {e}")
        theme_title = video_title
    
    print("=" * 100)
    print("🔧 测试修复后的翻译功能")
    print("=" * 100)
    print(f"📋 播放列表: {playlist_name}")
    print(f"🎬 英文标题: {video_title}")
    print(f"📝 主题描述: {theme_title[:50]}...")
    print("-" * 100)
    
    # 执行测试
    final_title = generate_new_title(playlist_name, video_title, theme_title)
    
    print("-" * 100)
    print("📊 最终结果:")
    print(f"🎯 新标题: {final_title}")
    print(f"📏 标题长度: {len(final_title)} 字符")
    
    # 验证格式
    success_checks = []
    success_checks.append(("包含播放列表标识", f"【{playlist_name}】" in final_title))
    success_checks.append(("包含分隔符", "——" in final_title))
    success_checks.append(("包含中文翻译", any('\u4e00' <= char <= '\u9fff' for char in final_title[:50])))
    success_checks.append(("标题不为空", len(final_title) > 0))
    
    print("\n📋 验证结果:")
    all_passed = True
    for check_name, passed in success_checks:
        status = "✅" if passed else "❌"
        print(f"   {status} {check_name}")
        if not passed:
            all_passed = False
    
    print(f"\n🎉 总体结果: {'测试成功！' if all_passed else '测试失败！'}")
    print("=" * 100)
    
    return final_title

if __name__ == "__main__":
    main()