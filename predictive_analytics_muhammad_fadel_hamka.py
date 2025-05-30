# -*- coding: utf-8 -*-
"""Predictive Analytics - Muhammad Fadel Hamka.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1P5tFcwEJI9Esx9v3JtRM20F2mOBOm6k2

# **1. Import Library & Load Dataset**
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

"""### **Penjelasan Impor:**

* import pandas as pd: Mengimpor library Pandas dan memberinya alias pd. Pandas digunakan untuk manipulasi dan analisis data, terutama untuk bekerja dengan struktur data tabular seperti DataFrame.
* import numpy as np: Mengimpor library NumPy dengan alias np. NumPy adalah dasar untuk komputasi numerik di Python, menyediakan dukungan untuk array multidimensi dan berbagai fungsi matematika.
* import matplotlib.pyplot as plt: Mengimpor modul pyplot dari library Matplotlib dengan alias plt. Matplotlib adalah library untuk membuat visualisasi statis, animasi, dan interaktif.
* import seaborn as sns: Mengimpor library Seaborn dengan alias sns. Seaborn dibangun di atas Matplotlib dan menyediakan antarmuka tingkat tinggi untuk membuat grafik statistik yang menarik dan informatif.
* from sklearn.model_selection import train_test_split: Mengimpor fungsi train_test_split dari modul model_selection dalam library Scikit-learn (sklearn). Fungsi ini digunakan untuk membagi dataset menjadi set pelatihan (train) dan pengujian (test).
* from sklearn.linear_model import LinearRegression: Mengimpor kelas LinearRegression dari modul linear_model di Scikit-learn. Ini digunakan untuk membuat model regresi linear.
* from sklearn.tree import DecisionTreeRegressor: Mengimpor kelas DecisionTreeRegressor dari modul tree di Scikit-learn. Ini digunakan untuk membuat model regresi berdasarkan decision tree.
* from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score: Mengimpor beberapa fungsi metrik evaluasi dari modul metrics di Scikit-learn:
    * mean_absolute_error (MAE): Mengukur rata-rata selisih absolut antara nilai aktual dan prediksi.
    * mean_squared_error (MSE): Mengukur rata-rata kuadrat selisih antara nilai aktual dan prediksi.
    * r2_score (R-squared): Mengukur proporsi varians dalam variabel dependen yang dapat diprediksi dari variabel independen.
"""

# URL ke file CSV mentah di GitHub
url = 'https://raw.githubusercontent.com/Fadelhamkaa/Predictive-Analytics-Dicoding/main/DailyDelhiClimateTrain.csv'

# Membaca dataset
df = pd.read_csv(url)

# Menampilkan beberapa baris pertama dari dataset
print(df.head())

"""**Langkah: Memuat dan Meninjau Dataset**

- Pada tahap ini, kita memuat dataset mentah dari repository GitHub menggunakan `pd.read_csv(url)`.  
- Kemudian, kita menampilkan 5 baris pertama dataset dengan `df.head()` untuk mendapatkan gambaran awal struktur data.  
- Dari output terlihat bahwa dataset memiliki kolom:
  - `date`: tanggal pencatatan cuaca (sebagai string)
  - `meantemp`: suhu rata-rata harian (float)
  - `humidity`: persentase kelembapan (float)
  - `wind_speed`: kecepatan angin rata-rata (float)
  - `meanpressure`: tekanan udara rata-rata (float)

> Insight awal: Data sudah berhasil dimuat dan struktur kolom sesuai ekspektasi. Selanjutnya akan kita cek tipe data dan kondisi missing/duplikat.

# **2. Data Understanding**
"""

# Info dataset
df.info()

"""Output dan Penjelasan:

Jumlah baris: 1462

Jumlah kolom: 5

Semua kolom memiliki 1462 nilai non-null, artinya tidak ada missing values.

Tipe data:

4 kolom bertipe float64 (meantemp, humidity, wind_speed, meanpressure)

1 kolom bertipe object yaitu date yang perlu dikonversi ke tipe datetime di tahap selanjutnya.

Informasi ini menjadi dasar untuk menentukan langkah persiapan data berikutnya seperti konversi tipe data dan pengecekan outlier.
"""

# Statistik deskriptif
df.describe()

"""Penjelasan Hasil:

meantemp: Suhu rata-rata berkisar dari 6°C hingga 38.7°C, dengan rata-rata sekitar 25.5°C. Data cukup tersebar dengan standar deviasi sekitar 7.35.

