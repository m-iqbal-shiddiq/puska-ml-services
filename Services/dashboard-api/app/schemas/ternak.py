from typing import List, Optional
from pydantic import BaseModel


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
    region: Optional[str]
    title: str
    populasi: int

# Ini harusnya apa ya?

# class JumlahPerahDewasa(BaseModel):
#     produksi: float 
#     distribusi: float

# class JumlahPerahAnakan(BaseModel):
#     produksi: float 
#     distribusi: float

# class JumlahPedagingDewasa(BaseModel):
#     produksi: float 
#     distribusi: float

# class JumlahPedagingAnakan(BaseModel):
#     produksi: float 
#     distribusi: float

# class RingkasanPopulasi(BaseModel): 
#     jumlah_perah_dewasa: JumlahPerahDewasa
#     jumlah_perah_anakan: JumlahPerahAnakan
#     jumlah_pedaging_dewasa: JumlahPedagingDewasa
#     jumlah_pedaging_anakan: JumlahPedagingAnakan
    
class RingkasanPopulasi(BaseModel): 
    jumlah_perah_dewasa: int
    jumlah_perah_anakan: int
    jumlah_pedaging_dewasa: int
    jumlah_pedaging_anakan: int

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
    total_populasi: int


# Main Model
class TernakMasterData(BaseModel):
    ternak_potong: TernakPotong
    daging_ternak: DagingTernak
    susu_segar: SusuSegar
    pro_dis_ternak_potong: List[ProduksiDistribusiTernakPotong]
    pro_dis_daging_ternak: List[ProduksiDistribusiDagingTernak]
    pro_dis_susu_segar: List[ProduksiDistribusiSusuSegar]
    sebaran_populasi_all: List[SebaranPopulasi]
    ringkasan_populasi: RingkasanPopulasi
    table: List[TablePopulasi]
    
    