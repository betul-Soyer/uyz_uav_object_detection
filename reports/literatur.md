# Literatür Taraması

## Aynı veri setlerini kullanan çalışmalar

| # | Çalışma | Yayın | Veri seti | Yöntem | Raporlanan sonuç (COCO AP, %) | DOI |
|---|---|---|---|---|---|---|
| 1 | Yang vd. – ClusDet | ICCV 2019 | VisDrone (val), UAVDT, DOTA | Nesne kümelerini öneren alt ağ (CPNet) + kümelerin ölçeğini tahmin eden alt ağ (ScaleNet) + kırpılan küme bölgelerinde ayrıntılı tespit (DetecNet); Faster R-CNN tabanlı | VisDrone val: 26,7 (ResNet-50), 28,4 (ResNeXt-101); UAVDT: 13,7 (ResNet-50) | 10.1109/ICCV.2019.00840 |
| 2 | Li vd. – DMNet | CVPRW 2020 | VisDrone (val), UAVDT | Nesne yoğunluk haritası (MCNN) ile kırpma bölgelerinin belirlenmesi; Faster R-CNN + FPN ile tüm görüntü ve kırpıntılarda tespit, sonuçların birleştirilmesi | VisDrone val: 28,2 (ResNet-50), 29,4 (ResNeXt-101); UAVDT: 14,7 (ResNet-50). Aynı çalışmada temel Faster R-CNN + FPN: VisDrone val 21,4, UAVDT 11,0; SSD: UAVDT 9,3 | 10.1109/CVPRW50498.2020.00103 |
| 3 | Deng vd. – GLSAN | IEEE TIP 2021 | VisDrone2019-DET (val), UAVDT | Global-yerel tespit ağı + kalabalık bölgeleri uyarlanabilir seçen algoritma (SARSA) + kırpılan bölgeleri büyüten süper çözünürlük ağı (LSRN) | VisDrone val: 30,7; UAVDT: 17,0 (ResNet-50)* | 10.1109/TIP.2020.3045636 |
| 4 | Zhu vd. – TPH-YOLOv5 | ICCVW 2021 | VisDrone2021-DET | YOLOv5'e küçük nesneler için ek tahmin başlığı, Transformer tahmin başlıkları ve CBAM dikkat modülü eklenmesi | DET-test-challenge: 39,18; YOLOv5 tabanına göre yaklaşık %7 iyileşme | 10.1109/ICCVW54120.2021.00312 |
| 5 | Akyon vd. – SAHI | ICIP 2022 | VisDrone, xView | Görüntüyü örtüşen dilimlere bölerek çıkarım (SAHI) ve dilimlerle ince ayar; herhangi bir dedektöre eklenebilen genel çerçeve | Dilimlemeli çıkarım FCOS / VFNet / TOOD için AP'yi sırasıyla %6,8 / %5,1 / %5,3; dilimlemeli ince ayarla birlikte toplam %12,7 / %13,4 / %14,5 artırmıştır | 10.1109/ICIP46576.2022.9897990 |

\* GLSAN değerleri, UFPMP-Det (Huang vd., AAAI 2022) ve AD-Det (2025) çalışmalarının karşılaştırma tablolarından alınmıştır; orijinal makaleden doğrulanmalıdır.

## Veri seti kaynakları

- Zhu vd., "Detection and Tracking Meet Drones Challenge", IEEE TPAMI, 2022. DOI: 10.1109/TPAMI.2021.3119563
- Du vd., "The Unmanned Aerial Vehicle Benchmark: Object Detection and Tracking", ECCV 2018, LNCS, ss. 375–391. DOI: 10.1007/978-3-030-01249-6_23

## Yöntemlerin analizi ve özeti

- **Ortak problem:** İncelenen çalışmaların tamamı iki zorluğa odaklanmaktadır: nesnelerin görüntüye göre çok küçük olması ve görüntü içinde düzensiz (kümeler halinde) dağılması. Bu, kendi EDA bulgularımızla örtüşmektedir (VisDrone'da kutuların %60–69'u, UAVDT test kümesinde %75'i 32² pikselden küçüktür).
- **Yaklaşım 1 – Kırpma / yakınlaştırma tabanlı yöntemler (ClusDet, DMNet, GLSAN, SAHI):** Görüntünün nesne yoğun bölgeleri kırpılıp daha yüksek çözünürlükte tekrar işlenir. ClusDet ve DMNet bölgeleri öğrenilen bir ağla seçerken, SAHI eğitim gerektirmeyen düzenli dilimleme kullanır ve mevcut her dedektöre eklenebilir.
- **Yaklaşım 2 – Mimari iyileştirme (TPH-YOLOv5):** Tek aşamalı dedektöre küçük nesneler için ek tahmin başlığı ve dikkat mekanizmaları eklenir.
- **Genel amaçlı dedektörlerin performansı düşüktür:** UAVDT'de SSD 9,3 AP, Faster R-CNN + FPN 11,0 AP elde ederken, kırpma tabanlı yöntemler 13,7–17,0 AP'ye ulaşmaktadır (DMNet ve GLSAN tabloları).
- **Değerlendirme protokolü:** VisDrone test kümesinin değerlendirme sunucusu erişilebilir olmadığından ClusDet, DMNet ve GLSAN sonuçlarını doğrulama (val) kümesinde raporlamıştır. UAVDT sonuçları test kümesinde verilmektedir. Tüm çalışmalar COCO AP (IoU 0,50–0,95), AP50 ve AP75 kullanmaktadır.
- **Dikkat edilmesi gereken fark:** Bu çalışmalarda UAVDT için 23.258 eğitim ve 15.069 test görüntüsü raporlanmaktadır. Bizim sayımımızda etiketli kare sayısı 23.829 (train) ve 16.580 (test) çıkmıştır. Farkın kaynağı (tespit görevinde kullanılan kare alt kümesinin tanımı) Faz 2'de incelenecek ve karşılaştırmalar bu fark belirtilerek yapılacaktır.
