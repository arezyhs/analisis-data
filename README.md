# Proyek Analisis Data: Kualitas Udara (PRSA)

Proyek ini merupakan submission tugas akhir untuk kelas **Belajar Analisis Data dengan Python** di platform Dicoding. Data yang digunakan adalah data Air Quality di Beijing, dengan tujuan utama dari proyek ini menganalisis data kualitas udara dari 12 stasiun pengamatan di Beijing.

## Pertanyaan Bisnis (SMART)
1. Bagaimana tren rata-rata bulanan konsentrasi polusi (PM2.5) di seluruh stasiun (12 stasiun) pada tahun 2016, dan pada bulan apa tingkat polusi rata-rata mencapai puncaknya?
2. Bagaimana pengaruh suhu (TEMP) dan tingkat curah hujan (RAIN) terhadap fluktuasi konsentrasi PM2.5 secara agregat di seluruh stasiun selama musim panas (Juni-Agustus) tahun 2016?

## Struktur Direktori
```text
├── dashboard/
│   ├── dashboard.py
│   └── main_data.csv
├── PRSA_Data_20130301-20170228/
│   ├── (12 file CSV berisi raw data)
├── Proyek_Analisis_Data.ipynb
├── README.md
├── requirements.txt
```

## Setup Environment

Disarankan untuk menggunakan *virtual environment* terlebih dahulu untuk menghindari konflik antar *library*. Langkah-langkah instalasinya sebagai berikut:

### Menggunakan Conda:
```bash
conda create --name main-ds python=3.11
conda activate main-ds
pip install -r requirements.txt
```

### Menggunakan venv (Python bawaan):
```bash
# Pengguna Windows:
python -m venv venv
venv\\Scripts\\activate
pip install -r requirements.txt

# Pengguna Mac/Linux:
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Menjalankan Jupyter Notebook

1. Pastikan *virtual environment* telah aktif dan dependensi sudah terinstal.
2. Buka file `Proyek_Analisis_Data.ipynb` menggunakan editor yang digunakan (Jupyter Notebook, JupyterLab, atau VS Code).
3. Run seluruh *cell* secara berurutan (*Run All*). Proses ini akan melakukan penggabungan data, pembersihan, eksplorasi, hingga mengekspor hasil akhirnya ke dalam file `dashboard/main_data.csv`.

## Menjalankan Dashboard Streamlit

1. Buka terminal atau *command prompt*.
2. Arahkan *directory* (menggunakan perintah `cd`) ke folder utama proyek ini.
3. Jalankan perintah berikut:
   ```bash
   streamlit run dashboard/dashboard.py
   ```
4. Dashboard akan otomatis terbuka di dalam *browser* pada tautan `http://localhost:8501`.