import json
import random
import pandas as pd

from datetime import datetime, timedelta

from headers import *

ID_PETERNAK = 1
ID_MITRA_BISNIS = 1
MIN_VALUE = 1
MAX_VALUE = 50
MIN_SUSU_PRICE = 8000
MAX_SUSU_PRICE = 12000
MIN_DAGING_PRICE = 100000
MAX_DAGING_PRICE = 150000

def format_data(source, data, headers):
    datas = {}
    for header in headers:
        datas[header] = data[header]
    
    return {
        "source_table": source,
        "action": "CREATE",
        "data": datas
    }
    
def generate_history_populasi(n):
    res = []
    for i in range(n):
        new_data = {}
        for header in history_populasi_header:
            if header == 'id':
                new_data[header] = i
            elif header == 'tgl_pencatatan':
                new_data[header] = (datetime.now() + timedelta(days=i)).date().strftime('%Y-%m-%d')
            elif header == 'jml_pedaging_jantan':
                is_zero = random.choices([True, False], [0.7, 0.3])[0]
                if is_zero:
                    new_data[header] = 0
                else:
                    new_data[header] = random.randint(MIN_VALUE, MAX_VALUE)
            elif header == 'jml_pedaging_betina':
                is_zero = random.choices([True, False], [0.7, 0.3])[0]
                if is_zero:
                    new_data[header] = 0
                else:
                    new_data[header] = random.randint(MIN_VALUE, MAX_VALUE)
            elif header == 'jml_pedaging_anakan_jantan':
                is_zero = random.choices([True, False], [0.7, 0.3])[0]
                if is_zero:
                    new_data[header] = 0
                else:
                    new_data[header] = random.randint(MIN_VALUE, MAX_VALUE)                 
            elif header == 'jml_pedaging_anakan_betina':
                is_zero = random.choices([True, False], [0.7, 0.3])[0]
                if is_zero:
                    new_data[header] = 0
                else:
                    new_data[header] = random.randint(MIN_VALUE, MAX_VALUE)
            elif header == 'jml_perah_jantan':
                is_zero = random.choices([True, False], [0.7, 0.3])[0]
                if is_zero:
                    new_data[header] = 0
                else:
                    new_data[header] = random.randint(MIN_VALUE, MAX_VALUE)
            elif header == 'jml_perah_betina':
                is_zero = random.choices([True, False], [0.7, 0.3])[0]
                if is_zero:
                    new_data[header] = 0
                else:
                    new_data[header] = random.randint(MIN_VALUE, MAX_VALUE)
            elif header == 'jml_perah_anakan_jantan':
                is_zero = random.choices([True, False], [0.7, 0.3])[0]
                if is_zero:
                    new_data[header] = 0
                else:
                    new_data[header] = random.randint(MIN_VALUE, MAX_VALUE)
            elif header == 'jml_perah_anakan_betina':
                is_zero = random.choices([True, False], [0.7, 0.3])[0]
                if is_zero:
                    new_data[header] = 0
                else:
                    new_data[header] = random.randint(MIN_VALUE, MAX_VALUE)
            else:
                new_data[header] = ID_PETERNAK
        res.append(new_data)
        
    df = pd.DataFrame(res)
    df.columns = history_populasi_header
    df.to_csv('results/history_populasi.csv', index=False)
    
    with open('json/history_populasi.jsonl', 'w') as f:
        for _, row in df.iterrows():
            json_record = format_data('history_populasi', row, history_populasi_header)
            f.write(json.dumps(json_record) + '\n')      
    
    
