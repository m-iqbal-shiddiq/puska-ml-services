from typing import List, Optional
from pydantic import BaseModel


# Entity
# Sub Model
class TernakPotong(BaseModel):
    total_produksi: int
    total_distribusi: int
    persentase: float

class DagingTernak(BaseModel):
    total_produksi: int
    total_distribusi: int
    persentase: float

class SusuSegar(BaseModel):
    total_produksi: int
    total_distribusi: int
    persentase: float

class ProduksiDistribusiTernakPotong(BaseModel):
    label: str
    produksi: int
    distribusi: int

class ProduksiDistribusiDagingTernak(BaseModel):
    label: str
    produksi: int
    distribusi: int

class ProduksiDistribusiSusuSegar(BaseModel):
    label: str
    produksi: int
    distribusi: int

class SebaranPopulasi(BaseModel):
    region: Optional[str] #TODO: Revision (#1)
    title: str
    populasi: int

class SebaranPopulasiYearly(BaseModel):
    year: int
    sebaran_populasi: List[SebaranPopulasi]

class JumlahPerahDewasa(BaseModel):
    produksi: float
    distribusi: float

class JumlahPerahAnakan(BaseModel):
    produksi: float
    distribusi: float

class JumlahPedagingDewasa(BaseModel):
    produksi: float
    distribusi: float

class JumlahPedagingAnakan(BaseModel):
    produksi: float
    distribusi: float

class RingkasanPopulasi(BaseModel):
    jumlah_perah_dewasa: JumlahPerahDewasa
    jumlah_perah_anakan: JumlahPerahAnakan
    jumlah_pedaging_dewasa: JumlahPedagingDewasa
    jumlah_pedaging_anakan: JumlahPedagingAnakan

class TablePopulasi(BaseModel):
    wilayah: str
    perah_dewasa_jantan: int
    perah_dewasa_betina: int
    perah_anakan_jantan: int
    perah_anakan_betina: int
    pedaging_dewasa_jantan: int
    pedaging_dewasa_betina: int
    pedaging_anakan_jantan: int
    pedaging_anakan_betina: int


# Main Model
class TernakMasterData(BaseModel):
    ternak_potong: TernakPotong
    daging_ternak: DagingTernak
    susu_segar: SusuSegar
    pro_dis_ternak_potong: List[ProduksiDistribusiTernakPotong]
    pro_dis_daging_ternak: List[ProduksiDistribusiDagingTernak]
    pro_dis_susu_segar: List[ProduksiDistribusiSusuSegar]
    sebaran_populasi_all: List[SebaranPopulasiYearly]
    ringkasan_populasi: RingkasanPopulasi
    table: List[TablePopulasi]

"""
"sebaran_populasi_all": [
    {
        "year": 2023,
        "sebaran_populasi": [
            {
                "region": str,
                "label": str,
                "populasi: int,
            },
            {
                "region": str,
                "label": str,
                "populasi: int,
            }
        ]
    },
    {
        "year": 2024,
        "sebaran_populasi": [
            {
                "region": str,
                "label": str,
                "populasi: int,
            },
            {
                "region": str,
                "label": str,
                "populasi: int,
            }
        ]
    }
]
"""


