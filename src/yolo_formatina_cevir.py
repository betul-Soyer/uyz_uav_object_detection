"""VisDrone ve UAVDT etiketlerini YOLO formatına çevirme."""

import shutil
from pathlib import Path

import numpy as np
from PIL import Image
from tqdm import tqdm

from src.visdrone_okuma import bolum_oku, SINIF_ADLARI as VISDRONE_SINIFLAR
from src.uavdt_okuma import uavdt_oku, bolum_haritasi, SINIF_ADLARI as UAVDT_SINIFLAR

VISDRONE_BOLUMLER = {
    "train": "VisDrone2019-DET-train",
    "val": "VisDrone2019-DET-val",
    "test": "VisDrone2019-DET-test-dev",
}


def yolo_satiri(sinif, x, y, w, h, gen, yuk):
    """Piksel kutusunu (sol üst x, y, genişlik, yükseklik) görüntü sınırına kırpar ve YOLO satırına çevirir.
    Kırpmadan sonra kutu kalmazsa None döndürür."""
    x1, y1 = max(x, 0), max(y, 0)
    x2, y2 = min(x + w, gen), min(y + h, yuk)
    if x2 <= x1 or y2 <= y1:
        return None
    cx = (x1 + x2) / 2 / gen
    cy = (y1 + y2) / 2 / yuk
    return f"{sinif} {cx:.6f} {cy:.6f} {(x2 - x1) / gen:.6f} {(y2 - y1) / yuk:.6f}"


def ornek_yaz(goruntu_yolu, kutular, hedef_goruntu, hedef_etiket):
    """Görüntüyü kopyalar, kutularını YOLO formatında .txt dosyasına yazar.
    (yazılan kutu sayısı, atılan kutu sayısı) döndürür."""
    with Image.open(goruntu_yolu) as img:
        gen, yuk = img.size
    satirlar = []
    for sinif, x, y, w, h in kutular:
        satir = yolo_satiri(sinif, x, y, w, h, gen, yuk)
        if satir is not None:
            satirlar.append(satir)
    shutil.copy2(goruntu_yolu, hedef_goruntu)
    hedef_etiket.write_text("".join(s + "\n" for s in satirlar), encoding="utf-8")
    return len(satirlar), len(kutular) - len(satirlar)


def yaml_yaz(hedef_kok, siniflar):
    """Ultralytics'in okuyacağı veri seti tanım dosyasını (veri.yaml) yazar."""
    hedef_kok = Path(hedef_kok).resolve()
    satirlar = [
        f"path: {hedef_kok.as_posix()}",
        "train: images/train",
        "val: images/val",
        "test: images/test",
        "names:",
    ]
    satirlar += [f"  {i}: {ad}" for i, ad in enumerate(siniflar)]
    (hedef_kok / "veri.yaml").write_text("\n".join(satirlar) + "\n", encoding="utf-8")


def klasorleri_hazirla(hedef_kok, bolum):
    img = Path(hedef_kok) / "images" / bolum
    lbl = Path(hedef_kok) / "labels" / bolum
    img.mkdir(parents=True, exist_ok=True)
    lbl.mkdir(parents=True, exist_ok=True)
    return img, lbl


def visdrone_cevir(veri_kok, hedef_kok):
    """VisDrone'un üç bölümünü YOLO formatına çevirir; bölüm başına özet listesi döndürür."""
    ozet = []
    for bolum, klasor_adi in VISDRONE_BOLUMLER.items():
        kaynak = Path(veri_kok) / klasor_adi
        df = bolum_oku(kaynak)
        kutu_once = len(df)

        df = df[df["category"].between(1, 10)].copy()
        df["yolo_sinif"] = df["category"] - 1
        gruplar = {
            dosya: list(g[["yolo_sinif", "x", "y", "w", "h"]].itertuples(index=False, name=None))
            for dosya, g in df.groupby("dosya")
        }

        img_hedef, lbl_hedef = klasorleri_hazirla(hedef_kok, bolum)
        goruntuler = sorted((kaynak / "images").glob("*.jpg"))
        yazilan = gecersiz = 0
        for yol in tqdm(goruntuler, desc=f"VisDrone {bolum}"):
            y, a = ornek_yaz(yol, gruplar.get(yol.stem, []),
                             img_hedef / yol.name, lbl_hedef / f"{yol.stem}.txt")
            yazilan += y
            gecersiz += a

        ozet.append({
            "veri seti": "VisDrone", "bölüm": bolum,
            "görüntü (önce)": len(goruntuler), "görüntü (sonra)": len(goruntuler),
            "kutu (önce)": kutu_once,
            "atılan: ignored/others": kutu_once - len(df),
            "atılan: geçersiz kutu": gecersiz,
            "atılan: etiketsiz kare": 0,
            "kutu (sonra)": yazilan,
        })

    yaml_yaz(hedef_kok, [VISDRONE_SINIFLAR[i] for i in range(1, 11)])
    return ozet


