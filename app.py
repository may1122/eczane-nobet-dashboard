import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_calendar import calendar

st.set_page_config(page_title="Eczane Nöbet Dashboard", layout="wide")

st.title("💊 Eczane Nöbet Dashboard")

# -------------------------------------------------
# EXCEL OKUMA
# -------------------------------------------------

@st.cache_data
def load_excel(file):

    xls = pd.ExcelFile(file)

    df_list = []
    genel = None

    for sheet in xls.sheet_names:

        df = pd.read_excel(xls, sheet_name=sheet)

        # unnamed sütun sil
        df = df.loc[:, ~df.columns.astype(str).str.contains("Unnamed")]

        # GENEL sayfası
        if sheet.upper() == "GENEL":
            genel = df
            continue

        # boş satırları sil
        df = df.dropna(how="all")

        # Grup sütunu ekle
        df["Grup"] = sheet

        df_list.append(df)

    if len(df_list) == 0:
        st.error("Excel sayfaları okunamadı.")
        st.stop()

    df = pd.concat(df_list, ignore_index=True)

    # ----------------------------------------------
    # Tarih sütunlarını bul
    # ----------------------------------------------

    tarih_sutunlari = []

    for col in df.columns:

        try:
            pd.to_datetime(col)
            tarih_sutunlari.append(col)
        except:
            pass

    if len(tarih_sutunlari) == 0:
        st.error("Tarih sütunları bulunamadı.")
        st.stop()

    # ----------------------------------------------
    # LONG FORMAT
    # ----------------------------------------------

    df_long = df.melt(
        id_vars=["Grup"],
        value_vars=tarih_sutunlari,
        var_name="Tarih",
        value_name="Eczane"
    )

    df_long["Tarih"] = pd.to_datetime(df_long["Tarih"], errors="coerce")

    df_long = df_long.dropna(subset=["Tarih", "Eczane"])

    return df_long, genel


# -------------------------------------------------
# DOSYA YÜKLE
# -------------------------------------------------

file = st.file_uploader("Excel Dosyası Yükle", type=["xlsx"])

if file is None:
    st.stop()

df, genel = load_excel(file)

# -------------------------------------------------
# ECZANE ARAMA
# -------------------------------------------------

st.sidebar.header("🔎 Filtre")

eczane_arama = st.sidebar.text_input("Eczane Ara")

if eczane_arama:
    df = df[df["Eczane"].astype(str).str.contains(eczane_arama, case=False)]

# -------------------------------------------------
# GENEL İSTATİSTİK
# -------------------------------------------------

st.subheader("📊 Eczane Nöbet Sayıları")

sayim = df["Eczane"].value_counts().reset_index()
sayim.columns = ["Eczane", "Nöbet"]

fig = px.bar(sayim, x="Eczane", y="Nöbet")

st.plotly_chart(fig, use_container_width=True)

# -------------------------------------------------
# GRUP ANALİZ
# -------------------------------------------------

st.subheader("👥 Grup Analizi")

grup = df.groupby("Grup")["Eczane"].count().reset_index()

fig2 = px.bar(grup, x="Grup", y="Eczane")

st.plotly_chart(fig2, use_container_width=True)

# -------------------------------------------------
# TAKVİM
# -------------------------------------------------

st.subheader("📅 Nöbet Takvimi")

events = []

for _, row in df.iterrows():

    events.append(
        {
            "title": str(row["Eczane"]),
            "start": row["Tarih"].strftime("%Y-%m-%d")
        }
    )

calendar_options = {
    "initialView": "dayGridMonth"
}

calendar(events=events, options=calendar_options)

# -------------------------------------------------
# TARİH FİLTRE
# -------------------------------------------------

st.subheader("📆 Tarihe Göre Nöbet")

tarih = st.date_input("Tarih Seç")

sonuc = df[df["Tarih"] == pd.to_datetime(tarih)]

st.dataframe(sonuc)

# -------------------------------------------------
# ECZANE DETAY
# -------------------------------------------------

st.subheader("🏥 Eczane Detay")

eczane = st.selectbox("Eczane Seç", sorted(df["Eczane"].unique()))

eczane_df = df[df["Eczane"] == eczane]

st.write("Toplam nöbet:", len(eczane_df))

st.dataframe(eczane_df)
