# Mobil Radar Sistemi - Entegrasyon Kılavuzu

**Hazırlayan:** Yusuf Serhat Tümtürk
**Tarih:** 02.01.2026

Bu belge, geliştirdiğimiz yazılımın (Mobil Radar Sistemi) gerçek polis araçlarına nasıl uygulanacağını anlatır.

## 1. Donanım Gereksinimleri (Önerilen)
Sistemi araç içinde çalıştırmak için bir bilgisayar ünitesine ihtiyacınız var.
*   **Seçenek A (Mevcut Sistem):** Araçta hali hazırda Windows tabanlı bir Tablet/Laptop varsa direkt ona kurulabilir.
*   **Seçenek B (Mini PC):** NVIDIA Jetson Nano veya Intel NUC gibi küçük bir bilgisayar torpidoya monte edilebilir.

**Minimum Özellikler:**
*   İşletim Sistemi: Windows 10/11 veya Linux (Ubuntu)
*   İşlemci: Intel i5 veya eşdeğeri
*   RAM: 8 GB
*   Ekran Kartı: NVIDIA GPU önerilir (YOLOv8 performansı için, ama güçlü bir CPU ile de çalışır).

## 2. Kamera Bağlantısı
Sistemimiz `OpenCV` altyapısını kullandığı için her türlü kamerayı destekler.

### A. USB Kamera (Webcam)
Kamerayı bilgisayarın USB portuna takın.
*   **Çalıştırma:** `run.py` (Otomatik olarak algılar).

### B. IP Kamera / Araç İçi Kamera Sistemi (RTSP)
Eğer araçta profesyonel bir kamera sistemi varsa, görüntüyü ağ üzerinden (Ethernet kablosu ile) alabilirsiniz.
*   Kameranın RTSP adresini öğrenin (Örn: `rtsp://admin:1234@192.168.1.108:554/stream`).
*   **Çalıştırma:** Komut satırından şu şekilde başlatın:
    ```bash
    python run.py "rtsp://admin:1234@192.168.1.108:554/stream"
    ```

## 3. Otomatik Başlatma (Windows)
Polis memurunun her seferinde kod yazması gerekmez. Bilgisayar açıldığında sistemin otomatik gelmesi için:
1.  Masaüstündeki `RADAR_BASLAT.bat` dosyasına sağ tıklayın -> `Kısayol Oluştur`.
2.  `Win + R` tuşuna basın, `shell:startup` yazın.
3.  Kısayolu açılan klasöre atın.
Artık bilgisayar açıldığında Radar Sistemi otomatik başlayacaktır.

## 4. GPS Entegrasyonu (Gelecek Planı)
Şu an sistem polis aracının hızını manuel girilen bir değerden (veya varsayılan) alıyor. Gerçek kullanımda, araca bir **USB GPS Alıcısı** takılarak `main.py` içindeki `own_speed` değişkeni dinamik hale getirilebilir.
