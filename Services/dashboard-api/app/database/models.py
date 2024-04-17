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
    
class ProduksiSusu(Base):
    
    __tablename__ = 'produksi_susu'
    
    id = Column(Integer, primary_key=True, index=True)
    tgl_produksi = Column(Date)
    jumlah = Column(Float)
    satuan = Column(String)
    sumber_pasokan = Column(String)