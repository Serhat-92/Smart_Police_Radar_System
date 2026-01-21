# DONANIM KRİTİKLERİ VE KURULUM MİMARİSİ

Bu rehber, Radar Sistemi'nin araç içine (Polis Aracı vb.) fiziksel entegrasyonu için **uymak zorunda olduğunuz** kuralları içerir.

## 🎯 1. Fiziksel Yerleşim (Araç İçi)
Sistem, araç ön camının arkasına veya ön panjura monte edildiğinde aşağıdaki şemaya sadık kalınmalıdır:

```text
[ ARAÇ ÖN CAMI / DASHBOARD ]
       │
       ├── [ KAMERA ]   ---> (Dar Açı: 25°–35° FOV) uzak mesafe plakaları için
       │
       ├── [ RADAR ]    ---> (HB100/OPS243) Tamamen kamera ile aynı yöne bakmalı
       │
       └── [ IR LED ]   ---> (Gece Görüş) Plaka parlamasını önleyen filtreli
```

## ⚠️ 2. Kritik Kural: Eksenel Hizalama (Axis Alignment)
**Kamera lensinin baktığı merkez nokta ile Radar'ın sinyal gönderdiği merkez nokta AYNI OLMALIDIR.**

*   **Neden?**: Yazılımımız "Görsel Takip" ve "Radar Hızını" birleştirmek için (Sensor Fusion) `tracker.py` içinde bir varsayım kullanır: *"Görüntünün merkezindeki araç, radarın gördüğü araçtır."*
*   **Risk**: Eğer Radar 10 derece sağa, Kamera düz bakarsa; kamera önündeki yavaş giden arabayı görürken, radar sağ şeritteki hızlı arabayı ölçer. Sonuç: **Ceza yanlış araca kesilir.**

## 3. Donanım Önerileri
*   **Kamera Açısı (FOV)**: 35 dereceden geniş olmamalıdır. Balık gözü lensler mesafe algısını bozar.
*   **Montaj**: Titreşimi önlemek için Kamera ve Radar aynı metal plakaya (rigid body) vidalanmalıdır.

## 🚀 4. Hareketli Radar Modu (Patrol Mode)
Sistem hareket halindeki bir polis aracında kullanıldığında, "Göreceli Hız" sorunu ortaya çıkar.

**Fizik Denklemi:**
`V_hedef = V_radar (Göreceli) ± V_polis`

Bu hesaplama için **V_polis** verisi kritik önem taşır. Sistem şu hiyerarşiyi kullanır:

1.  **OBD-II (Öncelikli)**: Aracın beyninden (ECU) tekerlek hızı okunur. Tünelde bile çalışır.
2.  **GPS (Yedek/Fallback)**: Uydu hızı kullanılır. Açık havada mükemmeldir, tünelde kopar.
3.  **Cross-Check (Çapraz Kontrol)**: İkisi de varsa ve aralarında fark > 5 km/s ise sistem kendini korumaya alır (HATA VERİR).

### Gerekli Modüller:
*   **OBD**: ELM327 Bluetooth/USB adaptörü.
*   **GPS**: NEO-6M veya USB GPS Mouse.
