from datetime import datetime, timezone
from sqlalchemy import (BigInteger,
                        Column, 
                        DateTime,
                        ForeignKey,
                        Integer,
                        Numeric,
                        String)
from sqlalchemy.orm import relationship

from app.database.connection import Base

class DimWaktu(Base):
    __tablename__ = 'dim_waktu'
    
    id = Column(BigInteger, primary_key=True)
    tahun = Column(BigInteger)
    bulan = Column(BigInteger)
    minggu = Column(BigInteger)
    tanggal = Column(BigInteger)
    
    created_dt = Column(DateTime(timezone=False),
                        default=datetime.now(timezone.utc))
    modified_dt = Column(DateTime(timezone=False),
                        default=datetime.now(timezone.utc),
                        onupdate=datetime.now(timezone.utc))
    
    
class DimLokasi(Base):
    __tablename__ = 'dim_lokasi'
    
    id = Column(BigInteger, primary_key=True)
    provinsi = Column(String(100))
    kabupaten_kota = Column(String(100))
    
    created_dt = Column(DateTime(timezone=False),
                        default=datetime.now(timezone.utc))
    modified_dt = Column(DateTime(timezone=False),
                        default=datetime.now(timezone.utc),
                        onupdate=datetime.now(timezone.utc))
    
    
class DimUnitTernak(Base):
    __tablename__ = 'dim_unit_ternak'
    
    id = Column(BigInteger, primary_key=True)
    id_lokasi = Column(BigInteger, ForeignKey('dim_lokasi.id'))
    lokasi = relationship(('DimLokasi'))
    nama_unit = Column(String(100))
    longitude = Column(Numeric(precision=12, scale=10))
    latitude = Column(Numeric(precision=12, scale=10))
    
    created_dt = Column(DateTime(timezone=False),
                        default=datetime.now(timezone.utc))
    modified_dt = Column(DateTime(timezone=False),
                        default=datetime.now(timezone.utc),
                        onupdate=datetime.now(timezone.utc))
    

class FactProduksi(Base):
    __tablename__ = 'fact_produksi'
    
    id_waktu = Column(BigInteger, primary_key=True)
    id_lokasi = Column(BigInteger, primary_key=True)
    id_unit_ternak = Column(BigInteger, primary_key=True)
    id_jenis_produk = Column(BigInteger, primary_key=True)
    id_sumber_pasokan = Column(BigInteger, primary_key=True )
    jumlah_produksi = Column(BigInteger)
    
    created_dt = Column(DateTime(timezone=False),
                        default=datetime.now(timezone.utc))
    modified_dt = Column(DateTime(timezone=False),
                        default=datetime.now(timezone.utc),
                        onupdate=datetime.now(timezone.utc))


class PredSusu(Base):
    __tablename__ = 'pred_susu'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    id_waktu = Column(BigInteger, ForeignKey('dim_waktu.id'))
    waktu = relationship('DimWaktu')
    id_lokasi = Column(BigInteger)
    # id_lokasi = Column(BigInteger, ForeignKey('dim_lokasi.id'))
    # lokasi = relationship('DimLokasi')
    id_unit_ternak = Column(BigInteger, ForeignKey('dim_unit_ternak.id'))
    unit_ternak = relationship('DimUnitTernak')
    prediction = Column(Numeric(precision=10, scale=2))
    latency = Column(Numeric(precision=10, scale=2))
    mape = Column(Numeric(precision=10, scale=2))
    
    created_at = Column(DateTime(timezone=False),
                        default=datetime.now(timezone.utc))
    # modified_dt = Column(DateTime(timezone=False),
    #                     default=datetime.now(timezone.utc),
    #                     onupdate=datetime.now(timezone.utc))