# Content Reader

> 读取小红书、B站、YouTube、抖音链接内容，自动转录/总结

## 设计理念

**让用户先用起来，碰到墙了再给梯子。**

- 不提前要求配置
- 默认使用无需登录的方案
- 用到时再提示可选项

## 平台支持

| 平台 | 内容获取 | ASR | 需要登录 |
|------|----------|-----|----------|
| YouTube | ✅ 字幕下载 | ✅ Whisper | ❌ |
| 抖音 | ✅ 直链获取 | ✅ Whisper | ❌ |
| B站 | ✅ AI字幕/官方字幕 | ✅ Whisper | ⚠️ 可选 |
| 小红书 | ✅ 图文+图片 | ⚠️ OCR | ❌ |

## 快速开始

### 一键安装

```bash
git clone https://github.com/Cccrayon/openclaw-content-reader.git
cd openclaw-content-reader
bash scripts/install.sh
```

### 立即使用

发送链接给 AI 助手，自动完成内容获取。

### 测试

```bash
# 测试抖音
python3 scripts/douyin_whisper.py "https://v.douyin.com/ih8cJfV/"

# 测试 YouTube
yt-dlp --write-sub --write-auto-sub --sub-lang en \
  --skip-download -o "/tmp/yt/test" "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
```

## 文档

```
docs/
├── install.md         # 安装指南
├── quickstart.md     # 快速入门
├── platforms.md      # 各平台详细说明（含可选配置说明）
└── troubleshooting.md # 常见问题
```

## 输出规范

- **中文内容** → 直接输出
- **英文/其他语言** → 翻译为中文输出
- **输出内容**：标题/作者/核心内容/关键观点

## 可选配置（按需）

| 配置 | 什么时候需要 | 是否必需 |
|------|-------------|----------|
| B站 Cookie | AI字幕不够好时 | ❌ |
| MiniMax API | 小红书图片OCR | ❌ |

**默认方案无需任何配置，直接可用。**

## 开源协议

MIT License
