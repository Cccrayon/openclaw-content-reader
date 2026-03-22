---
name: content-reader
description: 读取小红书、B站、YouTube、抖音链接内容。当用户发来这些平台链接时激活。
---

# Content Reader

读取小红书、B站、YouTube、抖音链接内容，自动转录/总结。

## 平台支持

| 平台 | 内容获取 | ASR | 需要登录 |
|------|----------|-----|----------|
| YouTube | ✅ 字幕下载 | ✅ Whisper | ❌ |
| 抖音 | ✅ 直链获取 | ✅ Whisper | ❌ |
| B站 | ✅ 字幕下载 | ✅ Whisper | ✅ Cookie |
| 小红书 | ✅ 图文+图片 | ⚠️ OCR | ❌ |

## 各平台工作流程

### YouTube

```bash
# 1. 获取字幕列表
yt-dlp --list-subs "URL"

# 2. 下载字幕
mkdir -p /tmp/yt
yt-dlp --write-sub --write-auto-sub --sub-lang en \
  --skip-download -o "/tmp/yt/%(id)s" "URL"

# 3. 解析 VTT（见下方 Python 脚本）

# 4. Whisper 兜底（无字幕时）
yt-dlp -x --audio-format mp3 -o "/tmp/yt/audio.%(ext)s" "URL"
python3 -c "
import whisper
model = whisper.load_model('base')
result = model.transcribe('/tmp/yt/audio.mp3', language='en', fp16=False)
print(result['text'])
"
```

### 抖音

```bash
# 使用脚本自动完成
python3 scripts/douyin_whisper.py "https://v.douyin.com/xxx/"

# 参数
# -m, --model: Whisper 模型 (tiny/base/small/medium) [默认: base]
# -l, --language: 语言代码 [默认: zh]
# -o, --output: 输出文件
# -k, --keep: 保留中间文件
```

### B站

```bash
# 1. 需要 Cookie（/tmp/bili_cookies.txt）
# 提取方法：browser_cookie3.chrome(domain_name='bilibili.com')

# 2. 下载字幕
mkdir -p /tmp/bili
yt-dlp --cookies /tmp/bili_cookies.txt \
  --write-sub --write-auto-sub --sub-lang zh-Hans,en \
  --skip-download -o "/tmp/bili/%(id)s" "URL"

# 3. Whisper 兜底
yt-dlp -x --audio-format mp3 -o "/tmp/bili/audio.%(ext)s" "URL"
python3 -c "
import whisper
model = whisper.load_model('base')
result = model.transcribe('/tmp/bili/audio.mp3', language='zh', fp16=False)
print(result['text'])
"
```

### 小红书

1. browser 打开页面
2. JS 滚动触发懒加载
3. JS 提取 `window.__INITIAL_STATE__`
4. MiniMax MCP 做图片 OCR

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

## 关键约束

### YouTube
- 无需 Cookie，字幕直接下载
- 字幕文件：`/tmp/yt/VIDEO_ID.en.vtt`

### 抖音
- 脚本：`scripts/douyin_whisper.py`
- 无需 API Key，本地 Whisper

### B站
- 需要 Cookie：`/tmp/bili_cookies.txt`
- Cookie 过期需重新导出

### 小红书
- 图片为 webp 压缩格式
- MiniMax API 用于 OCR

## 性能

| 场景 | 耗时 |
|------|------|
| 有字幕（YouTube/B站） | ~1分钟 |
| Whisper 兜底（base） | ~4分钟 |

## 文档

```
docs/
├── install.md        # 安装指南
├── quickstart.md    # 快速入门
├── platforms.md     # 平台详细说明
└── troubleshooting.md # 故障排除

examples/
└── sample-output.md # 输出示例
```
