# Akıllı Mobil Radar Sistemi (Smart Mobile Radar)

**Geliştirici:** [Adınız Soyadınız]
**Sürüm:** 1.0.0

## Proje Hakkında
Bu proje, trafik denetimlerinde kullanılmak üzere tasarlanmış, yapay zeka tabanlı yeni nesil bir hız tespit sistemidir. Geleneksel radar donanımlarına bağımlılığı azaltarak, bilgisayarlı görü (Computer Vision) teknikleriyle araçların hızını analiz eder ve ihlal durumlarını otomatik olarak raporlar.

## Temel Özellikler
*   **Yapay Zeka Destekli Tespit:** YOLOv8 mimarisi ile gerçek zamanlı araç (Otomobil, Kamyon, Motosiklet) sınıflandırması.
*   **Dinamik Hız Analizi:** Piksel yoğunluğu ve perspektif değişimine dayalı gelişmiş hız tahminleme algoritması.
*   **Odak Modu (Focus Mode):** Sürücü dikkatini dağıtmamak için sadece ihlal yapan araçların görselleştirilmesi.
*   **Otomatik Kanıt Sistemi:** Hız limiti aşıldığında plaka, tarih, saat ve hız verisini içeren şifreli kanıt fotoğrafının otomatik üretimi.
*   **Performans Optimizasyonu:** Çöp toplayıcı (Garbage Collector) ve akıllı filtreleme algoritmaları ile uzun süreli stabil çalışma.

## Kurulum

1.  Gerekli kütüphaneleri yükleyin:
    ```bash
    pip install -r requirements.txt
    ```

2.  Sistemi başlatın:
    ```bash
    python run.py
    ```
    *veya*
    ```bash
    RADAR_BASLAT.bat
    ```

## Sistem Mimarisi
Proje, modüler bir yapıda tasarlanmıştır:
*   `src/detector.py`: Nesne algılama motoru (Neural Network Wrapper).
*   `src/tracker.py`: Hız hesaplama çekirdeği ve Kalman filtresi benzeri durum yönetimi.
*   `src/recorder.py`: İhlal verilerinin güvenli kaydı.
*   `src/ui.py`: Operatör Bilgi Ekranı (HUD).

## Lisans
Bu proje [Yusuf Serhat Tümtürk] tarafından geliştirilmiştir. Tüm hakları saklıdır.
