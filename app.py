import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

def get_total_df_Perjam_count(df_Perjam):
  df_Perjam_count =  df_Perjam.groupby(by="hours").agg({"count_cr": ["sum"]})
  return df_Perjam

def df_harian_count(df_harian):
    df_harian_2011 = df_harian.query(str('dteday >= "2011-01-01" and dteday < "2012-12-31"'))
    return df_harian_count_2011
  


Harian_df = pd.read_csv("df_harian_clean.csv")
Perjam_df = pd.read_csv("df_Perjam_clean.csv")

Harian_df['dteday'] = pd.to_datetime(Harian_df['date'])
Perjam_df['dteday'] = pd.to_datetime(Perjam_df['date'])

st.set_page_config(layout="wide")
st.title("Analisis Data Bike Sharing")

daily_count = Harian_df.groupby('dteday').agg({'casual': 'sum', 'registered': 'sum'}).reset_index()
daily_count.rename(columns={'casual': 'casual_user', 'registered': 'registered_user'}, inplace=True)  


fig, ax = plt.subplots(figsize=(12, 6))
sns.lineplot(x='dteday', y='casual_user', data=daily_count, label='Casual Users', ax=ax)
sns.lineplot(x='dteday', y='registered_user', data=daily_count, label='Registered Users', ax=ax)
ax.set_title('Daily Casual vs. Registered Users Over Time')
ax.set_xlabel('Date')
ax.set_ylabel('Number of Users')
ax.legend()
ax.tick_params(axis='x', rotation=45)
plt.tight_layout()
st.pyplot(fig)

st.subheader(" Data Penyewaan Berdasarkan Jam ")
hourly_count = Perjam_df.groupby('hour')['count'].sum()
fig, ax = plt.subplots(figsize=(10, 6))
hourly_count.plot(kind='bar', ax=ax)
ax.set_title('Jumlah Penyewaan Berdasarkan Jam')
ax.set_xlabel('Jam')
ax.set_ylabel('Jumlah Penyewaan')
plt.tight_layout()
st.pyplot(fig)



st.subheader(" Data Penyewaan Berdasarkan Season")
season_count = Harian_df.groupby('season')['count'].sum()
fig, ax = plt.subplots(figsize=(10, 6))
season_count.plot(kind='bar', ax=ax)
ax.set_title('Jumlah Penyewaan Berdasarkan Musim')
ax.set_xlabel('Musim')
ax.set_ylabel('Jumlah Penyewaan')
plt.tight_layout()
st.pyplot(fig)

#Menambahkan filtering pada streamlit
# Filtering logic
filtered_harian_df = Harian_df[
    (Harian_df['dteday'].dt.date >= start_date) &
    (Harian_df['dteday'].dt.date <= end_date) &
    (Harian_df['season'].isin(selected_season)) &
    (Harian_df['month'].isin(selected_months)) &
    (Harian_df['weekday'].isin(selected_weekdays)) &
    (Harian_df['weather_situation'].isin(selected_weather_conds))
].copy()

filtered_perjam_df = Perjam_df[
    (Perjam_df['dteday'].dt.date >= start_date) &
    (Perjam_df['dteday'].dt.date <= end_date) &
    (Perjam_df['season'].isin(selected_season)) &
    (Perjam_df['hour'].isin(selected_hour_int)) &
    (Perjam_df['month'].isin(selected_months)) &
    (Perjam_df['weekday'].isin(selected_weekdays)) &
    (Perjam_df['weather_situation'].isin(selected_weather_conds))
].copy()

# Recalculate daily_count and hourly_count based on filtered data
daily_count = filtered_harian_df.groupby('dteday').agg({'casual': 'sum', 'registered': 'sum'}).reset_index()
daily_count.rename(columns={'casual': 'casual_user', 'registered': 'registered_user'}, inplace=True)
hourly_count = filtered_perjam_df.groupby('hour')['count'].sum()
season_count = filtered_harian_df.groupby('season')['count'].sum()
