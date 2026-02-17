
from fastapi import FastAPI, UploadFile, File, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uvicorn
import shutil
import os
import json
from datetime import datetime
from typing import Optional

# Klasör Yapılandırması
UPLOAD_DIR = "server_data"
if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

app = FastAPI(title="5G Akıllı Yol Güvenliği - Komuta Merkezi")

# Statik dosyalar (Yüklenen resimlere erişim için)
app.mount("/static", StaticFiles(directory=UPLOAD_DIR), name="static")

# Basit HTML Dashboard (Jinja2 gerekmeden string olarak)
html_dashboard = """
<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>5G KOMUTA MERKEZİ - TEKNOFEST 2026</title>
    <meta http-equiv="refresh" content="5"> <!-- 5 Saniyede bir yenile -->
    <style>
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #0d1117; color: #c9d1d9; margin: 0; padding: 20px; }
        h1 { color: #58a6ff; text-align: center; border-bottom: 2px solid #30363d; padding-bottom: 10px; }
        .grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 20px; margin-top: 20px; }
        .card { background-color: #161b22; border: 1px solid #30363d; border-radius: 6px; overflow: hidden; transition: transform 0.2s; }
        .card:hover { transform: translateY(-5px); border-color: #8b949e; }
        .card img { width: 100%; height: 200px; object-fit: cover; border-bottom: 1px solid #30363d; }
        .info { padding: 15px; }
        .badge { display: inline-block; padding: 2px 8px; border-radius: 12px; font-size: 12px; font-weight: bold; margin-bottom: 5px; }
        .badge-danger { background-color: #da3633; color: white; }
        .badge-warning { background-color: #d29922; color: black; }
        .meta { font-size: 13px; color: #8b949e; margin-top: 10px; }
        .stat-box { background: #21262d; padding: 10px; border-radius: 4px; text-align: center; margin-bottom: 20px; }
    </style>
</head>
<body>
    <h1>🛰️ 5G AKILLI YOL GÜVENLİĞİ - MERKEZ</h1>
    
    <div class="stat-box">
        <h3>CANLI İHLAL AKIŞI (5G STREAM)</h3>
        <p>Sistem Durumu: <span style="color:#3fb950">ONLINE</span> | Bağlı Araçlar: 1</p>
    </div>

    <div class="grid" id="violations">
        <!-- İhlaller buraya gelecek -->
        {% for v in violations %}
        <div class="card">
            <img src="/static/{{ v.image_path }}" alt="Kanıt Fotoğrafı">
            <div class="info">
                <span class="badge badge-danger">HIZ İHLALİ</span>
                <h3 style="margin: 5px 0">{{ v.speed }} km/s</h3>
                <p style="margin: 0">Limit: {{ v.limit }} km/s</p>
                <div class="meta">
                    <div>Araç ID: {{ v.vehicle_id }}</div>
                    <div>Lokasyon: {{ v.location }}</div>
                    <div>Zaman: {{ v.timestamp }}</div>
                </div>
            </div>
        </div>
        {% endfor %}
    </div>
</body>
</html>
"""

@app.get("/", response_class=HTMLResponse)
async def dashboard():
    # Klasördeki dosyaları oku ve listele
    violations = []
    files = sorted(os.listdir(UPLOAD_DIR), reverse=True)
    
    for f in files:
        if f.endswith(".json"):
            try:
                with open(os.path.join(UPLOAD_DIR, f), "r", encoding="utf-8") as jf:
                    data = json.load(jf)
                    # Resim yolunu web path'e çevir
                    img_name = data["record_id"] + ".jpg"
                    if os.path.exists(os.path.join(UPLOAD_DIR, img_name)):
                        violations.append({
                            "image_path": img_name,
                            "speed": data["measurements"]["final_speed"],
                            "limit": data["limit"],
                            "vehicle_id": data["vehicle_id"],
                            "location": data["location"],
                            "timestamp": data["timestamp"]
                        })
            except Exception as e:
                print(f"Veri okuma hatası: {e}")
                
    # Basit bir template render işlemi (Jinja kullanmadan manuel replace)
    # Gerçek Jinja2 kullanmak daha temiz olurdu ama dependency azaltmak için:
    # (Yukarıdaki HTML'de {% for %} döngüsü var, bunu Jinja2 ile render etmeliyiz)
    # Neyse ki Jinja2 FastAPI ile geliyor (starlette üzerinden).
    
    from jinja2 import Template
    t = Template(html_dashboard)
    return t.render(violations=violations)

@app.post("/api/violation")
async def upload_violation(
    request: Request,
    file: UploadFile = File(...),
    jsonData: str = Form(...)
):
    """
    Radar sisteminden gelen ihlal verisini karşılar.
    """
    print(f"📡 [5G] Veri Alındı: {file.filename}")
    
    try:
        data = json.loads(jsonData)
        
        # Dosya isimlerini oluştur
        base_name = data["record_id"]
        img_path = os.path.join(UPLOAD_DIR, f"{base_name}.jpg")
        json_path = os.path.join(UPLOAD_DIR, f"{base_name}.json")
        
        # 1. Fotoğrafı Kaydet
        with open(img_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
            
        # 2. JSON Verisini Kaydet
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
            
        return {"status": "success", "message": "Violation received at HQ", "id": base_name}
        
    except Exception as e:
        print(f"❌ HATA: {str(e)}")
        return {"status": "error", "message": str(e)}

if __name__ == "__main__":
    # Tüm IP'lerden erişime aç (0.0.0.0) böylece telefon hotspot'undan da bağlanılabilir
    uvicorn.run(app, host="0.0.0.0", port=8000)
