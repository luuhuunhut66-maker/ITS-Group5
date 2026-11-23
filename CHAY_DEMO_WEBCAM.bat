@echo off
chcp 65001 > nul
cd /d "%~dp0"
title ITS Nhóm 5 - Demo Nhận Diện Khuôn Mặt Webcam

echo =================================================================
echo        HỆ THỐNG GIAO THÔNG THÔNG MINH (ITS) - NHÓM 5
echo        CHƯƠNG TRÌNH NHẬN DIỆN KHUÔN MẶT REAL-TIME
echo =================================================================
echo.
echo [*] Đang kích hoạt môi trường ảo Python (.venv)...

if not exist ".venv\Scripts\python.exe" (
    echo [LỖI] Không tìm thấy môi trường ảo .venv!
    pause
    exit /b
)

echo [*] Đang khởi động Webcam...
echo     - Nhấn phím 'q' hoặc 'ESC' để dừng camera.
echo     - Nhấn phím 's' để chụp ảnh màn hình.
echo.

".venv\Scripts\python.exe" "scripts\test_webcam.py"

if %errorlevel% neq 0 (
    echo.
    echo =================================================================
    echo [THÔNG BÁO] Chương trình kết thúc hoặc gặp sự cố khi mở Webcam.
    echo Vui lòng kiểm tra:
    echo  1. Máy tính đã bật quyền truy cập Camera cho ứng dụng chưa.
    echo  2. Có ứng dụng nào khác (Zalo, Zoom, Teams, Web) đang chiếm Camera không.
    echo =================================================================
    pause
)
