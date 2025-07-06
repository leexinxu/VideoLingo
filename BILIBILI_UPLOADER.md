# Bilibili上传器使用说明

## 功能概述

Bilibili上传器为VideoLingo项目提供自动上传到bilibili的功能，支持：
- 自动标题生成（基于terminology.json的theme字段）
- 智能标签生成
- 定时发布
- Cookie管理
- 错误处理和重试

## 标题长度限制

**重要：bilibili标题长度限制为80个字符**

- 如果标题超过80个字符，会自动截断并添加"..."
- 添加emoji后如果仍超过限制，会再次截断
- 系统会显示警告信息提示标题被截断

## 安装依赖

```bash
pip install biliup
```

## 配置文件

### 1. 上传器配置 (uploader_config.json)

```json
{
  "bilibili": {
    "enabled": true,
    "auto_upload": true,
    "schedule_time": null  // null表示立即发布，或设置时间如"16:00"
  }
}
```

### 2. Cookie配置 (uploader_config/bilibili_cookies.json)

```json
{
  "cookie_info": {
    "cookies": [
      {
        "name": "SESSDATA",
        "value": "your_sessdata_here"
      },
      {
        "name": "bili_jct",
        "value": "your_bili_jct_here"
      },
      {
        "name": "DedeUserID",
        "value": "your_dede_user_id_here"
      },
      {
        "name": "DedeUserID__ckMd5",
        "value": "your_dede_user_id_ck_md5_here"
      }
    ]
  },
  "token_info": {
    "access_token": "your_access_token_here"
  }
}
```

## 获取Cookie

1. 登录bilibili网站
2. 打开浏览器开发者工具 (F12)
3. 在Console中运行以下代码：

```javascript
let cookies = {};
document.cookie.split(';').forEach(function(cookie) {
    let parts = cookie.split('=');
    if (parts.length === 2) {
        cookies[parts[0].trim()] = parts[1].trim();
    }
});
console.log(JSON.stringify(cookies, null, 2));
```

4. 复制输出的cookie信息
5. 按照示例格式创建 `uploader_config/bilibili_cookies.json` 文件

## 设置脚本

运行设置脚本检查配置：

```bash
python setup_bilibili.py
```

## 使用方法

### 1. 基本使用

```python
from uploader.bilibili_uploader import BilibiliUploader

uploader = BilibiliUploader()
success = await uploader.upload_video(
    video_file="path/to/video.mp4",
    playlist_name="中字",
    custom_title="自定义标题"
)
```

### 2. 在播放列表监控器中使用

播放列表监控器会自动调用bilibili上传器：

```python
# 在playlist_monitor.py中已集成
if self.uploader_config.get("bilibili", {}).get("enabled", False):
    await self.upload_to_bilibili(video_info, playlist_name)
```

## 功能特性

### 1. 自动标题生成

- 优先使用 `terminology.json` 中的 `theme` 字段
- 如果不存在，使用视频文件名
- 自动添加随机emoji避免重复标题
- 自动截断超过80个字符的标题

### 2. 智能标签生成

- 基础标签：VideoLingo, AI翻译, 自动生成
- 根据播放列表类型添加特定标签：
  - 中字：中文字幕, 字幕翻译
  - 中配：中文配音, AI配音, 语音合成
- 从标题中提取关键词作为标签

### 3. 分区映射

```python
category_mapping = {
    "中字": 27,  # 综合
    "中配": 27,  # 综合
    "default": 27
}
```

### 4. 发布时间设置

- `schedule_time: null` - 立即发布
- `schedule_time: "16:00"` - 定时发布（明天16:00）

## 错误处理

### 常见错误及解决方案

1. **Cookie文件不存在**
   ```
   ❌ Bilibili cookie file not found: uploader_config/bilibili_cookies.json
   ```
   解决：创建cookie文件并填入有效cookie

2. **缺少必要的cookie字段**
   ```
   ❌ Missing required cookie fields: ['SESSDATA', 'bili_jct', 'DedeUserID']
   ```
   解决：确保cookie文件包含所有必要字段

3. **标题长度超限**
   ```
   ⚠️ Title truncated to 80 characters: 标题内容...
   ```
   这是正常行为，系统会自动处理

4. **上传失败**
   ```
   ❌ 视频文件上传失败: 错误信息
   ```
   检查网络连接和cookie有效性

## 测试

运行测试脚本验证配置：

```bash
python test_bilibili_integration.py
```

## 注意事项

1. **标题长度**：bilibili限制标题最多80个字符
2. **Cookie有效期**：定期更新cookie以确保上传功能正常
3. **网络环境**：确保网络连接稳定
4. **上传频率**：避免过于频繁的上传，建议间隔适当时间

## 变更日志

- **2024-01-XX**：添加bilibili上传器支持
  - 集成social-auto-upload项目的bilibili上传功能
  - 支持自动标题生成和标签管理
  - 添加标题长度限制（80字符）
  - 支持定时发布功能 