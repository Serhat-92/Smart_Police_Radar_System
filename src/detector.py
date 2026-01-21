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
        yolov8n.pt (Nano) en hızlısıdır. Optimize ayarlar ile kullanılır.
        """
        print(f"Model yükleniyor: {model_path}...")
        self.model = YOLO(model_path)
        # Sadece araç sınıflarını filtrelemek için COCO ID'leri
        # 2: car, 3: motorcycle, 5: bus, 7: truck
        self.vehicle_classes = [2, 3, 5, 7]

    def detect_and_track(self, frame):
        """
        Görüntü karesindeki araçları tespit eder ve takip eder.
        
        Args:
            frame (numpy.ndarray): OpenCV formatında görüntü karesi (BGR).
            
        Returns:
            ultralytics.engine.results.Results: Tespit ve takip sonuçlarını içeren nesne.
            
        Teknik Detaylar:
             - persist=True: Nesne kimliklerinin (ID) kareler arasında korunmasını sağlar.
                            Bir araç "ID:5" ise, sonraki karede de "ID:5" kalır.
             - classes=[2,3,5,7]: Sadece Car, Motorcycle, Bus, Truck sınıflarını algılar.
                                  İnsanları veya trafik ışıklarını yoksayar.
             - conf=0.3: Güven eşiği. Modelin en az %30 emin olduğu nesneleri kabul eder.
                         Daha düşük değer = Daha çok nesne (ama hatalı tespit riski artar).
                         Daha yüksek değer = Sadece çok net araçları görür.
             - iou=0.5: Intersection Over Union. Üst üste binen kutuların (bounding box)
                        nasıl ayıklanacağını belirler. %50 çakışmaya izin verir.
             - imgsz=640: Görüntü, modele girmeden önce 640x640 piksele yeniden boyutlandırılır.
                          Daha düşük = Hızlı (CPU dostu). Daha yüksek = Uzaktaki araçları görür.
        """
        results = self.model.track(
            frame, 
            persist=True, 
            classes=self.vehicle_classes, 
            verbose=False,
            conf=0.3, # Hassas yakalama için 0.3 (Nano model optimizasyonu)
            iou=0.5,
            imgsz=640, # CPU performansı için standart çözünürlük
            tracker="bytetrack.yaml" # Takip algoritması (DeepSort alternatifi)
        )
        return results[0]
