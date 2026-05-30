from flask import Flask, render_template_string
import requests

app = Flask(__name__)

# ==========================================
# 1. TEMPLATE HTML (TAMPILAN WEBSITE)
# ==========================================

# Template Halaman Utama (Daftar Toko)
HTML_INDEX = """
<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Cek Kopi Kenangan</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body class="bg-light">
    <div class="container py-5">
        <h1 class="text-center mb-4">📍 Status Toko Kopi Kenangan</h1>
        <div class="row">
            {% for store in stores %}
            <div class="col-md-6 mb-3">
                <div class="card shadow-sm">
                    <div class="card-body">
                        <h5 class="card-title">{{ store.name }}</h5>
                        {% if store.is_open %}
                            <p class="text-success fw-bold mb-1">✅ BUKA (Tutup jam {{ store.real_close_time }})</p>
                            <a href="/menu/{{ store.code }}" class="btn btn-primary btn-sm mt-2">Lihat Menu</a>
                        {% else %}
                            <p class="text-danger fw-bold mb-1">❌ TUTUP</p>
                            <small class="text-muted">{{ store.open_status }}</small>
                            <br>
                            <button class="btn btn-secondary btn-sm mt-2" disabled>Lihat Menu</button>
                        {% endif %}
                    </div>
                </div>
            </div>
            {% endfor %}
        </div>
    </div>
</body>
</html>
"""

# Template Halaman Menu
HTML_MENU = """
<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Menu - {{ store_code }}</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body class="bg-light">
    <div class="container py-5">
        <a href="/" class="btn btn-outline-dark mb-4">⬅ Kembali ke Daftar Toko</a>
        <h2 class="mb-4">☕ Menu di Toko: {{ store_code }}</h2>
        
        {% for kategori in menu_groups %}
        <div class="card mb-4 shadow-sm">
            <div class="card-header bg-dark text-white fw-bold">
                {{ kategori.group_name }}
            </div>
            <ul class="list-group list-group-flush">
                {% for item in kategori.menu_products %}
                <li class="list-group-item d-flex justify-content-between align-items-center">
                    <div>
                        <span class="fw-semibold">{{ item.name }}</span><br>
                        <small class="text-muted">Rp {{ "{:,}".format(item.price).replace(',', '.') }}</small>
                    </div>
                    {% if item.is_sold_out %}
                        <span class="badge bg-danger rounded-pill">Habis</span>
                    {% else %}
                        <span class="badge bg-success rounded-pill">Tersedia</span>
                    {% endif %}
                </li>
                {% endfor %}
            </ul>
        </div>
        {% endfor %}
    </div>
</body>
</html>
"""

# ==========================================
# 2. KONFIGURASI API & HEADERS
# ==========================================

# ⚠️ GANTI DENGAN TOKEN ASLI DARI HTTP TOOLKIT
TOKEN_AUTHORIZATION = "GANTI_DENGAN_TOKEN_ASLI_YANG_DISEMBUNYIKAN"

def get_base_headers(clsignature):
    return {
        "accept": "application/json",
        "accept-language": "zh-cn",
        "appid": "kopikenangan",
        "appsflyer_id": "1780137547376-7149569020529056668",
        "authorization": TOKEN_AUTHORIZATION, 
        "clsignature": clsignature,
        "deviceid": "b0cc5c0c5f2bc222",
        "devicetype": "Android",
        "gopay_v2": "true",
        "gopay_v3": "true",
        "islogin": "false",
        "language": "id",
        "sign_version": "256",
        "supportsharebuy": "true",
        "timezone": "25200",
        "user-agent": "Dart/3.10 (dart:io)",
        "version": "126.05.21",
        "versioncode": "365",
        "wtoken": "0005_9E7877C6B8348FE8617F5A32F87DAD9B34C93C75A568A9EFAFAC4208A4ACFBCE106EF8CB63DAD49F42EB02C71FC7C28E7272A7EC2114GHYXdFfZvLqNkCP6g6hT9eVy9VdTHOAcUIlYKxkqZhaMM5aMkHe4eqoM7Buopr7p0DsmkDBo8zO4e/FErOB+VwCKvGwMaN/NcWjwspH917PY3a2SoDfQkCezmvdjqoi5IoXa8dl3nXmWEB5DOrmmGgeUO6YtCdB3GCtk6qS7E3DIRY1iH0gPgszxXnTte23WHtpI0jZmIE0241dIM3OD5pll01Wo+u5aTbhR8djGw21mZuJ73VFZN4zgpS13vHGgxmk+hU1PtSYH/h2wkkefL8NwbAINRAX9XJLAhk8iWiQJ2pYyg1qVsACYyB+RUFK4bKTNjJFxpCuh+k+tdEmofGn7tmITlWx8AaoZ23agDehf5xMV5vY6cgvj/ra67A3eAL+A0s0/HkY0lgVePPdMrg==_fHw=_"
    }

# ==========================================
# 3. ROUTING FLASK (LOGIKA BACKEND)
# ==========================================

@app.route("/")
def home():
    url = "https://apps.kopikenangan.com/kk-api-kopikenangan/api/store/query_pageable_store"
    # Menggunakan clsignature spesifik untuk API Store (berdasarkan datamu)
    headers = get_base_headers("224a017a62a28e838ecfa60840cd2d9e2bb2900402f0040dad75a14756720ed7")
    payload = {
        "fuzzy_name": "",
        "lat": -6.2147222,
        "lng": 106.8450012,
        "deliverable": 0,
        "order_type": [],
        "page": {"page_index": 1, "page_size": 100},
        "brand_codes": [],
        "disable_delivery_distance_limit": True
    }
    
    response = requests.post(url, headers=headers, json=payload)
    stores = []
    if response.status_code == 200:
        stores = response.json().get("data", {}).get("store", [])
        
    # Mengirim data JSON toko ke template HTML_INDEX
    return render_template_string(HTML_INDEX, stores=stores)


@app.route("/menu/<store_code>")
def menu(store_code):
    url = "https://apps.kopikenangan.com/kk-api-kopikenangan/api/product/query_product_menu"
    # Menggunakan clsignature spesifik untuk API Menu (berdasarkan datamu)
    headers = get_base_headers("543921ba021628693d9994d922925707d13dc43e29aee1ececc151e47df62c4c")
    payload = {
        "store_code": store_code,
        "voucher_code": None,
        "product_without_promo": True,
        "display_combo_v2": True,
        "for_shipping": False,
        "display_merchandise_product": True,
        "display_mix_match_optional": True,
        "support_discount_percentage": True
    }
    
    response = requests.post(url, headers=headers, json=payload)
    menu_groups = []
    if response.status_code == 200:
        menu_groups = response.json().get("data", {}).get("menu_groups", [])
        
    # Mengirim data JSON menu ke template HTML_MENU
    return render_template_string(HTML_MENU, store_code=store_code, menu_groups=menu_groups)

# ==========================================
# 4. MENJALANKAN SERVER
# ==========================================
if __name__ == "__main__":
    app.run()