from typing import Optional, List
from pydantic import BaseModel

# Entity
# Sub Model
class SusuSegar(BaseModel):
    distribusi: int
    produksi: int

class SusuPasteurisasi(BaseModel):
    distribusi: int
    produksi: int

class SusuKefir(BaseModel):
    distribusi: int
    produksi: int

class Yogurt(BaseModel):
    distribusi: int
    produksi: int

class Keju(BaseModel):
    distribusi: int
    produksi: int

class PrediksiValue(BaseModel):
    label: str
    actual: Optional[int]
    predict: Optional[int]

class PersentaseProduksi(BaseModel):
    susu_segar: float
    susu_pasteurisasi: float
    susu_kefir: float
    yogurt: float

class PersentaseDistribusi(BaseModel):
    susu_segar: float
    susu_pasteurisasi: float
    susu_kefir: float
    yogurt: float

class ProduksiDistribusiSusuSegar(BaseModel):
    label: str
    produksi: int
    distribusi: int

class PermintaanSusuSegarPerMitra(BaseModel):
    label: str
    value: int

class HargaSusu(BaseModel):
    minimum: int
    maximum: int
    rata_rata: float

class SusuKabupatenData(BaseModel):
    susu_segar: SusuSegar
    susu_pasteurisasi: SusuPasteurisasi
    susu_kefir: SusuKefir
    yogurt: Yogurt
    keju: Keju
    prediksi: List[PrediksiValue]
    persentase_produksi: PersentaseProduksi
    persentase_distribusi: PersentaseDistribusi
    prod_dis_susu_segar: List[ProduksiDistribusiSusuSegar]
    permintaan_susu_segar_dari_mitra_all: List[PermintaanSusuSegarPerMitra]
    total_persentase_distribusi: float
    total_pendapatan: int
    harga_susu: HargaSusu


# Main Model
class SusuMasterData(BaseModel):
    year: Optional[int]
    data: Optional[SusuKabupatenData]