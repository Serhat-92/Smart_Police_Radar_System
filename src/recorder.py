"""
KANIT VE İHLAL KAYIT SİSTEMİ
Geliştirici: Yusuf Serhat Tümtürk
"""
import cv2
import os
import datetime

class EvidenceRecorder:
    def __init__(self, output_dir="ihlaller"):
        self.output_dir = output_dir
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
            
    def save_violation(self, frame, speed, limit, plate, track_id):
        """
        İhlal anını fotoğraflar ve diske kaydeder.
        """
        # Dosya ismi: 2026-01-02_15-30-01_120kmh.jpg
        now = datetime.datetime.now()
        timestamp = now.strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"{timestamp}_{int(speed)}kmh.jpg"
        path = os.path.join(self.output_dir, filename)
        
        # Fotoğraf üzerine kalıcı damga (Burn-in)
        evidence_img = frame.copy()
        h, w = evidence_img.shape[:2]
        
        # Bilgi kutusu
        cv2.rectangle(evidence_img, (0, h-150), (w, h), (0, 0, 150), -1) # Koyu Kırmızı Arkaplan
        
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(evidence_img, f"IHLAL TESPITI - HIZ LIMIT ASIMI", (20, h-110), font, 1.0, (255,255,255), 2)
        cv2.putText(evidence_img, f"TARIH: {now.strftime('%d.%m.%Y %H:%M:%S')}", (20, h-70), font, 0.7, (255,255,255), 1)
        cv2.putText(evidence_img, f"HIZ: {int(speed)} km/s | LIMIT: {limit}", (20, h-30), font, 0.8, (0, 255, 255), 2)
        
        # Kaydet
        cv2.imwrite(path, evidence_img)
        print(f"IHLAL KAYDEDILDI: {path}")
