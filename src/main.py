"""
MOBIL RADAR SISTEMI - ANA UYGULAMA
Geliştirici: Yusuf Serhat Tümtürk
"""
import cv2
import sys
import os

# src klasörünü path'e ekle (eğer src dışından çağrılırsa diye)
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from detector import VehicleDetector
from tracker import SpeedEstimator
from ui import RadarUI
from recorder import EvidenceRecorder

def main(video_source=0, max_speed=90, min_speed=30, speed_factor=1.0):
    print(f"Sistem Başlatılıyor (MAX: {max_speed}, MIN: {min_speed}, FACTOR: {speed_factor})...")
    
    # Bileşenleri oluştur
    detector = VehicleDetector() 
    tracker = SpeedEstimator(speed_factor=speed_factor)
    ui = RadarUI(max_speed=max_speed, min_speed=min_speed)
    recorder = EvidenceRecorder(output_dir="ihlaller")
    
    # Video kaynağını aç
    cap = cv2.VideoCapture(video_source)
    
    if not cap.isOpened():
        print(f"Hata: Video kaynağı açılamadı ({video_source})")
        return

    print("Kayıt başladı. Çıkmak için 'q' tuşuna basın.")
    
    # Polis aracı telemetri verisi (OBD-II Entegrasyonu için placeholder)
    own_speed = 75

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Video sonu veya okuma hatası.")
            break
            
        # 1. Tespit ve Takip
        detections = detector.detect_and_track(frame)
        
        # 2. Hız Hesaplama
        vehicle_data = tracker.update(detections)
        
        #İhlal Kontrolü ve Kayıt
        for track_id, data in vehicle_data.items():
            speed = data['speed']
            captured = data.get('captured', False)
            plate = data.get('plate', 'UNKNOWN')
            
            # Eğer hız limiti aşıldıysa VE daha önce çekilmediyse
            if speed > max_speed and not captured:
                # Fotoğrafı çek
                recorder.save_violation(frame, speed, max_speed, plate, track_id)
                # Durumu güncelle (Bir kere çekilsin)
                tracker.mark_captured(track_id)
        
        # 3. Arayüz Çizimi
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

if __name__ == "__main__":
    # Eğer doğrudan bu dosya çalıştırılırsa varsayılan değerleri kullan
    source = 0
    if len(sys.argv) > 1:
        source = sys.argv[1]
        if source.isdigit():
            source = int(source)
            
    main(source)
