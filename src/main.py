"""
MOBIL RADAR SISTEMI - ANA UYGULAMA
Geliştirici: Yusuf Serhat Tümtürk
"""
import cv2
import sys
import os
import argparse

# src klasörünü path'e ekle (eğer src dışından çağrılırsa diye)
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from detector import VehicleDetector
from tracker import SpeedEstimator
from ui import RadarUI
from recorder import EvidenceRecorder
from radar_hardware import RadarSensor, MockRadarSensor
from patrol_speed import PatrolSpeedMonitor # YENI: Polis Hızı Modülü

def main(video_source=0, max_speed=90, min_speed=30, speed_factor=1.0, hardware_port=None, server_url=None):
    print(f"Sistem Başlatılıyor (MAX: {max_speed}, MIN: {min_speed}, FACTOR: {speed_factor})...")
    if server_url:
        print(f"📡 5G MODÜLÜ AKTİF: {server_url}")
    
    # Donanım Başlatma (Radar Sensör)
    hw_radar = None
    if hardware_port:
        if hardware_port.upper() == "MOCK":
            print("SIMULASYON MODU: Sanal Radar ve Sanal OBD Devrede.")
            hw_radar = MockRadarSensor()
        else:
            print(f"DONANIM MODU: {hardware_port} üzerinden sensör bekleniyor...")
            hw_radar = RadarSensor(port=hardware_port)
        
        if hw_radar and hw_radar.start():
            print(f"!!! DONANIM RADAR MODU AKTİF: {hardware_port} !!!")
        else:
            print("Donanım sensörü başlatılamadı, görsel tahmine dönülüyor.")
            hw_radar = None
            
    # Polis Aracı Hız Sensörü (OBD)
    # Donanım modu varsa OBD'yi de gerçek portta arayabiliriz, şimdilik MOCK/AUTO
    obd_mock = (hardware_port == "MOCK") if hardware_port else True # Donanım yoksa OBD de sanal olsun
    patrol_monitor = PatrolSpeedMonitor(port="AUTO", mock_mode=obd_mock)
    
    # Bileşenleri oluştur
    detector = VehicleDetector() 
    tracker = SpeedEstimator(speed_factor=speed_factor)
    ui = RadarUI(max_speed=max_speed, min_speed=min_speed)
    
    # RECORDER (Sunucu URL'sini buraya veriyoruz)
    recorder = EvidenceRecorder(output_dir="ihlaller", server_url=server_url)
    
    # Video kaynağını aç
    cap = cv2.VideoCapture(video_source)
    
    if not cap.isOpened():
        print(f"Hata: Video kaynağı açılamadı ({video_source})")
        return

    print("Kayıt başladı. Çıkmak için 'q' tuşuna basın.")
    
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Video sonu veya okuma hatası.")
            break
            
        # 1. Tespit ve Takip
        detections = detector.detect_and_track(frame)
        
        # 2. Hız Hesaplama
        vehicle_data = tracker.update(detections)
        
        # Polis Hızı (OBD)
        # PatrolSpeedMonitor'dan güncel hız ve ivme verisini al
        current_patrol_speed, current_patrol_accel = patrol_monitor.get_speed_and_accel()

        hw_absolute_speed = 0 # Default

        # Donanım sensör verisi varsa, hız bilgisini güncelle ve karşılaştır
        if hw_radar:
            radar_relative_speed = hw_radar.get_speed() # Radar SİZE GÖRE hızı ölçer
            # --- İVME KONTROLÜ (UNSTABLE CHECK) ---
            # Eğer polis aracı ani hızlanıyor veya fren yapıyorsa (> 2 m/s^2)
            # Radar ölçümü geçersiz sayılmalıdır.
            is_stable = abs(current_patrol_accel) < 2.0
            
            # Absolute Speed Hesabı (Basit: Radar + Polis Hızı)
            # Yaklaşan araç: Radar hızı = Araç Hızı + Polis Hızı
            # Uzaklaşan araç: Radar hızı = Araç Hızı - Polis Hızı (veya tam tersi, duruma göre)
            # Şimdilik basit toplama (karşı şerit yaklaşan varsayımı)
            hw_absolute_speed = radar_relative_speed + current_patrol_speed

            # Ekranda araç varsa
            if len(vehicle_data) > 0:
                if radar_relative_speed > 5 and is_stable:
                    # --- AKILLI HEDEF EŞLEŞTİRME (SMART MATCHING) ---
                    # Radarın ölçtüğü hıza (hw_absolute_speed) görsel olarak EN YAKIN olan aracı buluyoruz.
                    
                    best_match_id = None
                    min_diff = float('inf')
                    
                    for vid, vdata in vehicle_data.items():
                        visual_val = vdata['speed']
                        diff = abs(visual_val - hw_absolute_speed)
                        if diff < min_diff:
                            min_diff = diff
                            best_match_id = vid
                    
                    # Eşleşme bulunduysa
                    if best_match_id is not None:
                        car_data = vehicle_data[best_match_id]
                        
                        car_data['radar_speed'] = hw_absolute_speed
                        
                        # Füzyon Durumu (Doğrulama)
                        if min_diff < 25: 
                            car_data['fusion_status'] = "VERIFIED"
                            car_data['color'] = (0, 255, 0)
                            car_data['speed'] = hw_absolute_speed 
                        else:
                            car_data['fusion_status'] = "UNCERTAIN"
                            car_data['color'] = (0, 255, 255) # Sarı
                            car_data['speed'] = hw_absolute_speed
                            
                elif not is_stable:
                    # İVME YÜKSEK - ÖLÇÜM GEÇERSİZ
                    # Tüm araçlara uyarı ver
                    for vid in vehicle_data:
                        vehicle_data[vid]['fusion_status'] = "UNSTABLE" 
                        vehicle_data[vid]['radar_speed'] = 0
            
            elif len(vehicle_data) > 0:
                # Radar sessizse temizle
                for vid in vehicle_data:
                    vehicle_data[vid]['radar_speed'] = 0
                    vehicle_data[vid]['fusion_status'] = None

        #İhlal Kontrolü ve Kayıt
        for track_id, data in vehicle_data.items():
            speed = data['speed']
            captured = data.get('captured', False)
            plate = data.get('plate', 'UNKNOWN')
            
            # Eğer hız limiti aşıldıysa VE daha önce çekilmediyse
            if speed > max_speed and not captured:
                # Meta verileri hazırla
                radar_val = data.get('radar_speed', 0)
                ai_val = data.get('speed', 0) 
                
                if radar_val == 0: radar_val = speed 
                ai_pure_val = ai_val 
                
                # Sapma Hesabı
                deviation = 0.0
                if ai_pure_val > 0:
                    deviation = abs(radar_val - ai_pure_val) / ai_pure_val * 100
                
                # Fotoğrafı çek ve Paketi Kaydet (Ve Sunucuya Gönder)
                recorder.save_violation(
                    frame, 
                    speed=speed, 
                    limit=max_speed, 
                    track_id=track_id, 
                    radar_speed=radar_val, 
                    ai_speed=ai_pure_val, 
                    deviation=deviation
                )
                
                # Durumu güncelle (Bir kere çekilsin)
                tracker.mark_captured(track_id)
        
        # 3. Arayüz Çizimi
        own_speed = current_patrol_speed
        
        frame = ui.draw_detections(frame, vehicle_data)
        frame = ui.draw_dashboard(frame, own_speed, track_count=len(vehicle_data))
        
        # Ekranda göster
        # Görüntü çok büyükse küçült (Opsiyonel)
        # frame = cv2.resize(frame, (1280, 720))
        
        cv2.imshow("MOBIL RADAR SISTEMI - PROTOTIP", frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
            
    cap.release()
    cv2.destroyAllWindows()
    if hw_radar:
        hw_radar.stop()
    # Recorder'ı durdur (Thread'leri temizle)
    recorder.stop()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Mobil Radar Sistemi")
    parser.add_argument("--source", type=str, default="0", help="Video kaynağı (0, 1 veya dosya yolu)")
    parser.add_argument("--max_speed", type=int, default=90, help="Hız Limiti")
    parser.add_argument("--port", type=str, default=None, help="Radar Donanım Portu (COM3, MOCK)")
    parser.add_argument("--server", type=str, default=None, help="5G Sunucu URL (örn: http://localhost:8000)")
    
    args = parser.parse_args()
    
    # Source int mi str mi kontrolü
    src = args.source
    if src.isdigit():
        src = int(src)
        
    main(
        video_source=src, 
        max_speed=args.max_speed, 
        hardware_port=args.port,
        server_url=args.server
    )
