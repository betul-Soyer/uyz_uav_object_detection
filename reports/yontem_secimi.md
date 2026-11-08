# Yöntem ve Model Seçimi

İki veri seti (VisDrone2019-DET, UAVDT-M) ayrı ayrı, kendi sınıflarıyla (10 ve 3 sınıf) eğitilecektir. Model seçimi, EDA bulgularına (küçük nesne baskınlığı, kalabalık sahneler, sınıf dengesizliği) ve literatür taramasına dayanmaktadır.

| # | Model | Tür | Veri setine uygunluk ve gerekçe |
|---|---|---|---|
| 1 | YOLOv8s | Tek aşamalı (Ultralytics) | **Uygun.** Temel model; hızlı, çok ölçekli (P3–P5) tahmin başlıkları. |
| 2 | YOLOv8s + SAHI | Tek aşamalı + dilimlemeli çıkarım | **Uygun.** Küçük nesneler için dilimleme; VisDrone üzerindeki katkısı literatürde gösterilmiştir (Akyon vd., 2022). EDA'da kutuların %60–75'inin küçük olması bu seçimi gerekçelendirir. |
| 3 | Faster R-CNN + FPN (ResNet-50) | İki aşamalı (torchvision) | **Kısmen uygun.** ClusDet ve DMNet'in temel dedektörüdür; literatürde VisDrone val için 21,4, UAVDT için 11,0 AP taban sonucu vardır → doğrudan karşılaştırma imkânı. |
| 4 | SSD300 (VGG16) | Tek aşamalı, düşük çözünürlüklü giriş (torchvision) | **Uygun değil.** 300×300 giriş: 1400 piksellik VisDrone görüntüsü ~4,7 kat küçülür, ~15 piksellik tipik nesne ~3 piksele iner. Literatürde UAVDT'de 9,3 AP ile en düşük sonuçlardandır. |

## Değerlendirme

- **Metrikler:** COCO AP (IoU 0,50–0,95), AP50, AP75, AP_small / AP_medium / AP_large, precision, recall, sınıf bazında AP, çıkarım hızı (FPS).
- **Değerlendirme kümeleri:** VisDrone için val (literatürle aynı protokol) ve test-dev; UAVDT için test kümesinin tamamı.
- **Karşılaştırma:** Sonuçlar literatür tablosundaki (reports/literatur.md) çalışmalarla karşılaştırılacaktır.