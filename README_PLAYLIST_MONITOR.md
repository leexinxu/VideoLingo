# 🎬 YouTube Playlist Monitor - 播放列表监控器

## 📋 项目概述

这是一个自动化脚本，用于监控指定的YouTube播放列表并使用VideoLingo进行翻译配音处理。

## ✨ 主要功能

- 🔍 **自动监控** - 每60秒检查播放列表中的新视频
- 📹 **自动下载** - 使用yt-dlp下载新视频
- 🌐 **自动翻译** - 使用WhisperX进行转录和翻译
- 🎤 **自动配音** - 支持多种TTS方法进行配音
- 📁 **自动存档** - 处理完成后自动存档到历史文件夹
- 📝 **智能记录** - 避免重复处理已完成的视频
- 🌐 **代理支持** - 支持通过代理访问YouTube
- 📱 **抖音上传** - 自动上传处理完成的视频到抖音

## 🎯 监控的播放列表

### 1. 中字播放列表
- **URL**: `https://www.youtube.com/playlist?list=PLxjtcx2z5_41xdgXxdXCZ8lFcSwTZujRt`
- **处理方式**: 仅翻译生成字幕
- **输出**: 带中文字幕的视频

### 2. 中配播放列表
- **URL**: `https://www.youtube.com/playlist?list=PLxjtcx2z5_42OhI7vyzYVxXpzb_XIadrN`
- **处理方式**: 翻译生成字幕 + 配音
- **输出**: 带中文字幕和中文配音的视频

## 🚀 快速开始

### 1. 环境准备

确保VideoLingo已正确安装：

```bash
# 激活conda环境
conda activate videolingo

# 检查安装
python install.py
```

### 2. 配置VideoLingo

运行配置界面：

```bash
streamlit run st.py
```

配置以下设置：
- API密钥（如需要）
- 目标语言：简体中文
- TTS方法（用于配音）
- 其他相关设置

### 3. 配置代理（可选）

如果需要通过代理访问YouTube，编辑 `proxy_config.json`：

```json
{
  "proxy_settings": {
    "enabled": true,
    "https_proxy": "http://127.0.0.1:7890",
    "http_proxy": "http://127.0.0.1:7890",
    "all_proxy": "socks5://127.0.0.1:7890"
  },
  "yt_dlp_proxy": "http://127.0.0.1:7890"
}
```

### 4. 启动监控器

#### Windows 用户
```bash
# 基本启动
start_monitor.bat

# 启用代理
start_monitor.bat --proxy

# 测试模式
start_monitor.bat --test
```

#### Linux/macOS 用户
```bash
# 基本启动
./start_monitor.sh

# 启用代理
./start_monitor.sh --proxy

# 测试模式
./start_monitor.sh --test
```

#### 通用方法
```bash
# 基本启动
python start_monitor.py

# 启用代理
python start_monitor.py --proxy

# 自定义检查间隔（30秒）
python start_monitor.py --interval 30

# 测试模式
python start_monitor.py --test
```

## 📁 文件结构

```
VideoLingo/
├── playlist_monitor.py              # 主监控脚本
├── start_monitor.py                 # 启动脚本
├── start_monitor.bat               # Windows启动脚本
├── start_monitor.sh                # Linux/macOS启动脚本
├── test_monitor.py                 # 测试脚本
├── proxy_config.json               # 代理配置文件
├── playlist_monitor_config.json    # 监控器配置文件
├── playlist_monitor/               # 监控器数据目录
│   └── processed_videos.json      # 已处理视频记录
├── output/                         # 处理中的文件
└── history/                        # 存档的文件
```

## ⚙️ 配置说明

### proxy_config.json
代理配置文件，用于设置YouTube访问代理：

```json
{
  "proxy_settings": {
    "enabled": true,
    "https_proxy": "http://127.0.0.1:7890",
    "http_proxy": "http://127.0.0.1:7890",
    "all_proxy": "socks5://127.0.0.1:7890"
  },
  "yt_dlp_proxy": "http://127.0.0.1:7890"
}
```

### playlist_monitor_config.json
监控器配置文件，用于自定义监控设置：

