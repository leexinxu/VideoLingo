#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
# ------------
# Test Apple Fonts
# ------------
# 测试苹果字体配置
# ------------
"""

import platform
import subprocess
import os

def test_apple_fonts():
    """测试苹果字体配置"""
    print("🧪 Testing Apple Fonts Configuration...")
    
    print(f"📋 Platform: {platform.system()}")
    
    # 测试字体文件是否存在
    font_files = {
        'Helvetica': '/System/Library/Fonts/Helvetica.ttc',
        'Songti': '/System/Library/Fonts/Supplemental/Songti.ttc',
        'Arial': '/System/Library/Fonts/Supplemental/Arial.ttf'
    }
    
    for font_name, font_path in font_files.items():
        if os.path.exists(font_path):
            print(f"✅ {font_name}: {font_path}")
        else:
            print(f"❌ {font_name}: {font_path} (not found)")
    
    # 测试ffmpeg字体渲染
    print("\n🎬 Testing FFmpeg Font Rendering...")
    
    test_texts = [
        ("English Test", "Helvetica"),
        ("中文测试", "Songti"),
        ("Mixed 中英文 Test", "Songti")
    ]
    
    for text, font in test_texts:
        output_file = f"test_{font.lower()}_{text.replace(' ', '_')}.mp4"
        
        # 构建ffmpeg命令
        if font == "Helvetica":
            font_path = "/System/Library/Fonts/Helvetica.ttc"
        elif font == "Songti":
            font_path = "/System/Library/Fonts/Supplemental/Songti.ttc"
        else:
            font_path = "/System/Library/Fonts/Supplemental/Arial.ttf"
        
        cmd = [
            'ffmpeg', '-f', 'lavfi', '-i', 
            f'testsrc=duration=2:size=640x480:rate=1',
            '-vf', f'drawtext=text=\'{text}\':fontfile={font_path}:fontsize=36:x=50:y=50:fontcolor=white',
            '-t', '2', '-y', output_file
        ]
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode == 0:
                print(f"✅ {font}: {text} - {output_file}")
                # 检查文件大小
                if os.path.exists(output_file):
                    size = os.path.getsize(output_file)
                    print(f"   📁 File size: {size} bytes")
            else:
                print(f"❌ {font}: {text} - Error: {result.stderr}")
        except Exception as e:
            print(f"❌ {font}: {text} - Exception: {e}")

def test_font_configuration():
    """测试字体配置"""
    print("\n📋 Testing Font Configuration...")
    
    # 模拟字体配置逻辑
    if platform.system() == 'Darwin':  # macOS
        font_name = 'Helvetica'
        trans_font_name = 'Songti'
        print(f"✅ macOS detected")
        print(f"   📝 Font Name: {font_name}")
        print(f"   📝 Trans Font Name: {trans_font_name}")
    elif platform.system() == 'Linux':
        font_name = 'NotoSansCJK-Regular'
        trans_font_name = 'NotoSansCJK-Regular'
        print(f"✅ Linux detected")
        print(f"   📝 Font Name: {font_name}")
        print(f"   📝 Trans Font Name: {trans_font_name}")
    else:  # Windows
        font_name = 'Arial'
        trans_font_name = 'Arial'
        print(f"✅ Windows detected")
        print(f"   📝 Font Name: {font_name}")
        print(f"   📝 Trans Font Name: {trans_font_name}")

def main():
    """主函数"""
    print("🚀 Starting Apple Fonts Test...")
    
    test_apple_fonts()
    test_font_configuration()
    
    print("\n🎉 Apple fonts test completed!")
    print("📝 Font configuration updated for macOS:")
    print("   - English: Helvetica (Apple's classic font)")
    print("   - Chinese: Songti (Apple's Chinese font)")

if __name__ == "__main__":
    main() 