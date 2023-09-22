import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st


sns.set(style='dark')

# Load cleaned data
com_df = pd.read_csv("data_combined.csv")

datetime_columns = ["datetime"]
com_df.sort_values(by="datetime", inplace=True)
com_df.reset_index(inplace=True)

for column in datetime_columns:
    com_df[column] = pd.to_datetime(com_df[column])


# Filter data
min_date = com_df["datetime"].min()
max_date = com_df["datetime"].max()

with st.sidebar:
    # Menambahkan logo perusahaan
    st.image("anim.gif")
    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu', min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

    # Pilihan stasiun
    selected_station = st.selectbox(
        'Pilih Stasiun', com_df['station'].unique())

main_df = com_df[(com_df["datetime"] >= str(start_date)) &
                 (com_df["datetime"] <= str(end_date))]


# MAFAS Trend Air Quality
st.header('MAFAS Trend Air Quality :sparkles:')
st.subheader('Monthly RAIN trend at each station')

station_data = main_df[main_df['station'] == selected_station]
# Mengelompokkan data berdasarkan bulan dan menghitung rata-rata cuaca (RAIN) untuk setiap bulan
monthly_rain_avg = station_data.groupby(
    station_data['datetime'].dt.to_period("M"))['RAIN'].mean()
# Mengubah indeks ke format yang diinginkan
monthly_rain_avg.index = monthly_rain_avg.index.strftime('%m/%y')

# Menampilkan nilai RAIN
avg_rain = station_data['RAIN'].mean()
st.write(f"Rata-rata Curah Hujan: {avg_rain:.2f}mm")

# Membuat plot untuk rata-rata cuaca (RAIN)
fig, ax = plt.subplots(figsize=(25, 10))
sns.lineplot(x=monthly_rain_avg.index,
             y=monthly_rain_avg.values, marker='o', ax=ax, linewidth=3, markersize=12)
ax.set_title(
    f'Tren Tingkat Cuaca (RAIN) di Stasiun {selected_station}', fontsize=30)
ax.set_xlabel('Bulan dan Tahun', fontsize=30)
ax.set_ylabel('Rata-rata Cuaca (RAIN)', fontsize=30)
ax.set_xticklabels(ax.get_xticklabels(), rotation=45, fontsize=18)
ax.set_yticklabels(ax.get_yticklabels(), fontsize=18)
ax.grid(True)
st.pyplot(fig)


st.subheader("Monthly PM2.5 trend at each station")


station_data = main_df[main_df['station'] == selected_station]
# Mengelompokkan data berdasarkan bulan dan menghitung rata-rata cuaca (RAIN) untuk setiap bulan
monthly_rain_avg = station_data.groupby(
    station_data['datetime'].dt.to_period("M"))['PM2.5'].mean()
# Mengubah indeks ke format yang diinginkan
monthly_rain_avg.index = monthly_rain_avg.index.strftime('%m/%y')

# Menampilkan nilai PM2.5
avg_rain = station_data['PM2.5'].mean()
st.write(f"Rata-rata Polusi (PM2.5): {avg_rain:.2f} µg/m")

# Membuat plot untuk rata-rata (PM2.5)
fig, ax = plt.subplots(figsize=(25, 10))
sns.lineplot(x=monthly_rain_avg.index,
             y=monthly_rain_avg.values, marker='o', ax=ax, linewidth=3, markersize=12)
ax.set_title(
    f'Tren Tingkat Polusi (PM2.5) di Stasiun {selected_station}', fontsize=30)
ax.set_xlabel('Bulan dan Tahun', fontsize=30)
ax.set_ylabel('Rata-rata Polusi (PM2.5)', fontsize=30)
ax.set_xticklabels(ax.get_xticklabels(), rotation=45, fontsize=18)
ax.set_yticklabels(ax.get_yticklabels(), fontsize=18)
ax.grid(True)
st.pyplot(fig)

st.subheader("Correlation Matrix")

# Pilih kolom yang ingin ditampilkan dalam matriks korelasi
selected_columns = st.multiselect('Pilih Kolom Korelasi', main_df.columns)

# Filter data berdasarkan kolom yang dipilih
correlation_data = com_df[selected_columns]

# Cek apakah ada kolom yang dipilih sebelum membuat matriks korelasi
if not selected_columns:
    st.warning("Pilih setidaknya satu kolom untuk membuat matriks korelasi.")
else:
    # Plot matriks korelasi menggunakan heatmap
    correlation_matrix = correlation_data.corr()
    plt.figure(figsize=(10, 8))
    sns.heatmap(correlation_matrix, annot=True,
                cmap='coolwarm', linewidths=0.5)
    plt.title('Matriks Korelasi antara Parameter Kualitas Udara')
    st.pyplot(plt)
