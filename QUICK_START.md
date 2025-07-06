# 🚀 YouTube Playlist Monitor - 快速启动指南

## 功能特性

- ✅ 自动监控YouTube播放列表
- ✅ 检测新视频并自动下载
- ✅ 智能翻译和字幕生成
- ✅ AI配音功能
- ✅ 代理支持
- ✅ 分目录存档
- ✅ 历史管理工具
- ✅ 抖音自动上传

## 一键启动

### Windows 用户
```bash
# 双击运行
start_monitor.bat

# 或者命令行运行
start_monitor.bat --test

# 启用代理模式
start_monitor.bat --proxy
```

### Linux/macOS 用户
```bash
# 运行启动脚本
./start_monitor.sh

# 测试模式
./start_monitor.sh --test

# 启用代理模式
./start_monitor.sh --proxy
```

### 通用方法
```bash
# 直接运行Python脚本
python start_monitor.py

# 测试模式
python start_monitor.py --test

# 自定义检查间隔（30秒）
python start_monitor.py --interval 30

# 启用代理模式
python start_monitor.py --proxy

# 测试模式 + 代理
python start_monitor.py --test --proxy
```

## 代理配置

### 1. 配置代理设置

编辑 `proxy_config.json` 文件来配置代理：

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

### 2. 使用代理启动

```bash
# 启用代理模式
python start_monitor.py --proxy

# 或者使用启动脚本
./start_monitor.sh --proxy  # Linux/macOS
start_monitor.bat --proxy   # Windows
```

## 抖音上传设置

### 1. 安装依赖
```bash
# 安装Playwright
pip install playwright

# 安装浏览器驱动
playwright install chromium
```

### 2. 设置抖音上传器
```bash
# 运行设置脚本
python setup_douyin_uploader.py
```

按提示完成：
- 启用抖音上传功能
- 设置自动上传和发布时间
- 配置位置和标签
- 生成抖音登录Cookie

### 3. 配置上传设置

编辑 `uploader_config.json`：
```json
{
  "douyin": {
    "enabled": true,
    "auto_upload": true,
    "schedule_time": "16:00",
    "location": "杭州市",
    "tags": ["VideoLingo", "AI翻译", "视频配音"]
  }
}
```

## 首次设置

### 1. 确保VideoLingo已安装
```bash
# 激活conda环境
conda activate videolingo

# 检查安装
python install.py
```

### 2. 配置VideoLingo
```bash
# 运行配置界面
streamlit run st.py
```

在配置界面中设置：
- API密钥（如需要）
- 目标语言：简体中文
- TTS方法（用于配音）
- 其他相关设置

### 3. 测试监控器
```bash
# 运行测试
python test_monitor.py
```

## 监控的播放列表

1. **中字播放列表** - 仅翻译生成字幕
   - URL: `https://www.youtube.com/playlist?list=PLxjtcx2z5_41xdgXxdXCZ8lFcSwTZujRt`

2. **中配播放列表** - 翻译并配音
   - URL: `https://www.youtube.com/playlist?list=PLxjtcx2z5_42OhI7vyzYVxXpzb_XIadrN`

## 工作流程

1. **监控** - 每60秒检查播放列表
2. **下载** - 自动下载新视频
3. **处理** - 根据播放列表类型处理
4. **存档** - 自动存档到历史文件夹
5. **上传** - 自动上传到抖音（如果启用）

## 输出文件

- `playlist_monitor/processed_videos.json` - 已处理记录
- `output/` - 处理中的文件
- `history/` - 存档的文件（按播放列表和视频分类）

### 历史文件管理

#### 命令行工具
```bash
# 查看所有存档视频
python history_manager.py --list

# 查看特定播放列表
python history_manager.py --list --playlist 中字

# 获取视频详细信息
python history_manager.py --info 中字 video_id_视频标题

# 清理旧文件
python history_manager.py --clean 30
```

#### 交互式工具
```bash
# 启动交互式历史管理器
python manage_history.py
```

## 停止监控

按 `Ctrl+C` 停止监控器

## 故障排除

### 常见问题

1. **配置文件不存在**
   ```bash
   streamlit run st.py
   ```

2. **API密钥错误**
   - 检查 `config.yaml` 中的API设置

3. **网络问题**
   - 检查网络连接和YouTube访问

4. **磁盘空间不足**
   - 清理磁盘空间或调整输出目录

## 自定义配置

编辑 `playlist_monitor_config.json` 来自定义：
- 检查间隔
- 播放列表设置
- 输出选项

## 支持

- 查看详细文档：`playlist_monitor_README.md`
- 抖音上传器文档：`DOUYIN_UPLOADER.md`
- 运行测试：`python test_monitor.py`
- 检查日志输出 