from datetime import datetime
from sqlalchemy import Column, String, Enum, Float,\
                       Integer, Numeric, Date, Boolean, DateTime, \
                       ForeignKey, Text, JSON
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

class DimWaktu(Base):
    
    __tablename__ = 'dim_waktu'
    
    id = Column(Integer, primary_key=True)
    tanggal = Column(Date)
    tahun = Column(Integer)
    bulan = Column(Integer)
    hari = Column(Integer)
    
    
class DimLokasi(Base):

    __tablename__ = 'dim_lokasi'
    
    id = Column(Integer, primary_key=True)
    provinsi = Column(String)
    kabupaten_kota = Column(String)
    kecamatan = Column(String)
    longitude = Column(Float)
    latitude = Column(Float)
    

class DimMitraBisnis(Base):
    
    __tablename__ = 'dim_mitra_bisnis'
    
    id = Column(Integer, primary_key=True)
    id_unit_peternak = Column(Integer)
    nama_mitra_bisnis = Column(String)
    kategori_mitra_bisnis = Column(String)


class FactDistribusi(Base):
    
    __tablename__ = 'fact_distribusi'
    
    id_waktu = Column(Integer, primary_key=True)
    id_lokasi = Column(Integer, primary_key=True)
    id_unit_peternak = Column(Integer, primary_key=True)
    id_mitra_bisnis = Column(Integer, primary_key=True)
    id_jenis_produk = Column(Integer, primary_key=True)
    jumlah_distribusi = Column(Float)
    harga_minimum = Column(Float)
    harga_maximum = Column(Float)
    harga_rata_rata = Column(Float)
    jumlah_penjualan = Column(Float)
    created_dt = Column(DateTime)
    modified_dt = Column(DateTime)
    
    
class FactProduksi(Base):
    
    __tablename__ = 'fact_produksi'
    
    id_waktu = Column(Integer, primary_key=True)
    id_lokasi = Column(Integer, primary_key=True)
    id_unit_peternak = Column(Integer, primary_key=True)
    id_jenis_produk = Column(Integer, primary_key=True)
    id_sumber_pasokan = Column(Integer, primary_key=True)
    jumlah_produksi = Column(Float)
    created_dt = Column(DateTime)
    modified_dt = Column(DateTime)
    

# class DistribusiTernak(Base):
    
#     __tablename__ = 'distribusi_ternak'
    
#     id = Column(Integer, primary_key=True, index=True)
#     tgl_distribusi = Column(Date)
#     jumlah = Column(Float)
#     satuan = Column(String)
#     harga_berlaku = Column(Float)

# class ProduksiTernak(Base):
    
#     __tablename__ = 'produksi_ternak'
    
#     id = Column(Integer, primary_key=True, index=True)
#     tgl_produksi = Column(Date)
#     jumlah = Column(Float)
#     satuan = Column(String)
#     sumber_pasokan = Column(String)
    
# class DistribusiSusu(Base):
    
#     __tablename__ = 'distribusi_susu'
    
#     id = Column(Integer, primary_key=True, index=True)
#     tgl_distribusi = Column(Date)
#     jumlah = Column(Float)
#     satuan = Column(String)
#     harga_berlaku = Column(Float)
#     id_unit_ternak = Column(Integer, ForeignKey('unit_ternak.id'))
#     id_jenis_produk = Column(Integer, ForeignKey('jenis_produk.id'))
    
# class ProduksiSusu(Base):
    
#     __tablename__ = 'produksi_susu'
    
#     id = Column(Integer, primary_key=True, index=True)
#     tgl_produksi = Column(Date)
#     jumlah = Column(Float)
#     satuan = Column(String)
#     sumber_pasokan = Column(String)
#     id_unit_ternak = Column(Integer, ForeignKey('unit_ternak.id'))
#     id_jenis_produk = Column(Integer, ForeignKey('jenis_produk.id'))
    
# class UnitTernak(Base):
    
#     __tablename__ = 'unit_ternak'
    
#     id = Column(Integer, primary_key=True, index=True)
#     nama_unit = Column(String)
#     provinsi_id = Column(Integer)
#     kota_id = Column(Integer)
#     kecamatan_id = Column(Integer)
#     kelurahan_id = Column(Integer)
    