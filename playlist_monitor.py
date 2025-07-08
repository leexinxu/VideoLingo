#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
# ------------
# YouTube Playlist Monitor and Auto Translation/Dubbing
# ------------
# This script monitors YouTube playlists and automatically processes videos
# using VideoLingo for translation and dubbing
# ------------
"""

import os
import sys
import time
import json
import requests
import yt_dlp
import logging
from datetime import datetime
from pathlib import Path
import shutil
from typing import Dict, List, Optional, Tuple

# Add current directory to path for imports
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

from core.st_utils.imports_and_utils import *
from core.utils.onekeycleanup import cleanup
from core.utils.config_utils import load_key, update_key
from core import *

# 设置日志配置
def setup_logging():
    """设置日志配置"""
    # 创建logs目录
    os.makedirs("logs", exist_ok=True)
    
    # 使用固定的日志文件名
    log_file = "logs/playlist_monitor.log"
    
    # 配置日志格式
    log_format = '%(asctime)s - %(levelname)s - %(message)s'
    date_format = '%Y-%m-%d %H:%M:%S'
    
    # 检查日志文件大小，如果超过限制则清理
    max_log_size = 10 * 1024 * 1024  # 10MB
    if os.path.exists(log_file) and os.path.getsize(log_file) > max_log_size:
        logger.info(f"Log file too large ({os.path.getsize(log_file)} bytes), cleaning old content...")
        # 保留最后1000行
        try:
            with open(log_file, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            with open(log_file, 'w', encoding='utf-8') as f:
                # 保留最后1000行
                f.writelines(lines[-1000:])
            logger.info(f"Log file cleaned, kept last 1000 lines")
        except Exception as e:
            logger.error(f"Error cleaning log file: {e}")
    
    # 配置日志处理器
    logging.basicConfig(
        level=logging.INFO,
        format=log_format,
        datefmt=date_format,
        handlers=[
            logging.FileHandler(log_file, encoding='utf-8', mode='a'),  # 追加模式
            logging.StreamHandler(sys.stdout)
        ]
    )
    
    # 创建logger
    logger = logging.getLogger(__name__)
    logger.info(f"Logging initialized. Log file: {log_file}")
    logger.info(f"Max log size: {max_log_size / (1024*1024):.1f}MB")
    
    # 重定向所有print输出到日志文件
    class LogRedirector:
        def __init__(self, logger, original_stdout):
            self.logger = logger
            self.original_stdout = original_stdout
            self.buffer = ""
        
        def write(self, text):
            # 保存到原始stdout
            self.original_stdout.write(text)
            # 添加到缓冲区
            self.buffer += text
            
            # 如果遇到换行符，记录日志
            if '\n' in text:
                lines = self.buffer.split('\n')
                for line in lines[:-1]:  # 除了最后一行（可能不完整）
                    if line.strip():  # 忽略空行
                        self.logger.info(f"[STDOUT] {line}")
                self.buffer = lines[-1]  # 保留最后一行（可能不完整）
        
        def flush(self):
            if self.buffer.strip():
                self.logger.info(f"[STDOUT] {self.buffer}")
                self.buffer = ""
            self.original_stdout.flush()
        
        def fileno(self):
            # 为subprocess提供文件描述符
            return self.original_stdout.fileno()
    
    # 重定向stdout
    original_stdout = sys.stdout
    sys.stdout = LogRedirector(logger, original_stdout)
    
    # 重定向stderr
    class ErrorLogRedirector:
        def __init__(self, logger, original_stderr):
            self.logger = logger
            self.original_stderr = original_stderr
            self.buffer = ""
        
        def write(self, text):
            # 保存到原始stderr
            self.original_stderr.write(text)
            # 添加到缓冲区
            self.buffer += text
            
            # 如果遇到换行符，记录日志
            if '\n' in text:
                lines = self.buffer.split('\n')
                for line in lines[:-1]:  # 除了最后一行（可能不完整）
                    if line.strip():  # 忽略空行
                        # 智能判断是否为真正的错误信息
                        if self._is_error_message(line):
                            self.logger.error(f"[STDERR] {line}")
                        else:
                            self.logger.info(f"[STDERR] {line}")
                self.buffer = lines[-1]  # 保留最后一行（可能不完整）
        
        def flush(self):
            if self.buffer.strip():
                if self._is_error_message(self.buffer):
                    self.logger.error(f"[STDERR] {self.buffer}")
                else:
                    self.logger.info(f"[STDERR] {self.buffer}")
                self.buffer = ""
            self.original_stderr.flush()
        
        def fileno(self):
            # 为subprocess提供文件描述符
            return self.original_stderr.fileno()
        
        def _is_error_message(self, message):
            """判断是否为真正的错误信息"""
            # 错误关键词
            error_keywords = [
                'error', 'Error', 'ERROR',
                'exception', 'Exception', 'EXCEPTION',
                'failed', 'Failed', 'FAILED',
                'failure', 'Failure', 'FAILURE',
                'warning', 'Warning', 'WARNING',
                'traceback', 'Traceback', 'TRACEBACK',
                'stack trace', 'Stack trace',
                'segmentation fault', 'Segmentation fault',
                'core dumped', 'Core dumped',
                'abort', 'Abort', 'ABORT',
                'fatal', 'Fatal', 'FATAL',
                'critical', 'Critical', 'CRITICAL'
            ]
            
            # 检查是否包含错误关键词
            for keyword in error_keywords:
                if keyword in message:
                    return True
            
            # 检查是否包含时间戳格式的错误日志（如：2025-07-08 22:32:40,701 - douyin_uploader - INFO）
            import re
            if re.match(r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d{3} - \w+ - (ERROR|WARNING|CRITICAL)', message):
                return True
            
            # 默认认为是正常信息
            return False
    
    original_stderr = sys.stderr
    sys.stderr = ErrorLogRedirector(logger, original_stderr)
    
    logger.info("All console output will be logged to file")
    
    return logger

# 初始化日志
logger = setup_logging()

# 导入上传器
try:
    from uploader.douyin_uploader import DouyinUploader
    UPLOADER_AVAILABLE = True
    logger.info("Douyin uploader imported successfully")
except ImportError:
    UPLOADER_AVAILABLE = False
    logger.warning("Douyin uploader not available. Please install: pip install playwright")

# 导入bilibili上传器
try:
    from uploader.bilibili_uploader import BilibiliUploader
    BILIBILI_UPLOADER_AVAILABLE = True
    logger.info("Bilibili uploader imported successfully")
except ImportError:
    BILIBILI_UPLOADER_AVAILABLE = False
    logger.warning("Bilibili uploader not available. Please install: pip install biliup")

class PlaylistMonitor:
    def __init__(self):
        logger.info("Initializing PlaylistMonitor...")
        
        self.processed_videos_file = "playlist_monitor/processed_videos.json"
        self.playlists = {
            "中字": {
                "url": "https://www.youtube.com/playlist?list=PLxjtcx2z5_41xdgXxdXCZ8lFcSwTZujRt",
                "dubbing": False,  # 只翻译生成字幕
                "description": "中字播放列表 - 仅翻译生成字幕"
            },
            "中配": {
                "url": "https://www.youtube.com/playlist?list=PLxjtcx2z5_42OhI7vyzYVxXpzb_XIadrN", 
                "dubbing": True,   # 翻译并配音
                "description": "中配播放列表 - 翻译并配音"
            }
        }
        
        # 创建必要的目录
        os.makedirs("playlist_monitor", exist_ok=True)
        os.makedirs("output", exist_ok=True)
        logger.info("Directories created successfully")
        
        # 加载代理配置
        self.proxy_config = self.load_proxy_config()
        logger.info(f"Proxy config loaded: {self.proxy_config.get('proxy_settings', {}).get('enabled', False)}")
        
        # 加载上传器配置
        self.uploader_config = self.load_uploader_config()
        logger.info(f"Uploader config loaded: {self.uploader_config}")
        
        # 加载已处理的视频记录
        self.processed_videos = self.load_processed_videos()
        logger.info(f"Processed videos loaded: {len(self.processed_videos.get('中字', []))} 中字, {len(self.processed_videos.get('中配', []))} 中配")
        
        logger.info("PlaylistMonitor initialized successfully")
        
    def load_processed_videos(self) -> Dict[str, List[str]]:
        """加载已处理的视频记录"""
        logger.info("Loading processed videos...")
        if os.path.exists(self.processed_videos_file):
            try:
                with open(self.processed_videos_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    
                # 清理过大的处理记录（保留最近1000个）
                cleaned_data = {}
                for playlist_name, video_ids in data.items():
                    if len(video_ids) > 1000:
                        logger.info(f"Cleaning {playlist_name} processed videos: {len(video_ids)} -> 1000")
                        cleaned_data[playlist_name] = video_ids[-1000:]  # 保留最近1000个
                    else:
                        cleaned_data[playlist_name] = video_ids
                
                logger.info(f"Processed videos loaded successfully: {cleaned_data}")
                return cleaned_data
            except Exception as e:
                logger.error(f"Error loading processed videos: {e}")
                return {"中字": [], "中配": []}
        logger.info("No processed videos file found, creating new one")
        return {"中字": [], "中配": []}
    
    def load_proxy_config(self) -> Dict:
        """加载代理配置"""
        logger.info("Loading proxy config...")
        if os.path.exists("proxy_config.json"):
            try:
                with open("proxy_config.json", 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    logger.info(f"Proxy config loaded: {config}")
                    return config
            except Exception as e:
                logger.error(f"Error loading proxy config: {e}")
                return {"proxy_settings": {"enabled": False}}
        logger.info("No proxy config file found, using default")
        return {"proxy_settings": {"enabled": False}}
    
    def load_uploader_config(self) -> Dict:
        """加载上传器配置"""
        logger.info("Loading uploader config...")
        if os.path.exists("uploader_config.json"):
            try:
                with open("uploader_config.json", 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    logger.info(f"Uploader config loaded: {config}")
                    return config
            except Exception as e:
                logger.error(f"Error loading uploader config: {e}")
                return {"douyin": {"enabled": False}, "bilibili": {"enabled": False}}
        logger.info("No uploader config file found, using default")
        return {"douyin": {"enabled": False}, "bilibili": {"enabled": False}}
    
    def save_processed_videos(self):
        """保存已处理的视频记录"""
        try:
            with open(self.processed_videos_file, 'w', encoding='utf-8') as f:
                json.dump(self.processed_videos, f, ensure_ascii=False, indent=2)
            logger.info(f"Processed videos saved: {self.processed_videos}")
        except Exception as e:
            logger.error(f"Error saving processed videos: {e}")
    
    def get_playlist_videos(self, playlist_url: str) -> List[Dict]:
        """获取播放列表中的所有视频信息"""
        logger.info(f"Getting playlist videos from: {playlist_url}")
        try:
            ydl_opts = {
                'quiet': True,
                'extract_flat': True,
                'playlist_items': '1-50'  # 获取前50个视频（最新加入的）
            }
            
            # 添加代理配置
            if self.proxy_config.get("proxy_settings", {}).get("enabled", False):
                ydl_opts['proxy'] = self.proxy_config.get("yt_dlp_proxy", "http://127.0.0.1:7890")
                logger.info(f"Using proxy: {ydl_opts['proxy']}")
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                playlist_info = ydl.extract_info(playlist_url, download=False)
                videos = playlist_info.get('entries', [])
                
                # 过滤掉无效的视频条目
                valid_videos = [v for v in videos if v and 'id' in v and 'title' in v]
                
                logger.info(f"Playlist info: {len(videos)} total videos, {len(valid_videos)} valid videos")
                
                return valid_videos
        except Exception as e:
            logger.error(f"Error getting playlist videos: {e}")
            return []
    
    def is_new_video(self, video_id: str, playlist_name: str) -> bool:
        """检查是否为新视频"""
        is_new = video_id not in self.processed_videos.get(playlist_name, [])
        logger.info(f"Video {video_id} in {playlist_name}: {'NEW' if is_new else 'ALREADY PROCESSED'}")
        return is_new
    
    def mark_video_processed(self, video_id: str, playlist_name: str):
        """标记视频为已处理"""
        if playlist_name not in self.processed_videos:
            self.processed_videos[playlist_name] = []
        self.processed_videos[playlist_name].append(video_id)
        self.save_processed_videos()
        logger.info(f"Marked video {video_id} as processed in {playlist_name}")
    
    def download_video(self, video_url: str) -> bool:
        """下载视频"""
        logger.info(f"Downloading video: {video_url}")
        try:
            # 设置代理环境变量
            if self.proxy_config.get("proxy_settings", {}).get("enabled", False):
                proxy_settings = self.proxy_config["proxy_settings"]
                os.environ['https_proxy'] = proxy_settings.get("https_proxy", "http://127.0.0.1:7890")
                os.environ['http_proxy'] = proxy_settings.get("http_proxy", "http://127.0.0.1:7890")
                os.environ['all_proxy'] = proxy_settings.get("all_proxy", "socks5://127.0.0.1:7890")
                logger.info(f"Using proxy: {os.environ['https_proxy']}")

            # === 临时还原stdout/stderr，避免yt-dlp输出被日志捕获 ===
            current_stdout = sys.stdout
            current_stderr = sys.stderr
            sys.stdout = sys.__stdout__
            sys.stderr = sys.__stderr__

            _1_ytdlp.download_video_ytdlp(video_url, resolution=load_key("ytb_resolution"))

            # 恢复日志重定向
            sys.stdout = current_stdout
            sys.stderr = current_stderr
            # === 还原结束 ===

            logger.info("Video downloaded successfully")
            return True
        except Exception as e:
            logger.error(f"Error downloading video: {e}")
            return False
    
    def process_text_only(self, video_url: str) -> bool:
        """仅处理文本翻译和字幕生成"""
        logger.info("Processing text translation and subtitle generation...")
        try:
            # 1. 转录
            logger.info("Step 1: Transcribing with Whisper...")
            _2_asr.transcribe()
            
            # 2. 分割句子
            logger.info("Step 2: Splitting sentences...")
            _3_1_split_nlp.split_by_spacy()
            _3_2_split_meaning.split_sentences_by_meaning()
            
            # 3. 总结和翻译
            logger.info("Step 3: Summarizing and translating...")
            _4_1_summarize.get_summary()
            _4_2_translate.translate_all()
            
            # 4. 处理和字幕对齐
            logger.info("Step 4: Processing and aligning subtitles...")
            _5_split_sub.split_for_sub_main()
            _6_gen_sub.align_timestamp_main()
            
            # 5. 合并字幕到视频
            logger.info("Step 5: Merging subtitles to video...")
            _7_sub_into_vid.merge_subtitles_to_video()
            
            logger.info("Text processing completed successfully!")
            return True
            
        except Exception as e:
            logger.error(f"Error in text processing: {e}")
            return False
    
    def process_with_dubbing(self, video_url: str) -> bool:
        """处理文本翻译、字幕生成和配音"""
        logger.info("Processing text translation, subtitle generation, and dubbing...")
        try:
            # 1-5. 文本处理步骤（与process_text_only相同）
            if not self.process_text_only(video_url):
                return False
            
            # 6. 生成音频任务
            logger.info("Step 6: Generating audio tasks...")
            _8_1_audio_task.gen_audio_task_main()
            _8_2_dub_chunks.gen_dub_chunks()
            
            # 7. 提取参考音频
            logger.info("Step 7: Extracting reference audio...")
            _9_refer_audio.extract_refer_audio_main()
            
            # 8. 生成音频
            logger.info("Step 8: Generating audio...")
            _10_gen_audio.gen_audio()
            
            # 9. 合并完整音频
            logger.info("Step 9: Merging full audio...")
            _11_merge_audio.merge_full_audio()
            
            # 10. 合并配音到视频
            logger.info("Step 10: Merging dubbing to video...")
            _12_dub_to_vid.merge_video_audio()
            
            logger.info("Dubbing processing completed successfully!")
            return True
            
        except Exception as e:
            logger.error(f"Error in dubbing processing: {e}")
            return False
    
    def archive_to_history(self, playlist_name: str, video_info: Dict = None):
        """存档到历史文件夹，按播放列表和视频信息划分"""
        logger.info(f"Archiving to history for playlist: {playlist_name}")
        try:
            # 创建播放列表特定的历史文件夹
            history_dir = f"history/{playlist_name}"
            os.makedirs(history_dir, exist_ok=True)
            
            # 如果有视频信息，创建更详细的文件夹结构
            if video_info:
                video_id = video_info.get('id', 'unknown')
                video_title = video_info.get('title', 'unknown')
                # 清理文件名中的非法字符
                safe_title = "".join(c for c in video_title if c.isalnum() or c in (' ', '-', '_')).rstrip()
                safe_title = safe_title[:50]  # 限制长度
                
                # 创建视频特定的文件夹
                video_dir = os.path.join(history_dir, f"{video_id}_{safe_title}")
                os.makedirs(video_dir, exist_ok=True)
                
                # 添加处理信息文件
                process_info = {
                    "video_id": video_id,
                    "video_title": video_title,
                    "playlist_name": playlist_name,
                    "process_time": datetime.now().isoformat(),
                    "playlist_config": self.playlists[playlist_name]
                }
                
                with open(os.path.join(video_dir, "process_info.json"), 'w', encoding='utf-8') as f:
                    json.dump(process_info, f, ensure_ascii=False, indent=2)
                
                logger.info(f"Created video directory: {video_dir}")
            else:
                video_dir = history_dir
            
            # 移动输出文件到视频特定的历史文件夹
            if os.path.exists("output"):
                moved_files = []
                for item in os.listdir("output"):
                    src_path = os.path.join("output", item)
                    dst_path = os.path.join(video_dir, item)
                    
                    if os.path.isfile(src_path):
                        shutil.move(src_path, dst_path)
                        moved_files.append(item)
                    elif os.path.isdir(src_path):
                        if os.path.exists(dst_path):
                            shutil.rmtree(dst_path)
                        shutil.move(src_path, dst_path)
                        moved_files.append(item)
                
                logger.info(f"Moved {len(moved_files)} files to history: {moved_files}")
            
            logger.info(f"Archive completed for {playlist_name}!")
            return True
        except Exception as e:
            logger.error(f"Error archiving to history: {e}")
            return False
    
    async def upload_to_douyin(self, video_info: Dict, playlist_name: str):
        """上传视频到抖音"""
        if not UPLOADER_AVAILABLE:
            logger.warning("Douyin uploader not available")
            return False
        
        try:
            # 查找处理后的视频文件
            video_id = video_info.get('id', 'unknown')
            video_title = video_info.get('title', 'unknown')
            safe_title = "".join(c for c in video_title if c.isalnum() or c in (' ', '-', '_')).rstrip()
            safe_title = safe_title[:50]
            
            # 根据播放列表类型确定视频文件
            if playlist_name == "中字":
                video_file = f"history/{playlist_name}/{video_id}_{safe_title}/output_sub.mp4"
            elif playlist_name == "中配":
                video_file = f"history/{playlist_name}/{video_id}_{safe_title}/output_dub.mp4"
            else:
                logger.error(f"Unknown playlist type: {playlist_name}")
                return False
            
            if not os.path.exists(video_file):
                logger.error(f"Video file not found: {video_file}")
                return False
            
            # 尝试读取terminology.json中的theme字段作为标题
            theme_title = None
            terminology_file = f"history/{playlist_name}/{video_id}_{safe_title}/log/terminology.json"
            if os.path.exists(terminology_file):
                try:
                    with open(terminology_file, 'r', encoding='utf-8') as f:
                        terminology_data = json.load(f)
                        theme_title = terminology_data.get('theme', video_title)
                        # 显示前200个字符的预览，支持1000字标题
                        preview_length = min(200, len(theme_title))
                        logger.info(f"Using theme from terminology.json: {theme_title[:preview_length]}...")
                        logger.info(f"Title length: {len(theme_title)} characters (max 1000)")
                except Exception as e:
                    logger.warning(f"Error reading terminology.json: {e}")
                    theme_title = video_title
            else:
                logger.warning(f"terminology.json not found: {terminology_file}")
                theme_title = video_title
            
            logger.info(f"Uploading to Douyin: {video_title}")
            # 显示标题预览，支持长标题
            preview_length = min(200, len(theme_title))
            logger.info(f"Title for Douyin: {theme_title[:preview_length]}...")
            if len(theme_title) > 200:
                logger.info(f"Full title length: {len(theme_title)} characters")
            
            # 创建上传器实例
            uploader = DouyinUploader()
            
            # 设置发布时间（如果配置了定时发布）
            schedule_time = None
            if self.uploader_config.get("douyin", {}).get("auto_upload", False):
                schedule_time_str = self.uploader_config["douyin"]["schedule_time"]
                
                # 如果schedule_time为null，则立即发布
                if schedule_time_str is None:
                    schedule_time = None  # 立即发布
                    logger.info("设置为立即发布")
                else:
                    # 解析时间字符串，设置为明天的指定时间
                    from datetime import timedelta
                    tomorrow = datetime.now() + timedelta(days=1)
                    hour, minute = map(int, schedule_time_str.split(':'))
                    schedule_time = tomorrow.replace(hour=hour, minute=minute, second=0, microsecond=0)
                    logger.info(f"设置为定时发布: {schedule_time}")
            
            # 执行上传，传递自定义标题
            success = await uploader.upload_video(video_file, playlist_name, schedule_time, custom_title=theme_title)
            
            if success:
                logger.info(f"Successfully uploaded to Douyin: {video_title}")
            else:
                logger.error(f"Failed to upload to Douyin: {video_title}")
            
            return success
            
        except Exception as e:
            logger.error(f"Error uploading to Douyin: {e}")
            return False
    
    async def upload_to_bilibili(self, video_info: Dict, playlist_name: str):
        """上传视频到bilibili"""
        if not BILIBILI_UPLOADER_AVAILABLE:
            logger.warning("Bilibili uploader not available")
            return False
        
        try:
            # 查找处理后的视频文件
            video_id = video_info.get('id', 'unknown')
            video_title = video_info.get('title', 'unknown')
            safe_title = "".join(c for c in video_title if c.isalnum() or c in (' ', '-', '_')).rstrip()
            safe_title = safe_title[:50]
            
            # 根据播放列表类型确定视频文件
            if playlist_name == "中字":
                video_file = f"history/{playlist_name}/{video_id}_{safe_title}/output_sub.mp4"
            elif playlist_name == "中配":
                video_file = f"history/{playlist_name}/{video_id}_{safe_title}/output_dub.mp4"
            else:
                logger.error(f"Unknown playlist type: {playlist_name}")
                return False
            
            if not os.path.exists(video_file):
                logger.error(f"Video file not found: {video_file}")
                return False
            
            # 尝试读取terminology.json中的theme字段作为标题
            theme_title = None
            terminology_file = f"history/{playlist_name}/{video_id}_{safe_title}/log/terminology.json"
            if os.path.exists(terminology_file):
                try:
                    with open(terminology_file, 'r', encoding='utf-8') as f:
                        terminology_data = json.load(f)
                        theme_title = terminology_data.get('theme', video_title)
                        # 显示前200个字符的预览，支持1000字标题
                        preview_length = min(200, len(theme_title))
                        logger.info(f"Using theme from terminology.json: {theme_title[:preview_length]}...")
                        logger.info(f"Title length: {len(theme_title)} characters (max 1000)")
                except Exception as e:
                    logger.warning(f"Error reading terminology.json: {e}")
                    theme_title = video_title
            else:
                logger.warning(f"terminology.json not found: {terminology_file}")
                theme_title = video_title
            
            logger.info(f"Uploading to Bilibili: {video_title}")
            # 显示标题预览，支持长标题
            preview_length = min(200, len(theme_title))
            logger.info(f"Title for Bilibili: {theme_title[:preview_length]}...")
            if len(theme_title) > 200:
                logger.info(f"Full title length: {len(theme_title)} characters")
            logger.info(f"Note: Bilibili title will be truncated to 80 characters if needed")
            
            # 创建上传器实例
            uploader = BilibiliUploader()
            
            # 设置发布时间（如果配置了定时发布）
            schedule_time = None
            if self.uploader_config.get("bilibili", {}).get("auto_upload", False):
                schedule_time_str = self.uploader_config["bilibili"]["schedule_time"]
                
                # 如果schedule_time为null，则立即发布
                if schedule_time_str is None:
                    schedule_time = None  # 立即发布
                    logger.info("设置为立即发布")
                else:
                    # 解析时间字符串，设置为明天的指定时间
                    from datetime import timedelta
                    tomorrow = datetime.now() + timedelta(days=1)
                    hour, minute = map(int, schedule_time_str.split(':'))
                    schedule_time = tomorrow.replace(hour=hour, minute=minute, second=0, microsecond=0)
                    logger.info(f"设置为定时发布: {schedule_time}")
            
            # 执行上传，传递自定义标题
            success = await uploader.upload_video(video_file, playlist_name, schedule_time, custom_title=theme_title)
            
            if success:
                logger.info(f"Successfully uploaded to Bilibili: {video_title}")
            else:
                logger.error(f"Failed to upload to Bilibili: {video_title}")
            
            return success
            
        except Exception as e:
            logger.error(f"Error uploading to Bilibili: {e}")
            return False
    
    async def process_video(self, video_info: Dict, playlist_name: str) -> bool:
        """处理单个视频"""
        video_id = video_info.get('id')
        video_url = f"https://www.youtube.com/watch?v={video_id}"
        video_title = video_info.get('title', 'Unknown')
        
        logger.info(f"Processing video: {video_title}")
        logger.info(f"Video ID: {video_id}")
        logger.info(f"Playlist: {playlist_name}")
        
        try:
            # 0. 清理output目录，确保只处理一个视频
            logger.info("Cleaning output directory...")
            if os.path.exists("output"):
                for item in os.listdir("output"):
                    item_path = os.path.join("output", item)
                    try:
                        if os.path.isfile(item_path):
                            os.remove(item_path)
                        elif os.path.isdir(item_path):
                            shutil.rmtree(item_path)
                    except Exception as e:
                        logger.warning(f"Could not remove {item_path}: {e}")
            
            # 1. 下载视频
            if not self.download_video(video_url):
                logger.error(f"Failed to download video {video_title}")
                # 标记为已处理，防止重复处理
                self.mark_video_processed(video_id, playlist_name)
                return False
            
            # 2. 根据播放列表类型选择处理方式
            playlist_config = self.playlists[playlist_name]
            success = False
            
            if playlist_config['dubbing']:
                # 中配播放列表：翻译并配音
                logger.info("Processing with dubbing...")
                success = self.process_with_dubbing(video_url)
            else:
                # 中字播放列表：仅翻译生成字幕
                logger.info("Processing text only...")
                success = self.process_text_only(video_url)
            
            if success:
                # 3. 存档到历史
                self.archive_to_history(playlist_name, video_info)
                
                # 4. 上传到抖音（如果启用）
                if self.uploader_config.get("douyin", {}).get("enabled", False):
                    logger.info("Uploading to Douyin...")
                    await self.upload_to_douyin(video_info, playlist_name)
                
                # 5. 上传到bilibili（如果启用）
                if self.uploader_config.get("bilibili", {}).get("enabled", False):
                    logger.info("Uploading to Bilibili...")
                    await self.upload_to_bilibili(video_info, playlist_name)
                
                logger.info(f"Video {video_title} processed successfully!")
            else:
                logger.error(f"Failed to process video {video_title}")
            
            # 无论成功还是失败，都标记为已处理，防止重复处理
            self.mark_video_processed(video_id, playlist_name)
            return success
                
        except Exception as e:
            logger.error(f"Error processing video {video_title}: {e}")
            # 即使发生异常，也标记为已处理，防止重复处理
            self.mark_video_processed(video_id, playlist_name)
            return False
    
    async def check_playlists(self):
        """检查所有播放列表的新视频"""
        logger.info(f"Checking playlists at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        total_new_videos = 0
        
        for playlist_name, playlist_config in self.playlists.items():
            logger.info(f"Checking playlist: {playlist_name}")
            logger.info(f"Description: {playlist_config['description']}")
            
            videos = self.get_playlist_videos(playlist_config['url'])
            if not videos:
                logger.error(f"Failed to get videos from playlist: {playlist_name}")
                continue
            
            # 统计已处理和新视频数量
            processed_count = len(self.processed_videos.get(playlist_name, []))
            new_videos = []
            for video in videos:
                if video and 'id' in video:
                    video_id = video['id']
                    if self.is_new_video(video_id, playlist_name):
                        new_videos.append(video)
            
            logger.info(f"{playlist_name} stats:")
            logger.info(f"  - Total videos in playlist: {len(videos)}")
            logger.info(f"  - Already processed: {processed_count}")
            logger.info(f"  - New videos found: {len(new_videos)}")
            
            if new_videos:
                logger.info(f"Processing {len(new_videos)} new videos...")
                
                # 处理新视频
                success_count = 0
                failed_count = 0
                
                for i, video in enumerate(new_videos, 1):
                    logger.info(f"Processing video {i}/{len(new_videos)}: {video.get('title', 'Unknown')[:50]}...")
                    
                    if await self.process_video(video, playlist_name):
                        logger.info(f"Successfully processed video: {video.get('title', 'Unknown')}")
                        success_count += 1
                        total_new_videos += 1
                    else:
                        logger.error(f"Failed to process video: {video.get('title', 'Unknown')}")
                        failed_count += 1
                    
                    # 处理间隔，避免过于频繁
                    if i < len(new_videos):  # 最后一个视频不需要等待
                        logger.info("Waiting 5 seconds before next video...")
                        time.sleep(5)
                
                logger.info(f"{playlist_name} processing summary:")
                logger.info(f"  - Successfully processed: {success_count}")
                logger.info(f"  - Failed to process: {failed_count}")
                logger.info(f"  - All videos marked as processed (including failed ones)")
            else:
                logger.info(f"No new videos to process in {playlist_name}")
        
        logger.info(f"Summary: Processed {total_new_videos} new videos across all playlists")
    
    async def run_monitor(self, check_interval: int = 60):
        """运行监控器"""
        logger.info("YouTube Playlist Monitor Started!")
        logger.info(f"Check interval: {check_interval} seconds")
        logger.info("Press Ctrl+C to stop")
        
        try:
            while True:
                await self.check_playlists()
                logger.info(f"Next check in {check_interval} seconds...")
                time.sleep(check_interval)
                
        except KeyboardInterrupt:
            logger.info("Monitor stopped by user")
        except Exception as e:
            logger.error(f"Monitor error: {e}")

async def main():
    """主函数"""
    logger.info("Starting YouTube Playlist Monitor...")
    
    monitor = PlaylistMonitor()
    
    # 检查设置
    if not os.path.exists("config.yaml"):
        logger.error("config.yaml not found. Please run the setup first.")
        return
    
    logger.info("This will monitor the following playlists:")
    for name, config in monitor.playlists.items():
        logger.info(f"  - {name}: {config['description']}")
    
    # 运行监控器
    await monitor.run_monitor()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main()) 