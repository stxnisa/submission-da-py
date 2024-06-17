import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

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

# Pertanyaan 1: Tren penyewaan sepeda
st.header("Tren Penyewaan Sepeda dari Waktu ke Waktu")
plt.figure(figsize=(10, 6))
sns.lineplot(data=df, x='dteday', y='cnt_daily')
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

df['season_category'] = df['mnth_daily'].apply(categorize_season)
df['weather_category'] = df['weathersit_daily'].apply(categorize_weather)

season_cluster = df.groupby('season_category').agg({
    'cnt_daily': 'mean',
    'temp_daily': 'mean',
    'hum_daily': 'mean',
    'windspeed_daily': 'mean'
}).reset_index()

weather_cluster = df.groupby('weather_category').agg({
    'cnt_daily': 'mean',
    'temp_daily': 'mean',
    'hum_daily': 'mean',
    'windspeed_daily': 'mean'
}).reset_index()

st.header("Pengaruh Musim dan Cuaca terhadap Penyewaan Sepeda")
st.subheader("Rata-rata Penyewaan Sepeda Berdasarkan Musim")
plt.figure(figsize=(10, 6))
sns.barplot(data=season_cluster, x='season_category', y='c
