#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
# ------------
# Douyin Uploader for VideoLingo
# ------------
# Auto upload processed videos to Douyin
# Based on social-auto-upload project
# ------------
"""

import os
import asyncio
import json
from datetime import datetime
from pathlib import Path
from typing import Optional, List, Dict
import logging

try:
    from playwright.async_api import Playwright, async_playwright, Page
    PLAYWRIGHT_AVAILABLE = True
except ImportError:
    PLAYWRIGHT_AVAILABLE = False
    print("⚠️ Playwright not available. Please install: pip install playwright")

class DouyinUploader:
    def __init__(self, config_file: str = "uploader_config.json"):
        self.config_file = config_file
        self.config = self.load_config()
        self.logger = self.setup_logger()
        
    def setup_logger(self):
        """设置日志"""
        logger = logging.getLogger('douyin_uploader')
        logger.setLevel(logging.INFO)
        
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            handler.setFormatter(formatter)
            logger.addHandler(handler)
        
        return logger
    
    def load_config(self) -> Dict:
        """加载配置文件"""
        default_config = {
            "douyin": {
                "enabled": False,
                "account_file": "cookies/douyin_uploader/account.json",
                "auto_upload": False,
                "schedule_time": "16:00",  # 默认发布时间
                "location": "杭州市",
                "tags": ["VideoLingo", "AI翻译", "视频配音"],
                "chrome_path": None
            },
            "upload_settings": {
                "max_title_length": 30,
                "max_tags": 10,
                "retry_times": 3,
                "wait_time": 2
            }
        }
        
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    user_config = json.load(f)
                    # 合并配置
                    for key, value in user_config.items():
                        if key in default_config:
                            default_config[key].update(value)
                        else:
                            default_config[key] = value
            except Exception as e:
                self.logger.error(f"Error loading config: {e}")
        
        return default_config
    
    def save_config(self):
        """保存配置文件"""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, ensure_ascii=False, indent=2)
        except Exception as e:
            self.logger.error(f"Error saving config: {e}")
    
    async def check_cookie_auth(self, account_file: str) -> bool:
        """检查Cookie是否有效"""
        if not PLAYWRIGHT_AVAILABLE:
            self.logger.error("Playwright not available")
            return False
            
        async with async_playwright() as playwright:
            # 获取Chrome路径配置
            chrome_path = self.config["douyin"].get("chrome_path")
            
            # 如果配置了Chrome路径且路径有效，使用指定的Chrome
            if chrome_path and chrome_path != "/" and os.path.exists(chrome_path):
                browser = await playwright.chromium.launch(headless=True, executable_path=chrome_path)
                self.logger.info(f"使用指定的Chrome: {chrome_path}")
            else:
                browser = await playwright.chromium.launch(headless=True)
                self.logger.info("使用Playwright默认的Chromium")
            
            context = await browser.new_context(storage_state=account_file)
            
            page = await context.new_page()
            await page.goto("https://creator.douyin.com/creator-micro/content/upload")
            
            try:
                await page.wait_for_url("https://creator.douyin.com/creator-micro/content/upload", timeout=5000)
            except:
                self.logger.info("Cookie已失效")
                await context.close()
                await browser.close()
                return False
            
            # 检查是否需要登录
            if await page.get_by_text('手机号登录').count() or await page.get_by_text('扫码登录').count():
                self.logger.info("Cookie已失效")
                await context.close()
                await browser.close()
                return False
            else:
                self.logger.info("Cookie有效")
                await context.close()
                await browser.close()
                return True
    
    async def generate_cookie(self, account_file: str):
        """生成Cookie文件"""
        if not PLAYWRIGHT_AVAILABLE:
            self.logger.error("Playwright not available")
            return False
            
        self.logger.info("即将打开浏览器，请扫码登录抖音创作者中心")
        
        async with async_playwright() as playwright:
            # 获取Chrome路径配置
            chrome_path = self.config["douyin"].get("chrome_path")
            
            # 如果配置了Chrome路径且路径有效，使用指定的Chrome
            if chrome_path and chrome_path != "/" and os.path.exists(chrome_path):
                browser = await playwright.chromium.launch(headless=False, executable_path=chrome_path)
                self.logger.info(f"使用指定的Chrome: {chrome_path}")
            else:
                browser = await playwright.chromium.launch(headless=False)
                self.logger.info("使用Playwright默认的Chromium")
            
            context = await browser.new_context()
            page = await context.new_page()
            
            await page.goto("https://creator.douyin.com/")
            await page.pause()  # 等待用户登录
            
            # 保存Cookie
            os.makedirs(os.path.dirname(account_file), exist_ok=True)
            await context.storage_state(path=account_file)
            
            await browser.close()
            self.logger.info("Cookie已保存")
            return True
    
    async def setup_douyin(self, account_file: str, handle: bool = True) -> bool:
        """设置抖音上传环境"""
        if not os.path.exists(account_file) or not await self.check_cookie_auth(account_file):
            if not handle:
                self.logger.error("Cookie文件不存在或已失效")
                return False
            
            self.logger.info("Cookie文件不存在或已失效，即将自动打开浏览器，请扫码登录")
            return await self.generate_cookie(account_file)
        
        return True
    
    def generate_title_and_tags(self, video_path: str, playlist_name: str) -> tuple:
        """生成标题和标签"""
        # 从文件名生成标题
        video_name = os.path.splitext(os.path.basename(video_path))[0]
        
        # 根据播放列表类型生成不同的标题
        if playlist_name == "中字":
            title = f"{video_name} - 中文字幕版"
            tags = self.config["douyin"]["tags"] + ["中文字幕", "翻译"]
        elif playlist_name == "中配":
            title = f"{video_name} - 中文配音版"
            tags = self.config["douyin"]["tags"] + ["中文配音", "AI配音"]
        else:
            title = video_name
            tags = self.config["douyin"]["tags"]
        
        # 限制标题长度
        max_length = self.config["upload_settings"]["max_title_length"]
        if len(title) > max_length:
            title = title[:max_length-3] + "..."
        
        # 限制标签数量
        max_tags = self.config["upload_settings"]["max_tags"]
        tags = tags[:max_tags]
        
        return title, tags
    
    async def upload_video(self, video_path: str, playlist_name: str, 
                          schedule_time: Optional[datetime] = None, custom_title: str = None) -> bool:
        """上传视频到抖音"""
        if not self.config["douyin"]["enabled"]:
            self.logger.info("抖音上传功能已禁用")
            return False
        
        if not PLAYWRIGHT_AVAILABLE:
            self.logger.error("Playwright not available")
            return False
        
        account_file = self.config["douyin"]["account_file"]
        
        # 设置抖音环境
        if not await self.setup_douyin(account_file):
            return False
        
        # 生成标题和标签
        if custom_title:
            # 使用自定义标题
            title = custom_title
            tags = self.generate_title_and_tags(video_path, playlist_name)[1]  # 只获取标签
            # 显示标题预览，支持1000字标题
            preview_length = min(200, len(title))
            self.logger.info(f"使用自定义标题: {title[:preview_length]}...")
            self.logger.info(f"标题长度: {len(title)} 字符 (最大1000)")
        else:
            # 使用默认标题生成逻辑
            title, tags = self.generate_title_and_tags(video_path, playlist_name)
        
        # 显示标题预览，支持长标题
        preview_length = min(200, len(title))
        self.logger.info(f"准备上传视频: {title[:preview_length]}...")
        if len(title) > 200:
            self.logger.info(f"完整标题长度: {len(title)} 字符")
        self.logger.info(f"标签: {tags}")
        
        # 创建上传任务
        upload_task = DouyinVideoUploader(
            title=title,
            file_path=video_path,
            tags=tags,
            publish_date=schedule_time,
            account_file=account_file,
            config=self.config
        )
        
        try:
            await upload_task.upload()
            self.logger.info(f"视频上传成功: {title[:preview_length]}...")
            return True
        except Exception as e:
            self.logger.error(f"视频上传失败: {title[:preview_length]}..., 错误: {e}")
            return False


class DouyinVideoUploader:
    """抖音视频上传器"""
    
    def __init__(self, title: str, file_path: str, tags: List[str], 
                 publish_date: datetime, account_file: str, config: Dict):
        self.title = title
        self.file_path = file_path
        self.tags = tags
        self.publish_date = publish_date
        self.account_file = account_file
        self.config = config
        self.logger = logging.getLogger('douyin_uploader')
    
    async def upload(self):
        """执行上传"""
        async with async_playwright() as playwright:
            # 获取Chrome路径配置
            chrome_path = self.config["douyin"].get("chrome_path")
            
            # 如果配置了Chrome路径且路径有效，使用指定的Chrome
            if chrome_path and chrome_path != "/" and os.path.exists(chrome_path):
                browser = await playwright.chromium.launch(headless=True, executable_path=chrome_path)
                self.logger.info(f"使用指定的Chrome: {chrome_path}")
            else:
                browser = await playwright.chromium.launch(headless=True)
                self.logger.info("使用Playwright默认的Chromium")
            
            # 创建上下文
            context = await browser.new_context(storage_state=self.account_file)
            page = await context.new_page()
            
            try:
                # 访问上传页面
                await page.goto("https://creator.douyin.com/creator-micro/content/upload")
                self.logger.info("正在打开抖音创作者中心...")
                
                # 等待页面加载
                await page.wait_for_url("https://creator.douyin.com/creator-micro/content/upload")
                
                # 上传视频文件
                await page.locator("div[class^='container'] input").set_input_files(self.file_path)
                self.logger.info("正在上传视频文件...")
                
                # 等待进入发布页面
                await self.wait_for_publish_page(page)
                
                # 填写标题和标签
                await self.fill_title_and_tags(page)
                
                # 等待视频上传完成
                await self.wait_for_upload_complete(page)
                
                # 设置位置
                await self.set_location(page)
                
                # 设置定时发布
                if self.publish_date and self.publish_date != datetime.now():
                    await self.set_schedule_time(page)
                
                # 发布视频
                await self.publish_video(page)
                
            finally:
                await browser.close()
    
    async def wait_for_publish_page(self, page: Page):
        """等待进入发布页面"""
        while True:
            try:
                await page.wait_for_url(
                    "https://creator.douyin.com/creator-micro/content/publish?enter_from=publish_page", 
                    timeout=3000)
                self.logger.info("成功进入发布页面!")
                break
            except Exception:
                try:
                    await page.wait_for_url(
                        "https://creator.douyin.com/creator-micro/content/post/video?enter_from=publish_page",
                        timeout=3000)
                    self.logger.info("成功进入发布页面!")
                    break
                except:
                    self.logger.info("等待进入发布页面...")
                    await asyncio.sleep(0.5)
    
    async def fill_title_and_tags(self, page: Page):
        """填写标题和标签"""
        self.logger.info("正在填写标题和标签...")
        
        # 填写标题
        title_container = page.get_by_text('作品标题').locator("..").locator("xpath=following-sibling::div[1]").locator("input")
        if await title_container.count():
            await title_container.fill(self.title)
        else:
            titlecontainer = page.locator(".notranslate")
            await titlecontainer.click()
            await page.keyboard.press("Backspace")
            await page.keyboard.press("Control+KeyA")
            await page.keyboard.press("Delete")
            await page.keyboard.type(self.title)
            await page.keyboard.press("Enter")
        
        # 填写标签
        css_selector = ".zone-container"
        for tag in self.tags:
            await page.type(css_selector, "#" + tag)
            await page.press(css_selector, "Space")
        
        self.logger.info(f"已添加 {len(self.tags)} 个标签")
    
    async def wait_for_upload_complete(self, page: Page):
        """等待视频上传完成"""
        while True:
            try:
                number = await page.locator('[class^="long-card"] div:has-text("重新上传")').count()
                if number > 0:
                    self.logger.info("视频上传完成")
                    break
                else:
                    self.logger.info("正在上传视频...")
                    await asyncio.sleep(2)
                    
                    if await page.locator('div.progress-div > div:has-text("上传失败")').count():
                        self.logger.error("上传失败，准备重试")
                        await self.handle_upload_error(page)
            except:
                self.logger.info("正在上传视频...")
                await asyncio.sleep(2)
    
    async def handle_upload_error(self, page: Page):
        """处理上传错误"""
        self.logger.info("重新上传视频...")
        await page.locator('div.progress-div [class^="upload-btn-input"]').set_input_files(self.file_path)
    
    async def set_location(self, page: Page):
        """设置位置"""
        location = self.config["douyin"]["location"]
        # TODO: 实现位置设置
        self.logger.info(f"设置位置: {location}")
    
    async def set_schedule_time(self, page: Page):
        """设置定时发布"""
        self.logger.info("设置定时发布...")
        
        # 选择定时发布
        label_element = page.locator("[class^='radio']:has-text('定时发布')")
        await label_element.click()
        await asyncio.sleep(1)
        
        # 设置时间
        publish_date_str = self.publish_date.strftime("%Y-%m-%d %H:%M")
        await page.locator('.semi-input[placeholder="日期和时间"]').click()
        await page.keyboard.press("Control+KeyA")
        await page.keyboard.type(publish_date_str)
        await page.keyboard.press("Enter")
        
        await asyncio.sleep(1)
    
    async def publish_video(self, page: Page):
        """发布视频"""
        self.logger.info("正在发布视频...")
        
        # 点击发布按钮
        publish_button = page.get_by_role('button', name="发布", exact=True)
        await publish_button.click()
        
        # 等待发布完成
        await asyncio.sleep(5)
        self.logger.info("视频发布成功!")


# 便捷函数
async def upload_to_douyin(video_path: str, playlist_name: str, 
                          schedule_time: Optional[datetime] = None, custom_title: str = None) -> bool:
    """便捷的上传函数"""
    uploader = DouyinUploader()
    return await uploader.upload_video(video_path, playlist_name, schedule_time, custom_title) 