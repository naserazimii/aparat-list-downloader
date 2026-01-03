#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import yt_dlp
import os
import sys
import re
import time
import json
import requests
from datetime import datetime
from urllib.parse import urljoin, urlparse, parse_qs
from bs4 import BeautifulSoup

# For loading JavaScript pages
try:
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.chrome.options import Options
    from selenium.common.exceptions import TimeoutException, WebDriverException
    SELENIUM_AVAILABLE = True
except ImportError:
    SELENIUM_AVAILABLE = False

def clear_screen():
    """Clear terminal screen"""
    os.system('cls' if os.name == 'nt' else 'clear')

def display_banner():
    """Display program banner"""
    banner = """
╔══════════════════════════════════════════════════════════════════════════╗
║    Advanced Aparat Playlist Downloader - Quality Selector Per Video      ║
║    Page Loading + Link Extraction + Quality Selection + Download         ║
╚══════════════════════════════════════════════════════════════════════════╝
    """
    print(banner)

def setup_selenium_driver():
    """Setup Selenium WebDriver"""
    if not SELENIUM_AVAILABLE:
        print("❌ Selenium is not installed!")
        print("\nTo install Selenium:")
        print("pip install selenium webdriver-manager")
        return None
    
    try:
        from selenium.webdriver.chrome.service import Service
        from webdriver_manager.chrome import ChromeDriverManager
        
        # Chrome settings
        chrome_options = Options()
        chrome_options.add_argument('--headless')  # No window display
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--window-size=1920,1080')
        chrome_options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')
        
        # Auto-install ChromeDriver
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        
        return driver
    except Exception as e:
        print(f"❌ Error setting up WebDriver: {e}")
        return None

def extract_video_links_from_page(playlist_url):
    """
    Load playlist page and extract video links
    """
    print(f"\n🔍 Loading playlist page: {playlist_url}")
    
    video_links = []
    
    # Method 1: Use Selenium for full page load
    driver = setup_selenium_driver()
    
    if driver:
        print("🌐 Loading page with virtual browser...")
        try:
            driver.get(playlist_url)
            
            # Wait for page to load
            time.sleep(5)
            
            # Scroll to load all content
            last_height = driver.execute_script("return document.body.scrollHeight")
            for i in range(3):  # Scroll 3 times
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(2)
                new_height = driver.execute_script("return document.body.scrollHeight")
                if new_height == last_height:
                    break
                last_height = new_height
            
            # Get complete HTML code
            page_html = driver.page_source
            
            # Close browser
            driver.quit()
            
            # Parse HTML with BeautifulSoup
            return extract_links_from_html(page_html, playlist_url)
            
        except Exception as e:
            print(f"❌ Error loading page with Selenium: {e}")
            if driver:
                driver.quit()
    
    # Method 2: Use requests and BeautifulSoup (for simpler pages)
    print("🔄 Using alternative method (requests)...")
    return extract_with_requests(playlist_url)

def extract_links_from_html(html_content, base_url):
    """
    Extract video links from HTML
    """
    print("🔎 Searching for video links in HTML...")
    
    soup = BeautifulSoup(html_content, 'html.parser')
    video_links = []
    
    # Search in all <a> tags
    for link in soup.find_all('a', href=True):
        href = link['href']
        
        # Convert relative links to absolute
        if href.startswith('/'):
            href = urljoin(base_url, href)
        
        # Check if link is a video
        if '/v/' in href and 'aparat.com' in href:
            # Clean the link
            href = href.split('?')[0]  # Remove query parameters
            video_links.append(href)
    
    # Search in iframe src attributes
    for iframe in soup.find_all('iframe', src=True):
        src = iframe['src']
        if 'aparat.com' in src and '/v/' in src:
            if src.startswith('/'):
                src = urljoin(base_url, src)
            src = src.split('?')[0]
            video_links.append(src)
    
    # Search in scripts
    for script in soup.find_all('script'):
        if script.string:
            script_text = script.string
            # Find video IDs
            video_ids = re.findall(r'/v/([a-zA-Z0-9_\-]+)', script_text)
            for video_id in video_ids:
                video_link = f"https://www.aparat.com/v/{video_id}"
                video_links.append(video_link)
    
    # Remove duplicate links
    unique_links = []
    seen = set()
    for link in video_links:
        if link not in seen:
            unique_links.append(link)
            seen.add(link)
    
    print(f"✅ Links found: {len(unique_links)}")
    
    # Display sample links
    if unique_links:
        print("\n📝 Sample links found:")
        for i, link in enumerate(unique_links[:5], 1):
            print(f"   {i}. {link}")
        if len(unique_links) > 5:
            print(f"   ... and {len(unique_links) - 5} more links")
    
    return unique_links

