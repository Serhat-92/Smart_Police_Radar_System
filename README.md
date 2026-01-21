# Akıllı Mobil Radar Sistemi (Smart Patrol Radar) v2.0
> **"TIRT" değil, Akıllı Sistem.**

**Geliştirici:** [Yusuf Serhat Tümtürk]  
**Sürüm:** 2.0.0 (Beta)

## 🚀 Proje Hakkında
Bu proje, sıradan bir hız tespit yazılımı değil; **hareketli polis araçları** ve karmaşık trafik senaryoları için tasarlanmış profesyonel bir **Elektronik Denetleme Sistemi (EDS)** prototipidir. 

Sistem, **Görüntü İşleme (YOLOv8)** ile **Donanım Radarını (Doppler)** birleştirerek (Sensor Fusion) çalışır.

## 🔥 Yeni Özellikler (v2.0)

### 1. Hareketli Radar Modu (Patrol Mode) 🚔
*   **Sorun:** Polis aracı hareket halindeyken radar "göreceli hız" ölçer.
*   **Çözüm:** Sistem, **OBD-II** üzerinden polis aracının hızını okur ve radar verisine ekleyerek **Gerçek Hedef Hızını** (Absolute Speed) hesaplar.
*   **Güvenlik:** Ani fren/gaz (İvme > 2m/s²) durumunda yanlış ölçüm yapmamak için kendini kilitler.

### 2. Akıllı Hedef Eşleştirme (Smart Matching) 🧠
*   **Sorun:** Radar sadece "120 km/s" der, ama hangi araç?
*   **Çözüm:** Sistem, ekrandaki tüm araçların hız profillerini analiz eder. Radar verisiyle matematiksel olarak en uyumlu aracı ("Best Fit") bulur ve cezayı ona keser.

### 3. Profesyonel Kanıt Paketi 📸
*   Sadece fotoğraf değil, **Adli Kanıt Paketi** üretir:
    *   **Fotoğraf (.jpg):** Üzerinde Tarih, Konum, Radar Hızı, AI Tahmini ve **Sapma Oranı (% Deviation)** filigranlı.
    *   **Veri (.json):** Mahkeme delili olabilecek yapılandırılmış metin dosyası.

### 4. Sensör Füzyonu & Hibrit Mod (Hybrid Mode)
*   Kamera: Araç Kimliği (Plaka/Tip)
*   Radar: Kesin Hız (Doppler)
*   AI: Doğrulama (Cross-Check)
*   **Sonuç:** İkisi de "Tamam" demeden ceza yazılmaz.

### 5. Kaos Simülasyonu (Chaos Mode) 🌪️
*   Sistemi test etmek için "Sinyal Kaybı", "Jitter", "Hayalet Hedef" gibi arıza senaryolarını simüle eden özel mod.

---

## 🛠️ Kurulum

1.  Gerekli kütüphaneleri yükleyin:
    ```bash
    pip install -r requirements.txt
    ```

2.  Sistemi başlatın:
    ```bash
    # Sadece Kamera Modu
    python run.py

    # Simülasyon Modu (Kaos Testi Dahil)
    python run.py MOCK

    # Gerçek Donanım Modu (OPS243 Radar)
    python run.py COM3
    ```

## ⚙️ Yapılandırma
Sistem ilk açılışta ayarlarınızı (`config.json`) kaydeder:
*   **Maksimum Hız**
*   **Hassasiyet Çarpanı**
*   **Minimum Hız**

## 📂 Sistem Mimarisi
*   `src/detector.py`: YOLOv8 Araç Algılama
*   `src/tracker.py`: Görsel Hız Takibi
*   `src/radar_hardware.py`: Radar Sensör Sürücüsü & Simülatör
*   `src/patrol_speed.py`: OBD-II / GPS Polis Hızı Modülü
*   `src/main.py`: Sensor Fusion & Karar Çekirdeği
*   `src/recorder.py`: Kanıt & İhlal Kayıtçısı

## ⚠️ Donanım Gereksinimleri
*   **Radar:** OmniPreSense OPS243 veya HB100 (UART Modlu)
*   **Polis Hızı:** ELM327 OBD-II Bluetooth/USB
*   **Kamera:** En az 720p, dar açı (35°) önerilir.
*   **Kurulum:** [Detaylı Donanım Rehberi](docs/DONANIM_KURULUMU.md)

## Lisans
Bu proje [Yusuf Serhat Tümtürk] tarafından geliştirilmiştir. Tüm hakları saklıdır.
