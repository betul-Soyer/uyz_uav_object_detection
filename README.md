# İHA Görüntülerinde Derin Öğrenme Tabanlı Nesne Tespiti Yöntemlerinin Karşılaştırılması

**Ders:** Uygulamalı Yapay Zeka (Dönem Projesi)
**Öğrenci:** Betül Soyer – 241230016
**Bölüm:** Yapay Zeka ve Makine Öğrenmesi, Konya Teknik Üniversitesi

## Problem

Bu projede drone (İHA) kamerasıyla çekilmiş görüntülerde araç, yaya ve bisiklet gibi nesnelerin tespit edilmesi ele alınmaktadır. Yukarıdan çekilen görüntülerde nesneler çok küçük görünür, sahneler kalabalıktır ve bakış açısı sık değişir; bu da normal görüntüler için geliştirilen modellerin başarısını düşürür. Projede farklı derin öğrenme tabanlı nesne tespiti modelleri iki hazır İHA veri seti üzerinde eğitilip karşılaştırılacaktır.

## Veri Setleri

- **VisDrone2019-DET:** Tianjin Üniversitesi tarafından yayınlanan, Çin'in 14 şehrinde drone ile çekilmiş görüntülerden oluşan veri seti. 6.471 eğitim, 548 doğrulama ve 1.610 test (test-dev) görüntüsü, 10 nesne sınıfı içerir.
  - Kaynak: Zhu vd., "Detection and Tracking Meet Drones Challenge", IEEE TPAMI.
  - İndirme: https://github.com/VisDrone/VisDrone-Dataset (Task 1: Object Detection in Images)
- **UAVDT (UAV-benchmark-M):** Drone videolarından alınmış etiketli karelerden oluşan araç tespiti ve takibi veri seti. Tespit için kullanılan M kısmı 50 video dizisinden (30 eğitim, 20 test) alınmış 40.735 kare içerir; sınıflar car, truck ve bus'tır.
  - Kaynak: Du vd., "The Unmanned Aerial Vehicle Benchmark: Object Detection and Tracking", ECCV 2018.
  - İndirme: https://sites.google.com/view/grli-uavdt/ (UAVDT-Benchmark-M: dataset, DET/MOT toolkit, Attributes)

Veri setleri boyutları nedeniyle depoya eklenmemiştir; `data/` klasörüne indirilerek kullanılır.

## Veri Analizi Özeti

| Özellik | VisDrone2019-DET | UAVDT-M |
|---|---|---|
| Görüntü sayısı | 6.471 / 548 / 1.610 (train / val / test-dev) | 24.143 / 16.592 kare (train / test) |
| Sınıf sayısı | 10 | 3 (car, truck, bus) |
| Kutu sayısı | 343.205 / 38.759 / 75.102 | 422.911 / 375.884 |
| Görüntü başına kutu | 47–71 | 18–23 |
| En büyük sınıfın payı | car %42 | car %93–96 |
| Renk | RGB | RGB |
| Çözünürlük | Değişken (480×360 – 2000×1500) | 1024×540 ve 960×540 |
| Küçük nesne (<32² piksel) oranı | %60–69 | %50 (train) / %75 (test) |
| Etiket durumu | Eksik/boş etiket yok | 326 kare etiketsiz |

Ayrıntılı analizler ve grafikler `notebooks/` klasöründeki defterlerde, grafiklerin kopyaları `reports/figures/` klasöründedir.

## Kapsam Değişikliği

29 Eylül 2026'da yüklenen proje önerisinin konusu "çoklu İHA formasyon kontrolünde derin pekiştirmeli öğrenme algoritmalarının karşılaştırılması" idi. Faz 1 rapor şablonu hazır veri setlerinin analizini, ön işlenmesini ve aynı veri setlerini kullanan çalışmalarla karşılaştırma yapılmasını istemektedir. Pekiştirmeli öğrenme konusu hazır bir veri setine dayanmadığı için bu şartlar karşılanamamış ve proje, aynı alanda kalarak İHA görüntülerinde nesne tespitine çevrilmiştir. Değişiklik 31 Ekim 2026'da ders sorumlusuna e-posta ile bildirilmiş ve onaylanmıştır.

## Proje Yapısı

```
uyz_uav_object_detection/
├── data/          # veri setleri (depoya eklenmez)
├── notebooks/     # veri analizi ve ön işleme defterleri
│   ├── 01_visdrone_eda.ipynb
│   └── 02_uavdt_eda.ipynb
├── src/           # veri okuma ve dönüştürme kodları
│   ├── visdrone_okuma.py
│   └── uavdt_okuma.py
└── reports/       # grafikler, literatür tablosu ve raporlar
    └── figures/
```

## Kurulum

```
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

Veri setleri yukarıdaki bağlantılardan indirilip `data/` altına açılır:
`data/VisDrone2019-DET-train`, `data/VisDrone2019-DET-val`, `data/VisDrone2019-DET-test-dev`, `data/UAVDT/`.

## Proje Durumu

- Faz 1 (sunum: 10 Kasım 2026)
  - [x] Veri setlerinin indirilmesi ve doğrulanması
  - [x] Veri okuma kodları
  - [x] Keşifsel veri analizi (VisDrone, UAVDT)
  - [ ] Ön işleme (YOLO formatı, sınıf eşleme, örnekleme)
  - [ ] Literatür taraması ve yöntem seçimi
- Faz 2: model eğitimi, değerlendirme ve makale formatında rapor