humidity: Kelembapan berkisar antara 13.4% hingga 100%, dengan rata-rata sekitar 60.8%. Distribusinya relatif seimbang.

wind_speed: Kecepatan angin memiliki rentang yang luas dari 0 hingga 42.22 km/h, namun nilai median (6.22) menunjukkan distribusi agak miring ke kanan.

meanpressure: Terlihat adanya nilai ekstrem dengan tekanan udara maksimum sebesar 7679.33 hPa, jauh di atas rata-rata 1011.10 hPa. Ini kemungkinan merupakan outlier dan akan diperiksa lebih lanjut di tahap pembersihan data.
"""

# Cek missing value
df.isnull().sum()

"""Penjelasan:

* Perintah df.isnull() akan menghasilkan DataFrame boolean dengan nilai True jika data pada sel tersebut hilang (NaN) dan False jika tidak.
* Kemudian, fungsi .sum() dijumlahkan per kolom. Karena True dievaluasi sebagai 1 dan False sebagai 0, hasil penjumlahan ini akan menunjukkan jumlah nilai yang hilang (missing values) untuk setiap kolom.
* Dalam kasus ini, semua kolom ('date', 'meantemp', 'humidity', 'wind_speed', 'meanpressure') menunjukkan angka 0. Ini berarti setiap kolom memiliki data yang lengkap dan tidak ada entri yang kosong atau tidak terdefinisi.
"""

# Convert kolom 'date' ke tipe datetime
df['date'] = pd.to_datetime(df['date'])

# Set sebagai index jika ingin analisis time series (opsional)
# df.set_index('date', inplace=True)

"""Penjelasan Kode:

df['date'] = pd.to_datetime(df['date'])

Baris ini mengonversi semua nilai dalam kolom 'date' dari tipe data aslinya (misalnya, string atau objek) menjadi tipe data datetime.
Ini adalah langkah penting karena memungkinkan Pandas untuk mengenali dan memanipulasi data tanggal dan waktu dengan benar, seperti melakukan ekstraksi komponen tanggal (tahun, bulan, hari) atau melakukan operasi berbasis waktu. 🗓️
# df.set_index('date', inplace=True)

