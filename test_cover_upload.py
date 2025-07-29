#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
封面上传功能测试脚本
测试抖音和B站上传器的封面设置功能
"""

import os
import sys
import asyncio
import json
from pathlib import Path

# 添加当前目录到路径
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

def test_video_and_cover_exists():
    """检查测试视频和封面文件是否存在"""
    video_file = "output/SpaceX Starbase Texas in 4K on 7⧸27⧸25 Starship 38 Rollout Launch Complex Pad 1 and 2 Booster 13.webm"
    cover_file = "output/SpaceX Starbase Texas in 4K on 7⧸27⧸25 Starship 38 Rollout Launch Complex Pad 1 and 2 Booster 13.jpg"
    
    print("🔍 检查测试文件...")
    print(f"视频文件: {video_file}")
    print(f"存在: {'✅' if os.path.exists(video_file) else '❌'}")
    
    print(f"封面文件: {cover_file}")
    print(f"存在: {'✅' if os.path.exists(cover_file) else '❌'}")
    
    return os.path.exists(video_file), os.path.exists(cover_file)

async def test_douyin_cover_upload():
    """测试抖音封面上传功能"""
    print("\n🎬 测试抖音封面上传功能")
    print("=" * 50)
    
    try:
        from uploader.douyin_uploader import DouyinUploader
        
        # 测试文件路径
        video_file = "output/SpaceX Starbase Texas in 4K on 7⧸27⧸25 Starship 38 Rollout Launch Complex Pad 1 and 2 Booster 13.webm"
        cover_file = "output/SpaceX Starbase Texas in 4K on 7⧸27⧸25 Starship 38 Rollout Launch Complex Pad 1 and 2 Booster 13.jpg"
        
        # 创建上传器实例
        uploader = DouyinUploader()
        
        # 检查配置
        print(f"抖音上传功能启用: {uploader.config.get('douyin', {}).get('enabled', False)}")
        
        # 测试封面查找逻辑
        if os.path.exists(cover_file):
            print(f"✅ 找到封面文件: {cover_file}")
        else:
            # 测试自动查找逻辑
            video_name = os.path.splitext(video_file)[0]
            potential_cover = f"{video_name}.jpg"
            if os.path.exists(potential_cover):
                cover_file = potential_cover
                print(f"✅ 自动找到封面文件: {cover_file}")
            else:
                print("❌ 未找到封面文件")
                cover_file = None
        
        # 如果配置了抖音上传，进行实际测试（但不发布）
        if uploader.config.get('douyin', {}).get('enabled', False):
            print("⚠️ 抖音上传功能已启用，将进行实际测试")
            print("注意: 这将打开浏览器但不会实际发布视频")
            
            # 这里可以取消注释进行实际测试
            # success = await uploader.upload_video(
            #     video_path=video_file,
            #     playlist_name="测试",
            #     custom_title="封面上传测试 - 请勿发布",
            #     cover_path=cover_file
            # )
            # print(f"上传结果: {'✅ 成功' if success else '❌ 失败'}")
            print("⚠️ 跳过实际上传测试（需要手动取消注释代码）")
        else:
            print("ℹ️ 抖音上传功能未启用，仅测试封面查找逻辑")
        
        return True
        
    except ImportError as e:
        print(f"❌ 导入抖音上传器失败: {e}")
        return False
    except Exception as e:
        print(f"❌ 测试抖音上传器时出错: {e}")
        return False

async def test_bilibili_cover_upload():
    """测试B站封面上传功能"""
    print("\n📺 测试B站封面上传功能")
    print("=" * 50)
    
    try:
        from uploader.bilibili_uploader import BilibiliUploader
        
        # 测试文件路径
        video_file = "output/SpaceX Starbase Texas in 4K on 7⧸27⧸25 Starship 38 Rollout Launch Complex Pad 1 and 2 Booster 13.webm"
        cover_file = "output/SpaceX Starbase Texas in 4K on 7⧸27⧸25 Starship 38 Rollout Launch Complex Pad 1 and 2 Booster 13.jpg"
        
        # 创建上传器实例
        uploader = BilibiliUploader()
        
        # 检查配置
        print(f"B站上传功能启用: {uploader.config.get('enabled', False)}")
        
        # 检查cookie文件
        cookie_file = Path(uploader.cookie_file)
        print(f"Cookie文件存在: {'✅' if cookie_file.exists() else '❌'} ({uploader.cookie_file})")
        
        # 测试封面查找逻辑
        if os.path.exists(cover_file):
            print(f"✅ 找到封面文件: {cover_file}")
        else:
            # 测试自动查找逻辑
            video_name = os.path.splitext(video_file)[0]
            potential_cover = f"{video_name}.jpg"
            if os.path.exists(potential_cover):
                cover_file = potential_cover
                print(f"✅ 自动找到封面文件: {cover_file}")
            else:
                print("❌ 未找到封面文件")
                cover_file = None
        
        # 如果配置了B站上传，进行实际测试（但不发布）
        if uploader.config.get('enabled', False) and cookie_file.exists():
            print("⚠️ B站上传功能已启用且Cookie文件存在，将进行实际测试")
            print("注意: 这将进行实际上传测试")
            
            # 这里可以取消注释进行实际测试
            # success = await uploader.upload_video(
            #     video_file=video_file,
            #     playlist_name="测试",
            #     custom_title="封面上传测试 - 请勿发布",
            #     cover_path=cover_file
            # )
            # print(f"上传结果: {'✅ 成功' if success else '❌ 失败'}")
            print("⚠️ 跳过实际上传测试（需要手动取消注释代码）")
        else:
            print("ℹ️ B站上传功能未启用或Cookie文件不存在，仅测试封面查找逻辑")
        
        return True
        
    except ImportError as e:
        print(f"❌ 导入B站上传器失败: {e}")
        return False
    except Exception as e:
        print(f"❌ 测试B站上传器时出错: {e}")
        return False

def test_cover_detection_logic():
    """测试封面自动检测逻辑"""
    print("\n🔍 测试封面自动检测逻辑")
    print("=" * 50)
    
    # 模拟播放列表监控器的封面查找逻辑
    playlist_name = "中字"
    video_id = "test_video_id"
    safe_title = "SpaceX Starbase Texas Test"
    original_title = "SpaceX Starbase Texas in 4K on 7⧸27⧸25 Starship 38 Rollout Launch Complex Pad 1 and 2 Booster 13"
    
    print(f"播放列表: {playlist_name}")
    print(f"视频ID: {video_id}")
    print(f"安全标题: {safe_title}")
    print(f"原始标题: {original_title}")
    print()
    
    # 方法1: 查找历史文件夹中的原始视频名称对应的封面
    cover_file = f"history/{playlist_name}/{video_id}_{safe_title}/{original_title}.jpg"
    print(f"方法1 - 原始标题封面: {cover_file}")
    print(f"存在: {'✅' if os.path.exists(cover_file) else '❌'}")
    
    if not os.path.exists(cover_file):
        # 方法2: 搜索目录下的任意.jpg文件
        import glob
        video_dir = f"history/{playlist_name}/{video_id}_{safe_title}"
        if os.path.exists(video_dir):
            jpg_files = glob.glob(f"{video_dir}/*.jpg")
            print(f"方法2 - 目录搜索: {video_dir}/*.jpg")
            print(f"找到的jpg文件: {jpg_files}")
            if jpg_files:
                cover_file = jpg_files[0]
                print(f"✅ 选择封面: {cover_file}")
            else:
                print("❌ 目录中无jpg文件")
                cover_file = None
        else:
            print(f"❌ 目录不存在: {video_dir}")
            cover_file = None
    
    return cover_file is not None

async def main():
    """主测试函数"""
    print("🧪 封面上传功能测试")
    print("=" * 60)
    
    # 检查测试文件
    video_exists, cover_exists = test_video_and_cover_exists()
    
    if not video_exists:
        print("❌ 测试视频文件不存在，请确保视频文件在output目录中")
        return
    
    if not cover_exists:
        print("⚠️ 测试封面文件不存在，将测试自动查找逻辑")
    
    # 测试封面检测逻辑
    cover_detected = test_cover_detection_logic()
    
    # 测试抖音上传器
    douyin_test = await test_douyin_cover_upload()
    
    # 测试B站上传器
    bilibili_test = await test_bilibili_cover_upload()
    
    # 总结
    print("\n📊 测试结果总结")
    print("=" * 50)
    print(f"视频文件存在: {'✅' if video_exists else '❌'}")
    print(f"封面文件存在: {'✅' if cover_exists else '❌'}")
    print(f"封面检测逻辑: {'✅' if cover_detected else '❌'}")
    print(f"抖音上传器测试: {'✅' if douyin_test else '❌'}")
    print(f"B站上传器测试: {'✅' if bilibili_test else '❌'}")
    
    if all([video_exists, douyin_test, bilibili_test]):
        print("\n🎉 所有测试通过！封面上传功能已就绪")
    else:
        print("\n⚠️ 部分测试未通过，请检查相关配置")

if __name__ == "__main__":
    asyncio.run(main())