"""
Akıllı Mobil Radar Sistemi (Smart Mobile Radar)
-----------------------------------------------
Geliştirici: Yusuf Serhat Tümtürk
Tarih: 02.01.2026
Lisans: Tüm Hakları Saklıdır
"""
import sys
import os

# src klasörünü modül yoluna ekle
sys.path.append(os.path.join(os.getcwd(), 'src'))

from src.main import main

if __name__ == "__main__":
    print("Mobil Radar Sistemi Başlatıcı")
    print("-----------------------------")
    
    # Varsayılanlar
    default_max = 90
    default_min = 30
    default_factor = 0.5
    
    # Kullanıcıdan Girdi Al (Opsiyonel)
    try:
        print(f"Varsayılan ayarlar: MAX={default_max}, MIN={default_min}, HASSASIYET={default_factor}")
        change_settings = input("Ayarları değiştirmek ister misiniz? (e/h): ").lower()
        
        max_speed = default_max
        min_speed = default_min
        speed_factor = default_factor
        
        if change_settings == 'e':
            try:
                max_speed = int(input(f"Maksimum Hız Limiti (Varsayılan {default_max}): ") or default_max)
                min_speed = int(input(f"Minimum Hız Limiti (Varsayılan {default_min}): ") or default_min)
                speed_factor = float(input(f"Hassasiyet Çarpanı (Varsayılan {default_factor}, Arttırmak hızı yükseltir): ") or default_factor)
            except ValueError:
                print("Hatalı giriş! Varsayılan değerler kullanılacak.")
        
    except KeyboardInterrupt:
        sys.exit()

    source = 0
    if len(sys.argv) > 1:
        source = sys.argv[1]
        
    main(source, max_speed=max_speed, min_speed=min_speed, speed_factor=speed_factor)
