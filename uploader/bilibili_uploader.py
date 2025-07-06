#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
# ------------
# Bilibili Uploader for VideoLingo
# ------------
# 基于social-auto-upload项目的bilibili上传器
# ------------
"""

import os
import sys
import json
import random
import asyncio
import threading
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, Optional, List

# 尝试导入biliup，如果不存在则提示安装
try:
    from biliup.plugins.bili_webup import BiliBili, Data
    BILIBILI_AVAILABLE = True
except ImportError:
    BILIBILI_AVAILABLE = False
    print("⚠️ Bilibili uploader not available. Please install: pip install biliup")

class BilibiliUploader:
    def __init__(self):
        self.upload_thread_num = 3
        self.copyright = 1
        self.lines = 'AUTO'
        self.cookie_file = "uploader_config/bilibili_cookies.json"
        self.config_file = "uploader_config.json"
        
        # 加载配置
        self.config = self.load_config()
        
    def load_config(self) -> Dict:
        """加载bilibili上传配置"""
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    return config.get("bilibili", {})
            except:
                return {"enabled": False}
        return {"enabled": False}
    
    def extract_keys_from_json(self, data: Dict) -> Dict:
        """从JSON数据中提取指定的键"""
        keys_to_extract = ["SESSDATA", "bili_jct", "DedeUserID__ckMd5", "DedeUserID", "access_token"]
        extracted_data = {}

        # 提取cookie数据
        if 'cookie_info' in data and 'cookies' in data['cookie_info']:
            for cookie in data['cookie_info']['cookies']:
                if cookie['name'] in keys_to_extract:
                    extracted_data[cookie['name']] = cookie['value']

        # 提取access_token
        if "token_info" in data and "access_token" in data['token_info']:
            extracted_data['access_token'] = data['token_info']['access_token']

        return extracted_data
    
    def read_cookie_json_file(self, filepath: Path) -> Dict:
        """读取cookie JSON文件"""
        with open(filepath, 'r', encoding='utf-8') as file:
            content = json.load(file)
            return content
    
    def random_emoji(self) -> str:
        """生成随机emoji"""
        emoji_list = ["🍏", "🍎", "🍊", "🍋", "🍌", "🍉", "🍇", "🍓", "🍈", "🍒", "🍑", "🍍", "🥭", "🥥", "🥝",
                      "🍅", "🍆", "🥑", "🥦", "🥒", "🥬", "🌶", "🌽", "🥕", "🥔", "🍠", "🥐", "🍞", "🥖", "🥨", "🥯", "🧀", "🥚", "🍳", "🥞",
                      "🥓", "🥩", "🍗", "🍖", "🌭", "🍔", "🍟", "🍕", "🥪", "🥙", "🌮", "🌯", "🥗", "🥘", "🥫", "🍝", "🍜", "🍲", "🍛", "🍣",
                      "🍱", "🥟", "🍤", "🍙", "🍚", "🍘", "🍥", "🥮", "🥠", "🍢", "🍡", "🍧", "🍨", "🍦", "🥧", "🍰", "🎂", "🍮", "🍭", "🍬",
                      "🍫", "🍿", "🧂", "🍩", "🍪", "🌰", "🥜", "🍯", "🥛", "🍼", "☕️", "🍵", "🥤", "🍶", "🍻", "🥂", "🍷", "🥃", "🍸", "🍹",
                      "🍾", "🥄", "🍴", "🍽", "🥣", "🥡", "🥢"]
        return random.choice(emoji_list)
    
    def get_category_id(self, playlist_name: str) -> int:
        """根据播放列表名称获取bilibili分区ID"""
        # 默认分区映射
        category_mapping = {
            "中字": 27,  # 综合
            "中配": 27,  # 综合
            "default": 27
        }
        return category_mapping.get(playlist_name, category_mapping["default"])
    
    def generate_tags(self, playlist_name: str, video_title: str) -> List[str]:
        """生成bilibili标签"""
        base_tags = ["VideoLingo", "AI翻译", "自动生成"]
        
        # 根据播放列表类型添加特定标签
        if playlist_name == "中字":
            base_tags.extend(["中文字幕", "字幕翻译"])
        elif playlist_name == "中配":
            base_tags.extend(["中文配音", "AI配音", "语音合成"])
        
        # 从视频标题中提取关键词作为标签
        title_words = video_title.split()
        for word in title_words[:3]:  # 取前3个词作为标签
            if len(word) > 2:  # 过滤太短的词
                base_tags.append(word)
        
        return base_tags[:10]  # 限制标签数量
    
    async def upload_video(self, video_file: str, playlist_name: str, 
                          schedule_time: Optional[datetime] = None, 
                          custom_title: str = None) -> bool:
        """上传视频到bilibili"""
        if not BILIBILI_AVAILABLE:
            print("⚠️ Bilibili uploader not available")
            return False
        
        if not self.config.get("enabled", False):
            print("⚠️ Bilibili uploader is disabled in config")
            return False
        
        try:
            # 检查cookie文件
            cookie_file = Path(self.cookie_file)
            if not cookie_file.exists():
                print(f"❌ Bilibili cookie file not found: {self.cookie_file}")
                return False
            
            # 读取cookie数据
            cookie_data = self.read_cookie_json_file(cookie_file)
            cookie_data = self.extract_keys_from_json(cookie_data)
            
            # 检查必要的cookie字段
            required_fields = ["SESSDATA", "bili_jct", "DedeUserID"]
            missing_fields = [field for field in required_fields if field not in cookie_data]
            if missing_fields:
                print(f"❌ Missing required cookie fields: {missing_fields}")
                return False
            
            # 准备上传数据
            video_path = Path(video_file)
            if not video_path.exists():
                print(f"❌ Video file not found: {video_file}")
                return False
            
            # 生成标题
            if custom_title:
                title = custom_title
            else:
                title = video_path.stem
            
            # 限制标题长度为80个字符（bilibili限制）
            if len(title) > 80:
                title = title[:77] + "..."  # 保留3个字符给省略号
                print(f"⚠️ Title truncated to 80 characters: {title}")
            
            # 避免重复标题，添加随机emoji
            title += self.random_emoji()
            
            # 再次检查长度（emoji可能占用多个字符）
            if len(title) > 80:
                # 移除emoji，重新截断
                title = title[:77] + "..."
                print(f"⚠️ Title truncated again after emoji: {title}")
            
            # 生成描述
            desc = f"AI自动翻译生成 - {title}\n\n#AI翻译"
            
            # 获取分区ID
            tid = self.get_category_id(playlist_name)
            
            # 生成标签
            tags = self.generate_tags(playlist_name, title)
            tags_str = ','.join(tags)
            
            # 设置发布时间
            if schedule_time:
                dtime = int(schedule_time.timestamp())
            else:
                dtime = 0  # 立即发布
            
            print(f"📺 Uploading to Bilibili: {title}")
            print(f"📏 Title length: {len(title)} characters (max 80)")
            print(f"📝 Description: {custom_title}")
            print(f"🏷️ Tags: {tags_str}")
            print(f"📂 Category ID: {tid}")
            
            # 创建上传器实例
            uploader = BilibiliUploaderClass(
                cookie_data, video_path, title, desc, tid, tags, dtime
            )
            
            # 执行上传
            success = uploader.upload()
            
            if success:
                print(f"✅ Successfully uploaded to Bilibili: {title}")
            else:
                print(f"❌ Failed to upload to Bilibili: {title}")
            
            return success
            
        except Exception as e:
            print(f"❌ Error uploading to Bilibili: {e}")
            return False


class BilibiliUploaderClass:
    """Bilibili上传器类（基于biliup）"""
    
    def __init__(self, cookie_data: Dict, file: Path, title: str, desc: str, 
                 tid: int, tags: List[str], dtime: int):
        self.upload_thread_num = 3
        self.copyright = 1
        self.lines = 'AUTO'
        self.cookie_data = cookie_data
        self.file = file
        self.title = title
        self.desc = desc
        self.tid = tid
        self.tags = tags
        self.dtime = dtime
        self._init_data()
    
    def _init_data(self):
        """初始化上传数据"""
        self.data = Data()
        self.data.copyright = self.copyright
        self.data.title = self.title
        self.data.desc = self.desc
        self.data.tid = self.tid
        self.data.set_tag(self.tags)
        self.data.dtime = self.dtime
    
    def upload(self) -> bool:
        """执行上传"""
        try:
            # 使用线程来运行biliup，避免异步事件循环冲突
            result = [False]  # 使用列表来存储结果
            
            def upload_in_thread():
                try:
                    with BiliBili(self.data) as bili:
                        bili.login_by_cookies(self.cookie_data)
                        bili.access_token = self.cookie_data.get('access_token')
                        
                        # 上传视频文件
                        video_part = bili.upload_file(
                            str(self.file), 
                            lines=self.lines,
                            tasks=self.upload_thread_num
                        )
                        
                        video_part['title'] = self.title
                        self.data.append(video_part)
                        
                        # 提交视频
                        ret = bili.submit()
                        
                        if ret.get('code') == 0:
                            print(f'✅ {self.file.name} 上传成功')
                            result[0] = True
                        else:
                            print(f'❌ {self.file.name} 上传失败: {ret.get("message")}')
                            result[0] = False
                            
                except Exception as e:
                    print(f"❌ Upload error: {e}")
                    result[0] = False
            
            # 在新线程中运行上传
            upload_thread = threading.Thread(target=upload_in_thread)
            upload_thread.start()
            upload_thread.join()  # 等待线程完成
            
            return result[0]
                    
        except Exception as e:
            print(f"❌ Upload error: {e}")
            return False


# 测试函数
async def test_bilibili_uploader():
    """测试bilibili上传器"""
    print("🧪 Testing Bilibili Uploader...")
    
    uploader = BilibiliUploader()
    
    # 检查配置
    print(f"📋 Config enabled: {uploader.config.get('enabled', False)}")
    
    # 检查cookie文件
    cookie_file = Path(uploader.cookie_file)
    if cookie_file.exists():
        print(f"✅ Cookie file exists: {uploader.cookie_file}")
    else:
        print(f"❌ Cookie file not found: {uploader.cookie_file}")
    
    # 检查biliup可用性
    if BILIBILI_AVAILABLE:
        print("✅ Biliup library available")
    else:
        print("❌ Biliup library not available")
    
    return True


if __name__ == "__main__":
    asyncio.run(test_bilibili_uploader()) 