#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
# ------------
# Test Single Bilibili Upload
# ------------
# 测试单个视频的bilibili上传功能
# ------------
"""

import os
import sys
import json
import asyncio
from pathlib import Path
from datetime import datetime

# 添加项目根目录到路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

async def test_single_bilibili_upload():
    """测试单个视频的bilibili上传"""
    print("🧪 Testing Single Bilibili Upload...")
    
    # 视频信息
    video_id = "ONSwneu2tlQ"
    video_title = "Post Ship 36 RUD | Flyover Update 87"
    playlist_name = "中字"
    
    # 构建文件路径
    safe_title = "".join(c for c in video_title if c.isalnum() or c in (' ', '-', '_')).rstrip()
    safe_title = safe_title[:50]
    
    video_file = f"history/{playlist_name}/{video_id}_{safe_title}/output_sub.mp4"
    terminology_file = f"history/{playlist_name}/{video_id}_{safe_title}/log/terminology.json"
    
    print(f"📁 Video file: {video_file}")
    print(f"📁 Terminology file: {terminology_file}")
    
    # 检查文件是否存在
    if not os.path.exists(video_file):
        print(f"❌ Video file not found: {video_file}")
        return False
    
    if not os.path.exists(terminology_file):
        print(f"❌ Terminology file not found: {terminology_file}")
        return False
    
    # 读取terminology.json
    try:
        with open(terminology_file, 'r', encoding='utf-8') as f:
            terminology_data = json.load(f)
            theme_title = terminology_data.get('theme', video_title)
            print(f"📝 Theme from terminology.json: {theme_title}")
            print(f"📏 Title length: {len(theme_title)} characters")
    except Exception as e:
        print(f"❌ Error reading terminology.json: {e}")
        return False
    
    # 导入上传器
    try:
        from uploader.bilibili_uploader import BilibiliUploader
        uploader = BilibiliUploader()
        print("✅ BilibiliUploader imported successfully")
    except Exception as e:
        print(f"❌ Error importing BilibiliUploader: {e}")
        return False
    
    # 检查配置
    print(f"📋 Config enabled: {uploader.config.get('enabled', False)}")
    
    # 检查cookie文件
    cookie_file = Path(uploader.cookie_file)
    if cookie_file.exists():
        print(f"✅ Cookie file exists: {uploader.cookie_file}")
    else:
        print(f"❌ Cookie file not found: {uploader.cookie_file}")
        return False
    
    # 测试上传
    print("\n🚀 Starting upload test...")
    try:
        success = await uploader.upload_video(
            video_file=video_file,
            playlist_name=playlist_name,
            schedule_time=None,  # 立即发布
            custom_title=theme_title
        )
        
        if success:
            print("✅ Upload test successful!")
        else:
            print("❌ Upload test failed!")
        
        return success
        
    except Exception as e:
        print(f"❌ Upload test error: {e}")
        return False

def test_bilibili_uploader_class():
    """测试BilibiliUploaderClass"""
    print("\n🧪 Testing BilibiliUploaderClass...")
    
    try:
        from uploader.bilibili_uploader import BilibiliUploaderClass
        
        # 模拟数据
        test_cookie_data = {
            "SESSDATA": "test_sessdata",
            "bili_jct": "test_bili_jct", 
            "DedeUserID": "test_dede_user_id"
        }
        
        test_file = Path("test_video.mp4")
        test_title = "Test Video Title"
        test_desc = "Test Description"
        test_tid = 27
        test_tags = ["test", "video"]
        test_dtime = 0
        
        # 创建实例
        uploader_class = BilibiliUploaderClass(
            test_cookie_data, test_file, test_title, test_desc, test_tid, test_tags, test_dtime
        )
        print("✅ BilibiliUploaderClass instance created successfully")
        
        # 测试upload方法（不实际执行上传）
        print("✅ BilibiliUploaderClass test passed")
        return True
        
    except Exception as e:
        print(f"❌ BilibiliUploaderClass test failed: {e}")
        return False

def main():
    """主函数"""
    print("🚀 Starting Single Bilibili Upload Test...")
    
    # 测试BilibiliUploaderClass
    class_test = test_bilibili_uploader_class()
    
    # 测试单个视频上传
    upload_test = asyncio.run(test_single_bilibili_upload())
    
    if class_test and upload_test:
        print("\n🎉 All tests passed!")
        print("✅ Single bilibili upload is working correctly")
    else:
        print("\n❌ Some tests failed!")
        print("Please check the error messages above")

if __name__ == "__main__":
    main() 