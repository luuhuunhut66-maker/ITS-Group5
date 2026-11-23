@echo off
chcp 65001 > nul
cd /d "%~dp0"
title Xuất Hình Minh Họa & Kiểm Thử Ngưỡng

echo [*] Đang chạy script tạo hình minh họa Chương 2...
".venv\Scripts\python.exe" "scripts\prepare_chapter2_assets.py"
echo.
echo [*] Hoàn thành! Nhấn phím bất kỳ để đóng...
pause > nul
