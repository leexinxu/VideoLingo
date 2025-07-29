#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
抖音封面上传修复测试脚本
"""

import os
import sys
import asyncio

# 添加当前目录到路径
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

async def test_douyin_cover_fix():
    """测试修复后的抖音封面上传功能"""
    print("🎬 测试修复后的抖音封面上传功能")
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
        print("\n📋 修复内容:")
        print("  1. 使用正确的封面上传流程：点击'选择封面'")
        print("  2. 点击'设置竖封面'进入封面设置界面")
        print("  3. 使用正确的文件上传选择器")
        print("  4. 等待处理完成后点击'完成'按钮")
        print("  5. 调整封面设置时机到视频上传完成后")
        
        print("\n⚠️ 这将打开浏览器进行实际测试")
        confirm = input("是否继续测试修复后的封面上传？(y/N): ")
        if confirm.lower() != 'y':
            print("❌ 用户取消测试")
            return False
        
        # 执行上传测试
        success = await uploader.upload_video(
            video_path=video_file,
            playlist_name="测试",
            custom_title="【测试修复】抖音封面上传功能验证",
            cover_path=cover_file
        )
        
        if success:
            print("✅ 抖音封面上传测试成功！")
            print("🔍 请检查抖音创作者中心是否正确显示了封面")
            print("⚠️ 请记得删除测试视频")
        else:
            print("❌ 抖音封面上传测试失败")
        
        return success
        
    except Exception as e:
        print(f"❌ 测试出错: {e}")
        return False

async def main():
    """主函数"""
    result = await test_douyin_cover_fix()
    
    print("\n📊 测试结果")
    print("=" * 30)
    if result:
        print("🎉 封面上传功能修复成功！")
    else:
        print("⚠️ 测试未通过，请检查配置")

if __name__ == "__main__":
    asyncio.run(main())