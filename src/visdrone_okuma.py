"""VisDrone2019-DET etiket dosyalarını okuma fonksiyonları."""

from pathlib import Path

import pandas as pd
from tqdm import tqdm

# VisDrone kategori numaraları ve adları
SINIF_ADLARI = {
    0: "ignored regions",
    1: "pedestrian",
    2: "people",
    3: "bicycle",
    4: "car",
    5: "van",
    6: "truck",
    7: "tricycle",
    8: "awning-tricycle",
    9: "bus",
    10: "motor",
    11: "others",
}

# Etiket satırındaki 8 alanın sırası
SUTUNLAR = ["x", "y", "w", "h", "score", "category", "truncation", "occlusion"]


def etiket_oku(etiket_yolu):
    """Tek bir etiket dosyasını okur, her kutu bir satır olacak şekilde DataFrame döndürür."""
    kutular = []
    with open(etiket_yolu, encoding="utf-8") as f:
        for satir in f:
            satir = satir.strip().rstrip(",")
            if not satir:
                continue
            degerler = [int(v) for v in satir.split(",")[:8]]
            kutular.append(degerler)

    df = pd.DataFrame(kutular, columns=SUTUNLAR)
    df["sinif"] = df["category"].map(SINIF_ADLARI)
    df["dosya"] = Path(etiket_yolu).stem
    return df


def bolum_oku(bolum_klasoru):
    """Bir bölümdeki (train/val/test-dev) tüm etiket dosyalarını okuyup tek tabloda birleştirir."""
    etiket_klasoru = Path(bolum_klasoru) / "annotations"
    dosyalar = sorted(etiket_klasoru.glob("*.txt"))
    tablolar = [etiket_oku(d) for d in tqdm(dosyalar, desc=etiket_klasoru.parent.name)]
    return pd.concat(tablolar, ignore_index=True)


if __name__ == "__main__":
    # Hızlı deneme: en küçük bölüm olan val'i oku
    df = bolum_oku("data/VisDrone2019-DET-val")
    print("Toplam kutu sayısı:", len(df))
    print("Görüntü sayısı:", df["dosya"].nunique())
    print(df["sinif"].value_counts())