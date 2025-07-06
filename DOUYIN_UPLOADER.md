# 抖音上传器使用说明

## 概述

VideoLingo抖音上传器基于[social-auto-upload](https://github.com/dreammis/social-auto-upload)项目，实现了自动将处理完成的视频上传到抖音创作者中心的功能。

## 功能特性

- ✅ 自动上传处理完成的视频到抖音
- ✅ 支持定时发布功能
- ✅ 自动生成标题和标签
- ✅ 支持Cookie管理
- ✅ 根据播放列表类型生成不同内容
- ✅ 错误重试机制

## 安装依赖

### 1. 安装Playwright

```bash
pip install playwright
```

### 2. 安装浏览器驱动

```bash
playwright install chromium
```

## 快速设置

### 1. 运行设置脚本

```bash
python setup_douyin_uploader.py
```

设置脚本会引导你完成以下配置：
- 启用/禁用抖音上传功能
- 设置自动上传和发布时间
- 配置位置和标签
- 生成抖音登录Cookie

### 2. 手动配置（可选）

编辑 `uploader_config.json` 文件：

```json
{
  "douyin": {
    "enabled": true,
    "account_file": "cookies/douyin_uploader/account.json",
    "auto_upload": true,
    "schedule_time": "16:00",  // 或设置为 null 立即发布
    "location": "杭州市",
    "tags": ["VideoLingo", "AI翻译", "视频配音"],
    "chrome_path": null
  },
  "upload_settings": {
    "max_title_length": 30,
    "max_tags": 10,
    "retry_times": 3,
    "wait_time": 2
  }
}
```

## 配置说明

### 抖音配置 (douyin)

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `enabled` | 是否启用抖音上传 | `false` |
| `account_file` | Cookie文件路径 | `cookies/douyin_uploader/account.json` |
| `auto_upload` | 是否自动上传 | `false` |
| `schedule_time` | 定时发布时间 | `16:00` 或 `null`（立即发布） |
| `location` | 发布位置 | `杭州市` |
| `tags` | 默认标签列表 | `["VideoLingo", "AI翻译", "视频配音"]` |
| `chrome_path` | Chrome浏览器路径 | `null` |

### 上传设置 (upload_settings)

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `max_title_length` | 标题最大长度 | `30` |
| `max_tags` | 标签最大数量 | `10` |
| `retry_times` | 重试次数 | `3` |
| `wait_time` | 等待时间(秒) | `2` |

## 使用方法

### 1. 自动上传（推荐）

启用自动上传后，播放列表监控器会自动将处理完成的视频上传到抖音：

```bash
python playlist_monitor.py
```

### 发布模式

- **立即发布**: 设置 `schedule_time` 为 `null`，视频处理完成后立即发布
- **定时发布**: 设置 `schedule_time` 为时间字符串（如 `"16:00"`），视频将在指定时间发布

### 2. 手动上传

```python
from uploader.douyin_uploader import upload_to_douyin
import asyncio

async def upload_video():
    success = await upload_to_douyin(
        video_path="path/to/video.mp4",
        playlist_name="中配",  # 或 "中字"
        schedule_time=None  # 立即发布，或设置datetime对象
    )
    print("Upload success:", success)

asyncio.run(upload_video())
```

## 标题和标签生成

### 标题来源
- **优先使用**: `log/terminology.json` 文件中的 `theme` 字段作为标题
- **备用方案**: 如果找不到 `terminology.json` 文件，则使用默认标题生成逻辑
- **标题长度**: 支持最多1000字符的长标题，充分利用抖音平台的长标题功能

### 默认标题格式
- **中字播放列表**: `{原标题} - 中文字幕版`
- **中配播放列表**: `{原标题} - 中文配音版`

### 标签生成
- **中字播放列表**: 额外标签 `["中文字幕", "翻译"]`
- **中配播放列表**: 额外标签 `["中文配音", "AI配音"]`

## Cookie管理

### 生成Cookie

1. 运行设置脚本：
```bash
python setup_douyin_uploader.py
```

2. 按提示扫码登录抖音创作者中心
3. Cookie会自动保存到 `cookies/douyin_uploader/account.json`

### 检查Cookie有效性

```python
from uploader.douyin_uploader import DouyinUploader
import asyncio

async def check_cookie():
    uploader = DouyinUploader()
    is_valid = await uploader.check_cookie_auth("cookies/douyin_uploader/account.json")
    print("Cookie valid:", is_valid)

asyncio.run(check_cookie())
```

### 重新生成Cookie

如果Cookie失效，可以重新生成：

```python
from uploader.douyin_uploader import DouyinUploader
import asyncio

async def regenerate_cookie():
    uploader = DouyinUploader()
    success = await uploader.generate_cookie("cookies/douyin_uploader/account.json")
    print("Cookie regenerated:", success)

asyncio.run(regenerate_cookie())
```

## 故障排除

### 常见问题

1. **Playwright未安装**
   ```
   pip install playwright
   playwright install chromium
   ```

2. **Cookie失效**
   - 运行设置脚本重新生成Cookie
   - 确保登录的是抖音创作者中心

3. **上传失败**
   - 检查网络连接
   - 确认视频文件存在且格式正确
   - 查看日志获取详细错误信息

4. **浏览器路径问题**
   - 在配置中设置正确的Chrome路径
   - 或使用系统默认浏览器

### 调试模式

启用详细日志：

```python
import logging
logging.getLogger('douyin_uploader').setLevel(logging.DEBUG)
```

## 注意事项

1. **账号安全**
   - Cookie文件包含敏感信息，请妥善保管
   - 不要将Cookie文件提交到版本控制系统

2. **发布频率**
   - 避免过于频繁的上传，以免触发平台限制
   - 建议使用定时发布功能

3. **内容合规**
   - 确保上传内容符合抖音平台规范
   - 注意版权和内容审核

4. **网络环境**
   - 确保网络连接稳定
   - 如使用代理，请在配置中设置

## 更新日志

### v1.0.0
- 初始版本
- 支持抖音视频上传
- 支持定时发布
- 支持Cookie管理
- 集成播放列表监控器

## 技术支持

如遇到问题，请：
1. 查看本文档的故障排除部分
2. 检查日志文件获取详细错误信息
3. 确认所有依赖已正确安装
4. 验证网络连接和账号状态 