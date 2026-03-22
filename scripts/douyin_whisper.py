#!/usr/bin/env python3
"""
抖音视频 → Whisper 本地转写 v2

修复了 URL 提取逻辑
"""

import os
import re
import sys
import json
import argparse
import requests
import tempfile
import subprocess
from pathlib import Path
from urllib.parse import unquote
import whisper


HEADERS = {
    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1'
}


def parse_share_url(share_text: str) -> dict:
    """从分享文本中提取无水印视频链接"""
    # 提取分享链接
    urls = re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', share_text)
    if not urls:
        raise ValueError("未找到有效的分享链接")
    
    share_url = urls[0]
    print(f"[1] 访问分享链接: {share_url[:60]}...")
    
    response = requests.get(share_url, headers=HEADERS, allow_redirects=True)
    final_url = response.url
    print(f"[2] 重定向到: {final_url[:60]}...")
    
    # 访问最终页面
    response = requests.get(final_url, headers=HEADERS)
    response.raise_for_status()
    print(f"[3] 获取页面成功，内容长度: {len(response.text)}")
    
    # 提取 playwm URL 并转换成无水印
    pattern = r'"play_addr"\s*:\s*\{\s*"uri"\s*:\s*"([^"]+)"\s*,\s*"url_list"\s*:\s*\["([^"]+)"'
    match = re.search(pattern, response.text)
    
    if not match:
        raise ValueError("无法从HTML中解析视频信息")
    
    # 解码 Unicode 转义
    url_encoded = match.group(2)
    video_url = url_encoded.replace("\\u002F", "/")
    
    # 替换 playwm -> play 获取无水印
    if "playwm" in video_url:
        video_url = video_url.replace("playwm", "play")
        print(f"[4] 获取到无水印URL (playwm -> play)")
    else:
        print(f"[4] 获取到视频URL")
    
    # 提取视频ID
    video_id = final_url.split("/")[-1].split("?")[0]
    
    # 提取描述
    desc_match = re.search(r'"desc"\s*:\s*"([^"]+)"', response.text)
    desc = desc_match.group(1) if desc_match else f"douyin_{video_id}"
    desc = re.sub(r'[\\/:*?"<>|]', '_', desc)[:100]
    
    print(f"    视频ID: {video_id}")
    print(f"    标题: {desc[:50]}...")
    
    return {
        "url": video_url,
        "title": desc,
        "video_id": video_id
    }


def download_video(url: str, output_path: Path) -> Path:
    """下载视频"""
    print(f"[5] 开始下载视频...")
    
    response = requests.get(url, headers=HEADERS, stream=True, allow_redirects=True)
    response.raise_for_status()
    
    with open(output_path, 'wb') as f:
        for chunk in response.iter_content(chunk_size=8192):
            if chunk:
                f.write(chunk)
    
    size_mb = output_path.stat().st_size / 1024 / 1024
    print(f"[6] 下载完成，大小: {size_mb:.2f} MB")
    return output_path


def extract_audio(video_path: Path, audio_path: Path) -> Path:
    """从视频提取音频"""
    print(f"[7] 提取音频...")
    
    cmd = [
        'ffmpeg', '-i', str(video_path),
        '-vn', '-acodec', 'libmp3lame', '-ab', '128k',
        '-y', str(audio_path)
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        # 备用：直接复制
        cmd = ['ffmpeg', '-i', str(video_path), '-y', str(audio_path)]
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            raise RuntimeError(f"音频提取失败: {result.stderr[:200]}")
    
    size_mb = audio_path.stat().st_size / 1024 / 1024
    print(f"[8] 音频提取完成，大小: {size_mb:.2f} MB")
    return audio_path


def transcribe(audio_path: Path, model_name: str = "base", language: str = "zh") -> str:
    """使用Whisper转写"""
    print(f"[9] 加载 Whisper 模型: {model_name}...")
    model = whisper.load_model(model_name)
    print(f"[10] 开始转写 (语言: {language})...")
    
    result = model.transcribe(
        str(audio_path),
        language=language if language != "auto" else None,
        fp16=False
    )
    
    return result.get("text", "").strip()


def main():
    parser = argparse.ArgumentParser(description='抖音视频 → Whisper 转写')
    parser.add_argument('url', help='抖音分享链接')
    parser.add_argument('--model', '-m', default='base', 
                       choices=['tiny', 'base', 'small', 'medium', 'large'], 
                       help='Whisper模型')
    parser.add_argument('--language', '-l', default='zh', help='语言代码')
    parser.add_argument('--output', '-o', help='输出文件路径')
    parser.add_argument('--keep', '-k', action='store_true', help='保留中间文件')
    
    args = parser.parse_args()
    
    with tempfile.TemporaryDirectory() as tmpdir:
        tmppath = Path(tmpdir)
        video_path = tmppath / "video.mp4"
        audio_path = tmppath / "audio.mp3"
        
        # 1. 解析URL
        video_info = parse_share_url(args.url)
        
        # 2. 下载视频
        download_video(video_info['url'], video_path)
        
        # 3. 提取音频
        extract_audio(video_path, audio_path)
        
        # 4. 转写
        text = transcribe(audio_path, args.model, args.language)
        
        print(f"\n========== 转写结果 ==========\n")
        print(text)
        print(f"\n========== 结束 ==========")
        
        # 5. 保存结果
        if args.output:
            output_path = Path(args.output)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(text)
            print(f"\n已保存到: {args.output}")
        
        # 6. 保留中间文件
        if args.keep:
            out_dir = Path(args.output).parent if args.output else Path.cwd()
            import shutil
            vid_out = out_dir / f"{video_info['video_id']}_video.mp4"
            aud_out = out_dir / f"{video_info['video_id']}_audio.mp3"
            shutil.copy(video_path, vid_out)
            shutil.copy(audio_path, aud_out)
            print(f"中间文件已保存: {vid_out}, {aud_out}")


if __name__ == "__main__":
    main()
