#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
# ------------
# Test Download Fix
# ------------
# Test script to verify that video download works with logging
# ------------
"""

import os
import sys
import logging
from datetime import datetime

# Add current directory to path for imports
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

# 设置日志配置（与playlist_monitor.py相同）
def setup_logging():
    """设置日志配置"""
    # 创建logs目录
    os.makedirs("logs", exist_ok=True)
    
    # 生成日志文件名（包含时间戳）
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = f"logs/test_download_{timestamp}.log"
    
    # 配置日志格式
    log_format = '%(asctime)s - %(levelname)s - %(message)s'
    date_format = '%Y-%m-%d %H:%M:%S'
    
    # 配置日志处理器
    logging.basicConfig(
        level=logging.INFO,
        format=log_format,
        datefmt=date_format,
        handlers=[
            logging.FileHandler(log_file, encoding='utf-8'),
            logging.StreamHandler(sys.stdout)
        ]
    )
    
    # 创建logger
    logger = logging.getLogger(__name__)
    logger.info(f"Logging initialized. Log file: {log_file}")
    
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
                        self.logger.error(f"[STDERR] {line}")
                self.buffer = lines[-1]  # 保留最后一行（可能不完整）
        
        def flush(self):
            if self.buffer.strip():
                self.logger.error(f"[STDERR] {self.buffer}")
                self.buffer = ""
            self.original_stderr.flush()
        
        def fileno(self):
            # 为subprocess提供文件描述符
            return self.original_stderr.fileno()
    
    original_stderr = sys.stderr
    sys.stderr = ErrorLogRedirector(logger, original_stderr)
    
    logger.info("All console output will be logged to file")
    
    return logger

# 初始化日志
logger = setup_logging()

def test_download():
    """测试下载功能"""
    logger.info("Testing video download functionality...")
    
    try:
        from core import _1_ytdlp
        from core.utils.config_utils import load_key
        
        # 测试视频URL
        test_url = "https://www.youtube.com/watch?v=61hYyYc19qw"
        logger.info(f"Testing download with URL: {test_url}")
        
        # 设置代理环境变量（如果需要）
        proxy_config = {
            "proxy_settings": {
                "enabled": True,
                "https_proxy": "http://127.0.0.1:7890",
                "http_proxy": "http://127.0.0.1:7890",
                "all_proxy": "socks5://127.0.0.1:7890"
            }
        }
        
        if proxy_config["proxy_settings"]["enabled"]:
            os.environ['https_proxy'] = proxy_config["proxy_settings"]["https_proxy"]
            os.environ['http_proxy'] = proxy_config["proxy_settings"]["http_proxy"]
            os.environ['all_proxy'] = proxy_config["proxy_settings"]["all_proxy"]
            logger.info(f"Using proxy: {os.environ['https_proxy']}")
        
        # 执行下载
        logger.info("Starting download...")
        _1_ytdlp.download_video_ytdlp(test_url, resolution=load_key("ytb_resolution"))
        
        logger.info("Download completed successfully!")
        return True
        
    except Exception as e:
        logger.error(f"Download test failed: {e}")
        return False

if __name__ == "__main__":
    print("🧪 Testing download fix...")
    success = test_download()
    
    if success:
        print("✅ Download test passed!")
    else:
        print("❌ Download test failed!")
        print("Check the log file for details.") 