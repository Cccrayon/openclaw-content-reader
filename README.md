# Content Reader

> 读取小红书、B站、YouTube、抖音链接内容，自动转录/总结

## 功能支持

| 平台 | 内容获取 | ASR转写 | 需要登录 |
|------|----------|---------|----------|
| YouTube | ✅ 字幕直接下载 | ✅ Whisper | ❌ |
| 抖音 | ✅ 直链获取 | ✅ Whisper | ❌ |
| B站 | ✅ 字幕下载 | ✅ Whisper | ✅ Cookie |
| 小红书 | ✅ 图文+图片 | ⚠️ 图片OCR | ❌ |

## 快速安装

### 一键安装（推荐）

```bash
# 克隆仓库
git clone https://github.com/Cccrayon/openclaw-content-reader.git
cd openclaw-content-reader

# 运行安装脚本（自动检查并安装依赖）
bash scripts/install.sh
```

### 手动安装

```bash
# 1. 安装 Python 依赖
pip install -r requirements.txt

# 2. 安装系统工具
brew install ffmpeg        # macOS
# 或
apt install ffmpeg         # Ubuntu

# 3. 下载 Whisper 模型（首次使用自动下载）
python -c "import whisper; whisper.load_model('base')"
```

详细安装说明：[docs/install.md](docs/install.md)

## 快速开始

### YouTube
```bash
yt-dlp --write-sub --write-auto-sub --sub-lang en \
  --skip-download -o "/tmp/yt/%(id)s" "URL"
```

### 抖音
```bash
python3 scripts/douyin_whisper.py "https://v.douyin.com/xxx/"
```

### B站
```bash
# 需要先配置 Cookie（见文档）
yt-dlp --cookies /tmp/bili_cookies.txt --list-subs "URL"
```

详细用法：[docs/quickstart.md](docs/quickstart.md)

## 文档目录

```
docs/
├── install.md        # 完整安装指南
├── quickstart.md     # 快速入门
├── platforms.md      # 各平台详细说明
├── troubleshooting.md # 常见问题
└── changelog.md      # 更新日志

examples/
└── sample-output.md # 输出示例
```

## 平台速查

| 平台 | 难度 | 速度 | 推荐度 |
|------|------|------|--------|
| YouTube | ⭐ | 快 | ⭐⭐⭐⭐⭐ |
| 抖音 | ⭐⭐ | 中 | ⭐⭐⭐⭐ |
| B站 | ⭐⭐⭐ | 快 | ⭐⭐⭐ |
| 小红书 | ⭐⭐ | 慢 | ⭐⭐⭐ |

## 输出规范

- **中文内容** → 直接输出
- **英文/其他语言** → 翻译为中文输出
- **输出内容**：标题/作者/核心内容/关键观点

## 故障排除

常见问题：[docs/troubleshooting.md](docs/troubleshooting.md)

## 开源协议

MIT License

## 更新日志

见 [docs/changelog.md](docs/changelog.md)
