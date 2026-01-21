"""
Akıllı Mobil Radar Sistemi (Smart Mobile Radar)
-----------------------------------------------
Geliştirici: Yusuf Serhat Tümtürk
Tarih: 02.01.2026
Lisans: Tüm Hakları Saklıdır
"""
import sys
import os
import json

CONFIG_FILE = "config.json"

def load_config():
    defaults = {"max_speed": 90, "min_speed": 30, "speed_factor": 0.22}
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, 'r') as f:
                return {**defaults, **json.load(f)}
        except:
            pass
    return defaults

def save_config(config):
    try:
        with open(CONFIG_FILE, 'w') as f:
            json.dump(config, f)
    except Exception as e:
        print(f"Ayarlar kaydedilemedi: {e}")

# src klasörünü modül yoluna ekle
sys.path.append(os.path.join(os.getcwd(), 'src'))

from src.main import main

if __name__ == "__main__":
    print("Mobil Radar Sistemi Başlatıcı")
    print("-----------------------------")
    
    # Konfigürasyonu Yükle
    config = load_config()
    
    default_max = config.get("max_speed", 90)
    default_min = config.get("min_speed", 30)
    default_factor = config.get("speed_factor", 0.22)
    
    # Kullanıcıdan Girdi Al (Opsiyonel)
    try:
        print(f"Aktif Ayarlar: MAX={default_max}, MIN={default_min}, HASSASIYET={default_factor}")
        change_settings = input("Ayarları değiştirmek ister misiniz? (e/h): ").lower()
        
        max_speed = default_max
        min_speed = default_min
        speed_factor = default_factor
        
        if change_settings == 'e':
            try:
                max_speed = int(input(f"Maksimum Hız Limiti (Varsayılan {default_max}): ") or default_max)
                min_speed = int(input(f"Minimum Hız Limiti (Varsayılan {default_min}): ") or default_min)
                speed_factor = float(input(f"Hassasiyet Çarpanı (Varsayılan {default_factor}): ") or default_factor)
                
                # Yeni ayarları kaydet
                new_config = {"max_speed": max_speed, "min_speed": min_speed, "speed_factor": speed_factor}
                save_config(new_config)
                print(">> Ayarlar kaydedildi ve varsayılan yapıldı.")
                
            except ValueError:
                print("Hatalı giriş! Varsayılan değerler kullanılacak.")
        
    except KeyboardInterrupt:
        sys.exit()

    source = 0
    hw_port = None
    
    # Komut satırı argümanları basit kontrol
    if len(sys.argv) > 1:
        # Eğer COM port belirtilirse (örn: COM3)
        for arg in sys.argv[1:]:
            if "COM" in arg.upper() or arg.upper() == "MOCK":
                hw_port = arg
            elif arg.isdigit() or os.path.exists(arg):
                source = arg
                if source.isdigit(): source = int(source)

    # Kullanıcıya sor (Eğer argüman yoksa)
    if hw_port is None:
        use_hw = input("Donanım sensörü kullanılsın mı? (COM port adı veya 'h'ayır): ").strip()
        if use_hw.lower() != 'h' and len(use_hw) > 0:
            hw_port = use_hw

    main(source, max_speed=max_speed, min_speed=min_speed, speed_factor=speed_factor, hardware_port=hw_port)
