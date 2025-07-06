# 🌐 代理配置指南

## 概述

YouTube Playlist Monitor 支持通过代理访问YouTube，这对于在某些网络环境下访问YouTube很有用。

## 代理配置

### 1. 配置文件

编辑 `proxy_config.json` 文件：

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

### 2. 配置说明

- `enabled`: 是否启用代理（true/false）
- `https_proxy`: HTTPS代理地址
- `http_proxy`: HTTP代理地址
- `all_proxy`: SOCKS5代理地址
- `yt_dlp_proxy`: yt-dlp使用的代理地址

### 3. 常见代理配置

#### Clash 代理
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

#### V2Ray 代理
```json
{
  "proxy_settings": {
    "enabled": true,
    "https_proxy": "http://127.0.0.1:1087",
    "http_proxy": "http://127.0.0.1:1087",
    "all_proxy": "socks5://127.0.0.1:1086"
  },
  "yt_dlp_proxy": "http://127.0.0.1:1087"
}
```

#### 其他代理软件
根据你的代理软件配置，修改端口号即可。

## 使用方法

### 1. 启用代理模式

```bash
# 使用Python脚本
python start_monitor.py --proxy

# 使用启动脚本
./start_monitor.sh --proxy  # Linux/macOS
start_monitor.bat --proxy   # Windows
```

### 2. 测试代理连接

```bash
# 测试模式 + 代理
python start_monitor.py --test --proxy
```

### 3. 检查代理状态

启动时会显示代理信息：
```
🌐 Proxy mode enabled
Using proxy: http://127.0.0.1:7890
```

## 故障排除

### 1. 代理连接失败

**症状**: 无法下载视频或访问播放列表

**解决方案**:
1. 检查代理软件是否正在运行
2. 验证代理端口是否正确
3. 测试代理连接：
   ```bash
   curl --proxy http://127.0.0.1:7890 https://www.youtube.com
   ```

### 2. 代理配置错误

**症状**: 显示 "Proxy config not found or disabled"

**解决方案**:
1. 检查 `proxy_config.json` 文件是否存在
2. 确保 `enabled` 字段设置为 `true`
3. 验证代理地址格式是否正确

### 3. 网络超时

**症状**: 下载过程中出现超时错误

**解决方案**:
1. 增加代理超时时间
2. 检查网络连接稳定性
3. 尝试使用不同的代理服务器

## 环境变量设置

如果你希望全局设置代理环境变量，可以在启动前设置：

### Linux/macOS
```bash
export https_proxy=http://127.0.0.1:7890
export http_proxy=http://127.0.0.1:7890
export all_proxy=socks5://127.0.0.1:7890

python start_monitor.py
```

### Windows
```cmd
set https_proxy=http://127.0.0.1:7890
set http_proxy=http://127.0.0.1:7890
set all_proxy=socks5://127.0.0.1:7890

python start_monitor.py
```

## 注意事项

1. **代理性能**: 使用代理可能会影响下载速度
2. **稳定性**: 确保代理服务器稳定运行
3. **安全性**: 使用可信的代理服务器
4. **配置备份**: 建议备份代理配置文件

## 高级配置

### 自定义代理规则

你可以根据不同的网络环境配置不同的代理设置：

```json
{
  "proxy_settings": {
    "enabled": true,
    "https_proxy": "http://127.0.0.1:7890",
    "http_proxy": "http://127.0.0.1:7890",
    "all_proxy": "socks5://127.0.0.1:7890",
    "no_proxy": "localhost,127.0.0.1"
  },
  "yt_dlp_proxy": "http://127.0.0.1:7890"
}
```

### 多代理配置

如果需要支持多个代理配置，可以创建多个配置文件：

```bash
# 使用不同的代理配置
cp proxy_config.json proxy_config_clash.json
cp proxy_config.json proxy_config_v2ray.json

# 根据需要切换配置文件
python start_monitor.py --proxy
``` 