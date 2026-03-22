# 安装指南

## 系统要求

- **操作系统**：macOS 12+ / Ubuntu 20.04+ / Windows 10+
- **Python**：3.9 或更高版本
- **内存**：推荐 8GB+（Whisper 模型加载需要）

## 安装步骤

### 1. 安装 Python 依赖

```bash
# 克隆或下载本项目后
cd content-reader
pip install -r requirements.txt
```

### 2. 安装系统工具

#### macOS

```bash
# 使用 Homebrew
brew install ffmpeg
brew install yt-dlp
```

#### Ubuntu/Debian

```bash
sudo apt update
sudo apt install ffmpeg
pip install yt-dlp
```

#### Windows

```powershell
# 使用 winget
winget install ffmpeg
winget install yt-dlp
```

### 3. 验证安装

```bash
# 检查各工具是否安装成功
ffmpeg -version | head -1
yt-dlp --version
python -c "import whisper; print('Whisper OK')"
python -c "import requests; print('Requests OK')"
```

### 4. 下载 Whisper 模型（首次使用自动下载）

```bash
# base 模型（约140MB），平衡速度与精度
python -c "import whisper; whisper.load_model('base')"

# 如需更高精度，使用 small 模型（约450MB）
python -c "import whisper; whisper.load_model('small')"
```

## 可选配置

### B站 Cookie（获取官方字幕）

如需获取 B站 官方字幕，需要配置 Cookie：

1. 浏览器登录 [bilibili.com](https://bilibili.com)
2. 安装浏览器扩展 [EditThisCookie](https://www.editthiscookie.com/)
3. 导出 Cookie 为 Netscape 格式
4. 保存到 `/tmp/bili_cookies.txt`

### MiniMax API（如需小红书图片OCR）

```bash
# 安装 mcporter
npm install -g mcporter

# 配置 MiniMax API Key（用于图片文字识别）
# 在 OpenClaw 配置中设置 MINIMAX_API_KEY
```

## 目录结构

```
content-reader/
├── SKILL.md              # 主技能文档
├── README.md             # 项目说明
├── requirements.txt       # Python 依赖
├── scripts/
│   └── douyin_whisper.py # 抖音脚本
└── docs/
    ├── install.md         # 本文件
    ├── quickstart.md      # 快速入门
    ├── platforms.md       # 平台详细说明
    └── troubleshooting.md # 故障排除
```

## 依赖版本

| 依赖 | 最低版本 | 推荐版本 |
|------|----------|----------|
| Python | 3.9 | 3.11 |
| ffmpeg | 4.0 | 7.x |
| yt-dlp | 2024.01 | 最新 |
| whisper | 20231117 | 最新 |

## 下一步

安装完成后，前往 [快速入门](quickstart.md) 开始使用。
