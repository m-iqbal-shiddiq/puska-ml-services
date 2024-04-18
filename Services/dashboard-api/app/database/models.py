from datetime import datetime
from sqlalchemy import Column, String, Enum, Float,\
                       Integer, Numeric, Date, Boolean, DateTime, \
                       ForeignKey, Text, JSON
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

class DistribusiTernak(Base):
    
    __tablename__ = 'distribusi_ternak'
    
    id = Column(Integer, primary_key=True, index=True)
    tgl_distribusi = Column(Date)
    jumlah = Column(Float)
    satuan = Column(String)
    harga_berlaku = Column(Float)

class ProduksiTernak(Base):
    
    __tablename__ = 'produksi_ternak'
    
    id = Column(Integer, primary_key=True, index=True)
    tgl_produksi = Column(Date)
    jumlah = Column(Float)
    satuan = Column(String)
    sumber_pasokan = Column(String)
    
class DistribusiSusu(Base):
    
    __tablename__ = 'distribusi_susu'
    
    id = Column(Integer, primary_key=True, index=True)
    tgl_distribusi = Column(Date)
    jumlah = Column(Float)
    satuan = Column(String)
    harga_berlaku = Column(Float)
    id_unit_ternak = Column(Integer, ForeignKey('unit_ternak.id'))
    id_jenis_produk = Column(Integer, ForeignKey('jenis_produk.id'))
    
class ProduksiSusu(Base):
    
    __tablename__ = 'produksi_susu'
    
    id = Column(Integer, primary_key=True, index=True)
    tgl_produksi = Column(Date)
    jumlah = Column(Float)
    satuan = Column(String)
    sumber_pasokan = Column(String)
    id_unit_ternak = Column(Integer, ForeignKey('unit_ternak.id'))
    id_jenis_produk = Column(Integer, ForeignKey('jenis_produk.id'))
    
class UnitTernak(Base):
    
    __tablename__ = 'unit_ternak'
    
    id = Column(Integer, primary_key=True, index=True)
    nama_unit = Column(String)
    provinsi_id = Column(Integer)
    kota_id = Column(Integer)
    kecamatan_id = Column(Integer)
    kelurahan_id = Column(Integer)
    