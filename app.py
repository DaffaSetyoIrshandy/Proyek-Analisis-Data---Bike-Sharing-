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

# Fitur interaktif filtering 
st.sidebar.header("Filter Data")

season_map = {
    1: "Spring", 2: "Summer", 3: "Fall", 4: "Winter"
}
month_names_map = {
    1: "Januari", 2: "Februari", 3: "Maret", 4: "April", 5: "Mei", 6: "Juni",
    7: "Juli", 8: "Agustus", 9: "September", 10: "Oktober", 11: "November", 12: "Desember"
}
weekday_names_map = {
    0: "Minggu", 1: "Senin", 2: "Selasa", 3: "Rabu", 4: "Kamis", 5: "Jumat", 6: "Sabtu"
}



min_date_df = Harian_df['dteday'].min().date()
max_date_df = Harian_df['dteday'].max().date()

# Date range filter
start_date, end_date = st.sidebar.slider(
    "Pilih Rentang Tanggal",
    min_value=min_date_df,
    max_value=max_date_df,
    value=(min_date_df, max_date_df)
)

# Season filter
Harian_df['season_name'] = Harian_df['season'].map(season_map)
season_names_list = ["Spring", "Summer", "Fall", "Winter"]
selected_season = st.sidebar.multiselect(
    "Pilih Musim",
    options=season_names_list,
    default=season_names_list
)

# Hour filter
hours_str = [f"{i:02d}:00" for i in range(24)]

selected_hour = st.sidebar.multiselect(
    "Pilih Jam",
    options=hours_str,
    default=hours_str
)
selected_hour_int = [int(h.split(':')[0]) for h in selected_hour]


# Month filter
Harian_df['month_name'] = Harian_df['mnth'].map(month_names_map)
selected_month_names = st.sidebar.multiselect(
    "Pilih Bulan",
    options=list(month_names_map.values()),
    default=list(month_names_map.values())
)
selected_months = [k for k, v in month_names_map.items() if v in selected_month_names]

# Weekday filter
Harian_df['weekday_name'] = Harian_df['weekday'].map(weekday_names_map)
selected_weekday_names = st.sidebar.multiselect(
    "Pilih Hari",
    options=list(weekday_names_map.values()),
    default=list(weekday_names_map.values())
)
selected_weekdays = [k for k, v in weekday_names_map.items() if v in selected_weekday_names]


filtered_harian = Harian_df[
    (Harian_df['dteday'] >= pd.to_datetime(start_date)) &
    (Harian_df['dteday'] <= pd.to_datetime(end_date)) &
    (Harian_df['season_name'].isin(selected_season)) &
    (Harian_df['month_name'].isin(selected_month_names)) &
    (Harian_df['weekday_name'].isin(selected_weekday_names))
]

filtered_perjam = Perjam_df[
    (Perjam_df['dteday'] >= pd.to_datetime(start_date)) &
    (Perjam_df['dteday'] <= pd.to_datetime(end_date)) &
    (Perjam_df['hour'].isin(selected_hour_int)) &
    (Perjam_df['season'].isin(selected_season)) &
    (Perjam_df['month'].isin(selected_months)) &
    (Perjam_df['weekday'].isin(selected_weekdays))
]

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

hourly_count = (
    filtered_perjam
    .groupby('hour')['count']
    .sum()
    .reindex(range(24)) 
)

fig, ax = plt.subplots(figsize=(10, 6))
hourly_count.plot(kind='bar', ax=ax)
ax.set_title('Jumlah Penyewaan Berdasarkan jam ')
ax.set_xlabel('Jam')
ax.set_ylabel('Jumlah Penyewaan')
plt.tight_layout()
st.pyplot(fig)


st.subheader(" Data Penyewaan Berdasarkan Season")
season_order = ["Spring", "Summer", "Fall", "Winter"]
season_name_count = (
  filtered_harian
  .groupby('season_name')['count']
  .sum()
  .reindex(season_order)
)
fig, ax = plt.subplots(figsize=(10, 6))
season_name_count.plot(kind='bar', ax=ax)
ax.set_title('Jumlah Penyewaan Berdasarkan Musim')
ax.set_xlabel('Musim')
ax.set_ylabel('Jumlah Penyewaan')
plt.tight_layout()
st.pyplot(fig)
