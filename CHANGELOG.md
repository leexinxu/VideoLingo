# 📝 更新日志

## 版本 1.3.0 - 抖音上传器集成

### 🆕 新增功能

#### 1. 抖音自动上传器
- **功能**: 基于social-auto-upload项目的抖音上传器
- **特性**: 
  - 自动上传处理完成的视频到抖音
  - 支持定时发布功能
  - 自动生成标题和标签
  - 支持Cookie管理和验证
  - 根据播放列表类型生成不同内容
- **集成**: 与播放列表监控器无缝集成

#### 2. 上传器配置系统
- **配置文件**: `uploader_config.json` - 上传器配置
- **设置脚本**: `setup_douyin_uploader.py` - 交互式设置
- **测试工具**: `test_douyin_uploader.py` - 完整测试套件
- **功能**: 支持自定义标题、标签、发布时间、位置等

#### 3. 智能内容生成
- **中字播放列表**: 标题格式 `{原标题} - 中文字幕版`，标签包含 `["中文字幕", "翻译"]`
- **中配播放列表**: 标题格式 `{原标题} - 中文配音版`，标签包含 `["中文配音", "AI配音"]`
- **自动优化**: 标题长度限制、标签数量控制

#### 4. Cookie管理系统
- **自动生成**: 通过浏览器扫码登录生成Cookie
- **有效性检查**: 自动检查Cookie是否有效
- **重新生成**: 支持Cookie失效时重新生成
- **安全存储**: Cookie文件安全存储在 `cookies/douyin_uploader/` 目录

### 🔧 技术实现

#### 1. 异步上传处理
- **异步架构**: 使用asyncio实现异步上传
- **错误处理**: 完善的错误处理和重试机制
- **状态监控**: 详细的上传状态和进度显示

#### 2. 浏览器自动化
- **Playwright**: 使用Playwright进行浏览器自动化
- **多浏览器支持**: 支持Chrome、Firefox等浏览器
- **无头模式**: 支持有头和无头模式运行

#### 3. 配置管理
- **分层配置**: 默认配置 + 用户配置的合并机制
- **动态加载**: 运行时动态加载配置
- **配置验证**: 自动验证配置的有效性

### 📚 新增文档

1. **`DOUYIN_UPLOADER.md`** - 抖音上传器详细使用说明
2. **`uploader/`** - 上传器模块目录
3. **`uploader_config.json`** - 上传器配置文件
4. **`setup_douyin_uploader.py`** - 设置脚本
5. **`test_douyin_uploader.py`** - 测试脚本

### 🛠️ 文件结构更新

```
VideoLingo/
├── uploader/                       # 上传器模块
│   ├── __init__.py
│   └── douyin_uploader.py         # 抖音上传器
├── uploader_config.json            # 上传器配置
├── setup_douyin_uploader.py       # 设置脚本
├── test_douyin_uploader.py        # 测试脚本
├── cookies/                        # Cookie存储
│   └── douyin_uploader/
│       └── account.json           # 抖音Cookie
└── ...                            # 其他现有文件
```

### 🚀 使用示例

#### 快速设置
```bash
# 安装依赖
pip install playwright
playwright install chromium

# 运行设置
python setup_douyin_uploader.py

# 测试上传器
python test_douyin_uploader.py
```

#### 配置上传器
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

#### 自动上传
```bash
# 启动监控器（自动上传）
python playlist_monitor.py
```

### ⚠️ 注意事项

1. **依赖安装**: 需要安装Playwright和浏览器驱动
2. **Cookie安全**: Cookie文件包含敏感信息，请妥善保管
3. **发布频率**: 避免过于频繁的上传，以免触发平台限制
4. **内容合规**: 确保上传内容符合抖音平台规范
5. **网络环境**: 确保网络连接稳定

### 🆘 故障排除

#### 常见问题
1. **Playwright未安装**: `pip install playwright && playwright install chromium`
2. **Cookie失效**: 运行设置脚本重新生成Cookie
3. **上传失败**: 检查网络连接和视频文件格式
4. **浏览器问题**: 检查Chrome路径配置

#### 调试命令
```bash
# 测试上传器
python test_douyin_uploader.py

# 检查Cookie
python -c "import asyncio; from uploader.douyin_uploader import DouyinUploader; print(asyncio.run(DouyinUploader().check_cookie_auth('cookies/douyin_uploader/account.json')))"

# 重新生成Cookie
python setup_douyin_uploader.py
```