def generate_history_kelahiran_kematian(n):
    res = []
    for i in range(n):
        new_data = {}
        for header in history_kelahiran_kematian_header:
            if header == 'id':
                new_data[header] = i
            elif header == 'tgl_pencatatan':
                new_data[header] = (datetime.now() + timedelta(days=i)).date().strftime('%Y-%m-%d')
            elif header == 'jml_lahir_pedaging_jantan':
                is_zero = random.choices([True, False], [0.7, 0.3])[0]
                if is_zero:
                    new_data[header] = 0
                else:
                    new_data[header] = random.randint(MIN_VALUE, MAX_VALUE)
            elif header == 'jml_lahir_pedaging_betina':
                is_zero = random.choices([True, False], [0.7, 0.3])[0]
                if is_zero:
                    new_data[header] = 0
                else:
                    new_data[header] = random.randint(MIN_VALUE, MAX_VALUE)
            elif header == 'jml_lahir_perah_jantan':
                is_zero = random.choices([True, False], [0.7, 0.3])[0]
                if is_zero:
                    new_data[header] = 0
                else:
                    new_data[header] = random.randint(MIN_VALUE, MAX_VALUE)                 
            elif header == 'jml_lahir_perah_betina':
                is_zero = random.choices([True, False], [0.7, 0.3])[0]
                if is_zero:
                    new_data[header] = 0
                else:
                    new_data[header] = random.randint(MIN_VALUE, MAX_VALUE)
            elif header == 'jml_mati_pedaging_jantan':
                is_zero = random.choices([True, False], [0.7, 0.3])[0]
                if is_zero:
                    new_data[header] = 0
                else:
                    new_data[header] = random.randint(MIN_VALUE, MAX_VALUE)
            elif header == 'jml_mati_pedaging_betina':
                is_zero = random.choices([True, False], [0.7, 0.3])[0]
                if is_zero:
                    new_data[header] = 0
                else:
                    new_data[header] = random.randint(MIN_VALUE, MAX_VALUE)
            elif header == 'jml_mati_perah_jantan':
                is_zero = random.choices([True, False], [0.7, 0.3])[0]
                if is_zero:
                    new_data[header] = 0
                else:
                    new_data[header] = random.randint(MIN_VALUE, MAX_VALUE)
            elif header == 'jml_mati_perah_betina':
                is_zero = random.choices([True, False], [0.7, 0.3])[0]
                if is_zero:
                    new_data[header] = 0
                else:
                    new_data[header] = random.randint(MIN_VALUE, MAX_VALUE)
            elif header == 'jml_mati_pedaging_anakan_jantan':
                is_zero = random.choices([True, False], [0.7, 0.3])[0]
                if is_zero:
                    new_data[header] = 0
                else:
                    new_data[header] = random.randint(MIN_VALUE, MAX_VALUE)
            elif header == 'jml_mati_pedaging_anakan_betina':
                is_zero = random.choices([True, False], [0.7, 0.3])[0]
                if is_zero:
                    new_data[header] = 0
                else:
                    new_data[header] = random.randint(MIN_VALUE, MAX_VALUE)
            elif header == 'jml_mati_perah_anakan_jantan': 
                is_zero = random.choices([True, False], [0.7, 0.3])[0]
                if is_zero:
                    new_data[header] = 0
                else:
                    new_data[header] = random.randint(MIN_VALUE, MAX_VALUE)
            elif header == 'jml_mati_perah_anakan_betina': 
                is_zero = random.choices([True, False], [0.7, 0.3])[0]
                if is_zero:
                    new_data[header] = 0
                else:
                    new_data[header] = random.randint(MIN_VALUE, MAX_VALUE)
            else:
                new_data[header] = ID_PETERNAK
                
        res.append(new_data)
    
    df = pd.DataFrame(res)
    df.columns = history_kelahiran_kematian_header
    df.to_csv('results/history_kelahiran_kematian.csv', index=False)
    
    with open('json/history_kelahiran_kematian.jsonl', 'w') as f:
        for _, row in df.iterrows():
            json_record = format_data('history_kelahiran_kematian', row, history_kelahiran_kematian_header)
            f.write(json.dumps(json_record) + '\n')
            
    
def generate_pencatatan_ternak_masuk(n):
    res = []
    for i in range(n):
        new_data = {}
        for header in pencatatan_ternak_masuk_header:
            if header == 'id':
                new_data[header] = i
            elif header == 'tgl_pencatatan':
                new_data[header] = (datetime.now() + timedelta(days=i)).date().strftime('%Y-%m-%d')
            elif header == 'jenis_mitra_pengirim':
                new_data[header] = random.randint(MIN_VALUE, MAX_VALUE)
            elif header == 'jml_pedaging_jantan':
                new_data[header] = random.randint(MIN_VALUE, MAX_VALUE)
            elif header == 'jml_pedaging_betina':
                new_data[header] = random.randint(MIN_VALUE, MAX_VALUE)
            elif header == 'jml_pedaging_anakan_jantan':
                new_data[header] = random.randint(MIN_VALUE, MAX_VALUE)
            elif header == 'jml_pedaging_anakan_betina':
                new_data[header] = random.randint(MIN_VALUE, MAX_VALUE)
            elif header == 'jml_perah_jantan':
                new_data[header] = random.randint(MIN_VALUE, MAX_VALUE)
            elif header == 'jml_perah_betina':
                new_data[header] = random.randint(MIN_VALUE, MAX_VALUE)
            elif header == 'jml_perah_anakan_jantan':
                new_data[header] = random.randint(MIN_VALUE, MAX_VALUE)
            elif header == 'jml_perah_anakan_betina':
                new_data[header] = random.randint(MIN_VALUE, MAX_VALUE)
            else:
                new_data[header] = ID_PETERNAK
        res.append(new_data)
        
    df = pd.DataFrame(res)
    df.columns = pencatatan_ternak_masuk_header
    df.to_csv('results/pencatatan_ternak_masuk.csv', index=False)
    
    with open('json/pencatatan_ternak_masuk.jsonl', 'w') as f:
        for _, row in df.iterrows():
            json_record = format_data('pencatatan_ternak_masuk', row, pencatatan_ternak_masuk_header)
            f.write(json.dumps(json_record) + '\n')
 
    