def uavdt_val_dizileri(uavdt_kok, adet=6, tohum=42):
    """Train dizilerinden doğrulama için rastgele dizi seçer. Tek yüksek irtifa dizisi train'de kalır."""
    adaylar = []
    for dosya in sorted((Path(uavdt_kok) / "M_attr" / "train").glob("*_attr.txt")):
        degerler = [int(v) for v in dosya.read_text().strip().split(",")]
        if degerler[5] == 0:  # 6. değer high-alt
            adaylar.append(dosya.name[:5])
    rng = np.random.default_rng(tohum)
    return sorted(rng.choice(adaylar, size=adet, replace=False).tolist())


def uavdt_cevir(uavdt_kok, hedef_kok, adim=10, val_adet=6):
    """UAVDT-M'yi YOLO formatına çevirir: dizi bazında val ayırma, train/val'de adım örnekleme,
    etiketsiz karelerin atılması. Bölüm başına özet listesi ve val dizilerini döndürür."""
    df = uavdt_oku(uavdt_kok)
    df["yolo_sinif"] = df["category"] - 1

    harita = bolum_haritasi(uavdt_kok)
    val_diziler = uavdt_val_dizileri(uavdt_kok, val_adet)
    for dizi in val_diziler:
        harita[dizi] = "val"

    gruplar = {
        anahtar: list(g[["yolo_sinif", "x", "y", "w", "h"]].itertuples(index=False, name=None))
        for anahtar, g in df.groupby(["dizi", "frame"])
    }

    sayac = {b: {"dizi": 0, "kare_once": 0, "kare_sonra": 0, "kutu_once": 0,
                 "kutu_sonra": 0, "etiketsiz": 0, "gecersiz": 0} for b in ["train", "val", "test"]}
    klasorler = {b: klasorleri_hazirla(hedef_kok, b) for b in ["train", "val", "test"]}

    for dizi, bolum in tqdm(sorted(harita.items()), desc="UAVDT"):
        s = sayac[bolum]
        img_hedef, lbl_hedef = klasorler[bolum]
        kareler = sorted((Path(uavdt_kok) / "UAV-benchmark-M" / dizi).glob("*.jpg"))
        s["dizi"] += 1
        s["kare_once"] += len(kareler)
        s["kutu_once"] += int((df["dizi"] == dizi).sum())

        secilen = kareler if bolum == "test" else kareler[::adim]
        for yol in secilen:
            kare_no = int(yol.stem[3:])  # "img000001" -> 1
            kutular = gruplar.get((dizi, kare_no))
            if not kutular:
                s["etiketsiz"] += 1
                continue
            ad = f"{dizi}_{yol.stem}"
            y, a = ornek_yaz(yol, kutular, img_hedef / f"{ad}.jpg", lbl_hedef / f"{ad}.txt")
            s["kare_sonra"] += 1
            s["kutu_sonra"] += y
            s["gecersiz"] += a

    ozet = []
    for bolum in ["train", "val", "test"]:
        s = sayac[bolum]
        ozet.append({
            "veri seti": "UAVDT", "bölüm": bolum,
            "görüntü (önce)": s["kare_once"], "görüntü (sonra)": s["kare_sonra"],
            "kutu (önce)": s["kutu_once"],
            "atılan: ignored/others": 0,
            "atılan: geçersiz kutu": s["gecersiz"],
            "atılan: etiketsiz kare": s["etiketsiz"],
            "kutu (sonra)": s["kutu_sonra"],
        })

    yaml_yaz(hedef_kok, [UAVDT_SINIFLAR[i] for i in range(1, 4)])
    return ozet, val_diziler