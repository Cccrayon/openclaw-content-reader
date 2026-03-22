# 各平台详细说明

## YouTube

### 特点
- ✅ **最简单**：无需登录，字幕直接可下载
- ✅ **速度快**：字幕下载通常只需几秒
- ✅ **覆盖广**：几乎所有视频都有英文自动字幕
- ⚠️ 中文语音字幕覆盖率逐渐提高但仍有限

### 工作流程

```
发送链接 → yt-dlp 获取字幕 → 解析 VTT → 输出
    ↓（无字幕）
yt-dlp 下载音频 → Whisper 转写 → 输出
```

### 获取字幕

```bash
# 查看可用字幕
yt-dlp --list-subs "URL"

# 下载英文字幕
yt-dlp --write-sub --write-auto-sub --sub-lang en \
  --skip-download -o "/tmp/yt/%(id)s" "URL"

# 下载中文字幕（如有）
yt-dlp --write-sub --write-auto-sub --sub-lang zh-Hans \
  --skip-download -o "/tmp/yt/%(id)s" "URL"
```

### 字幕格式转换

VTT 格式转换为纯文本：
```python
import re

with open('video.en.vtt', 'r') as f:
    content = f.read()

# 移除 HTML 标签
content = re.sub(r'<[^>]+>', '', content)

# 提取时间轴之间的文本
pattern = r'\d{2}:\d{2}:\d{2}\.\d{3}\s*-->\s*\d{2}:\d{2}:\d{2}\.\d{3}[^\n]*\n([^\n<]+)'
matches = re.findall(pattern, content)

# 去重合并
seen = set()
result = []
for m in matches:
    m = m.strip()
    if m and m not in seen and len(m) > 2:
        seen.add(m)
        result.append(m)

print('\n'.join(result))
```

---

## 抖音

### 特点
- ✅ **本地运行**：无需 API Key
- ✅ **无需登录**：分享链接即可
- ⚠️ **视频较大**：下载需要较长时间
- ⚠️ 部分视频可能无法获取

### 工作流程

```
分享链接 → iesdouyin.com 获取视频URL → 下载 → ffmpeg提取音频 → Whisper转写
```

### 技术原理

```
分享链接 → iesdouyin.com/share/video/{id}
  → 提取 HTML 中的 window._ROUTER_DATA JSON
  → 找到 playwm URL → 替换为 play（无水印）
  → 下载视频 → ffmpeg 提取音频 → Whisper 转写
```

### 脚本参数

```bash
python3 scripts/douyin_whisper.py [OPTIONS]

Options:
  -m, --model      Whisper 模型 (tiny/base/small/medium/large) [默认: base]
  -l, --language   语言代码 (zh/en等) [默认: zh]
  -o, --output     输出文件路径
  -k, --keep       保留中间文件（视频+音频）
  -h, --help       显示帮助
```

### 示例

```bash
# 中文视频（默认）
python3 scripts/douyin_whisper.py "https://v.douyin.com/xxx/"

# 英文视频
python3 scripts/douyin_whisper.py "URL" -l en

# 高精度中文
python3 scripts/douyin_whisper.py "URL" -m small -l zh

# 保存结果
python3 scripts/douyin_whisper.py "URL" -o /tmp/result.txt
```

---

## B站（哔哩哔哩）

### 特点
- ✅ **字幕质量高**：官方字幕准确
- ✅ **速度快**：字幕下载通常只需几秒
- ⚠️ **需要 Cookie**：获取官方字幕需要登录

### 工作流程

```
有 Cookie → 官方字幕（最佳）
    ↓（无 Cookie）
AI字幕（ai-zh）→ 自动生成
    ↓（都无）
Whisper 转写（兜底）
```

### 配置 Cookie

1. 浏览器登录 [bilibili.com](https://bilibili.com)
2. 安装 [EditThisCookie](https://www.editthiscookie.com/) 扩展
3. 导出 Cookie 为 Netscape 格式
4. 保存到 `/tmp/bili_cookies.txt`

### 获取字幕

```bash
# 查看可用字幕
yt-dlp --cookies /tmp/bili_cookies.txt --list-subs "URL"

# 下载官方字幕
yt-dlp --cookies /tmp/bili_cookies.txt \
  --write-sub --write-auto-sub --sub-lang zh-Hans,en \
  --skip-download -o "/tmp/bili/%(id)s" "URL"

# 下载 AI 字幕（无需 Cookie）
yt-dlp --cookies /tmp/bili_cookies.txt \
  --write-sub --write-auto-sub --sub-lang ai-zh \
  --skip-download -o "/tmp/bili/%(id)s" "URL"
```

### Cookie 过期处理

Cookie 通常有效期较短，需要定期更新：

```bash
# 重新导出 Cookie 后更新文件
cp ~/Downloads/cookies.txt /tmp/bili_cookies.txt
```

---

## 小红书

### 特点
- ✅ **图文完整**：可获取笔记正文+图片+评论
- ✅ **无需登录**
- ⚠️ **速度较慢**：需要浏览器渲染
- ⚠️ **视频有限**：部分视频直链可能获取失败

### 工作流程

```
发送链接 → browser 打开 → JS 滚动触发懒加载
  → JS 提取内容 → 下载图片 → MiniMax OCR → 汇总
```

### 内容获取

通过 AI 助手发送小红书链接，自动完成全部流程：

1. 打开页面
2. 滚动加载
3. 提取正文+图片
4. 图片 OCR（可选）
5. 汇总输出

### 限制

- 图片为 webp 压缩格式，无法获取原图
- 视频直链从 `imageList[i].stream.h264[0].masterUrl` 获取
- MiniMax API 用于图片文字识别

---

## 性能对比

| 平台 | 有字幕/内容获取 | Whisper 兜底 | 总体速度 |
|------|----------------|---------------|----------|
| YouTube | ~10秒 | ~3分钟 | ⭐⭐⭐⭐⭐ |
| 抖音 | ~1分钟 | ~4分钟 | ⭐⭐⭐⭐ |
| B站 | ~10秒 | ~3分钟 | ⭐⭐⭐⭐ |
| 小红书 | ~2分钟 | N/A | ⭐⭐⭐ |

---

## 推荐使用场景

| 场景 | 推荐平台 | 原因 |
|------|----------|------|
| 快速获取 | YouTube | 字幕直接下，无需等待 |
| 中文视频 | 抖音/B站 | 字幕/语音识别更准 |
| 图文内容 | 小红书 | 支持图文+图片 |
| 最佳效果 | YouTube/抖音 | Whisper 转写质量高 |
