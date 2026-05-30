const express = require('express');
const axios = require('axios');
const path = require('path');

const app = express();
const PORT = process.env.PORT || 3000;

// Setup EJS sebagai template engine
app.set('view engine', 'ejs');
app.set('views', path.join(__dirname, 'views'));

// Fungsi pembuat Headers API
function getBaseHeaders(clsignature) {
    return {
        "accept": "application/json",
        "accept-language": "zh-cn",
        "appid": "kopikenangan",
        "appsflyer_id": "1780137547376-7149569020529056668",
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
    };
}

// Route Halaman Utama (Daftar Toko)
app.get('/', async (req, res) => {
    const url = "https://apps.kopikenangan.com/kk-api-kopikenangan/api/store/query_pageable_store";
    const headers = getBaseHeaders("224a017a62a28e838ecfa60840cd2d9e2bb2900402f0040dad75a14756720ed7");
    const payload = {
        "fuzzy_name": "",
        "lat": -6.2147222,
        "lng": 106.8450012,
        "deliverable": 0,
        "order_type": [],
        "page": { "page_index": 1, "page_size": 100000 },
        "brand_codes": [],
        "disable_delivery_distance_limit": true
    };

    try {
        const response = await axios.post(url, payload, { headers });
        const stores = response.data?.data?.store || [];
        res.render('index', { stores });
    } catch (error) {
        console.error("Gagal mengambil data toko:", error.message);
        res.render('index', { stores: [] });
    }
});

// Route Halaman Menu
app.get('/menu/:storeCode', async (req, res) => {
    const storeCode = req.params.storeCode;
    const url = "https://apps.kopikenangan.com/kk-api-kopikenangan/api/product/query_product_menu";
    const headers = getBaseHeaders("543921ba021628693d9994d922925707d13dc43e29aee1ececc151e47df62c4c");
    const payload = {
        "store_code": storeCode,
        "voucher_code": null,
        "product_without_promo": true,
        "display_combo_v2": true,
        "for_shipping": false,
        "display_merchandise_product": true,
        "display_mix_match_optional": true,
        "support_discount_percentage": true
    };

    try {
        const response = await axios.post(url, payload, { headers });
        const menuGroups = response.data?.data?.menu_groups || [];
        res.render('menu', { storeCode, menuGroups });
    } catch (error) {
        console.error("Gagal mengambil data menu:", error.message);
        res.render('menu', { storeCode, menuGroups: [] });
    }
});

// Jalankan Server
app.listen(PORT, () => {
    console.log(`Server berjalan di http://localhost:${PORT}`);
});