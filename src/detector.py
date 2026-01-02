"""
NESNE TESPİT MODÜLÜ (YOLOv8)
Geliştirici: Yusuf Serhat Tümtürk
"""
from ultralytics import YOLO
import cv2

class VehicleDetector:
    def __init__(self, model_path='yolov8n.pt'):
        """
        YOLOv8 Modelini başlatır.
        yolov8n.pt (Nano) en hızlısıdır, gerçek zamanlı işlem için idealdir.
        """
        print(f"Model yükleniyor: {model_path}...")
        self.model = YOLO(model_path)
        # Sadece araç sınıflarını filtrelemek için COCO ID'leri
        # 2: car, 3: motorcycle, 5: bus, 7: truck
        self.vehicle_classes = [2, 3, 5, 7]

    def detect_and_track(self, frame):
        """
        Görüntü karesindeki araçları tespit eder ve takip eder via BYTETrack (YOLO default).
        """
        # persist=True: Takip işleminin kareler arasında devam etmesini sağlar
        # conf=0.5: Sadece %50 ve üzeri emin olduğu nesneleri al (Gürültüyü azaltır)
        # iou=0.5: Çakışma eşiği. Kalabalık trafikte araçları ayırt etmeye yarar.
        results = self.model.track(
            frame, 
            persist=True, 
            classes=self.vehicle_classes, 
            verbose=False,
            conf=0.4, 
            iou=0.5,
            tracker="bytetrack.yaml" # Kalabalık ve üst üste binmeler için başarılıdır
        )
        return results[0]
