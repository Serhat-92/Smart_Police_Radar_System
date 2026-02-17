@echo off
title 5G MOBIL RADAR BASLATICI - PROFESYONEL MOD
color 0f
cls

echo ==========================================================
echo   MOBIL RADAR SISTEMI - 5G BAGLANTILI MOD (v2.0)
echo   Gelistirici: Yusuf Serhat Tumturk
echo ==========================================================
echo.
echo [1/3] GEREKLI KUTUPHANELER KONTROL EDILIYOR...
pip install -r requirements.txt > nul 2>&1
if %errorlevel% neq 0 (
    echo [!] Kutuphaneler yuklenirken hata olustu veya pip bulunamadi.
    echo     Internet baglantinizi kontrol edin.
) else (
    echo [OK] Kutuphaneler hazir.
)

echo.
echo [2/3] KOMUTA MERKEZI (SUNUCU) BASLATILIYOR...
echo       (Bu pencereyi kapatmayin, arka planda calisacak)
start "5G KOMUTA MERKEZI (HQ)" cmd /k "python src/server.py"
timeout /t 2 > nul

echo.
echo [3/3] RADAR SISTEMI (ISTEMCI) BASLATILIYOR...
echo.
echo SECENEKLER:
echo 1. WEBKAMERA MODU (Sadece Kamera)
echo 2. DONANIM MODU (OPS243 Radar + OBD Bagli ise)
echo 3. FULL SIMULASYON MODU (Donanim yoksa bunu secin)
echo.
set /p secim="Mod Seciniz (1-3) [Varsayilan: 3]: "

if "%secim%"=="" set secim=3

if "%secim%"=="1" (
    echo.
    echo BASLATILIYOR: Webkamera + 5G Modu...
    python src/main.py --source 0 --server http://127.0.0.1:8000 --max_speed 90
)

if "%secim%"=="2" (
    echo.
    echo BASLATILIYOR: Donanim Entegrasyonu Modu...
    set /p radar_port="Radar Portu Girin (orn: COM3): "
    python src/main.py --source 0 --server http://127.0.0.1:8000 --port %radar_port% --max_speed 90
)

if "%secim%"=="3" (
    echo.
    echo BASLATILIYOR: Full Simulasyon Modu (Mock Radar + Mock OBD)...
    python src/main.py --source 0 --server http://127.0.0.1:8000 --port MOCK --max_speed 90
)

echo.
echo Sistem kapatildi.
pause
