import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency

# Pengaturan gaya untuk seaborn
sns.set(style='dark')

# Judul aplikasi
st.title("Proyek Analisis Data: Bike Sharing Dataset")

# Memuat data
df_hour = pd.read_csv('hour.csv')
df_daily = pd.read_csv('day.csv')

# Cleaning data
df_hour['dteday'] = pd.to_datetime(df_hour['dteday'])
df_daily['dteday'] = pd.to_datetime(df_daily['dteday'])

# Data Merging
hourly_agg = df_hour.groupby('dteday').agg({
    'season': 'first',
    'yr': 'first',
    'mnth': 'first',
    'holiday': 'first',
    'weekday': 'first',
    'workingday': 'first',
    'weathersit': 'mean',
    'temp': 'mean',
    'atemp': 'mean',
    'hum': 'mean',
    'windspeed': 'mean',
    'casual': 'sum',
    'registered': 'sum',
    'cnt': 'sum'
}).reset_index()

df = pd.merge(df_daily, hourly_agg, on='dteday', suffixes=('_daily', '_hourly'))

# Mengatur rent_start_date dan rent_end_date
df['rent_start_date'] = df['dteday']  # Misalkan dteday sebagai rent_start_date
df['rent_end_date'] = df['dteday']  # Misalkan dteday sebagai rent_end_date

# Sort dan reset index
df.sort_values(by="rent_start_date", inplace=True)
df.reset_index(inplace=True)

# Rentang tanggal untuk sidebar
min_date = df["rent_start_date"].min()
max_date = df["rent_start_date"].max()
 
with st.sidebar:
    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu', min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

# Filter data berdasarkan rentang tanggal
main_df = df[(df["rent_start_date"] >= str(start_date)) & 
             (df["rent_start_date"] <= str(end_date))]

# Pertanyaan 1: Tren penyewaan sepeda
st.header("Tren Penyewaan Sepeda dari Waktu ke Waktu")
plt.figure(figsize=(10, 6))
sns.lineplot(data=main_df, x='dteday', y='cnt_daily')
plt.title('Total Rentals Over Time (Daily)')
st.pyplot(plt)

# Pertanyaan 2: Pengaruh Cuaca
def categorize_season(month):
    if month in [3, 4, 5]:
        return 'Spring'
    elif month in [6, 7, 8]:
        return 'Summer'
    elif month in [9, 10, 11]:
        return 'Fall'
    else:
        return 'Winter'

def categorize_weather(weather):
    if weather == 1:
        return 'Clear'
    elif weather == 2:
        return 'Mist'
    elif weather == 3:
        return 'Light Snow/Rain'
    else:
        return 'Heavy Rain/Snow'

main_df['season_category'] = main_df['mnth_daily'].apply(categorize_season)
main_df['weather_category'] = main_df['weathersit_daily'].apply(categorize_weather)

season_cluster = main_df.groupby('season_category').agg({
    'cnt_daily': 'mean',
    'temp_daily': 'mean',
    'hum_daily': 'mean',
    'windspeed_daily': 'mean'
}).reset_index()

weather_cluster = main_df.groupby('weather_category').agg({
    'cnt_daily': 'mean',
    'temp_daily': 'mean',
    'hum_daily': 'mean',
    'windspeed_daily': 'mean'
}).reset_index()

st.header("Pengaruh Musim dan Cuaca terhadap Penyewaan Sepeda")
st.subheader("Rata-rata Penyewaan Sepeda Berdasarkan Musim")
plt.figure(figsize=(10, 6))
sns.barplot(data=season_cluster, x='season_category', y='cnt_daily')
plt.title('Average Rentals by Season')
st.pyplot(plt)

st.subheader("Rata-rata Penyewaan Sepeda Berdasarkan Cuaca")
plt.figure(figsize=(10, 6))
sns.barplot(data=weather_cluster, x='weather_category', y='cnt_daily')
plt.title('Average Rentals by Weather')
st.pyplot(plt)

# Pertanyaan 3: Pengaruh Suhu, Kelembapan, dan Kecepatan Angin
st.header("Pengaruh Suhu, Kelembapan, dan Kecepatan Angin terhadap Penyewaan Sepeda Harian")
st.subheader("Rentals vs Temperature (Daily)")
plt.figure(figsize=(10, 6))
sns.scatterplot(data=main_df, x='temp_daily', y='cnt_daily')
plt.title('Rentals vs Temperature (Daily)')
st.pyplot(plt)

st.subheader("Rentals vs Humidity (Daily)")
plt.figure(figsize=(10, 6))
sns.scatterplot(data=main_df, x='hum_daily', y='cnt_daily')
plt.title('Rentals vs Humidity (Daily)')
st.pyplot(plt)

st.subheader("Rentals vs Wind Speed (Daily)")
plt.figure(figsize=(10, 6))
sns.scatterplot(data=main_df, x='windspeed_daily', y='cnt_daily')
plt.title('Rentals vs Wind Speed (Daily)')
st.pyplot(plt)
