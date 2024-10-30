from datetime import datetime, timezone
from sqlalchemy import (BigInteger,
                        Column, 
                        Date,
                        DateTime,
                        Float,
                        ForeignKey,
                        Integer,
                        Numeric,
                        String)
from sqlalchemy.orm import declarative_base


Base = declarative_base()

class DimWaktu(Base):
    
    __tablename__ = 'dim_waktu'
    
    id = Column(Integer, primary_key=True)
    tanggal = Column(Date)
    tahun = Column(Integer)
    bulan = Column(Integer)
    hari = Column(Integer)
    created_dt = Column(DateTime(timezone=False), default=datetime.now(timezone.utc))
    modified_dt = Column(DateTime(timezone=False), default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))
    
    
class DimLokasi(Base):

    __tablename__ = 'dim_lokasi'
    
    id = Column(Integer, primary_key=True)
    provinsi = Column(String)
    kabupaten_kota = Column(String)
    kecamatan = Column(String)
    created_dt = Column(DateTime(timezone=False), default=datetime.now(timezone.utc))
    modified_dt = Column(DateTime(timezone=False), default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))
    
    
class DimUnitPeternakan(Base):
    
    __tablename__ = 'dim_unit_peternakan'
    
    id = Column(Integer, primary_key=True)
    id_lokasi = Column(Integer)
    nama_unit = Column(String)
    alamat = Column(String)
    longitude = Column(Float)
    latitude = Column(Float)
    created_dt = Column(DateTime(timezone=False), default=datetime.now(timezone.utc))
    modified_dt = Column(DateTime(timezone=False), default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))

class FactProduksi(Base):
    
    __tablename__ = 'fact_produksi'
    
    id_waktu = Column(Integer, primary_key=True)
    id_lokasi = Column(Integer, primary_key=True)
    id_unit_peternakan = Column(Integer, primary_key=True)
    id_jenis_produk = Column(Integer, primary_key=True)
    id_sumber_pasokan = Column(Integer, primary_key=True)
    jumlah_produksi = Column(Float)
    created_dt = Column(DateTime(timezone=False), default=datetime.now(timezone.utc))
    modified_dt = Column(DateTime(timezone=False), default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))

    
class FactProduksiStream(Base):
        
    __tablename__ = 'fact_produksi_stream'
    
    id_waktu = Column(Integer, primary_key=True)
    id_lokasi = Column(Integer, primary_key=True)
    id_unit_peternakan = Column(Integer, primary_key=True)
    id_jenis_produk = Column(Integer, primary_key=True)
    id_sumber_pasokan = Column(Integer, primary_key=True)
    jumlah_produksi = Column(Float)
    created_dt = Column(DateTime)
    modified_dt = Column(DateTime)


class PredSusu(Base):
    
    __tablename__ = 'pred_susu'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    id_waktu = Column(Integer, primary_key=True)
    id_lokasi = Column(Integer, primary_key=True)
    id_unit_peternakan = Column(Integer, primary_key=True)
    prediction = Column(Numeric(precision=10, scale=2))
    latency = Column(Numeric(precision=10, scale=2))
    mape = Column(Numeric(precision=10, scale=2))
    created_at = Column(DateTime(timezone=False), default=datetime.now(timezone.utc))
    # modified_dt = Column(DateTime(timezone=False), default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))