# 播放列表监控器修复说明

## 问题描述

播放列表监控器在处理多个视频时出现错误：
```
Error in text processing: Number of videos found 32 is not unique. Please check.
```

## 问题原因

这个错误来自 `core/_1_ytdlp.py` 中的 `find_video_files` 函数。该函数期望在 `output` 目录中只有一个视频文件，但是当播放列表监控器处理多个视频时，会在 `output` 目录中留下多个文件，导致函数抛出错误。

## 修复方案

在 `playlist_monitor.py` 的 `process_video` 方法开始时添加了清理 `output` 目录的逻辑：

```python
# 0. 清理output目录，确保只处理一个视频
print("🧹 Cleaning output directory...")
if os.path.exists("output"):
    for item in os.listdir("output"):
        item_path = os.path.join("output", item)
        try:
            if os.path.isfile(item_path):
                os.remove(item_path)
            elif os.path.isdir(item_path):
                shutil.rmtree(item_path)
        except Exception as e:
            print(f"⚠️ Warning: Could not remove {item_path}: {e}")
```

## 修复效果

1. **确保单一视频处理**：每次处理新视频前，都会清理 `output` 目录中的所有文件
2. **避免文件冲突**：防止多个视频文件同时存在于 `output` 目录中
3. **保持处理流程**：不影响后续的视频下载和处理步骤

## 测试验证

修复已通过以下测试验证：

1. ✅ **Output目录清理功能**：正确清理所有文件和目录
2. ✅ **监控器初始化**：正常加载配置和播放列表
3. ✅ **播放列表访问**：能够正确获取播放列表中的视频
4. ✅ **已处理视频跟踪**：正确记录已处理的视频ID
5. ✅ **find_video_files函数**：正确处理单个视频文件的情况

## 使用方法

修复后的播放列表监控器可以正常使用：

```bash
python playlist_monitor.py
```

## 注意事项

1. **清理过程**：每次处理新视频时，会显示清理进度
2. **错误处理**：如果某些文件无法删除，会显示警告但不会中断处理
3. **历史存档**：处理完成的视频仍会正确存档到 `history` 目录

## 变更日志

- **2024-01-XX**：修复播放列表监控器的多视频处理错误
  - 添加 `output` 目录清理逻辑
  - 确保每次只处理一个视频
  - 通过测试验证修复效果 