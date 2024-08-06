import pandas as pd

history_populasi_header = [
    'id', 'tgl_pencatatan', 'jml_pedaging_jantan', 'jml_pedaging_betina', 
    'jml_pedaging_anakan_jantan', 'jml_pedaging_anakan_betina', 'jml_perah_jantan', 
    'jml_perah_betina', 'jml_perah_anakan_jantan', 'jml_perah_anakan_betina', 'id_peternak'
]

history_kelahiran_kematian_header = [
    'id', 'tgl_pencatatan', 'jml_lahir_pedaging_jantan', 'jml_lahir_pedaging_betina', 
    'jml_lahir_perah_jantan', 'jml_lahir_perah_betina', 'jml_mati_pedaging_jantan', 'jml_mati_pedaging_betina',
    'jml_mati_perah_jantan', 'jml_mati_perah_betina', 'jml_mati_pedaging_anaan_jantan', 'jml_mati_pedaging_anakan_betina',
    'jml_mati_perah_anakan_jantan', 'jml_mati_perah_anakan_betina', 'id_peternak'
]

pencatatan_ternak_masuk_header = [
    'id', 'tgl_pencatatan', 'jenis_mitra_pengirim', 'jml_pedaging_jantan', 'jml_pedaging_betina',
    'jml_pedaging_anakan_jantan', 'jml_pedaging_anakan_betina', 'jml_perah_jantan', 'jml_perah_betina',
    'jml_perah_anakan_jantan', 'jml_perah_anakan_betina', 'id_peternak'
]

pencatatan_ternak_keluar_header = [
    'id', 'tgl_pencatatan', 'jenis_mitra_penerima', 'jml_pedaging_jantan', 'jml_pedaging_betina',
    'jml_pedaging_anakan_jantan', 'jml_pedaging_anakan_betina', 'jml_perah_jantan', 'jml_perah_betina',
    'jml_perah_anakan_jantan', 'jml_perah_anakan_betina', 'id_peternak'
]

distribusi_susu_header = [
    'id', 'tgl_distribusi', 'jumlah', 'satuan', 'harga_berlaku', 'id_unit_ternak', 'id_jenis_produk', 'id_mitra_bisnis'
]

distribusi_ternak_header = [
    'id', 'tgl_distribusi', 'jumlah', 'satuan', 'harga_berlaku', 'id_unit_ternak', 'id_jenis_produk', 'id_mitra_bisnis'
]

produksi_susu_header = [
    'id', 'tgl_produksi', 'jumlah', 'satuan', 'sumber_pasokan', 'id_unit_ternak', 'id_jenis_produk'
]

produksi_ternak_header = [
    'id', 'tgl_produksi', 'jumlah', 'satuan', 'sumber_pasokan', 'id_unit_ternak', 'id_jenis_produk'
]