```json
{
  "monitor_settings": {
    "check_interval": 60,
    "max_videos_per_check": 50,
    "processing_delay": 5
  },
  "playlists": {
    "中字": {
      "url": "播放列表URL",
      "dubbing": false,
      "description": "描述",
      "enabled": true
    }
  }
}
```

## 🔄 工作流程

1. **监控阶段**
   - 每60秒检查播放列表
   - 识别新添加的视频
   - 对比已处理记录

2. **下载阶段**
   - 使用yt-dlp下载视频
   - 支持代理访问
   - 自动选择最佳质量

3. **处理阶段**
   - **中字播放列表**：
     - WhisperX转录
     - NLP句子分割
     - AI翻译
     - 字幕生成和对齐
     - 合并字幕到视频
   
   - **中配播放列表**：
     - 完成中字播放列表的所有步骤
     - 生成音频任务
     - 提取参考音频
     - TTS配音生成
     - 音频合并
     - 配音合并到视频

4. **存档阶段**
   - 自动存档到历史文件夹
   - 记录已处理视频
   - 清理临时文件

5. **上传阶段**
   - 自动上传到抖音（如果启用）
   - 生成标题和标签
   - 支持定时发布

## 📊 输出文件

### 处理中的文件
- `output/output_sub.mp4` - 带字幕的视频（中字播放列表）
- `output/output_dub.mp4` - 带配音的视频（中配播放列表）
- `output/` - 其他处理文件

### 存档文件
- `history/` - 处理完成的文件存档（按播放列表和视频分类）
  - `history/中字/` - 中字播放列表的视频
  - `history/中配/` - 中配播放列表的视频
  - 每个视频都有独立的文件夹，包含处理信息和输出文件

### 记录文件
- `playlist_monitor/processed_videos.json` - 已处理视频记录

### 上传文件
- `cookies/douyin_uploader/` - 抖音登录Cookie
- `uploader_config.json` - 上传器配置文件

## 🛠️ 故障排除

### 常见问题

1. **配置文件不存在**
   ```bash
   streamlit run st.py
   ```

2. **API密钥错误**
   - 检查 `config.yaml` 中的API设置
   - 确保API密钥有效

3. **网络连接问题**
   - 检查网络连接
   - 尝试启用代理模式
   - 验证YouTube访问

4. **磁盘空间不足**
   - 清理磁盘空间
   - 调整输出目录

5. **代理连接失败**
   - 检查代理软件是否运行
   - 验证代理端口配置
   - 测试代理连接

### 调试方法

1. **运行测试**
   ```bash
   python test_monitor.py
   ```

2. **测试模式**
   ```bash
   python start_monitor.py --test
   ```

3. **检查日志**
   - 查看控制台输出
   - 检查错误信息

## 🔧 高级配置

### 自定义播放列表

编辑 `playlist_monitor_config.json` 添加新播放列表：

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

### 环境变量设置

可以设置全局代理环境变量：

```bash
# Linux/macOS
export https_proxy=http://127.0.0.1:7890
export http_proxy=http://127.0.0.1:7890
export all_proxy=socks5://127.0.0.1:7890

# Windows
set https_proxy=http://127.0.0.1:7890
set http_proxy=http://127.0.0.1:7890
set all_proxy=socks5://127.0.0.1:7890
```

## 📚 相关文档

- [快速启动指南](QUICK_START.md)
- [代理配置指南](PROXY_SETUP.md)
- [历史文件管理](HISTORY_MANAGEMENT.md)
- [抖音上传器文档](DOUYIN_UPLOADER.md)
- [详细使用说明](playlist_monitor_README.md)

## ⚠️ 注意事项

1. **资源消耗** - 视频处理需要大量CPU和内存资源
2. **网络带宽** - 下载视频需要稳定的网络连接
3. **存储空间** - 确保有足够的磁盘空间
4. **API限制** - 注意API调用限制和费用
5. **代理性能** - 使用代理可能影响下载速度

## 🆘 支持

如果遇到问题：

1. 查看详细文档
2. 运行测试脚本
3. 检查日志输出
4. 提交Issue到GitHub仓库

---

**🎉 享受自动化的视频翻译配音体验！** 