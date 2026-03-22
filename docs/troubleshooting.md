# 故障排除

## 常见问题

### 1. yt-dlp 相关

#### `command not found: yt-dlp`

**原因**：yt-dlp 未安装
**解决**：
```bash
pip install yt-dlp
# 或
brew install yt-dlp  # macOS
```

#### `ERROR: Unable to extract uploader nickname`

**原因**：视频页面结构变化，yt-dlp 版本过旧
**解决**：
```bash
pip install -U yt-dlp
```

#### B站 `Fresh cookies needed`

**原因**：Cookie 过期或无效
**解决**：
1. 重新登录 B站
2. 使用 EditThisCookie 导出新 Cookie
3. 保存到 `/tmp/bili_cookies.txt`

---

### 2. 抖音相关

#### `ValueError: 无法从HTML中解析视频信息`

**原因**：
- 分享链接已过期
- 视频被删除
- 抖音页面结构变化

**解决**：
1. 获取新的分享链接
2. 确认视频仍可播放

#### 视频下载很慢

**原因**：视频文件较大（抖音视频通常 50-500MB）

**解决**：
- 选择较短的视频测试
- 等待下载完成
- 使用 `-k` 参数保留中间文件，避免重复下载

#### `ffmpeg` 相关错误

**原因**：ffmpeg 未安装或版本过旧

**解决**：
```bash
# macOS
brew install ffmpeg

# Ubuntu
sudo apt install ffmpeg

# 验证
ffmpeg -version
```

---

### 3. Whisper 相关

#### `ModuleNotFoundError: No module named 'whisper'`

**原因**：Whisper 未安装
**解决**：
```bash
pip install openai-whisper
```

#### 内存不足（`RuntimeError: CUDA out of memory`）

**原因**：GPU 内存不足
**解决**：
1. 使用更小的模型：`python3 douyin_whisper.py "URL" -m tiny`
2. 或使用 CPU：`python3 douyin_whisper.py "URL"`（默认 CPU）

#### 转写很慢

**原因**：使用 CPU + 大模型

**解决**：
| 方案 | 速度 | 精度 |
|------|------|------|
| tiny 模型 | 快 | 较低 |
| base 模型（默认） | 中 | 中等 |
| small 模型 | 较慢 | 较高 |

---

### 4. 小红书相关

#### 获取不到内容

**原因**：
- 页面未完全加载
- 懒加载未触发

**解决**：
1. 确认页面已完全加载
2. 手动滚动页面
3. 重试

#### 图片下载失败

**原因**：
- URL 过期
- 网络问题

**解决**：
重试或跳过图片

---

### 5. 环境相关

#### `zsh: no matches found: *.py`

**原因**：Shell  globbing 未匹配到文件
**解决**：
```bash
python3 scripts/douyin_whisper.py "URL"
```

#### SSL 证书错误

**原因**：Python SSL 证书配置问题
**解决**：
```bash
# macOS
/Applications/Python\ 3.x/Install\ Certificates.command

# 或
pip install --upgrade certifi
```

---

## 诊断命令

运行以下命令快速诊断问题：

```bash
# 1. 检查 Python 环境
python --version

# 2. 检查依赖
python -c "import whisper, requests; print('OK')"
pip list | grep -E "whisper|yt-dlp|requests"

# 3. 检查系统工具
which ffmpeg yt-dlp

# 4. 测试网络
curl -I https://www.youtube.com
curl -I https://www.douyin.com
```

---

## 获取帮助

如问题无法解决：

1. 查看 [GitHub Issues](https://github.com/your-repo/issues)
2. 提供以下信息：
   - 操作系统和版本
   - Python 版本
   - 相关错误日志
   - 复现步骤
