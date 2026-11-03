"""UAVDT (UAV-benchmark-M) etiket dosyalarını okuma fonksiyonları."""

from pathlib import Path

import pandas as pd
from tqdm import tqdm

# UAVDT kategori numaraları ve adları
SINIF_ADLARI = {1: "car", 2: "truck", 3: "bus"}

# *_gt_whole.txt satırındaki 9 alanın sırası
SUTUNLAR = [
    "frame", "target_id", "x", "y", "w", "h",
    "out_of_view", "occlusion", "category",
]


def bolum_haritasi(kok):
    """M_attr/train ve M_attr/test klasörlerinden {dizi_adı: bölüm} sözlüğü üretir."""
    harita = {}
    for bolum in ["train", "test"]:
        for dosya in sorted((Path(kok) / "M_attr" / bolum).glob("*_attr.txt")):
            dizi = dosya.name[:5]          # "M0101_attr.txt" -> "M0101"
            harita[dizi] = bolum
    return harita


def dizi_oku(kok, dizi):
    """Bir video dizisinin etiket dosyasını okur, her kutu bir satır olacak şekilde DataFrame döndürür."""
    gt_yolu = Path(kok) / "UAV-benchmark-MOTD_v1.0" / "GT" / f"{dizi}_gt_whole.txt"
    kutular = []
    with open(gt_yolu, encoding="utf-8") as f:
        for satir in f:
            satir = satir.strip().rstrip(",")
            if not satir:
                continue
            degerler = [int(v) for v in satir.split(",")[:9]]
            kutular.append(degerler)

    df = pd.DataFrame(kutular, columns=SUTUNLAR)
    df["sinif"] = df["category"].map(SINIF_ADLARI)
    df["dizi"] = dizi
    df["dosya"] = df["frame"].apply(lambda n: f"img{n:06d}")
    return df


def uavdt_oku(kok):
    """Bütün dizileri okuyup bölüm bilgisiyle birlikte tek tabloda birleştirir."""
    harita = bolum_haritasi(kok)
    tablolar = []
    for dizi, bolum in tqdm(harita.items(), desc="UAVDT"):
        t = dizi_oku(kok, dizi)
        t["bolum"] = bolum
        tablolar.append(t)
    return pd.concat(tablolar, ignore_index=True)


if __name__ == "__main__":
    KOK = "data/UAVDT"
    df = uavdt_oku(KOK)

    goruntu_sayisi = len(list((Path(KOK) / "UAV-benchmark-M").glob("*/*.jpg")))
    print("Toplam kare (görüntü) sayısı:", goruntu_sayisi)
    print("Toplam kutu sayısı:", len(df))
    print()
    print("Bölüm başına etiketli kare sayısı:")
    print(df.groupby("bolum").apply(lambda d: d[["dizi", "frame"]].drop_duplicates().shape[0]))
    print()
    print(df["sinif"].value_counts(dropna=False))