def extract_with_requests(playlist_url):
    """
    Extract with requests (without JavaScript)
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
    }
    
    try:
        response = requests.get(playlist_url, headers=headers, timeout=30)
        response.raise_for_status()
        
        # Extract links
        return extract_links_from_html(response.text, playlist_url)
        
    except Exception as e:
        print(f"❌ Error loading page: {e}")
        return []

def get_video_info_with_selenium(video_url):
    """
    Get video information using Selenium (for pages that need JavaScript)
    """
    driver = setup_selenium_driver()
    if not driver:
        return None
    
    try:
        print(f"🌐 Loading video page: {video_url}")
        driver.get(video_url)
        
        # Wait for video to load
        time.sleep(5)
        
        # Try to get page source
        page_html = driver.page_source
        
        # Try to find video information in the page
        soup = BeautifulSoup(page_html, 'html.parser')
        
        # Try to extract video title
        title = "Unknown Title"
        title_elem = soup.find('h1') or soup.find('title')
        if title_elem:
            title = title_elem.text.strip()
        
        driver.quit()
        
        return {
            'title': title[:100],  # Limit title length
            'webpage_url': video_url
        }
        
    except Exception as e:
        print(f"❌ Error loading video page with Selenium: {e}")
        if driver:
            driver.quit()
        return None

def get_video_formats(video_url):
    """
    Get available formats for a video using yt-dlp
    """
    print(f"\n🔍 Getting available formats for video...")
    
    formats_info = {
        'title': 'Unknown Title',
        'formats': [],
        'best_format': None,
        'webpage_url': video_url
    }
    
    try:
        # First try to get info with yt-dlp
        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
            'extract_flat': False,
            'force_generic_extractor': True,
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=False)
            
            if info:
                formats_info['title'] = info.get('title', 'Unknown Title')
                formats_info['webpage_url'] = info.get('webpage_url', video_url)
                
                # Extract available formats
                if 'formats' in info:
                    formats = info['formats']
                    
                    # Filter and organize formats
                    video_formats = []
                    for f in formats:
                        format_id = f.get('format_id', 'N/A')
                        ext = f.get('ext', 'unknown')
                        filesize = f.get('filesize')
                        filesize_mb = filesize / (1024 * 1024) if filesize else 0
                        
                        # Try to get resolution
                        height = f.get('height', 0) or 0
                        width = f.get('width', 0) or 0
                        
                        # Determine quality name
                        if height >= 2160:
                            quality = "4K"
                        elif height >= 1440:
                            quality = "1440p"
                        elif height >= 1080:
                            quality = "1080p"
                        elif height >= 720:
                            quality = "720p"
                        elif height >= 480:
                            quality = "480p"
                        elif height >= 360:
                            quality = "360p"
                        elif height >= 240:
                            quality = "240p"
                        elif height >= 144:
                            quality = "144p"
                        else:
                            quality = f"{height}p" if height > 0 else "Unknown"
                        
                        # Get fps safely
                        fps_val = f.get('fps')
                        fps = fps_val if fps_val and fps_val > 0 else 0
                        
                        # Only include video formats
                        if f.get('vcodec') != 'none':
                            format_info = {
                                'format_id': format_id,
                                'ext': ext,
                                'quality': quality,
                                'height': height,
                                'width': width,
                                'filesize_mb': round(filesize_mb, 2) if filesize_mb > 0 else "Unknown",
                                'format_note': f.get('format_note', ''),
                                'url': f.get('url', ''),
                                'fps': fps
                            }
                            video_formats.append(format_info)
                    
                    # Sort by height (quality) descending
                    video_formats.sort(key=lambda x: x['height'], reverse=True)
                    
                    formats_info['formats'] = video_formats
                    
                    # Find best format
                    if video_formats:
                        formats_info['best_format'] = video_formats[0]
    
    except Exception as e:
        print(f"⚠️ Could not get formats with yt-dlp: {e}")
        
        # Try alternative method with Selenium
        video_info = get_video_info_with_selenium(video_url)
        if video_info:
            formats_info['title'] = video_info['title']
    
    return formats_info

def display_and_select_format(formats_info, video_number, total_videos):
    """
    Display available formats and let user select one
    """
    title = formats_info['title']
    formats = formats_info['formats']
    
    print(f"\n{'='*60}")
    print(f"📹 Video {video_number}/{total_videos}: {title}")
    print(f"🔗 URL: {formats_info['webpage_url']}")
    print(f"{'='*60}")
    
    if not formats:
        print("❌ No video formats found!")
        print("Possible reasons:")
        print("1. Video is private or requires login")
        print("2. Video is not available in your region")
        print("3. Website structure has changed")
        
        # Offer to skip or try alternative
        choice = input("\n❓ What would you like to do? (s=skip, t=try alternative, q=quit): ").strip().lower()
        
        if choice == 's':
            return None
        elif choice == 't':
            # Try with Selenium to get at least basic info
            print("🔄 Trying alternative method...")
            return get_video_info_with_selenium(formats_info['webpage_url'])
        else:
            return None
    
    # Display available formats
    print(f"\n📊 Available formats ({len(formats)} options):")
    print("-" * 80)
    print(f"{'No.':<4} {'Quality':<10} {'Resolution':<12} {'Format':<8} {'Size':<10} {'FPS':<6} {'ID':<10}")
    print("-" * 80)
    
    for i, fmt in enumerate(formats, 1):
        quality = fmt['quality']
        
        # Handle resolution display safely
        width = fmt['width'] or 0
        height = fmt['height'] or 0
        resolution = f"{width}x{height}" if width and height else "N/A"
        
        file_ext = fmt['ext']
        
        # Handle size display
        size_val = fmt['filesize_mb']
        if isinstance(size_val, (int, float)):
            size = f"{size_val:.1f} MB"
        else:
            size = str(size_val)
        
        # Handle FPS display safely
        fps_val = fmt['fps']
        if fps_val and fps_val > 0:
            fps = str(fps_val)
        else:
            fps = "N/A"
        
        format_id = fmt['format_id'][:15]  # Limit length
        
        print(f"{i:<4} {quality:<10} {resolution:<12} {file_ext:<8} {size:<10} {fps:<6} {format_id:<10}")
    
    print("-" * 80)
    
    # Get user selection
    while True:
        try:
            choice = input(f"\nSelect format (1-{len(formats)}, b=best, s=skip, i=info, q=quit): ").strip().lower()
            
            if choice == 'b':
                # Select best quality (first in list)
                selected_format = formats[0]
                print(f"✓ Selected: Best quality ({selected_format['quality']})")
                return selected_format
            
            elif choice == 's':
                print("⏭️ Skipping this video")
                return None
            
            elif choice == 'q':
                print("👋 Exiting program")
                sys.exit(0)
            
            elif choice == 'i':
                # Show more info about formats
                print("\n📋 Detailed format information:")
                for i, fmt in enumerate(formats, 1):
                    print(f"\n{i}. {fmt['quality']} - ID: {fmt['format_id']}")
                    print(f"   Resolution: {fmt['width']}x{fmt['height']}")
                    print(f"   Format: {fmt['ext']}")
                    print(f"   Size: {fmt['filesize_mb']}")
                    if fmt['format_note']:
                        print(f"   Note: {fmt['format_note']}")
                continue
            
            else:
                # Try to parse as number
                choice_num = int(choice)
                if 1 <= choice_num <= len(formats):
                    selected_format = formats[choice_num - 1]
                    print(f"✓ Selected: {selected_format['quality']} (ID: {selected_format['format_id']})")
                    return selected_format
                else:
                    print(f"⚠️ Please enter a number between 1 and {len(formats)}")
        
        except ValueError:
            print("⚠️ Invalid input. Please enter a number or one of the letters (b,s,i,q)")

def get_download_path():
    """Get download location from user"""
    default_path = "Aparat_Downloads"
    print(f"\n📁 Download Settings:")
    print("-" * 40)
    
    download_path = input(f"Save location (Enter for default [{default_path}]): ").strip()
    download_path = download_path if download_path else default_path
    
    # Create folder
    os.makedirs(download_path, exist_ok=True)
    
    return download_path

def download_video_with_format(video_url, selected_format, download_path, video_number, total_videos, stats):
    """
    Download a single video with selected format
    """
    try:
        # Get video info for title
        ydl_opts_info = {'quiet': True}
        with yt_dlp.YoutubeDL(ydl_opts_info) as ydl:
            video_info = ydl.extract_info(video_url, download=False)
            video_title = video_info.get('title', f'Video_{video_number}')
            video_id = video_info.get('id', str(video_number))
        
        # Clean title for filename
        safe_title = re.sub(r'[^\w\-_\. ]', '_', video_title)
        safe_title = safe_title[:100]  # Limit length
        
        # Create filename
        filename = f"{video_number:03d}_{video_id}_{safe_title}.mp4"
        filepath = os.path.join(download_path, filename)
        
        print(f"\n📥 Downloading video {video_number}/{total_videos}")
        print(f"📹 Title: {video_title}")
        print(f"🎯 Quality: {selected_format['quality']}")
        print(f"💾 Saving as: {filename}")
        
        # yt-dlp options for specific format
        ydl_opts = {
            'outtmpl': filepath,
            'format': selected_format['format_id'],
            'quiet': False,
            'no_warnings': False,
            'ignoreerrors': True,
            'nooverwrites': True,
            'retries': 3,
            'fragment_retries': 3,
            'progress_hooks': [lambda d: print_progress(d, video_number)],
        }
        
        # Download video
        start_time = time.time()
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([video_url])
        
        download_time = time.time() - start_time
        
        # Check if file was downloaded
        if os.path.exists(filepath):
            file_size = os.path.getsize(filepath) / (1024 * 1024)  # MB
            stats['downloaded'] += 1
            stats['total_size_mb'] += file_size
            
            print(f"\n✅ Download completed in {download_time:.1f} seconds")
            print(f"💾 File size: {file_size:.2f} MB")
            
            # Save download info
            with open(os.path.join(download_path, 'download_log.txt'), 'a', encoding='utf-8') as f:
                f.write(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] ")
                f.write(f"Video {video_number}: {video_title} | ")
                f.write(f"Quality: {selected_format['quality']} | ")
                f.write(f"Size: {file_size:.2f} MB | ")
                f.write(f"URL: {video_url}\n")
            
            return True
        else:
            print("❌ Download failed - File not created")
            stats['failed'] += 1
            return False
            
    except Exception as e:
        print(f"❌ Error downloading video: {str(e)[:200]}")
        stats['failed'] += 1
        
        # Save error
        with open(os.path.join(download_path, 'errors.txt'), 'a', encoding='utf-8') as f:
            f.write(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] ")
            f.write(f"Video {video_number}: {video_url}\n")
            f.write(f"Error: {str(e)}\n\n")
        
        return False

def print_progress(d, video_number):
    """Print download progress"""
    if d['status'] == 'downloading':
        percent = d.get('_percent_str', '0%').strip()
        speed = d.get('_speed_str', 'N/A')
        eta = d.get('_eta_str', 'N/A')
        
        print(f"\r🎬 Video {video_number}: {percent} | Speed: {speed} | ETA: {eta}", end='', flush=True)
    elif d['status'] == 'finished':
        print(f"\r🎬 Video {video_number}: Download completed!{' ' * 50}")

def download_playlist_with_quality_selection(video_links, download_path):
    """
    Download playlist with quality selection for each video
    """
    if not video_links:
        print("❌ No videos found to download.")
        return
    
    total_videos = len(video_links)
    
    # Statistics
    stats = {
        'total': total_videos,
        'downloaded': 0,
        'failed': 0,
        'skipped': 0,
        'total_size_mb': 0,
        'start_time': datetime.now(),
        'selected_formats': []
    }
    
    print(f"\n🎬 Starting download of {total_videos} videos...")
    print("=" * 60)
    
    # Create playlist folder with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    playlist_folder = os.path.join(download_path, f"Playlist_{timestamp}")
    os.makedirs(playlist_folder, exist_ok=True)
    
    # Process each video
    for index, video_url in enumerate(video_links, 1):
        print(f"\n\n📋 Processing video {index} of {total_videos}")
        
        # Get available formats for this video
        formats_info = get_video_formats(video_url)
        
        # Let user select format
        selected_format = display_and_select_format(formats_info, index, total_videos)
        
        if selected_format is None:
            print(f"⏭️ Skipping video {index}")
            stats['skipped'] += 1
            continue
        
        # Download video with selected format
        success = download_video_with_format(
            video_url, 
            selected_format, 
            playlist_folder, 
            index, 
            total_videos,
            stats
        )
        
        # Save selected format info
        stats['selected_formats'].append({
            'video': index,
            'url': video_url,
            'quality': selected_format['quality'],
            'format_id': selected_format['format_id']
        })
        
        # Delay between downloads
        if index < total_videos and success:
            print("\n⏳ Waiting before next video...")
            time.sleep(3)
    
    # Show summary
    show_download_summary(stats, playlist_folder)

def show_download_summary(stats, download_path):
    """Display download summary"""
    end_time = datetime.now()
    duration = end_time - stats['start_time']
    
    # Calculate time
    hours, remainder = divmod(duration.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    
    print("\n" + "=" * 60)
    print("📊 FINAL DOWNLOAD SUMMARY")
    print("=" * 60)
    print(f"• Total videos in playlist: {stats['total']}")
    print(f"• Successfully downloaded: {stats['downloaded']}")
    print(f"• Failed: {stats['failed']}")
    print(f"• Skipped: {stats['skipped']}")
    print(f"• Total file size: {stats['total_size_mb']:.2f} MB")
    print(f"• Total duration: {hours:02d}:{minutes:02d}:{seconds:02d}")
    print(f"• Save location: {download_path}")
    print("=" * 60)
    
    if stats['total'] > 0:
        success_rate = (stats['downloaded'] / stats['total']) * 100
        print(f"• Success rate: {success_rate:.1f}%")
    
    # Save summary
    summary_file = os.path.join(download_path, 'download_summary.txt')
    with open(summary_file, 'w', encoding='utf-8') as f:
        f.write("Download Summary\n")
        f.write("=" * 40 + "\n")
        f.write(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Total videos: {stats['total']}\n")
        f.write(f"Downloaded: {stats['downloaded']}\n")
        f.write(f"Failed: {stats['failed']}\n")
        f.write(f"Skipped: {stats['skipped']}\n")
        f.write(f"Total size: {stats['total_size_mb']:.2f} MB\n")
        f.write(f"Duration: {hours:02d}:{minutes:02d}:{seconds:02d}\n\n")
        
        f.write("Selected Qualities:\n")
        for fmt in stats['selected_formats']:
            f.write(f"  Video {fmt['video']}: {fmt['quality']} (ID: {fmt['format_id']})\n")
    
    print(f"\n💾 Summary saved to: {summary_file}")
    print("\n🎉 Download operation completed!")
    print(f"✅ Files saved in folder:")
    print(f"   {os.path.abspath(download_path)}")

def check_dependencies():
    """Check required dependencies"""
    dependencies = {
        'yt-dlp': False,
        'requests': False,
        'beautifulsoup4': False,
        'selenium': SELENIUM_AVAILABLE
    }
    
    print("🔍 Checking required dependencies...")
    
    try:
        import yt_dlp
        dependencies['yt-dlp'] = True
        print("   ✅ yt-dlp: Installed")
    except:
        print("   ❌ yt-dlp: Not installed")
    
    try:
        import requests
        dependencies['requests'] = True
        print("   ✅ requests: Installed")
    except:
        print("   ❌ requests: Not installed")
    
    try:
        import bs4
        dependencies['beautifulsoup4'] = True
        print("   ✅ beautifulsoup4: Installed")
    except:
        print("   ❌ beautifulsoup4: Not installed")
    
    print(f"   {'✅' if SELENIUM_AVAILABLE else '❌'} selenium: {'Installed' if SELENIUM_AVAILABLE else 'Not installed'}")
    
    # Installation suggestions
    missing = [dep for dep, installed in dependencies.items() if not installed]
    if missing:
        print(f"\n⚠️ Following dependencies are not installed:")
        for dep in missing:
            print(f"   pip install {dep}")
        
        if 'selenium' in missing:
            print("   Also for selenium you need:")
            print("   pip install webdriver-manager")
        
        install_all = input("\n❓ Install all missing dependencies? (y/n): ").strip().lower()
        if install_all == 'y':
            for dep in missing:
                print(f"📦 Installing {dep}...")
                os.system(f"pip install {dep}")
            
            # Install webdriver-manager if selenium was installed
            if 'selenium' in missing:
                os.system("pip install webdriver-manager")
            
            print("\n✅ Dependencies installed. Please run the script again.")
            sys.exit(0)
    
    return all(dependencies.values())

def main():
    """Main function"""
    clear_screen()
    display_banner()
    
    # Check dependencies
    if not check_dependencies():
        print("\n❌ Some dependencies are not installed.")
        print("Please install the required dependencies.")
        sys.exit(1)
    
    # Get playlist URL
    print("\n" + "-" * 50)
    
    example_url = "https://www.aparat.com/playlist/9583120/"
    print(f"📝 Example playlist URL: {example_url}")
    
    while True:
        playlist_url = input("\n🔗 Enter Aparat playlist URL: ").strip()
        
        if not playlist_url:
            print("❌ Please enter a URL.")
            continue
        
        # Validate URL
        if 'aparat.com' not in playlist_url:
            print("⚠️ The entered URL is not from Aparat.")
            print("   URL must contain 'aparat.com'")
            continue
        
        break
    
    # Extract links from playlist page
    print("\n" + "=" * 60)
    print("🌐 Loading playlist page...")
    
    video_links = extract_video_links_from_page(playlist_url)
    
    if not video_links:
        print("\n❌ No video links found on the page.")
        print("   Possible reasons:")
        print("   1. Playlist is private")
        print("   2. Login required")
        print("   3. Page structure changed")
        print("   4. Page loads with JavaScript and requires Selenium")
        sys.exit(1)
    
    # Display information
    print(f"\n📋 Playlist Information:")
    print(f"   Links found: {len(video_links)}")
    
    # Save link list
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    links_file = f"video_links_{timestamp}.txt"
    
    with open(links_file, 'w', encoding='utf-8') as f:
        f.write(f"Playlist: {playlist_url}\n")
        f.write(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Total links: {len(video_links)}\n\n")
        
        for i, link in enumerate(video_links, 1):
            f.write(f"{i}. {link}\n")
    
    print(f"💾 Link list saved to '{links_file}'")
    
    # Get download path
    download_path = get_download_path()
    
    # Final confirmation
    print(f"\n⚠️ Final confirmation:")
    print(f"   Total videos: {len(video_links)}")
    print(f"   Save location: {download_path}")
    print(f"\n📝 Note: You will be asked to select quality for EACH video individually.")
    
    confirm = input("\n❓ Start download? (y/n): ").strip().lower()
    
    if confirm not in ['y', 'yes']:
        print("❌ Operation cancelled.")
        sys.exit(0)
    
    # Start download with quality selection
    download_playlist_with_quality_selection(video_links, download_path)

if __name__ == "__main__":
    main()