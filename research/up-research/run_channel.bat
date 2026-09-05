@echo off
cd /d D:\motion\data\tmp\up-research
set http_proxy=http://127.0.0.1:7890
set https_proxy=http://127.0.0.1:7890
tasklist | findstr /i "chrome.exe" >nul
if errorlevel 1 (
  start "" "C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9333 --user-data-dir=D:\motion\data\tmp\up-research\profile --proxy-server=http://127.0.0.1:7890 --no-first-run --no-default-browser-check --headless=new about:blank
  timeout /t 6 >nul
)
"C:\Users\10777\.workbuddy\binaries\node\versions\22.22.2-2\node.exe" get_channel2.mjs > _channel_out.txt 2>&1
echo DONE_CHANNEL_SCRAPE