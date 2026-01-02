# Akıllı Mobil Radar Sistemi - Teknik Tasarım Belgesi

**Hazırlayan:** Yusuf Serhat Tümtürk
**Tarih:** 02.01.2026

## 1. Yönetici Özeti
Bu proje, polis devriye araçlarında kullanılmak üzere, maliyet etkin ve yüksek teknolojili bir trafik denetim çözümü sunmayı hedefler. Sistem, görüntü işleme ve derin öğrenme teknolojilerini birleştirerek, ek radar donanımına ihtiyaç duymadan hız tespiti yapabilmektedir.

## 2. Sistem Mimarisi

### 2.1. Algılama Katmanı (Perception Layer)
Sistem, gerçek zamanlı video akışı üzerinden **Convolutional Neural Networks (CNN)** kullanarak araç tespiti yapar.
*   **Model:** YOLOv8 (You Only Look Once)
*   **Hassasiyet:** %40 Güven Eşiği (Confidence Threshold)
*   **Performans:** Gerçek zamanlı (30+ FPS)

### 2.2. Analiz Katmanı (Analysis Core)
Tespit edilen nesnelerin uzay-zamansal (spatiotemporal) hareketleri analiz edilir.
*   **Hız Algoritması:** Kareler arası piksel yer değiştirmesi (Delta-Pixel) ve perspektif düzeltme katsayıları kullanılarak aracın göreli hızı hesaplanır.
*   **Stabilizasyon:** Hız verisindeki anlık gürültüleri filtrelemek için **Hareketli Ortalama (Rolling Average)** penceresi kullanılır.

### 2.3. Uygulama Katmanı (Application Layer)
*   **İhlal Yönetimi:** Belirlenen eşik değerleri (Min/Max Limit) aşıldığında olay tetiklenir.
*   **Kanıt Kaydı:** İhlal anı, üzerine meta-veri (Metadata) işlenmiş yüksek çözünürlüklü görüntü olarak arşivlenir.

## 3. Kullanılan Teknolojiler
*   **Programlama Dili:** Python 3.10+
*   **Görüntü İşleme:** OpenCV
*   **Derin Öğrenme:** PyTorch & Ultralytics
*   **Veri Yönetimi:** NumPy

## 4. Sonuç
Geliştirilen bu sistem, modern trafik denetim ihtiyaçlarını karşılayacak ölçeklenebilir ve sağlam bir altyapıya sahiptir.
