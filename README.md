# aparat-list-downloader
# راهنمای برنامه دانلود پلی‌لیست Aparat

## 📖 English Guide

### Overview
An advanced Aparat playlist downloader with per-video quality selection. This tool allows you to download entire playlists from Aparat.com with custom quality settings for each video.

### Features
- ✅ **Automatic playlist link extraction** (supports JavaScript pages)
- ✅ **Per-video quality selection** (choose different quality for each video)
- ✅ **Multiple download methods** (yt-dlp + Selenium fallback)
- ✅ **Resume capability** and error handling
- ✅ **Detailed statistics** and download logs
- ✅ **User-friendly interface** with progress display

### Installation

#### Method 1: Quick Install
```bash
# Clone the repository or download the script
git clone <repository-url>
cd <repository-folder>

# Install required dependencies
pip install -r requirements.txt
```

#### Method 2: Manual Installation
```bash
# Install core dependencies
pip install yt-dlp requests beautifulsoup4

# Optional: For JavaScript pages
pip install selenium webdriver-manager
```

### Requirements
- Python 3.7 or higher
- Required packages:
  - `yt-dlp`
  - `requests`
  - `beautifulsoup4`
  - `selenium` (optional, for JavaScript pages)
  - `webdriver-manager` (optional, for ChromeDriver auto-install)

### Usage

#### Step 1: Run the program
```bash
python aparat_downloader.py
```

#### Step 2: Enter playlist URL
```
Enter Aparat playlist URL: https://www.aparat.com/playlist/9583120/
```

#### Step 3: Select download location
```
Save location (Enter for default [Aparat_Downloads]):
```

#### Step 4: Quality selection per video
For each video, you'll see:
```
1. Select format (1-5, b=best, s=skip, i=info, q=quit):
```

Options:
- **Number (1-5)**: Select specific quality
- **b**: Best quality available
- **s**: Skip this video
- **i**: Show detailed format information
- **q**: Quit program

### Output Structure
```
Aparat_Downloads/
├── Playlist_20240115_143022/
│   ├── 001_video_id_Title1.mp4
│   ├── 002_video_id_Title2.mp4
│   ├── download_log.txt
│   ├── download_summary.txt
│   └── errors.txt
└── video_links_20240115_142955.txt
```

### Quality Options
The program detects available qualities:
- 4K (2160p)
- 1440p
- 1080p
- 720p
- 480p
- 360p
- 240p
- 144p

### Troubleshooting

#### Issue: "No video links found"
**Solutions:**
1. Ensure the playlist is public
2. Try with Selenium installed:
   ```bash
   pip install selenium webdriver-manager
   ```
3. Check if the URL is correct

#### Issue: "No video formats found"
**Solutions:**
1. Video might be private/restricted
2. Try alternative method (press 't' when prompted)
3. Check internet connection

#### Issue: Slow download
**Solutions:**
1. Select lower quality
2. Check your internet speed
3. The server might be slow

### Common Commands
```bash
# Check dependencies
python aparat_downloader.py --check

# Run with specific Python
python3 aparat_downloader.py

# Create log file
python aparat_downloader.py 2>&1 | tee download.log
```

### Notes
- Program creates a new folder for each download session
- Download logs are saved for future reference
- Supports resume if interrupted
- Auto-creates necessary directories

## 📖 راهنمای فارسی

### معرفی برنامه
یک دانلودر پیشرفته پلی‌لیست Aparat با قابلیت انتخاب کیفیت جداگانه برای هر ویدیو. این ابزار به شما امکان می‌دهد کل پلی‌لیست‌های Aparat.com را با کیفیت دلخواه برای هر ویدیو دانلود کنید.

