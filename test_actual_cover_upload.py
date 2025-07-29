#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
实际封面上传测试脚本
用于测试抖音和B站的封面上传功能
"""

import os
import sys
import asyncio
import argparse
from pathlib import Path

# 添加当前目录到路径
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

async def test_douyin_actual_upload():
    """实际测试抖音封面上传"""
    print("🎬 开始抖音封面上传测试")
    print("=" * 50)
    
    try:
        from uploader.douyin_uploader import DouyinUploader
        
        # 测试文件路径
        video_file = "output/SpaceX Starbase Texas in 4K on 7⧸27⧸25 Starship 38 Rollout Launch Complex Pad 1 and 2 Booster 13.webm"
        cover_file = "output/SpaceX Starbase Texas in 4K on 7⧸27⧸25 Starship 38 Rollout Launch Complex Pad 1 and 2 Booster 13.jpg"
        
        if not os.path.exists(video_file):
            print(f"❌ 视频文件不存在: {video_file}")
            return False
            
        if not os.path.exists(cover_file):
            print(f"❌ 封面文件不存在: {cover_file}")
            return False
        
        # 创建上传器实例
        uploader = DouyinUploader()
        
        # 检查配置
        if not uploader.config.get('douyin', {}).get('enabled', False):
            print("❌ 抖音上传功能未启用，请在uploader_config.json中启用")
            return False
        
        print(f"✅ 视频文件: {video_file}")
        print(f"✅ 封面文件: {cover_file}")
        print("⚠️ 这将打开浏览器进行实际上传测试")
        print("⚠️ 请确保在发布前取消或删除测试视频")
        
        # 确认是否继续
        confirm = input("是否继续测试？(y/N): ")
        if confirm.lower() != 'y':
            print("❌ 用户取消测试")
            return False
        
        # 执行上传测试
        success = await uploader.upload_video(
            video_path=video_file,
            playlist_name="测试",
            custom_title="【测试】封面上传功能测试 - 请勿发布",
            cover_path=cover_file
        )
        
        if success:
            print("✅ 抖音封面上传测试成功！")
            print("⚠️ 请记得在抖音创作者中心删除测试视频")
        else:
            print("❌ 抖音封面上传测试失败")
        
        return success
        
    except Exception as e:
        print(f"❌ 抖音上传测试出错: {e}")
        return False

async def test_bilibili_actual_upload():
    """实际测试B站封面上传"""
    print("📺 开始B站封面上传测试")
    print("=" * 50)
    
    try:
        from uploader.bilibili_uploader import BilibiliUploader
        
        # 测试文件路径
        video_file = "output/SpaceX Starbase Texas in 4K on 7⧸27⧸25 Starship 38 Rollout Launch Complex Pad 1 and 2 Booster 13.webm"
        cover_file = "output/SpaceX Starbase Texas in 4K on 7⧸27⧸25 Starship 38 Rollout Launch Complex Pad 1 and 2 Booster 13.jpg"
        
        if not os.path.exists(video_file):
            print(f"❌ 视频文件不存在: {video_file}")
            return False
            
        if not os.path.exists(cover_file):
            print(f"❌ 封面文件不存在: {cover_file}")
            return False
        
        # 创建上传器实例
        uploader = BilibiliUploader()
        
        # 检查配置
        if not uploader.config.get('enabled', False):
            print("❌ B站上传功能未启用，请在uploader_config.json中启用")
            return False
        
        # 检查cookie文件
        cookie_file = Path(uploader.cookie_file)
        if not cookie_file.exists():
            print(f"❌ Cookie文件不存在: {uploader.cookie_file}")
            return False
        
        print(f"✅ 视频文件: {video_file}")
        print(f"✅ 封面文件: {cover_file}")
        print("⚠️ 这将进行实际的B站上传测试")
        print("⚠️ 请确保在发布前检查视频内容")
        
        # 确认是否继续
        confirm = input("是否继续测试？(y/N): ")
        if confirm.lower() != 'y':
            print("❌ 用户取消测试")
            return False
        
        # 执行上传测试
        success = await uploader.upload_video(
            video_file=video_file,
            playlist_name="测试",
            custom_title="【测试】封面上传功能测试",
            cover_path=cover_file
        )
        
        if success:
            print("✅ B站封面上传测试成功！")
            print("⚠️ 请检查B站后台的视频和封面")
        else:
            print("❌ B站封面上传测试失败")
        
        return success
        
    except Exception as e:
        print(f"❌ B站上传测试出错: {e}")
        return False

async def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='封面上传功能实际测试')
    parser.add_argument('--platform', choices=['douyin', 'bilibili', 'both'], 
                       default='both', help='选择测试平台')
    
    args = parser.parse_args()
    
    print("🧪 封面上传实际测试")
    print("=" * 60)
    print("⚠️ 这将进行实际的上传测试，请谨慎操作")
    print("⚠️ 建议先在平台设置中关闭自动发布")
    print()
    
    results = {}
    
    if args.platform in ['douyin', 'both']:
        results['douyin'] = await test_douyin_actual_upload()
        print()
    
    if args.platform in ['bilibili', 'both']:
        results['bilibili'] = await test_bilibili_actual_upload()
        print()
    
    # 总结
    print("📊 测试结果总结")
    print("=" * 50)
    for platform, result in results.items():
        status = "✅ 成功" if result else "❌ 失败"
        print(f"{platform}: {status}")
    
    if all(results.values()):
        print("\n🎉 所有测试成功！封面上传功能正常工作")
    else:
        print("\n⚠️ 部分测试失败，请检查配置和网络连接")

if __name__ == "__main__":
    print("使用方法:")
    print("python test_actual_cover_upload.py --platform douyin    # 仅测试抖音")
    print("python test_actual_cover_upload.py --platform bilibili # 仅测试B站")
    print("python test_actual_cover_upload.py --platform both     # 测试两个平台")
    print()
    
    asyncio.run(main())