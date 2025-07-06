# -*- coding: utf-8 -*-
"""
# ------------
# VideoLingo Uploaders
# ------------
# 支持抖音和bilibili自动上传
# ------------
"""

from .douyin_uploader import DouyinUploader
from .bilibili_uploader import BilibiliUploader

__all__ = ['DouyinUploader', 'BilibiliUploader'] 