### ویژگی‌ها
- ✅ **استخراج خودکار لینک‌های پلی‌لیست** (پشتیبانی از صفحات JavaScript)
- ✅ **انتخاب کیفیت جداگانه برای هر ویدیو**
- ✅ **روش‌های دانلود متعدد** (yt-dlp + Selenium پشتیبان)
- ✅ **قابلیت ادامه دانلود** و مدیریت خطاها
- ✅ **آمار دقیق** و لاگ دانلود
- ✅ **رابط کاربری ساده** با نمایش پیشرفت

### نصب برنامه

#### روش ۱: نصب سریع
```bash
# دانلود سورس کد
git clone <آدرس-مخزن>
cd <پوشه-برنامه>

# نصب پیش‌نیازها
pip install -r requirements.txt
```

#### روش ۲: نصب دستی
```bash
# نصب پیش‌نیازهای اصلی
pip install yt-dlp requests beautifulsoup4

# اختیاری: برای صفحات JavaScript
pip install selenium webdriver-manager
```

### پیش‌نیازها
- پایتون ۳.۷ یا بالاتر
- پکیج‌های مورد نیاز:
  - `yt-dlp`
  - `requests`
  - `beautifulsoup4`
  - `selenium` (اختیاری، برای صفحات JavaScript)
  - `webdriver-manager` (اختیاری، برای نصب خودکار ChromeDriver)

### نحوه استفاده

#### مرحله ۱: اجرای برنامه
```bash
python aparat_downloader.py
```

#### مرحله ۲: وارد کردن آدرس پلی‌لیست
```
آدرس پلی‌لیست Aparat را وارد کنید: https://www.aparat.com/playlist/9583120/
```

#### مرحله ۳: انتخاب محل ذخیره‌سازی
```
محل ذخیره‌سازی (Enter برای پیش‌فرض [Aparat_Downloads]):
```

#### مرحله ۴: انتخاب کیفیت برای هر ویدیو
برای هر ویدیو مشاهده می‌کنید:
```
۱. فرمت را انتخاب کنید (۱-۵, b=بهترین, s=رد کردن, i=اطلاعات, q=خروج):
```

گزینه‌ها:
- **عدد (۱-۵)**: انتخاب کیفیت خاص
- **b**: بهترین کیفیت موجود
- **s**: رد کردن این ویدیو
- **i**: نمایش اطلاعات دقیق فرمت
- **q**: خروج از برنامه

### ساختار خروجی
```
Aparat_Downloads/
├── Playlist_20240115_143022/
│   ├── ۰۰۱_شناسه_ویدیو_عنوان۱.mp4
│   ├── ۰۰۲_شناسه_ویدیو_عنوان۲.mp4
│   ├── download_log.txt
│   ├── download_summary.txt
│   └── errors.txt
└── video_links_20240115_142955.txt
```

### کیفیت‌های موجود
برنامه کیفیت‌های موجود را تشخیص می‌دهد:
- 4K (2160p)
- 1440p
- 1080p
- 720p
- 480p
- 360p
- 240p
- 144p

### عیب‌یابی

#### مشکل: "هیچ لینک ویدیویی یافت نشد"
**راه‌حل‌ها:**
۱. مطمئن شوید پلی‌لیست عمومی است
۲. با Selenium امتحان کنید:
   ```bash
   pip install selenium webdriver-manager
   ```
۳. صحت آدرس URL را بررسی کنید

#### مشکل: "هیچ فرمت ویدیویی یافت نشد"
**راه‌حل‌ها:**
۱. ویدیو ممکن است خصوصی/محدود باشد
۲. روش جایگزین را امتحان کنید (با فشار دادن 't')
۳. اتصال اینترنت را بررسی کنید

#### مشکل: سرعت دانلود کم
**راه‌حل‌ها:**
۱. کیفیت پایین‌تر انتخاب کنید
۲. سرعت اینترنت را بررسی کنید
۳. ممکن است سرور کند باشد

### دستورات پرکاربرد
```bash
# بررسی پیش‌نیازها
python aparat_downloader.py --check

# اجرا با پایتون خاص
python3 aparat_downloader.py

# ایجاد فایل لاگ
python aparat_downloader.py 2>&1 | tee download.log
```

