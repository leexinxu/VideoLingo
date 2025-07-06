# YouTube Playlist Monitor - 播放列表监控器

## 概述

这是一个自动化脚本，用于监控YouTube播放列表并使用VideoLingo进行翻译配音处理。

## 功能特性

- 🔍 自动监控指定的YouTube播放列表
- 📹 自动下载新视频
- 🌐 自动翻译并生成字幕
- 🎤 自动配音（可选）
- 📁 自动存档到历史文件夹
- 📝 记录已处理的视频，避免重复处理

## 播放列表配置

脚本监控两个播放列表：

1. **中字播放列表** (`PLxjtcx2z5_41xdgXxdXCZ8lFcSwTZujRt`)
   - 仅翻译生成字幕
   - 不进行配音

2. **中配播放列表** (`PLxjtcx2z5_42OhI7vyzYVxXpzb_XIadrN`)
   - 翻译生成字幕
   - 进行配音

## 安装和设置

### 1. 确保VideoLingo已正确安装

```bash
# 激活conda环境
conda activate videolingo

# 确保所有依赖已安装
python install.py
```

### 2. 配置VideoLingo设置

运行Streamlit界面进行配置：

```bash
streamlit run st.py
```

确保以下设置已正确配置：
- API密钥（如果需要）
- 目标语言
- TTS方法（用于配音）
- 其他相关设置

### 3. 检查配置文件

确保 `config.yaml` 文件存在并配置正确。

## 使用方法

### 基本使用

```bash
# 使用默认设置启动监控器（60秒检查间隔）
python start_monitor.py

# 自定义检查间隔（30秒）
python start_monitor.py --interval 30

# 测试模式 - 检查一次播放列表并退出
python start_monitor.py --test
```

### 直接运行监控器

```bash
# 直接运行监控器脚本
python playlist_monitor.py
```

## 配置文件

### playlist_monitor_config.json

你可以通过编辑 `playlist_monitor_config.json` 来自定义设置：

```json
{
  "monitor_settings": {
    "check_interval": 60,           // 检查间隔（秒）
    "max_videos_per_check": 50,     // 每次检查的最大视频数
    "processing_delay": 5           // 处理间隔（秒）
  },
  "playlists": {
    "中字": {
      "url": "播放列表URL",
      "dubbing": false,             // 是否配音
      "description": "描述",
      "enabled": true              // 是否启用
    }
  }
}
```

## 工作流程

1. **监控播放列表** - 每60秒检查一次播放列表
2. **识别新视频** - 对比已处理记录，找出新视频
3. **下载视频** - 使用yt-dlp下载视频
4. **处理视频** - 根据播放列表类型选择处理方式
   - 中字播放列表：仅翻译生成字幕
   - 中配播放列表：翻译生成字幕 + 配音
5. **存档** - 处理完成后自动存档到历史文件夹
6. **记录** - 标记视频为已处理

## 输出文件

- `playlist_monitor/processed_videos.json` - 已处理视频记录
- `output/` - 处理中的文件
- `history/` - 存档的文件

## 日志和调试

脚本会输出详细的处理日志，包括：
- 播放列表检查状态
- 视频下载进度
- 处理步骤状态
- 错误信息

## 故障排除

### 常见问题

1. **配置文件不存在**
   ```
   ❌ config.yaml not found
   ```
   解决：运行 `streamlit run st.py` 进行初始配置

2. **API密钥错误**
   ```
   Error in text processing: API key invalid
   ```
   解决：检查 `config.yaml` 中的API设置

3. **网络连接问题**
   ```
   Error getting playlist videos
   ```
   解决：检查网络连接和YouTube访问

4. **磁盘空间不足**
   ```
   Error downloading video: No space left on device
   ```
   解决：清理磁盘空间或调整输出目录

### 重启和恢复

脚本会自动记录已处理的视频，重启后不会重复处理。

如果需要重新处理某个视频，可以：
1. 编辑 `playlist_monitor/processed_videos.json`
2. 删除对应的视频ID
3. 重启监控器

## 高级配置

### 自定义播放列表

编辑 `playlist_monitor_config.json` 添加新的播放列表：

```json
{
  "playlists": {
    "新播放列表": {
      "url": "https://www.youtube.com/playlist?list=YOUR_PLAYLIST_ID",
      "dubbing": true,
      "description": "新播放列表描述",
      "enabled": true
    }
  }
}
```

### 调整处理参数

在 `config.yaml` 中可以调整：
- 视频分辨率
- 字幕长度限制
- TTS方法
- 音频处理参数

## 注意事项

1. **资源消耗** - 视频处理需要大量CPU和内存资源
2. **网络带宽** - 下载视频需要稳定的网络连接
3. **存储空间** - 确保有足够的磁盘空间
4. **API限制** - 注意API调用限制和费用

## 支持

如果遇到问题，可以：
1. 查看日志输出
2. 检查配置文件
3. 运行测试模式进行调试
4. 提交Issue到GitHub仓库 