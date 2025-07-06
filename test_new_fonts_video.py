#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
# ------------
# Test New Fonts Video
# ------------
# 使用新字体重新生成字幕视频
# ------------
"""

import os
import subprocess
import platform
from pathlib import Path

def get_font_config():
    """获取字体配置"""
    if platform.system() == 'Darwin':  # macOS
        return {
            'font_name': 'Helvetica',
            'trans_font_name': 'Songti',
            'font_path': '/System/Library/Fonts/Helvetica.ttc',
            'trans_font_path': '/System/Library/Fonts/Supplemental/Songti.ttc'
        }
    elif platform.system() == 'Linux':
        return {
            'font_name': 'NotoSansCJK-Regular',
            'trans_font_name': 'NotoSansCJK-Regular',
            'font_path': '/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc',
            'trans_font_path': '/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc'
        }
    else:  # Windows
        return {
            'font_name': 'Arial',
            'trans_font_name': 'Arial',
            'font_path': 'C:/Windows/Fonts/arial.ttf',
            'trans_font_path': 'C:/Windows/Fonts/arial.ttf'
        }

def create_new_fonts_video():
    """使用新字体重新生成字幕视频"""
    print("🎬 Creating video with new Apple fonts...")
    
    # 视频信息
    video_dir = "history/中字/Inside Rocket Lab ｜ Spacecraft Production at Scale"
    video_file = f"{video_dir}/Inside Rocket Lab ｜ Spacecraft Production at Scale.webm"
    src_srt = f"{video_dir}/src.srt"
    trans_srt = f"{video_dir}/trans.srt"
    output_file = f"{video_dir}/output_sub_new_fonts.mp4"
    
    # 检查文件是否存在
    if not os.path.exists(video_file):
        print(f"❌ Video file not found: {video_file}")
        return False
    
    if not os.path.exists(src_srt):
        print(f"❌ Source subtitle file not found: {src_srt}")
        return False
    
    if not os.path.exists(trans_srt):
        print(f"❌ Translation subtitle file not found: {trans_srt}")
        return False
    
    print(f"✅ Found video: {video_file}")
    print(f"✅ Found source subtitles: {src_srt}")
    print(f"✅ Found translation subtitles: {trans_srt}")
    
    # 获取字体配置
    font_config = get_font_config()
    print(f"📝 Using fonts:")
    print(f"   - English: {font_config['font_name']} ({font_config['font_path']})")
    print(f"   - Chinese: {font_config['trans_font_name']} ({font_config['trans_font_path']})")
    
    # 获取视频分辨率
    try:
        cmd = ['ffprobe', '-v', 'quiet', '-select_streams', 'v:0', 
               '-show_entries', 'stream=width,height', '-of', 'csv=p=0', video_file]
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            width, height = result.stdout.strip().split(',')
            print(f"📐 Video resolution: {width}x{height}")
        else:
            print("⚠️ Could not get video resolution, using default")
            width, height = 1920, 1080
    except Exception as e:
        print(f"⚠️ Error getting video resolution: {e}")
        width, height = 1920, 1080
    
    # 字体大小配置
    src_font_size = 15
    trans_font_size = 17
    
    # 颜色配置
    src_font_color = '&HFFFFFF'  # 白色
    src_outline_color = '&H000000'  # 黑色边框
    src_outline_width = 1
    src_shadow_color = '&H80000000'  # 半透明黑色阴影
    
    trans_font_color = '&H00FFFF'  # 青色
    trans_outline_color = '&H000000'  # 黑色边框
    trans_outline_width = 1
    trans_back_color = '&H33000000'  # 半透明黑色背景
    
    # 构建FFmpeg命令
    ffmpeg_cmd = [
        'ffmpeg', '-i', video_file,
        '-vf', (
            f"scale={width}:{height}:force_original_aspect_ratio=decrease,"
            f"pad={width}:{height}:(ow-iw)/2:(oh-ih)/2,"
            f"subtitles={src_srt}:force_style='FontSize={src_font_size},FontName={font_config['font_name']}," 
            f"PrimaryColour={src_font_color},OutlineColour={src_outline_color},OutlineWidth={src_outline_width},"
            f"ShadowColour={src_shadow_color},BorderStyle=1',"
            f"subtitles={trans_srt}:force_style='FontSize={trans_font_size},FontName={font_config['trans_font_name']},"
            f"PrimaryColour={trans_font_color},OutlineColour={trans_outline_color},OutlineWidth={trans_outline_width},"
            f"BackColour={trans_back_color},Alignment=2,MarginV=27,BorderStyle=4'"
        ).encode('utf-8'),
        '-c:v', 'libx264', '-preset', 'medium', '-crf', '23',
        '-y', output_file
    ]
    
    print(f"\n🚀 Starting video generation with new fonts...")
    print(f"📁 Output file: {output_file}")
    
    # 执行FFmpeg命令
    try:
        process = subprocess.Popen(ffmpeg_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # 实时显示进度
        while True:
            output = process.stderr.readline()
            if output == b'' and process.poll() is not None:
                break
            if output:
                line = output.decode().strip()
                if 'time=' in line:
                    print(f"⏳ {line}")
        
        # 等待进程完成
        return_code = process.wait()
        
        if return_code == 0:
            print(f"\n✅ Video generated successfully!")
            print(f"📁 Output: {output_file}")
            
            # 检查文件大小
            if os.path.exists(output_file):
                size_mb = os.path.getsize(output_file) / (1024 * 1024)
                print(f"📏 File size: {size_mb:.1f} MB")
            
            return True
        else:
            print(f"\n❌ FFmpeg failed with return code: {return_code}")
            return False
            
    except Exception as e:
        print(f"\n❌ Error during video generation: {e}")
        return False

def main():
    """主函数"""
    print("🚀 Starting New Fonts Video Test...")
    
    success = create_new_fonts_video()
    
    if success:
        print("\n🎉 New fonts video test completed!")
        print("📝 You can now compare the new video with the original to see the font difference")
    else:
        print("\n❌ New fonts video test failed!")

if __name__ == "__main__":
    main() 