"""
HIZ TAKİP VE ANALİZ ALGORİTMASI
Geliştirici: Yusuf Serhat Tümtürk
"""
import time

class SpeedEstimator:
    def __init__(self, speed_factor=1.0):
        # track_id -> {last_y: int, last_time: float, speed: float, captured: bool}
        self.vehicle_states = {}
        
        # Hız Kalibrasyon Katsayısı
        # Bu değer, piksel/zaman oranını fiziksel hıza (km/s) dönüştürmek için kullanılır.
        # Saha testlerine göre optimize edilmelidir.
        self.SPEED_FACTOR = speed_factor

    def update(self, detections):
        """
        Nesne takibi ve hız hesaplama algoritmasını çalıştırır.
        N-Frame Rolling Average yöntemi ile gürültü filtrelenir.
        """
        current_time = time.time()
        current_data = {}
        
        if detections.boxes is None or detections.boxes.id is None:
            return current_data

        # Ultralytics sonuçlarını al
        ids = detections.boxes.id.int().cpu().tolist()
        boxes = detections.boxes.xyxy.cpu().tolist()
        
        for i, track_id in enumerate(ids):
            box = boxes[i]
            x1, y1, x2, y2 = box
            
            # Aracın merkezi ve yüksekliği
            center_y = int(y2)
            height = int(y2 - y1)
            
            display_speed = 0.0
            
            # Tracker State Başlatma
            if track_id not in self.vehicle_states:
                self.vehicle_states[track_id] = {
                    'history': [], 
                    'speed_buffer': [], 
                    'last_speed': 0.0,
                    'captured': False # İhlal durumu
                }
            
            state = self.vehicle_states[track_id]
            
            # Geçmişe ekle
            state['history'].append((current_time, center_y))
            
            # Sadece son 10 kareyi tut (Hafıza yönetimi)
            if len(state['history']) > 10:
                state['history'].pop(0)
            
            # Algoritma konverjansı için minimum veri seti kontrolü
            if len(state['history']) >= 5:
                # 5 kare öncesine göre değişim
                prev_time, prev_y = state['history'][0]
                curr_time, curr_y = state['history'][-1]
                
                delta_time = curr_time - prev_time
                delta_pixel = abs(curr_y - prev_y)
                
                if delta_time > 0 and height > 0:
                    relative_movement = delta_pixel / height
                    speed_mps = relative_movement / delta_time 
                    
                    # Hız dönüşümü
                    raw_speed = speed_mps * self.SPEED_FACTOR * 100
                    
                    # Anomali Filtresi (Outlier Rejection)
                    if raw_speed > 300: raw_speed = state['last_speed']
                    # Mikro-hareket Filtresi (Jitter Reduction)
                    if delta_pixel < 2: raw_speed = 0
                    
                    state['speed_buffer'].append(raw_speed)
                    if len(state['speed_buffer']) > 15:
                        state['speed_buffer'].pop(0)
                        
                    avg_speed = sum(state['speed_buffer']) / len(state['speed_buffer'])
                    
                    display_speed = avg_speed
                    state['last_speed'] = avg_speed
            
            current_data[track_id] = {
                'box': box,
                'speed': display_speed,
                'captured': state['captured']
            }
            
        # Bellek Yönetimi (Memory Garbage Collection)
        self._cleanup(current_time)
            
        return current_data
    
    def mark_captured(self, track_id):
        """Bir aracın cezasının kesildiğini işaretler"""
        if track_id in self.vehicle_states:
            self.vehicle_states[track_id]['captured'] = True

    def _cleanup(self, current_time, timeout=2.0):
        """
        Belirtilen süre boyunca güncellenmeyen ID'leri siler.
        """
        # Silinecek ID'leri bul
        ids_to_delete = []
        for track_id, state in self.vehicle_states.items():
            last_seen = state['history'][-1][0] if state['history'] else 0
            if current_time - last_seen > timeout:
                ids_to_delete.append(track_id)
        
        # Güvenli silme
        for trash_id in ids_to_delete:
            del self.vehicle_states[trash_id]

