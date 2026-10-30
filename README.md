# Proyek Analisis Data: E-Commerce Dashboard

Proyek akhir kelas **Belajar Fundamental Analisis Data** (Dicoding x DBS).
Dashboard online: https://9laksnkqrcctv7yxzigspy.streamlit.app/

## Deskripsi Proyek
Proyek ini menganalisis performa penjualan e-commerce dari **Olist Brazilian E-Commerce Public Dataset** (9 file CSV, disimpan di folder `data/`). Seluruh analisis memakai order berstatus *delivered* pada tahun 2017, dan revenue dihitung dari jumlah `price` tanpa ongkos kirim.

Pertanyaan bisnis yang dijawab:
1. Berapa total revenue per bulan sepanjang tahun 2017, dan bulan apa yang tertinggi dan terendah?
2. Kategori produk apa yang masuk 5 terlaris dan 5 paling sedikit terjual berdasarkan jumlah item sepanjang tahun 2017?

Proses analisis lengkap (gathering, assessing, cleaning, EDA, visualisasi, dan kesimpulan) ada di `notebook.ipynb`. Data hasil pembersihan yang dipakai dashboard disimpan di `dashboard/main_data.csv`.

## Struktur Direktori
```
submission
├── dashboard
│   ├── dashboard.py
│   └── main_data.csv
├── data
│   ├── customers_dataset.csv
│   ├── geolocation_dataset.csv
│   ├── order_items_dataset.csv
│   ├── order_payments_dataset.csv
│   ├── order_reviews_dataset.csv
│   ├── orders_dataset.csv
│   ├── product_category_name_translation.csv
│   ├── products_dataset.csv
│   └── sellers_dataset.csv
├── notebook.ipynb
├── README.md
├── requirements.txt
└── url.txt
```

## Persiapan Environment
Pastikan Python 3 sudah terpasang. Proyek ini dikembangkan dengan Python 3.14. Dari folder `submission`, buat dan aktifkan virtual environment:

Windows:
```
python -m venv venv
venv\Scripts\activate
```

macOS / Linux:
```
python3 -m venv venv
source venv/bin/activate
```

## Instalasi Dependensi
Dengan virtual environment aktif, pasang semua library yang dibutuhkan notebook dan dashboard:
```
pip install -r requirements.txt
```

## Menjalankan Dashboard
Jalankan perintah berikut dari folder `submission` (satu level di atas folder `dashboard`):
```
streamlit run dashboard/dashboard.py
```
Dashboard akan terbuka di browser, biasanya di `http://localhost:8501`.

## Fitur Dashboard
- **Filter rentang waktu** di sidebar untuk membatasi data berdasarkan tanggal pembelian.
- **Ringkasan metrik**: Total Revenue dan Total Item Terjual pada rentang yang dipilih.
- **Total Revenue per Bulan**: grafik garis dengan penanda merah pada bulan tertinggi dan terendah.
- **Best & Worst Performing Category**: dua grafik batang berdampingan yang menampilkan 5 kategori terlaris dan 5 kategori paling sedikit terjual.