---

## 版本 1.1.0 - 历史文件管理增强

### 🆕 新增功能

#### 1. 按播放列表划分的历史文件组织
- **功能**: 存档的视频现在按播放列表和视频信息进行组织
- **结构**: 
  ```
  history/
  ├── 中字/                          # 中字播放列表
  │   ├── video_id_1_视频标题1/      # 视频1的文件夹
  │   │   ├── process_info.json      # 处理信息
  │   │   ├── output_sub.mp4         # 带字幕的视频
  │   │   └── ...                    # 其他处理文件
  └── 中配/                          # 中配播放列表
      ├── video_id_2_视频标题2/      # 视频2的文件夹
      │   ├── process_info.json
      │   ├── output_dub.mp4         # 带配音的视频
      │   └── ...
  ```

#### 2. 处理信息文件
- **功能**: 每个视频文件夹包含详细的处理信息
- **内容**: 视频ID、标题、播放列表、处理时间、配置信息
- **格式**: JSON格式，便于程序读取和人工查看

#### 3. 历史管理工具
- **命令行工具**: `history_manager.py` - 完整的命令行历史管理工具
- **交互式工具**: `manage_history.py` - 简化的交互式历史管理器
- **功能**: 查看、清理、导出历史文件

#### 4. 代理支持
- **功能**: 支持通过代理访问YouTube
- **配置**: `proxy_config.json` 配置文件
- **使用**: `--proxy` 参数启用代理模式

### 🔧 改进功能

#### 1. 存档流程优化
- **改进**: 存档时自动创建播放列表和视频特定的文件夹
- **改进**: 自动生成处理信息文件
- **改进**: 安全的文件名处理（移除特殊字符，限制长度）

#### 2. 配置管理
- **新增**: `playlist_monitor_config.json` - 监控器配置文件
- **新增**: `proxy_config.json` - 代理配置文件
- **改进**: 支持自定义播放列表和处理参数

#### 3. 启动脚本
- **新增**: `start_monitor.bat` - Windows启动脚本
- **新增**: `start_monitor.sh` - Linux/macOS启动脚本
- **改进**: 支持代理模式和测试模式

### 📚 新增文档

1. **`HISTORY_MANAGEMENT.md`** - 历史文件管理详细说明
2. **`PROXY_SETUP.md`** - 代理配置指南
3. **`README_PLAYLIST_MONITOR.md`** - 完整功能说明
4. **`QUICK_START.md`** - 快速启动指南

### 🛠️ 技术改进

#### 1. 文件组织
- **改进**: 按播放列表分类存储
- **改进**: 按视频信息创建独立文件夹
- **改进**: 安全的文件名处理

#### 2. 错误处理
- **改进**: 更好的错误处理和日志记录
- **改进**: 代理连接失败的处理
- **改进**: 文件操作的安全检查

#### 3. 用户体验
- **新增**: 交互式历史管理工具
- **新增**: 详细的处理状态显示
- **新增**: 多种启动方式支持

### 📁 文件结构更新

```
VideoLingo/
├── playlist_monitor.py              # 主监控脚本
├── start_monitor.py                 # 启动脚本
├── start_monitor.bat               # Windows启动脚本
├── start_monitor.sh                # Linux/macOS启动脚本
├── test_monitor.py                 # 测试脚本
├── history_manager.py              # 历史管理工具
├── manage_history.py               # 交互式历史管理
├── proxy_config.json               # 代理配置文件
├── playlist_monitor_config.json    # 监控器配置文件
├── playlist_monitor/               # 监控器数据目录
│   └── processed_videos.json      # 已处理视频记录
├── output/                         # 处理中的文件
└── history/                        # 存档的文件（按播放列表分类）
    ├── 中字/                      # 中字播放列表
    └── 中配/                      # 中配播放列表
```

### 🚀 使用示例

#### 基本启动
```bash
# Windows
start_monitor.bat

# Linux/macOS
./start_monitor.sh

# 通用方法
python start_monitor.py
```

#### 启用代理
```bash
# 启用代理模式
python start_monitor.py --proxy

# 测试模式 + 代理
python start_monitor.py --test --proxy
```

#### 历史管理
```bash
# 命令行工具
python history_manager.py --list

# 交互式工具
python manage_history.py
```

### 🔄 向后兼容性

- ✅ 保持原有的处理流程不变
- ✅ 兼容现有的配置文件
- ✅ 支持原有的启动方式
- ✅ 历史文件可以平滑迁移

