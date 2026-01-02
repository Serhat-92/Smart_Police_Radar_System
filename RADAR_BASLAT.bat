@echo off
title MOBIL RADAR SISTEMI - BASLATILIYOR
color 0A
:: Geliştirici: Yusuf Serhat Tümtürk

echo ===================================================
echo   MOBIL RADAR SISTEMI - OTOYOL DEVRIYE MODU
echo ===================================================
echo.
echo Sistem konfigurasyonu yukleniyor...
echo.

:: Python'un kurulu oldugundan emin olun
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [HATA] Python bulunamadi! Lutfen Python'u yukleyin.
    pause
    exit
)

:: Uygulamayi baslat
:: Eger IP kameraniz varsa parantez icine RTSP adresini yazin
:: Orn: python run.py "rtsp://192.168.1.55/live"
python run.py

if %errorlevel% neq 0 (
    echo.
    echo [HATA] Sistem beklenmedik sekilde kapandi.
    pause
)
