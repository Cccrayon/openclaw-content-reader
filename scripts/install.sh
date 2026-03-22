#!/bin/bash
#
# Content Reader 安装脚本
# 先检查后安装，幂等操作
#

set -e

echo "======================================"
echo "  Content Reader 安装脚本"
echo "======================================"
echo ""

# 检测操作系统
detect_os() {
    if [[ "$OSTYPE" == "darwin"* ]]; then
        echo "macOS"
    elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
        if command -v apt &> /dev/null; then
            echo "Ubuntu/Debian"
        elif command -v yum &> /dev/null; then
            echo "CentOS/RHEL"
        else
            echo "Linux"
        fi
    else
        echo "Unknown"
    fi
}

# 检查命令是否存在
check_cmd() {
    command -v "$1" &> /dev/null
}

# 检查 Python 包
check_python_pkg() {
    python3 -c "import $1" 2>/dev/null
}

# 安装 macOS 包
install_macos() {
    local pkg=$1
    if check_cmd "$pkg"; then
        echo "  ✓ $pkg 已安装"
    else
        echo "  → 安装 $pkg..."
        brew install "$pkg"
    fi
}

# 安装 Ubuntu/Debian 包
install_ubuntu() {
    local pkg=$1
    if check_cmd "$pkg"; then
        echo "  ✓ $pkg 已安装"
    else
        echo "  → 安装 $pkg..."
        sudo apt update && sudo apt install -y "$pkg"
    fi
}

# 主安装流程
main() {
    local os=$(detect_os)
    echo "检测到系统: $os"
    echo ""

    # 1. 检查/安装 Python
    echo "[1/5] 检查 Python..."
    if check_cmd python3; then
        python_version=$(python3 --version | cut -d' ' -f2)
        echo "  ✓ Python $python_version 已安装"
    else
        echo "  ✗ Python 未安装"
        echo "  请从 https://www.python.org/downloads/ 下载安装"
        exit 1
    fi

    # 2. 检查/安装 ffmpeg
    echo ""
    echo "[2/5] 检查 ffmpeg..."
    if check_cmd ffmpeg; then
        ffmpeg_version=$(ffmpeg -version 2>&1 | head -1 | cut -d' ' -f3)
        echo "  ✓ ffmpeg $ffmpeg_version 已安装"
    else
        echo "  → 安装 ffmpeg..."
        case "$os" in
            macOS)
                brew install ffmpeg
                ;;
            Ubuntu|Debian)
                install_ubuntu ffmpeg
                ;;
            *)
                echo "  不支持的系统，请手动安装 ffmpeg"
                exit 1
                ;;
        esac
    fi

    # 3. 检查/安装 yt-dlp
    echo ""
    echo "[3/5] 检查 yt-dlp..."
    if check_cmd yt-dlp; then
        yt_version=$(yt-dlp --version)
        echo "  ✓ yt-dlp $yt_version 已安装"
    else
        echo "  → 安装 yt-dlp..."
        pip3 install yt-dlp
    fi

    # 4. 检查/安装 Whisper
    echo ""
    echo "[4/5] 检查 Whisper..."
    if check_python_pkg whisper; then
        echo "  ✓ Whisper 已安装"
    else
        echo "  → 安装 Whisper（可能需要几分钟）..."
        pip3 install openai-whisper
    fi

    # 5. 安装 Python 依赖
    echo ""
    echo "[5/5] 安装其他 Python 依赖..."
    pip3 install requests ffmpeg-python browser-cookie3

    echo ""
    echo "======================================"
    echo "  ✓ 安装完成！"
    echo "======================================"
    echo ""
    echo "下一步："
    echo "  1. 运行测试: python3 scripts/douyin_whisper.py \"https://v.douyin.com/xxx/\""
    echo "  2. 查看文档: docs/quickstart.md"
    echo ""
}

# 运行
main "$@"
