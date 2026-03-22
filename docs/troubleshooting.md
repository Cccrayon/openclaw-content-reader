# 故障排除

## 设计理念

**让用户先用起来，碰到墙了再给梯子。**

以下问题按需查阅，不需要提前了解所有问题。

---

## 常见问题

### YouTube

#### `ERROR: Unable to extract uploader`

**原因**：视频页面结构变化
**解决**：
```bash
# 更新 yt-dlp
pip install -U yt-dlp
```

#### 无字幕可用

**原因**：视频没有自动字幕
**解决**：Whisper 兜底自动启用，无需操作

---

### 抖音

#### `ValueError: 无法从HTML中解析视频信息`

**原因**：链接过期或视频已删除
**解决**：获取新的分享链接重试

#### 视频下载很慢

**原因**：视频文件较大
**解决**：选择较短的视频；或等待下载完成

#### `ffmpeg` 相关错误

**原因**：ffmpeg 未安装
**解决**：
```bash
# macOS
brew install ffmpeg
# Ubuntu
sudo apt install ffmpeg
```

---

### B站

#### AI 字幕质量不好

**原因**：AI 生成字幕有误差
**解决**：配置 Cookie 获取官方字幕

**配置步骤：**
```bash
# 1. 浏览器登录 bilibili.com
# 2. 安装 EditThisCookie 扩展
# 3. 导出 Cookie 为 Netscape 格式，保存到 /tmp/bili_cookies.txt
# 4. 使用官方字幕下载
yt-dlp --cookies /tmp/bili_cookies.txt \
  --write-sub --write-auto-sub --sub-lang zh-Hans \
  --skip-download -o "/tmp/bili/%(id)s" "URL"
```

#### `Fresh cookies needed`

**原因**：Cookie 过期
**解决**：重新导出 Cookie

#### 不想配置 Cookie

**原因**：不想登录
**解决**：完全没问题，AI 字幕已足够日常使用

---

### Whisper

#### `ModuleNotFoundError: No module named 'whisper'`

**解决**：
```bash
pip install openai-whisper
```

#### 转写很慢

**原因**：CPU 处理大模型较慢
**解决**：使用更小的模型
```bash
python3 scripts/douyin_whisper.py "URL" -m tiny  # 更快，精度稍低
python3 scripts/douyin_whisper.py "URL" -m base  # 平衡（默认）
```

#### 内存不足

**原因**：GPU 内存不够
**解决**：使用 CPU（默认）
```bash
# 已默认使用 CPU，无需额外操作
```

---

### 小红书

#### 获取不到内容

**原因**：页面未完全加载
**解决**：重试，或手动滚动页面

#### 图片下载失败

**原因**：网络问题或 URL 过期
**解决**：重试，或跳过图片

---

## 诊断命令

快速检查环境：
```bash
# 检查 Python
python --version

# 检查依赖
python -c "import whisper, requests; print('OK')"

# 检查系统工具
which ffmpeg yt-dlp

# 检查网络
curl -I https://www.youtube.com
curl -I https://www.douyin.com
```

---

## 获取帮助

1. 查看 [GitHub Issues](https://github.com/Cccrayon/openclaw-content-reader/issues)
2. 提供：
   - 操作系统和版本
   - Python 版本
   - 错误日志
   - 复现步骤