Baris ini (saat ini dikomentari, ditandai dengan #) bertujuan untuk menetapkan kolom 'date' sebagai indeks dari DataFrame df.
Menjadikan kolom tanggal sebagai indeks sangat berguna untuk analisis deret waktu (time series analysis), karena memudahkan operasi seperti resampling, rolling windows, dan pengirisan data berdasarkan rentang waktu.
inplace=True berarti perubahan akan diterapkan langsung ke DataFrame df tanpa perlu membuat DataFrame baru. Karena dikomentari, langkah ini tidak dieksekusi dalam kode saat ini.

# **3. Exploratory Data Analysis (EDA)**
"""

# Korelasi antar fitur
plt.figure(figsize=(8, 6))
sns.heatmap(df.corr(), annot=True, cmap='coolwarm')
plt.title("Korelasi Antar Fitur")
plt.show()

"""### Interpretasi Utama Heatmap:


* meantemp vs humidity: Korelasi negatif sedang (-0.57). Kenaikan suhu cenderung diikuti penurunan kelembapan.
* humidity vs wind_speed: Korelasi negatif sedang (-0.37). Kenaikan kelembapan cenderung diikuti penurunan kecepatan angin.
* meantemp vs wind_speed: Korelasi positif lemah (0.31).
* Fitur lain umumnya menunjukkan korelasi lemah satu sama lain.
date memiliki korelasi sangat rendah dengan fitur lainnya.
"""

# Visualisasi tren suhu harian
plt.figure(figsize=(10, 4))
plt.plot(df['date'], df['meantemp'])
plt.title("Tren Suhu Rata-Rata Harian (meantemp)")
plt.xlabel("Tanggal")
plt.ylabel("Suhu (°C)")
plt.grid()
plt.show()

"""### **Interpretasi Utama Plot:**


* Pola Musiman (Seasonality): Grafik dengan jelas menunjukkan adanya pola musiman tahunan pada suhu rata-rata harian. Suhu cenderung mencapai puncaknya di pertengahan tahun dan titik terendahnya di awal/akhir tahun.
* Rentang Waktu: Data yang divisualisasikan mencakup periode dari awal tahun 2013 hingga awal tahun 2017.
* Variasi Suhu: Suhu rata-rata harian bervariasi, dengan nilai terendah mendekati 5-10°C dan tertinggi mencapai sekitar 35-40°C.

# **4. Data Preparation**
"""

# Fitur dan target
X = df[['humidity', 'wind_speed', 'meanpressure']]
y = df['meantemp']

# Split data: 80% train, 20% test
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42)

"""Penjelasan Kode:

Definisi Fitur dan Target:

X: Variabel independen (fitur) yang terdiri dari 'humidity', 'wind_speed', dan 'meanpressure'.
y: Variabel dependen (target) yang akan diprediksi, yaitu 'meantemp'.
Pembagian Data:

Menggunakan train_test_split untuk membagi X dan y.
test_size=0.2: 20% data untuk pengujian (X_test, y_test), 80% untuk pelatihan (X_train, y_train).
random_state=42: Memastikan pembagian data yang konsisten dan dapat direproduksi.

# **5. Modelling**

## **A. Linear Regression**
"""

lr_model = LinearRegression()
lr_model.fit(X_train, y_train)

y_pred_lr = lr_model.predict(X_test)

"""Penjelasan Kode:

* lr_model = LinearRegression(): Menginisialisasi model Regresi Linear.
* lr_model.fit(X_train, y_train): Melatih model menggunakan data fitur (X_train) dan target (y_train) dari set pelatihan. Model mempelajari hubungan linear antara fitur dan target.
* y_pred_lr = lr_model.predict(X_test): Membuat prediksi nilai target pada data uji (X_test) menggunakan model yang telah dilatih. y_pred_lr berisi hasil prediksi.

## **B. Decision Tree Regressor**
"""

dt_model = DecisionTreeRegressor(random_state=42)
dt_model.fit(X_train, y_train)

y_pred_dt = dt_model.predict(X_test)

"""### Penjelasan Kode:

* dt_model = DecisionTreeRegressor(random_state=42): Menginisialisasi model Decision Tree Regressor.
    * random_state=42 digunakan untuk memastikan hasil yang konsisten dan dapat direproduksi saat model dibangun.
* dt_model.fit(X_train, y_train): Melatih model decision tree menggunakan data fitur (X_train) dan target (y_train) dari set pelatihan. Model belajar dengan membuat serangkaian aturan keputusan berdasarkan fitur untuk memprediksi target.
* y_pred_dt = dt_model.predict(X_test): Membuat prediksi nilai target pada data uji (X_test) menggunakan model decision tree yang telah dilatih. y_pred_dt berisi hasil prediksi.

# **6. Evaluation**

## **Fungsi Evaluasi**
"""

# Fungsi evaluasi model
def evaluate_model(y_true, y_pred, model_name="Model"):
    mae = mean_absolute_error(y_true, y_pred)
    rmse = np.sqrt(mean_squared_error(y_true, y_pred))  # RMSE manual
    r2 = r2_score(y_true, y_pred)

    print(f"Evaluasi {model_name}:")
    print(f"  - MAE  : {mae:.2f}")
    print(f"  - RMSE : {rmse:.2f}")
    print(f"  - R²   : {r2:.2f}")
    print("-" * 40)

# Evaluasi Linear Regression
evaluate_model(y_test, y_pred_lr, "Linear Regression")

# Evaluasi Decision Tree
evaluate_model(y_test, y_pred_dt, "Decision Tree Regressor")

"""Penjelasan Kode:

1. Fungsi evaluate_model:

  * Fungsi ini menerima tiga argumen: y_true (nilai target sebenarnya), y_pred (nilai target yang diprediksi model), dan model_name (nama model untuk pelaporan).
  * Menghitung tiga metrik evaluasi umum untuk regresi:
      * MAE (Mean Absolute Error): Rata-rata dari selisih absolut antara nilai aktual dan prediksi. Semakin kecil nilainya, semakin baik.
      * RMSE (Root Mean Squared Error): Akar kuadrat dari rata-rata selisih kuadrat antara nilai aktual dan prediksi. Memberikan bobot lebih pada kesalahan besar. Semakin kecil nilainya, semakin baik.
      * R² (R-squared): Koefisien determinasi yang menunjukkan seberapa baik varians dalam variabel target dapat dijelaskan oleh model. Nilainya berkisar antara 0 dan 1 (atau bisa negatif untuk model yang sangat buruk). Semakin mendekati 1, semakin baik.
  * Mencetak hasil metrik yang diformat untuk model yang dievaluasi.
2. Pemanggilan Fungsi Evaluasi:

  * evaluate_model(y_test, y_pred_lr, "Linear Regression"): Mengevaluasi model Linear Regression menggunakan nilai target sebenarnya dari set uji (y_test) dan prediksi yang dihasilkan oleh model tersebut (y_pred_lr).
  * evaluate_model(y_test, y_pred_dt, "Decision Tree Regressor"): Mengevaluasi model Decision Tree Regressor menggunakan y_test dan prediksi dari model decision tree (y_pred_dt).
----------------------------------------

### Interpretasi Output:

Evaluasi Linear Regression:
  - MAE  : 5.20
  - RMSE : 6.10
  - R²   : 0.31
----------------------------------------
Evaluasi Decision Tree Regressor:
  - MAE  : 2.73
  - RMSE : 3.70
  - R²   : 0.75
----------------------------------------
1. Linear Regression:

  * MAE sebesar 5.20 dan RMSE sebesar 6.10 menunjukkan rata-rata kesalahan prediksi.
  * R² sebesar 0.31 mengindikasikan bahwa model ini hanya mampu menjelaskan sekitar 31% variabilitas dalam data suhu rata-rata.
2. Decision Tree Regressor:

  * MAE (2.73) dan RMSE (3.70) jauh lebih rendah dibandingkan Linear Regression, menunjukkan kesalahan prediksi yang lebih kecil.
  * R² sebesar 0.75 jauh lebih tinggi, menandakan bahwa model Decision Tree Regressor mampu menjelaskan sekitar 75% variabilitas dalam data suhu rata-rata.
Berdasarkan metrik ini, **Decision Tree Regressor** menunjukkan performa yang lebih baik daripada Linear Regression dalam memprediksi suhu rata-rata pada dataset ini.

# **7. Visualisasi Hasil Prediksi**
"""

plt.figure(figsize=(10,5))
plt.plot(y_test.values[:50], label='Actual')
plt.plot(y_pred_lr[:50], label='Predicted - LinearReg', linestyle='--')
plt.plot(y_pred_dt[:50], label='Predicted - DecisionTree', linestyle=':')
plt.legend()
plt.title("Perbandingan Prediksi vs Aktual (50 Sampel Pertama)")
plt.xlabel("Index")
plt.ylabel("Mean Temperature")
plt.grid()
plt.show()

"""### Penjelasan Kode:

  * plt.figure(figsize=(10,5)): Mengatur ukuran gambar plot menjadi 10x5 inci.
  * plt.plot(y_test.values[:50], label='Actual'): Memplot 50 nilai pertama dari y_test (suhu aktual) sebagai garis solid.
  * plt.plot(y_pred_lr[:50], label='Predicted - LinearReg', linestyle='--'): Memplot 50 prediksi pertama dari model Linear Regression (y_pred_lr) sebagai garis putus-putus.
  * plt.plot(y_pred_dt[:50], label='Predicted - DecisionTree', linestyle=':'): Memplot 50 prediksi pertama dari model Decision Tree (y_pred_dt) sebagai garis titik-titik.
  * plt.legend(): Menampilkan legenda untuk membedakan garis-garis pada plot.
  * plt.title(...), plt.xlabel(...), plt.ylabel(...): Mengatur judul dan label sumbu-sumbu plot.
  * plt.grid(): Menambahkan grid pada plot untuk mempermudah pembacaan.
  * plt.show(): Menampilkan plot.
---

## **Interpretasi Output (Plot):**


### Plot di atas membandingkan secara visual bagaimana prediksi dari kedua model mengikuti nilai aktual untuk 50 sampel data pertama.

  * Actual (Garis Solid Biru): Menunjukkan nilai suhu rata-rata yang sebenarnya.
  * Predicted - LinearReg (Garis Putus-putus Oranye): Menunjukkan prediksi dari model Linear Regression. Terlihat bahwa prediksi ini menangkap tren umum tetapi kurang mampu mengikuti fluktuasi spesifik dari data aktual.
  * Predicted - DecisionTree (Garis Titik-titik Hijau): Menunjukkan prediksi dari model Decision Tree Regressor. Garis ini tampak lebih dekat dan lebih sering mengikuti pola naik turun dari nilai aktual dibandingkan dengan prediksi Linear Regression.
  Secara visual, plot ini mendukung kesimpulan dari metrik evaluasi sebelumnya, yaitu **Decision Tree Regressor** memberikan prediksi yang lebih akurat dan lebih sesuai dengan data aktual untuk sampel yang ditampilkan.
"""