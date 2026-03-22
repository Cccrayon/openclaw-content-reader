---
name: content-reader
description: 读取小红书、B站、YouTube、抖音链接内容。当用户发来这些平台链接时激活。
---

# Content Reader

读取小红书、B站、YouTube、抖音链接内容，自动转录/总结。

## 平台支持

| 平台 | 内容获取 | ASR | 无字幕时 |
|------|----------|-----|---------|
| YouTube | ✅ 字幕下载 | ✅ Whisper | 自动降级 |
| 抖音 | ✅ 直链获取 | ✅ Whisper | 无需降级 |
| B站 | ✅ AI字幕/官方字幕 | ✅ Whisper | 自动降级 |
| 小红书 | ✅ 图文+图片 | ⚠️ MiniMax OCR | 图片文字识别 |

**注意：**
- B站需要 Cookie 获取官方字幕，但 AI 字幕（无需 Cookie）已足够日常使用
- 小红书图片 OCR 需要 MiniMax API（如未配置，跳过图片文字识别）

## 工作流程

### YouTube

```
发送链接
    ↓
尝试下载字幕（无需登录）
    ↓
【成功】→ 解析 VTT → 输出
【失败/无字幕】→ Whisper 转写 → 输出
```

```bash
# 字幕下载（无需 Cookie）
mkdir -p /tmp/yt
yt-dlp --write-sub --write-auto-sub --sub-lang en,zh-Hans \
  --skip-download -o "/tmp/yt/%(id)s" "URL"

# Whisper 兜底
yt-dlp -x --audio-format mp3 -o "/tmp/yt/audio.%(ext)s" "URL"
python3 -c "
import whisper
model = whisper.load_model('base')
result = model.transcribe('/tmp/yt/audio.mp3', language='auto', fp16=False)
print(result['text'])
"
```

### 抖音

```
发送链接
    ↓
自动完成：解析URL → 下载视频 → ffmpeg提取音频 → Whisper转写
```

```bash
python3 scripts/douyin_whisper.py "https://v.douyin.com/XOK_H3t9n38/"

# 参数
# -m, --model: Whisper 模型 (tiny/base/small/medium) [默认: base]
# -l, --language: 语言代码 [默认: zh]
# -o, --output: 输出文件
# -k, --keep: 保留中间文件
```

### B站

```
发送链接
    ↓
【优先】尝试 AI 字幕（无需 Cookie）
    ↓
【失败】提示：可配置 Cookie 获取官方字幕（可选）
    ↓
【都行】Whisper 兜底 → 输出
```

```bash
# AI 字幕（无需 Cookie，大多数情况够用）
mkdir -p /tmp/bili
yt-dlp --write-sub --write-auto-sub --sub-lang ai-zh \
  --skip-download -o "/tmp/bili/%(id)s" "URL"

# 如果需要官方字幕（可选，需要 Cookie）
# 详见 docs/platforms.md - B站 Cookie 配置

# Whisper 兜底
yt-dlp -x --audio-format mp3 -o "/tmp/bili/audio.%(ext)s" "URL"
python3 -c "
import whisper
model = whisper.load_model('base')
result = model.transcribe('/tmp/bili/audio.mp3', language='zh', fp16=False)
print(result['text'])
"
```

### 小红书

```
发送链接
    ↓
browser 打开 → JS 滚动加载 → 提取内容
    ↓
【可选】MiniMax OCR 图片文字识别
    ↓
输出
```

## B站 Cookie 配置（可选）

**什么时候需要？**
- AI 字幕质量不够好时
- 需要获取特定语言的官方字幕

**如何配置：**
```bash
# 1. 浏览器登录 bilibili.com
# 2. 使用 EditThisCookie 扩展导出 Cookie
# 3. 保存到 /tmp/bili_cookies.txt
```

**如果未配置？**
- 不影响使用，AI 字幕（无需 Cookie）已足够

## VTT 解析脚本

```python
import re

with open('/tmp/yt/VIDEO_ID.en.vtt', 'r') as f:
    content = f.read()

content = re.sub(r'<[^>]+>', '', content)
pattern = r'\d{2}:\d{2}:\d{2}\.\d{3}\s*-->\s*\d{2}:\d{2}:\d{2}\.\d{3}[^\n]*\n([^\n<]+)'
matches = re.findall(pattern, content)

seen = set()
result = []
for m in matches:
    m = m.strip()
    if m and m not in seen and len(m) > 2:
        seen.add(m)
        result.append(m)

with open('/tmp/yt/transcript.txt', 'w') as f:
    f.write('\n'.join(result))
```

## 性能

| 场景 | 耗时 |
|------|------|
| YouTube/B站 有字幕 | ~1分钟 |
| 抖音视频 | ~1-5分钟（取决于视频长度） |
| Whisper 兜底 | ~4分钟 |

## 文档

```
docs/
├── install.md        # 安装指南
├── quickstart.md    # 快速入门
├── platforms.md     # 平台详细说明
└── troubleshooting.md # 常见问题

examples/
└── sample-output.md # 输出示例
```
