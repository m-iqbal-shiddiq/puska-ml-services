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
    
class DimUnitPeternakan(Base):
    
    __tablename__ = 'dim_unit_peternakan'
    
    id = Column(Integer, primary_key=True)
    id_lokasi = Column(Integer)
    nama_unit = Column(String)
    alamat = Column(String)
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
    id_unit_peternakan = Column(Integer, primary_key=True)
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
    id_unit_peternakan = Column(Integer, primary_key=True)
    id_jenis_produk = Column(Integer, primary_key=True)
    id_sumber_pasokan = Column(Integer, primary_key=True)
    jumlah_produksi = Column(Float)
    created_dt = Column(DateTime)
    modified_dt = Column(DateTime)
    
class FactPopulasi(Base):
    
    __tablename__ = 'fact_populasi'
    
    id_waktu = Column(Integer, primary_key=True)
    id_lokasi = Column(Integer, primary_key=True)
    id_peternakan = Column(Integer, primary_key=True)
    jenis_kelamin = Column(String)
    tipe_ternak = Column(String)
    tipe_usia = Column(String)
    jumlah_lahir = Column(Integer)
    jumlah_mati = Column(Integer)
    jumlah_masuk = Column(Integer)
    jumlah_keluar = Column(Integer)
    jumlah = Column(Integer)
    created_dt = Column(DateTime)
    modified_dt = Column(DateTime)
    