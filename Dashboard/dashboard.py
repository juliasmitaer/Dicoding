import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Membuat judul untuk dashboard
st.title("Dashboard Penyewaan Sepeda Capital Bikeshare")

# Membaca data
hour_df = pd.read_csv('Dashboard/all_data.csv')
st.write("Data berhasil diunggah")

# Ubah kolom 'dteday' menjadi datetime
hour_df['dteday'] = pd.to_datetime(hour_df['dteday'])

# Menentukan rentang tanggal untuk date_input
min_date = hour_df['dteday'].min().date()
max_date = hour_df['dteday'].max().date()

# Sidebar untuk input rentang waktu
with st.sidebar:
     # Menambahkan logo perusahaan
    st.image("https://raw.githubusercontent.com/citrawarna/sepeda/master/img/logo-sepeda.png")
    start_date, end_date = st.date_input(
        label='Rentang Waktu',
        min_value=min_date,
        max_value=max_date,
        value=(min_date, max_date)
    )
    st.write("Perhatikan! \njika ingin menampilkan perbandingan pada weekday dan weekend, \nmaka pilih tanggal dalam rentang yang benar")

# Filter data berdasarkan rentang waktu yang dipilih
filtered_data = hour_df[(hour_df['dteday'].dt.date >= start_date) & 
                         (hour_df['dteday'].dt.date <= end_date)]


# Menambahkan kolom holiday_hour
filtered_data['holiday_hour'] = filtered_data['dteday'].dt.weekday // 5  # 0 untuk Weekday, 1 untuk Weekend

# Mengelompokkan data untuk dianalisis
kelompok_hari = filtered_data.groupby('holiday_hour')['cnt_hour'].agg(['mean', 'median', 'sum']).reset_index()
kelompok_hari['holiday_hour'] = kelompok_hari['holiday_hour'].map({0: 'Weekday', 1: 'Weekend'})


# Tampilkan hasil pengelompokan
st.write(kelompok_hari)

# Tampilkan rata-rata penyewaan untuk hari kerja dan akhir pekan
st.subheader("Rata-rata Penyewaan Sepeda: Weekday vs Weekend")
st.dataframe(kelompok_hari)



# Jumlah sewa rata-rata plot
plt.figure(figsize=(10, 5))
sns.barplot(x='holiday_hour', y='mean', data=kelompok_hari)
plt.title('Rata-rata Jumlah Penyewaan Sepeda: Hari Kerja vs Hari Libur')
plt.xlabel('Tipe Hari')
plt.ylabel('Rata-rata Jumlah Penyewaan')
plt.grid(axis='y')
st.pyplot(plt)

 # Analisis jumlah sewa per jam
perhitungan_jam = hour_df.groupby('hr')['cnt_hour'].sum().reset_index()

# Penyewaan plot dihitung per jam
plt.figure(figsize=(10, 5))
sns.lineplot(x='hr', y='cnt_hour', data=perhitungan_jam, marker='o')
plt.title('Jumlah Penyewaan Sepeda Berdasarkan Jam')
plt.xlabel('Jam')
plt.ylabel('Jumlah Penyewaan')
plt.xticks(range(0, 24))
plt.grid()
st.pyplot(plt)

# Analisis korelasi
korelasi = hour_df[['temp_hour', 'weathersit_hour', 'windspeed_hour', 'hr', 'cnt_hour']].corr()
st.subheader("Matriks Korelasi")
st.write(korelasi)

 # Visualisasi faktor-faktor yang mempengaruhi penyewaan sepeda
st.subheader("Faktor-faktor yang Mempengaruhi Penyewaan Sepeda")

plt.figure(figsize=(15, 10))

# temepratur dan jumlah sewa
plt.subplot(2, 2, 1)
sns.scatterplot(x='temp_hour', y='cnt_hour', data=hour_df, alpha=0.6)
plt.title('Korelasi antara temp_hourerature dan Jumlah Penyewaan')
plt.xlabel('temp_hourerature')
plt.ylabel('Jumlah Penyewaan')

# windspeed vs jumkah seva
plt.subplot(2, 2, 2)
sns.scatterplot(x='windspeed_hour', y='cnt_hour', data=hour_df, alpha=0.6)
plt.title('Korelasi antara windspeed_hour dan Jumlah Penyewaan')
plt.xlabel('windspeed_hour')
plt.ylabel('Jumlah Penyewaan')

# jam dan jumlah sewa
plt.subplot(2, 2, 3)
sns.scatterplot(x='hr', y='cnt_hour', data=hour_df, alpha=0.6)
plt.title('Korelasi antara Jam dan Jumlah Penyewaan')
plt.xlabel('Jam')
plt.ylabel('Jumlah Penyewaan')

# cuaca vs Rental Count
plt.subplot(2, 2, 4)
sns.stripplot(x='weathersit_hour', y='cnt_hour', data=hour_df, jitter=True, alpha=0.6)
plt.title('Jumlah Penyewaan berdasarkan Weather Situation')
plt.xlabel('Weather Situation')
plt.ylabel('Jumlah Penyewaan')

plt.tight_layout()
st.pyplot(plt)

# kesimpulan
st.subheader("Kesimpulan")
st.write("""
- Jumlah penyewaan sepeda lebih tinggi pada hari kerja dibandingkan hari libur.
- Terdapat jam-jam tertentu di mana penyewaan mencapai puncaknya, terutama di pagi dan sore hari.
- Faktor-faktor seperti suhu, cuaca, dan waktu dalam sehari mempengaruhi jumlah penyewaan.
""")

# Run the Streamlit app