def generate_pencatatan_ternak_keluar(n):
    res = []
    for i in range(n):
        new_data = {}
        for header in pencatatan_ternak_keluar_header:
            if header == 'id':
                new_data[header] = i
            elif header == 'tgl_pencatatan':
                new_data[header] = (datetime.now() + timedelta(days=i)).date().strftime('%Y-%m-%d')
            elif header == 'jenis_mitra_penerima':
                new_data[header] = random.randint(MIN_VALUE, MAX_VALUE)
            elif header == 'jml_pedaging_jantan':
                new_data[header] = random.randint(MIN_VALUE, MAX_VALUE)
            elif header == 'jml_pedaging_betina':
                new_data[header] = random.randint(MIN_VALUE, MAX_VALUE)
            elif header == 'jml_pedaging_anakan_jantan':
                new_data[header] = random.randint(MIN_VALUE, MAX_VALUE)
            elif header == 'jml_pedaging_anakan_betina':
                new_data[header] = random.randint(MIN_VALUE, MAX_VALUE)
            elif header == 'jml_perah_jantan':
                new_data[header] = random.randint(MIN_VALUE, MAX_VALUE)
            elif header == 'jml_perah_betina':
                new_data[header] = random.randint(MIN_VALUE, MAX_VALUE)
            elif header == 'jml_perah_anakan_jantan':
                new_data[header] = random.randint(MIN_VALUE, MAX_VALUE)
            elif header == 'jml_perah_anakan_betina':
                new_data[header] = random.randint(MIN_VALUE, MAX_VALUE)
            else:
                new_data[header] = ID_PETERNAK
        res.append(new_data)
    
    df = pd.DataFrame(res)
    df.columns = pencatatan_ternak_keluar_header
    df.to_csv('results/pencatatan_ternak_keluar.csv', index=False)

    with open('json/pencatatan_ternak_keluar.jsonl', 'w') as f:
        for _, row in df.iterrows():
            json_record = format_data('pencatatan_ternak_keluar', row, pencatatan_ternak_keluar_header)
            f.write(json.dumps(json_record) + '\n')


def generate_distribusi_susu(n):
    res = []
    for i in range(n):
        new_data = {}
        for header in distribusi_susu_header:
            if header == 'id':
                new_data[header] = i
            elif header == 'tgl_distribusi':
                new_data[header] = (datetime.now() + timedelta(days=i)).date().strftime('%Y-%m-%d')
            elif header == 'id_unit_ternak':
                new_data[header] = ID_PETERNAK
            elif header == 'id_jenis_produk':
                new_data[header] = random.choices([3, 5], [0.5, 0.5])[0]
            elif header == 'id_mitra_bisnis':
                new_data[header] = ID_MITRA_BISNIS
                
        if new_data['id_jenis_produk'] == 3:
            new_data['jumlah'] = random.randint(MIN_VALUE, MAX_VALUE)
            new_data['satuan'] = 'liter'
            new_data['harga_berlaku'] = random.randint(MIN_SUSU_PRICE, MAX_SUSU_PRICE)
        else:
            new_data['jumlah'] = random.randint(MIN_VALUE, MAX_VALUE)
            new_data['satuan'] = 'kg'
            new_data['harga_berlaku'] = random.randint(MIN_DAGING_PRICE, MAX_DAGING_PRICE)
        res.append(new_data)
    
    df = pd.DataFrame(res)
    df = df[distribusi_susu_header]
    df.to_csv('results/distribusi_susu.csv', index=False)

    with open('json/distribusi_susu.jsonl', 'w') as f:
        for _, row in df.iterrows():
            json_record = format_data('distribusi_susu', row, distribusi_susu_header)
            f.write(json.dumps(json_record) + '\n')
            

