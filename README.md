# İHA Görüntülerinde Derin Öğrenme Tabanlı Nesne Tespiti Yöntemlerinin Karşılaştırılması

**Ders:** Uygulamalı Yapay Zeka (Dönem Projesi)
**Öğrenci:** Betül Soyer – 241230016
**Bölüm:** Yapay Zeka ve Makine Öğrenmesi, Konya Teknik Üniversitesi

## Problem

Bu projede drone (İHA) kamerasıyla çekilmiş görüntülerde araç, yaya ve bisiklet gibi nesnelerin tespit edilmesi ele alınmaktadır. Yukarıdan çekilen görüntülerde nesneler çok küçük görünür, sahneler kalabalıktır ve bakış açısı sık değişir; bu da normal görüntüler için geliştirilen modellerin başarısını düşürür. Projede farklı derin öğrenme tabanlı nesne tespiti modelleri iki hazır İHA veri seti üzerinde eğitilip karşılaştırılacaktır.

## Veri Setleri

- **VisDrone2019-DET:** Tianjin Üniversitesi tarafından yayınlanan, Çin'in 14 şehrinde drone ile çekilmiş görüntülerden oluşan veri seti. 6.471 eğitim, 548 doğrulama ve 1.610 test görüntüsü, 10 nesne sınıfı içerir.
  - Kaynak: Zhu vd., "Detection and Tracking Meet Drones Challenge", IEEE TPAMI.
  - Bilgi: https://docs.ultralytics.com/datasets/detect/visdrone/
- **UAVDT:** Drone videolarından seçilmiş etiketli karelerden oluşan, araç tespiti ve takibi için hazırlanmış veri seti.
  - Kaynak: Du vd., "The Unmanned Aerial Vehicle Benchmark: Object Detection and Tracking", ECCV 2018.
  - Bağlantı: https://sites.google.com/view/daweidu/projects/uavdt

Veri setleri boyutları nedeniyle depoya eklenmemiştir; `data/` klasörüne indirilerek kullanılır.

## Kapsam Değişikliği

29 Eylül 2026'da yüklenen proje önerisinin konusu "çoklu İHA formasyon kontrolünde derin pekiştirmeli öğrenme algoritmalarının karşılaştırılması" idi. Faz 1 rapor şablonu hazır veri setlerinin analizini, ön işlenmesini ve aynı veri setlerini kullanan çalışmalarla karşılaştırma yapılmasını istemektedir. Pekiştirmeli öğrenme konusu hazır bir veri setine dayanmadığı için bu şartlar karşılanamamış ve proje, aynı alanda kalarak İHA görüntülerinde nesne tespitine çevrilmiştir. Değişiklik 31 Ekim 2026'da ders sorumlusuna e-posta ile bildirilmiş ve onaylanmıştır.

## Proje Yapısı

    uyz_uav_object_detection/
    ├── data/          # veri setleri (depoya eklenmez)
    ├── notebooks/     # veri analizi ve ön işleme defterleri
    ├── src/           # veri okuma ve dönüştürme kodları
    └── reports/       # grafikler, literatür tablosu ve raporlar

## Proje Durumu

- [ ] Faz 1: veri seti analizi, ön işleme, literatür taraması ve yöntem seçimi (sunum: 10 Kasım 2026)
- [ ] Faz 2: model eğitimi, değerlendirme ve makale formatında rapor