### نکات مهم
- برنامه برای هر جلسه دانلود یک پوشه جدید ایجاد می‌کند
- لاگ‌های دانلود برای مراجعات بعدی ذخیره می‌شوند
- از دانلود مجدد پس از قطعی پشتیبانی می‌کند
- پوشه‌های لازم را به صورت خودکار ایجاد می‌کند

### مثال آدرس پلی‌لیست
```
https://www.aparat.com/playlist/9583120/
https://www.aparat.com/playlist?list_id=12345
https://www.aparat.com/videos?playlist=67890
```

### نکات امنیتی
- برنامه فقط از سایت Aparat.com دانلود می‌کند
- هیچ اطلاعات شخصی ذخیره نمی‌شود
- از User-Agent معتبر استفاده می‌کند
- دانلود ویدیوهای خصوصی نیاز به لاگین دارد

### پشتیبانی
برای گزارش مشکل یا پیشنهاد:
۱. بررسی کنید آخرین نسخه را دارید
۲. خطاهای فایل `errors.txt` را بررسی کنید
۳. لاگ برنامه را ذخیره و ارسال کنید

## ⚡ راهنمای سریع شروع

### مرحله به مرحله:
۱. **نصب پایتون** (از python.org)
۲. **دانلود فایل برنامه**
۳. **باز کردن ترمینال/CMD** در محل فایل
۴. **نصب پیش‌نیازها:**
   ```bash
   pip install yt-dlp requests beautifulsoup4
   ```
۵. **اجرای برنامه:**
   ```bash
   python aparat_downloader.py
   ```
۶. **وارد کردن آدرس پلی‌لیست**
۷. **انتخاب کیفیت برای هر ویدیو**
۸. **انتظار برای پایان دانلود**

### مثال عملی:
```bash
# ورود به پوشه برنامه
cd Downloads/aparat-downloader

# نصب بسته‌ها
pip install yt-dlp requests beautifulsoup4

# اجرای برنامه
python aparat_downloader.py

# وارد کردن آدرس
https://www.aparat.com/playlist/9583120/

# انتخاب محل ذخیره (فشار دادن Enter)

# برای هر ویدیو: انتخاب کیفیت (b برای بهترین کیفیت)
```

## 📊 اطلاعات فنی

### فایل‌های ایجاد شده:
۱. **video_links_*.txt**: لیست تمام لینک‌های پیدا شده
۲. **download_log.txt**: تاریخچه کامل دانلودها
۳. **download_summary.txt**: خلاصه آماری دانلود
۴. **errors.txt**: خطاهای رخ داده

### تنظیمات قابل تغییر:
- زمان انتظار بین دانلودها (خط ۴۷۰)
- تعداد تلاش مجدد (خط ۳۸۶)
- مسیر پیش‌فرض ذخیره‌سازی (خط ۳۵۵)

### محدودیت‌ها:
- نیاز به اینترنت پرسرعت برای کیفیت‌های بالا
- ویدیوهای خصوصی نیاز به دسترسی دارند
- ممکن است با تغییرات سایت Aparat نیاز به بروزرسانی باشد

## 🎯 نکات نهایی

### برای بهترین تجربه:
۱. از اتصال اینترنت پایدار استفاده کنید
۲. فضای کافی در دیسک داشته باشید
۳. آنتی‌ویروس را موقتاً غیرفعال کنید (اگر مشکلی داشت)
۴. برای پلی‌لیست‌های بزرگ، زمان کافی در نظر بگیرید

### در صورت مشکل:
۱. فایل `requirements.txt` را بررسی کنید
۲. نسخه پایتون را بررسی کنید (باید ۳.۷+ باشد)
۳. خطاها را در `errors.txt` ببینید
۴. از دستور `--help` استفاده کنید

این برنامه به صورت رایگان ارائه شده و برای استفاده شخصی طراحی شده است.
