#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
# ------------
# Bilibili Uploader Setup
# ------------
# bilibili上传器设置脚本
# ------------
"""

import os
import json
import asyncio
from pathlib import Path

def setup_bilibili():
    """设置bilibili上传器"""
    print("🎬 Bilibili Uploader Setup")
    print("=" * 50)
    
    # 1. 检查依赖
    print("\n1. 检查依赖...")
    try:
        import biliup
        print("✅ biliup 已安装")
    except ImportError:
        print("❌ biliup 未安装")
        print("请运行: pip install biliup")
        return False
    
    # 2. 创建配置目录
    print("\n2. 创建配置目录...")
    config_dir = Path("uploader_config")
    config_dir.mkdir(exist_ok=True)
    print(f"✅ 配置目录已创建: {config_dir}")
    
    # 3. 检查cookie文件
    print("\n3. 检查cookie文件...")
    cookie_file = config_dir / "bilibili_cookies.json"
    example_file = config_dir / "bilibili_cookies.json.example"
    
    if cookie_file.exists():
        print(f"✅ Cookie文件已存在: {cookie_file}")
    else:
        print(f"❌ Cookie文件不存在: {cookie_file}")
        print("请按照以下步骤获取cookie:")
        print("1. 登录bilibili网站")
        print("2. 打开浏览器开发者工具")
        print("3. 在Console中运行以下代码:")
        print("""
        let cookies = {};
        document.cookie.split(';').forEach(function(cookie) {
            let parts = cookie.split('=');
            if (parts.length === 2) {
                cookies[parts[0].trim()] = parts[1].trim();
            }
        });
        console.log(JSON.stringify(cookies, null, 2));
        """)
        print("4. 复制输出的cookie信息")
        print("5. 创建 uploader_config/bilibili_cookies.json 文件")
        print("6. 参考 uploader_config/bilibili_cookies.json.example 格式")
        return False
    
    # 4. 验证cookie文件格式
    print("\n4. 验证cookie文件格式...")
    try:
        with open(cookie_file, 'r', encoding='utf-8') as f:
            cookie_data = json.load(f)
        
        # 检查必要的字段
        required_fields = ["SESSDATA", "bili_jct", "DedeUserID"]
        cookie_info = cookie_data.get("cookie_info", {})
        cookies = cookie_info.get("cookies", [])
        
        cookie_dict = {}
        for cookie in cookies:
            cookie_dict[cookie.get("name")] = cookie.get("value")
        
        missing_fields = [field for field in required_fields if field not in cookie_dict]
        if missing_fields:
            print(f"❌ 缺少必要的cookie字段: {missing_fields}")
            return False
        
        print("✅ Cookie文件格式正确")
        
    except Exception as e:
        print(f"❌ Cookie文件格式错误: {e}")
        return False
    
    # 5. 更新上传器配置
    print("\n5. 更新上传器配置...")
    config_file = Path("uploader_config.json")
    
    if config_file.exists():
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                config = json.load(f)
        except:
            config = {}
    else:
        config = {}
    
    # 添加bilibili配置
    if "bilibili" not in config:
        config["bilibili"] = {
            "enabled": True,
            "auto_upload": True,
            "schedule_time": "16:00"
        }
    
    with open(config_file, 'w', encoding='utf-8') as f:
        json.dump(config, f, ensure_ascii=False, indent=2)
    
    print("✅ 上传器配置已更新")
    
    # 6. 测试上传器
    print("\n6. 测试上传器...")
    try:
        from uploader.bilibili_uploader import BilibiliUploader
        uploader = BilibiliUploader()
        print("✅ Bilibili上传器初始化成功")
    except Exception as e:
        print(f"❌ Bilibili上传器初始化失败: {e}")
        return False
    
    print("\n🎉 Bilibili上传器设置完成!")
    print("\n📋 配置信息:")
    print(f"   - Cookie文件: {cookie_file}")
    print(f"   - 配置文件: {config_file}")
    print(f"   - 自动上传: {config['bilibili']['auto_upload']}")
    print(f"   - 发布时间: {config['bilibili']['schedule_time']}")
    
    return True

async def test_bilibili_upload():
    """测试bilibili上传功能"""
    print("\n🧪 测试Bilibili上传功能...")
    
    try:
        from uploader.bilibili_uploader import BilibiliUploader
        
        uploader = BilibiliUploader()
        
        # 检查配置
        print(f"📋 配置状态: {uploader.config.get('enabled', False)}")
        
        # 检查cookie文件
        cookie_file = Path(uploader.cookie_file)
        if cookie_file.exists():
            print(f"✅ Cookie文件存在: {uploader.cookie_file}")
        else:
            print(f"❌ Cookie文件不存在: {uploader.cookie_file}")
            return False
        
        print("✅ Bilibili上传器测试通过")
        return True
        
    except Exception as e:
        print(f"❌ Bilibili上传器测试失败: {e}")
        return False

async def main():
    """主函数"""
    print("🎬 Bilibili Uploader Setup for VideoLingo")
    print("=" * 60)
    
    # 设置
    if not setup_bilibili():
        print("\n❌ 设置失败，请检查上述错误信息")
        return
    
    # 测试
    if not await test_bilibili_upload():
        print("\n❌ 测试失败，请检查配置")
        return
    
    print("\n🎉 所有设置和测试都通过了!")
    print("\n💡 现在您可以在播放列表监控器中同时上传到抖音和bilibili了!")

if __name__ == "__main__":
    asyncio.run(main()) 