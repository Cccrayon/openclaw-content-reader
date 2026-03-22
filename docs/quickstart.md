# 快速入门

## 5 分钟开始使用

### 第 1 分钟：验证安装

```bash
# 运行以下命令验证环境
ffmpeg -version | head -1    # 应显示 ffmpeg 版本
yt-dlp --version             # 应显示 yt-dlp 版本
python -c "import whisper; print('OK')"  # 应显示 OK
```

### 第 2 分钟：测试 YouTube

```bash
# 下载一个测试视频的字幕
yt-dlp --write-sub --write-auto-sub --sub-lang en \
  --skip-download \
  -o "/tmp/yt/test" \
  "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
```

### 第 3 分钟：测试抖音

```bash
# 运行抖音脚本
python3 scripts/douyin_whisper.py "https://v.douyin.com/ih8cJfV/"
```

### 第 4 分钟：开始使用

将链接发送给配置好 content-reader skill 的 AI 助手，即可自动获取内容。

### 第 5 分钟：熟悉输出格式

正常输出包含：
- **标题/作者/时长**
- **字幕内容或转写稿**
- **核心内容解读**

---

## 各平台使用示例

### YouTube

**有字幕的视频（推荐）：**
```bash
yt-dlp --write-sub --write-auto-sub --sub-lang en \
  --skip-download -o "/tmp/yt/%(id)s" \
  "https://www.youtube.com/watch?v=VIDEO_ID"
```

**无字幕或需要中文：**
```bash
# 下载音频
yt-dlp -x --audio-format mp3 -o "/tmp/yt/audio.%(ext)s" "URL"

# Whisper 转写
python3 -c "
import whisper
model = whisper.load_model('base')
result = model.transcribe('/tmp/yt/audio.mp3', language='zh', fp16=False)
print(result['text'])
"
```

### 抖音

```bash
# 基本用法
python3 scripts/douyin_whisper.py "https://v.douyin.com/ih8cJfV/"

# 指定语言（中文视频）
python3 scripts/douyin_whisper.py "URL" -l zh

# 指定模型（更高精度）
python3 scripts/douyin_whisper.py "URL" -m small

# 保存结果到文件
python3 scripts/douyin_whisper.py "URL" -o /tmp/result.txt

# 保留中间文件（视频+音频）
python3 scripts/douyin_whisper.py "URL" -k
```

### B站

**配置 Cookie：**
```bash
# 1. 浏览器登录 B站
# 2. 使用 EditThisCookie 导出 Netscape 格式
# 3. 保存到 /tmp/bili_cookies.txt
```

**下载字幕：**
```bash
# 官方字幕
yt-dlp --cookies /tmp/bili_cookies.txt \
  --write-sub --write-auto-sub --sub-lang zh-Hans,en \
  --skip-download -o "/tmp/bili/%(id)s" "URL"

# AI字幕（无需Cookie）
yt-dlp --write-sub --write-auto-sub --sub-lang ai-zh \
  --skip-download -o "/tmp/bili/%(id)s" "URL"
```

### 小红书

通过 AI 助手发送链接，自动完成：
1. 打开页面
2. 提取内容
3. 图片 OCR
4. 汇总输出

---

## Whisper 模型选择

| 模型 | 大小 | 速度 | 精度 | 推荐场景 |
|------|------|------|------|----------|
| tiny | ~75MB | 最快 | 较低 | 快速测试 |
| **base** | ~140MB | 快 | 中等 | **日常使用** |
| small | ~450MB | 较慢 | 较高 | 需要高精度的中文 |
| medium | ~1.5GB | 慢 | 高 | 专业转写 |

---

## 下一步

- [平台详细说明](platforms.md)
- [故障排除](troubleshooting.md)
