# 📁 历史文件管理

## 概述

VideoLingo播放列表监控器现在支持按播放列表和视频信息组织历史文件，方便管理和查找已处理的视频。

## 文件组织结构

```
history/
├── 中字/                          # 中字播放列表
│   ├── video_id_1_视频标题1/      # 视频1的文件夹
│   │   ├── process_info.json      # 处理信息
│   │   ├── output_sub.mp4         # 带字幕的视频
│   │   ├── output_sub.srt         # 字幕文件
│   │   └── ...                    # 其他处理文件
│   └── video_id_2_视频标题2/      # 视频2的文件夹
│       ├── process_info.json
│       └── ...
└── 中配/                          # 中配播放列表
    ├── video_id_3_视频标题3/      # 视频3的文件夹
    │   ├── process_info.json
    │   ├── output_dub.mp4         # 带配音的视频
    │   └── ...
    └── ...
```

## 处理信息文件

每个视频文件夹都包含一个 `process_info.json` 文件，记录处理详情：

```json
{
  "video_id": "dQw4w9WgXcQ",
  "video_title": "视频标题",
  "playlist_name": "中字",
  "process_time": "2024-01-15T10:30:45.123456",
  "playlist_config": {
    "url": "播放列表URL",
    "dubbing": false,
    "description": "中字播放列表 - 仅翻译生成字幕"
  }
}
```

## 历史管理工具

### 基本使用

```bash
# 列出所有存档的视频
python history_manager.py

# 列出特定播放列表的视频
python history_manager.py --list --playlist 中字

# 获取特定视频的详细信息
python history_manager.py --info 中字 video_id_视频标题

# 清理30天前的旧文件
python history_manager.py --clean 30

# 导出历史摘要
python history_manager.py --export summary.json
```

### 命令行选项

- `--list, -l`: 列出存档的视频
- `--playlist, -p`: 指定播放列表名称
- `--info, -i`: 获取特定视频的详细信息
- `--clean, -c`: 清理指定天数前的文件
- `--export, -e`: 导出历史摘要到文件

## 使用示例

### 1. 查看所有存档视频

```bash
python history_manager.py --list
```

输出示例：
```
📁 Archived Videos:
================================================================================

🎬 Playlist: 中字
----------------------------------------
   1. 示例视频标题
      Folder: dQw4w9WgXcQ_示例视频标题
      Processed: 2024-01-15 10:30:45
      Files: output_sub.mp4, output_sub.srt

🎬 Playlist: 中配
----------------------------------------
   1. 另一个视频标题
      Folder: abc123_另一个视频标题
      Processed: 2024-01-15 09:15:30
      Files: output_dub.mp4, output_dub.srt
```

### 2. 查看特定播放列表

```bash
python history_manager.py --list --playlist 中字
```

### 3. 获取视频详细信息

```bash
python history_manager.py --info 中字 dQw4w9WgXcQ_示例视频标题
```

输出示例：
```
📹 Video Information:
==================================================
Title: 示例视频标题
Video ID: dQw4w9WgXcQ
Playlist: 中字
Process Time: 2024-01-15T10:30:45.123456

📁 Files:
  output_sub.mp4 (15.2 MB)
  output_sub.srt (2.1 MB)
  process_info.json (0.5 KB)
```

### 4. 清理旧文件

```bash
# 清理7天前的文件
python history_manager.py --clean 7

# 清理30天前的文件
python history_manager.py --clean 30
```

### 5. 导出摘要

```bash
python history_manager.py --export my_summary.json
```

## 配置选项

在 `playlist_monitor_config.json` 中可以配置历史文件管理：

```json
{
  "output_settings": {
    "history_organization": {
      "enabled": true,           // 是否启用历史文件组织
      "by_playlist": true,       // 是否按播放列表分类
      "by_video": true,          // 是否按视频分类
      "include_process_info": true, // 是否包含处理信息文件
      "auto_cleanup_days": 30    // 自动清理天数
    }
  }
}
```

## 文件命名规则

### 视频文件夹命名
- 格式：`{video_id}_{safe_title}`
- `video_id`: YouTube视频ID
- `safe_title`: 清理后的视频标题（移除特殊字符，限制长度）

### 安全标题处理
- 移除特殊字符，只保留字母、数字、空格、连字符、下划线
- 限制标题长度为50个字符
- 移除末尾空格

## 自动清理

### 清理策略
- 默认清理30天前的文件
- 基于 `process_info.json` 中的处理时间
- 只清理整个视频文件夹，不会部分删除

### 手动清理
```bash
# 清理指定天数前的文件
python history_manager.py --clean 7   # 7天前
python history_manager.py --clean 30  # 30天前
python history_manager.py --clean 90  # 90天前
```

## 备份和恢复

### 备份历史文件
```bash
# 创建备份
tar -czf history_backup_$(date +%Y%m%d).tar.gz history/

# 或使用zip
zip -r history_backup_$(date +%Y%m%d).zip history/
```

### 恢复历史文件
```bash
# 解压备份
tar -xzf history_backup_20240115.tar.gz

# 或使用zip
unzip history_backup_20240115.zip
```

## 故障排除

### 常见问题

1. **文件夹名称过长**
   - 系统会自动截断标题长度
   - 确保视频ID正确

2. **特殊字符问题**
   - 系统会自动清理特殊字符
   - 如果仍有问题，检查视频标题

3. **权限问题**
   - 确保对history目录有读写权限
   - 检查磁盘空间

4. **文件损坏**
   - 检查 `process_info.json` 文件完整性
   - 可以手动删除损坏的文件夹

### 调试命令

```bash
# 检查历史目录结构
ls -la history/

# 检查特定播放列表
ls -la history/中字/

# 检查文件大小
du -sh history/*

# 查找损坏的文件
find history/ -name "process_info.json" -exec python -m json.tool {} \;
```

## 最佳实践

1. **定期清理**: 建议每月清理一次旧文件
2. **备份重要文件**: 定期备份重要的处理结果
3. **监控磁盘空间**: 确保有足够的存储空间
4. **检查处理质量**: 定期检查处理结果的质量

## 高级功能

### 自定义清理规则
可以修改 `history_manager.py` 中的清理逻辑，添加自定义规则：

```python
def custom_cleanup_rule(self, video_info):
    """自定义清理规则"""
    # 例如：只保留特定播放列表的文件
    if video_info.get('playlist_name') == '中字':
        return True
    return False
```

### 批量操作
可以编写脚本进行批量操作：

```bash
# 批量重命名
for dir in history/中字/*/; do
    # 自定义重命名逻辑
done

# 批量移动
mv history/中字/* history/archive/
``` 