### ⚠️ 注意事项

1. **磁盘空间**: 新的文件组织方式可能需要更多磁盘空间
2. **权限**: 确保对history目录有读写权限
3. **代理**: 使用代理时确保代理服务器稳定运行
4. **备份**: 建议定期备份重要的处理结果

### 🆘 故障排除

#### 常见问题
1. **文件夹名称过长**: 系统会自动截断标题长度
2. **特殊字符问题**: 系统会自动清理特殊字符
3. **权限问题**: 确保对history目录有读写权限
4. **代理连接失败**: 检查代理配置和网络连接

#### 调试命令
```bash
# 测试监控器
python test_monitor.py

# 查看历史文件
python history_manager.py --list

# 检查代理连接
curl --proxy http://127.0.0.1:7890 https://www.youtube.com
```

---

**🎉 享受更强大的视频翻译配音自动化体验！**

---

## 版本 1.2.0 - 抖音上传标题优化

### 🆕 新增功能

#### 1. 自定义标题支持
- **功能**: 支持使用 `log/terminology.json` 中的 `theme` 字段作为抖音标题
- **优势**: 提供更详细和准确的视频描述，提升内容质量
- **长度**: 支持最多1000字符的长标题，充分利用抖音平台功能
- **备用**: 如果找不到 `terminology.json` 文件，自动回退到默认标题生成逻辑

#### 2. 标题读取逻辑
- **路径**: `history/{playlist_name}/{video_id}_{safe_title}/log/terminology.json`
- **字段**: 读取 `theme` 字段作为标题
- **处理**: 自动处理文件不存在和读取错误的情况
- **日志**: 详细记录标题读取过程

### 🔧 改进功能

#### 1. 上传器接口优化
- **新增**: `custom_title` 参数支持自定义标题
- **改进**: 上传函数支持传递自定义标题
- **改进**: 日志记录优化，显示标题预览

#### 2. 播放列表监控器集成
- **集成**: 自动读取 `terminology.json` 中的主题信息
- **处理**: 智能处理文件路径和读取错误
- **日志**: 详细记录标题读取和使用过程

### 📚 文档更新

1. **`DOUYIN_UPLOADER.md`** - 更新标题生成说明
2. **变更日志** - 添加新版本功能说明

### 🛠️ 技术改进

#### 1. 文件读取
- **改进**: 安全的JSON文件读取
- **改进**: 错误处理和日志记录
- **改进**: 文件路径构建逻辑

#### 2. 标题处理
- **改进**: 支持长标题（抖音支持长标题）
- **改进**: 智能回退机制
- **改进**: 详细的处理状态显示

### 📁 文件结构

```
VideoLingo/
├── uploader/
│   └── douyin_uploader.py         # 更新：支持自定义标题
├── playlist_monitor.py             # 更新：集成标题读取逻辑
└── history/
    └── {playlist_name}/
        └── {video_id}_{title}/
            └── log/
                └── terminology.json # 标题来源文件
```

### 🚀 使用示例

#### 自动标题读取
```bash
# 启动监控器，自动使用terminology.json中的theme作为标题
python playlist_monitor.py

# 手动上传，使用自定义标题
python -c "
import asyncio
from uploader.douyin_uploader import upload_to_douyin
asyncio.run(upload_to_douyin('video.mp4', '中字', custom_title='自定义标题'))
"
```

### ⚠️ 注意事项

1. **文件依赖**: 需要 `log/terminology.json` 文件存在
2. **标题长度**: 抖音支持长标题，但建议控制在合理范围内
3. **文件编码**: 确保 `terminology.json` 使用UTF-8编码
4. **错误处理**: 系统会自动处理文件不存在的情况

### 🆘 故障排除

#### 常见问题
1. **terminology.json不存在**: 系统会自动使用默认标题
2. **theme字段为空**: 系统会使用视频原标题
3. **文件读取错误**: 检查文件权限和编码格式
4. **标题过长**: 系统会显示前100个字符的预览

#### 调试命令
```bash
# 检查terminology.json文件
find history -name "terminology.json" -exec cat {} \;

# 测试标题读取逻辑
python -c "
import json
with open('history/中字/Inside Rocket Lab ｜ Spacecraft Production at Scale/log/terminology.json', 'r', encoding='utf-8') as f:
    data = json.load(f)
    print('Theme:', data.get('theme', 'Not found'))
"
```

---

**🎉 享受更智能的视频标题生成体验！** 