def generate_distribusi_ternak(n):
    res = []
    for i in range(n):
        new_data = {}
        for header in distribusi_ternak_header:
            if header == 'id':
                new_data[header] = i
            elif header == 'tgl_distribusi':
                new_data[header] = (datetime.now() + timedelta(days=i)).date().strftime('%Y-%m-%d')
            elif header == 'id_unit_ternak':
                new_data[header] = ID_PETERNAK
            elif header == 'id_jenis_produk':
                new_data[header] = random.choices([2, 4], [0.5, 0.5])[0]
            elif header == 'id_mitra_bisnis':
                new_data[header] = ID_MITRA_BISNIS
                
        if new_data['id_jenis_produk'] == 2:
            new_data['jumlah'] = random.randint(MIN_VALUE, MAX_VALUE)
            new_data['satuan'] = 'ekor'
            new_data['harga_berlaku'] = random.randint(MIN_DAGING_PRICE, MAX_DAGING_PRICE)
        else:
            new_data['jumlah'] = random.randint(MIN_VALUE, MAX_VALUE)
            new_data['satuan'] = 'kg'
            new_data['harga_berlaku'] = random.randint(MIN_DAGING_PRICE, MAX_DAGING_PRICE)
        res.append(new_data)
        
    df = pd.DataFrame(res)
    df = df[distribusi_ternak_header]
    df.to_csv('results/distribusi_ternak.csv', index=False)
    
    with open('json/distribusi_ternak.jsonl', 'w') as f:
        for _, row in df.iterrows():
            json_record = format_data('distribusi_ternak', row, distribusi_ternak_header)
            f.write(json.dumps(json_record) + '\n')
            
    
def generate_produksi_susu(n):
    res = []
    for i in range(n):
        new_data = {}
        for header in produksi_susu_header:
            if header == 'id':
                new_data[header] = i
            elif header == 'tgl_produksi':
                new_data[header] = (datetime.now() + timedelta(days=i)).date().strftime('%Y-%m-%d')
            elif header == 'id_unit_ternak':
                new_data[header] = ID_PETERNAK
            elif header == 'id_jenis_produk':
                new_data[header] = 3
            elif header == 'sumber_pasokan':
                new_data[header] = random.choices(['Peternakan Sendiri', 'Peternakan Lain', 'Pengepul'], [0.3, 0.4, 0.3])[0]
                
        new_data['jumlah'] = random.randint(MIN_VALUE, MAX_VALUE)
        new_data['satuan'] = 'liter'
        res.append(new_data)
        
    df = pd.DataFrame(res)
    df = df[produksi_susu_header]
    df.to_csv('results/produksi_susu.csv', index=False)

    with open('json/produksi_susu.jsonl', 'w') as f:
        for _, row in df.iterrows():
            json_record = format_data('produksi_susu', row, produksi_susu_header)
            f.write(json.dumps(json_record) + '\n')
            

def generate_produksi_ternak(n):
    res = []
    for i in range(n):
        new_data = {}
        for header in produksi_ternak_header:
            if header == 'id':
                new_data[header] = i
            elif header == 'tgl_produksi':
                new_data[header] = (datetime.now() + timedelta(days=i)).date().strftime('%Y-%m-%d')
            elif header == 'id_unit_ternak':
                new_data[header] = ID_PETERNAK
            elif header == 'id_jenis_produk':
                new_data[header] = 5
            elif header == 'sumber_pasokan':
                new_data[header] = random.choices(['Peternakan Sendiri', 'Peternakan Lain', 'Pengepul'], [0.3, 0.4, 0.3])[0]
            elif header == 'satuan':
                new_data[header] = random.choices(['ekor', 'kg'], [0.5, 0.5])[0]

        new_data['jumlah'] = random.randint(MIN_VALUE, MAX_VALUE)
        res.append(new_data)
        
    df = pd.DataFrame(res)
    df = df[produksi_ternak_header]
    df.to_csv('results/produksi_ternak.csv', index=False)
    df.to_json('json/produksi_ternak.jsonl', orient='records', lines=True)

    with open('json/produksi_ternak.jsonl', 'w') as f:
        for _, row in df.iterrows():
            json_record = format_data('produksi_ternak', row, produksi_ternak_header)
            f.write(json.dumps(json_record) + '\n')
            

def main(n=10):
    generate_history_populasi(n)
    generate_history_kelahiran_kematian(n)
    generate_pencatatan_ternak_masuk(n)
    generate_pencatatan_ternak_keluar(n)
    generate_distribusi_susu(n)
    generate_distribusi_ternak(n)
    generate_produksi_susu(n)
    generate_produksi_ternak(n)
    
main(n=10000)