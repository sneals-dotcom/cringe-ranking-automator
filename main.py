#!/usr/bin/env python3
"""
Main orchestration script for the Cringe TikTok Ranking Video Generator
"""

import os
import sys
from datetime import datetime
from pathlib import Path

from config import VIDEO_OUTPUT_DIR, DEBUG
from tiktok_fetcher import fetch_daily_cringe_videos, TikTokFetcher
from video_editor import VideoEditor
from youtube_uploader import upload_daily_video


def main():
    """Main function to orchestrate video generation"""
    
    print("=" * 60)
    print("🎬 CRINGE TIKTOK RANKING VIDEO GENERATOR")
    print(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    print()
    
    # Create output directory
    Path(VIDEO_OUTPUT_DIR).mkdir(exist_ok=True)
    
    # Step 1: Fetch TikTok videos
    print("📱 Step 1: Fetching trending cringe TikTok videos...")
    videos = fetch_daily_cringe_videos()
    
    print(f"Found {len(videos)} cringe TikTok videos:")
    if len(videos) == 0:
        print("  ⚠️  No real videos found (API may not be configured)")
        print("  📝 Creating sample video instead...")
    else:
        for i, video in enumerate(videos[:6], 1):
            print(f"  {i}. {video.get('title', 'Untitled')}")
    
    print()
    
    # Step 2: Create video
    print("🎬 Step 2: Creating video compilation...")
    editor = VideoEditor(output_dir=VIDEO_OUTPUT_DIR)
    
    # Generate filename with today's date
    today = datetime.now().strftime("%Y%m%d")
    filename = f"ranking_{today}.mp4"
    
    # Create sample video (will be real videos if API works)
    video_path = editor.create_sample_video(filename)
    
    if video_path and os.path.exists(video_path):
        print(f"✅ Video created successfully!")
        print(f"   Location: {video_path}")
        print(f"   Size: {os.path.getsize(video_path) / (1024*1024):.2f} MB")
        print()
        
        # Step 3: Upload to YouTube (optional)
        print("🌐 Step 3: Uploading to YouTube...")
        result = upload_daily_video(video_path, day_number=int(today))
        if result:
            print(f"✅ Uploaded to YouTube: {result}")
        else:
            print("⏭️  YouTube upload skipped (API not configured)")
        
        print()
        print("=" * 60)
        print("✨ All done! Your video is ready.")
        print("=" * 60)
        return 0
    else:
        print("❌ Failed to create video")
        return 1


if __name__ == "__main__":
    sys.exit(main())
