"""
KANIT VE İHLAL KAYIT SİSTEMİ
Geliştirici: Yusuf Serhat Tümtürk
"""
import cv2
import os
import cv2
import os
import datetime
import json

class EvidenceRecorder:
    def __init__(self, output_dir="ihlaller"):
        self.output_dir = output_dir
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
            
    def save_violation(self, frame, speed, limit, track_id, radar_speed=0, ai_speed=0, deviation=0.0):
        """
        İhlal anını 'İhlal Paketi' olarak (JPG + JSON) kaydeder.
        """
        now = datetime.datetime.now()
        timestamp_str = now.strftime("%Y-%m-%d_%H-%M-%S")
        
        # 1. Fotoğraf İşlemleri (Watermark)
        evidence_img = frame.copy()
        h, w = evidence_img.shape[:2]
        
        # Bilgi kutusu (Alt şerit)
        cv2.rectangle(evidence_img, (0, h-180), (w, h), (0, 0, 150), -1) 
        
        font = cv2.FONT_HERSHEY_SIMPLEX
        # Başlık ve ID
        cv2.putText(evidence_img, f"RESMI IHLAL KAYDI - ID:{track_id}", (20, h-140), font, 1.0, (255,255,255), 2)
        
        # Sol Kolon (Temel Bilgiler)
        cv2.putText(evidence_img, f"TARIH: {now.strftime('%d.%m.%Y %H:%M:%S')}", (20, h-100), font, 0.6, (255,255,255), 1)
        cv2.putText(evidence_img, f"KONUM: OTOYOL K3 NOKTASI (SABIT)", (20, h-70), font, 0.6, (255,255,255), 1)
        
        # Sağ Kolon (Hız Verileri - Kritik)
        col2_x = w // 2
        # Yasal Hız (Radar) - Sarı Renk
        cv2.putText(evidence_img, f"RADAR HIZI: {int(radar_speed)} km/s", (col2_x, h-100), font, 0.8, (0, 255, 255), 2)
        # AI Tahmini - Beyaz (Referans)
        cv2.putText(evidence_img, f"AI TAHMINI: {int(ai_speed)} km/s", (col2_x, h-70), font, 0.6, (200, 200, 200), 1)
        # Sapma Oranı
        cv2.putText(evidence_img, f"SAPMA: %{deviation:.1f}", (col2_x, h-40), font, 0.6, (200, 200, 200), 1)
        
        # Limit Bilgisi
        cv2.putText(evidence_img, f"YASAL LIMIT: {limit} km/s", (20, h-40), font, 0.8, (255, 255, 0), 2)
        
        # Dosya İsimlendirme
        base_filename = f"{timestamp_str}_ID{track_id}_SPD{int(radar_speed)}"
        img_path = os.path.join(self.output_dir, base_filename + ".jpg")
        json_path = os.path.join(self.output_dir, base_filename + ".json")
        
        # 2. Resmi Kaydet
        cv2.imwrite(img_path, evidence_img)
        
        # 3. JSON Veri Paketi Oluştur
        violation_package = {
            "record_id": base_filename,
            "timestamp": now.isoformat(),
            "location": "OTOYOL_K3",
            "vehicle_id": track_id,
            "limit": limit,
            "measurements": {
                "radar_speed": radar_speed,
                "ai_vision_speed": ai_speed,
                "deviation_percent": deviation,
                "final_speed": speed  # Ceza kesilen hız (Genelde Radar)
            },
            "evidence_files": {
                "photo": img_path
            }
        }
        
        # JSON Kaydet
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(violation_package, f, indent=4, ensure_ascii=False)
            
        print(f"IHLAL PAKETI OLUSTURULDU: {base_filename}")
