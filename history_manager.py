#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
# ------------
# History Manager
# ------------
# Tool for managing archived video files
# ------------
"""

import os
import json
import shutil
from datetime import datetime
from pathlib import Path
import argparse

class HistoryManager:
    def __init__(self):
        self.history_dir = "history"
        
    def list_archived_videos(self, playlist_name: str = None):
        """列出存档的视频"""
        if not os.path.exists(self.history_dir):
            print("❌ History directory not found")
            return
        
        print("📁 Archived Videos:")
        print("=" * 80)
        
        if playlist_name:
            playlist_dir = os.path.join(self.history_dir, playlist_name)
            if os.path.exists(playlist_dir):
                self._list_playlist_videos(playlist_name, playlist_dir)
            else:
                print(f"❌ Playlist '{playlist_name}' not found in history")
        else:
            # 列出所有播放列表
            for playlist in os.listdir(self.history_dir):
                playlist_dir = os.path.join(self.history_dir, playlist)
                if os.path.isdir(playlist_dir):
                    print(f"\n🎬 Playlist: {playlist}")
                    print("-" * 40)
                    self._list_playlist_videos(playlist, playlist_dir)
    
    def _list_playlist_videos(self, playlist_name: str, playlist_dir: str):
        """列出播放列表中的视频"""
        videos = []
        
        for item in os.listdir(playlist_dir):
            item_path = os.path.join(playlist_dir, item)
            if os.path.isdir(item_path):
                # 检查是否有处理信息文件
                process_info_file = os.path.join(item_path, "process_info.json")
                if os.path.exists(process_info_file):
                    try:
                        with open(process_info_file, 'r', encoding='utf-8') as f:
                            info = json.load(f)
                        videos.append({
                            'folder': item,
                            'info': info
                        })
                    except:
                        videos.append({
                            'folder': item,
                            'info': {'video_title': 'Unknown', 'process_time': 'Unknown'}
                        })
                else:
                    videos.append({
                        'folder': item,
                        'info': {'video_title': 'Unknown', 'process_time': 'Unknown'}
                    })
        
        if not videos:
            print("  No videos found")
            return
        
        # 按处理时间排序
        videos.sort(key=lambda x: x['info'].get('process_time', ''), reverse=True)
        
        for i, video in enumerate(videos, 1):
            info = video['info']
            title = info.get('video_title', 'Unknown')
            process_time = info.get('process_time', 'Unknown')
            
            # 格式化时间
            try:
                dt = datetime.fromisoformat(process_time.replace('Z', '+00:00'))
                formatted_time = dt.strftime('%Y-%m-%d %H:%M:%S')
            except:
                formatted_time = process_time
            
            print(f"  {i:2d}. {title}")
            print(f"      Folder: {video['folder']}")
            print(f"      Processed: {formatted_time}")
            
            # 检查输出文件
            video_dir = os.path.join(playlist_dir, video['folder'])
            output_files = []
            for file in os.listdir(video_dir):
                if file.endswith(('.mp4', '.srt', '.json')) and file != 'process_info.json':
                    output_files.append(file)
            
            if output_files:
                print(f"      Files: {', '.join(output_files)}")
            print()
    
    def get_video_info(self, playlist_name: str, video_folder: str):
        """获取特定视频的详细信息"""
        video_dir = os.path.join(self.history_dir, playlist_name, video_folder)
        if not os.path.exists(video_dir):
            print(f"❌ Video folder not found: {video_dir}")
            return
        
        process_info_file = os.path.join(video_dir, "process_info.json")
        if os.path.exists(process_info_file):
            try:
                with open(process_info_file, 'r', encoding='utf-8') as f:
                    info = json.load(f)
                
                print(f"📹 Video Information:")
                print("=" * 50)
                print(f"Title: {info.get('video_title', 'Unknown')}")
                print(f"Video ID: {info.get('video_id', 'Unknown')}")
                print(f"Playlist: {info.get('playlist_name', 'Unknown')}")
                print(f"Process Time: {info.get('process_time', 'Unknown')}")
                
                # 列出文件
                print(f"\n📁 Files:")
                for file in os.listdir(video_dir):
                    file_path = os.path.join(video_dir, file)
                    if os.path.isfile(file_path):
                        size = os.path.getsize(file_path)
                        size_mb = size / (1024 * 1024)
                        print(f"  {file} ({size_mb:.1f} MB)")
                
            except Exception as e:
                print(f"❌ Error reading process info: {e}")
        else:
            print("❌ Process info file not found")
    
    def clean_history(self, days: int = 30):
        """清理指定天数前的历史文件"""
        if not os.path.exists(self.history_dir):
            print("❌ History directory not found")
            return
        
        cutoff_date = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        cutoff_date = cutoff_date.replace(day=cutoff_date.day - days)
        
        cleaned_count = 0
        
        for playlist in os.listdir(self.history_dir):
            playlist_dir = os.path.join(self.history_dir, playlist)
            if os.path.isdir(playlist_dir):
                for video_folder in os.listdir(playlist_dir):
                    video_dir = os.path.join(playlist_dir, video_folder)
                    if os.path.isdir(video_dir):
                        process_info_file = os.path.join(video_dir, "process_info.json")
                        if os.path.exists(process_info_file):
                            try:
                                with open(process_info_file, 'r', encoding='utf-8') as f:
                                    info = json.load(f)
                                process_time = info.get('process_time', '')
                                if process_time:
                                    dt = datetime.fromisoformat(process_time.replace('Z', '+00:00'))
                                    if dt < cutoff_date:
                                        print(f"🗑️ Removing old video: {info.get('video_title', 'Unknown')}")
                                        shutil.rmtree(video_dir)
                                        cleaned_count += 1
                            except:
                                pass
        
        print(f"✅ Cleaned {cleaned_count} old videos")
    
    def export_summary(self, output_file: str = "history_summary.json"):
        """导出历史摘要"""
        if not os.path.exists(self.history_dir):
            print("❌ History directory not found")
            return
        
        summary = {
            "export_time": datetime.now().isoformat(),
            "playlists": {}
        }
        
        for playlist in os.listdir(self.history_dir):
            playlist_dir = os.path.join(self.history_dir, playlist)
            if os.path.isdir(playlist_dir):
                summary["playlists"][playlist] = {
                    "videos": [],
                    "total_count": 0
                }
                
                for video_folder in os.listdir(playlist_dir):
                    video_dir = os.path.join(playlist_dir, video_folder)
                    if os.path.isdir(video_dir):
                        process_info_file = os.path.join(video_dir, "process_info.json")
                        if os.path.exists(process_info_file):
                            try:
                                with open(process_info_file, 'r', encoding='utf-8') as f:
                                    info = json.load(f)
                                summary["playlists"][playlist]["videos"].append(info)
                                summary["playlists"][playlist]["total_count"] += 1
                            except:
                                pass
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(summary, f, ensure_ascii=False, indent=2)
        
        print(f"✅ Summary exported to {output_file}")

def main():
    parser = argparse.ArgumentParser(description='History Manager for VideoLingo')
    parser.add_argument('--list', '-l', action='store_true',
                       help='List archived videos')
    parser.add_argument('--playlist', '-p', type=str,
                       help='Specific playlist to list')
    parser.add_argument('--info', '-i', nargs=2, metavar=('PLAYLIST', 'FOLDER'),
                       help='Get info for specific video')
    parser.add_argument('--clean', '-c', type=int, metavar='DAYS',
                       help='Clean videos older than DAYS')
    parser.add_argument('--export', '-e', type=str, metavar='FILE',
                       help='Export summary to FILE')
    
    args = parser.parse_args()
    
    manager = HistoryManager()
    
    if args.list:
        manager.list_archived_videos(args.playlist)
    elif args.info:
        playlist_name, video_folder = args.info
        manager.get_video_info(playlist_name, video_folder)
    elif args.clean:
        manager.clean_history(args.clean)
    elif args.export:
        manager.export_summary(args.export)
    else:
        # 默认列出所有视频
        manager.list_archived_videos()

if __name__ == "__main__":
    main() 