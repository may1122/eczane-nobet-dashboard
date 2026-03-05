import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_calendar import calendar

st.set_page_config(page_title="Eczane Nöbet Dashboard", layout="wide")

st.title("💊 Eczane Nöbet Analiz Dashboard")

# ---------------------------------------------------
# EXCEL OKUMA
# ---------------------------------------------------

@st.cache_data
def load_excel(file):

    xls = pd.ExcelFile(file)

    df_list = []

    for sheet in xls.sheet_names:

        if sheet.upper() == "GENEL":
            genel = pd.read_excel(xls, sheet_name=sheet)

            # unnamed sütun sil
            genel = genel.loc[:, ~genel.columns.str.contains("^Unnamed")]

        else:

            df = pd.read_excel(xls, sheet_name=sheet)

            # unnamed sütun sil
            df = df.loc[:, ~df.columns.str.contains("^Unnamed")]

            df["Grup"] = sheet

            df_list.append(df)

    df = pd.concat(df_list, ignore_index=True)

    # ------------------------------------------------
    # LONG FORMAT
    # ------------------------------------------------

    df_long = df.melt(
        id_vars=["Grup"],
        var_name="Tarih",
        value_name="Eczane"
    )

    # tarih güvenli parse
    df_long["Tarih"] = pd.to_datetime(
        df_long["Tarih"],
        errors="coerce"
    )

    # boş satırları sil
    df_long = df_long.dropna(subset=["Tarih", "Eczane"])

    return df_long, genel


# ---------------------------------------------------
# DOSYA YÜKLEME
# ---------------------------------------------------

file = st.file_uploader("Excel Dosyası Yükle", type=["xlsx"])

if file is None:
    st.stop()

df, genel = load_excel(file)

# ---------------------------------------------------
# ECZANE ARAMA
# ---------------------------------------------------

st.sidebar.header("🔎 Filtreler")

eczane_arama = st.sidebar.text_input("Eczane Ara")

if eczane_arama:
    df = df[df["Eczane"].str.contains(eczane_arama, case=False)]

# ---------------------------------------------------
# GENEL İSTATİSTİK
# ---------------------------------------------------

st.subheader("📊 Genel Nöbet Sayıları")

eczane_sayim = df["Eczane"].value_counts().reset_index()
eczane_sayim.columns = ["Eczane", "Nöbet"]

fig = px.bar(
    eczane_sayim,
    x="Eczane",
    y="Nöbet",
    title="Eczane Nöbet Sayısı"
)

st.plotly_chart(fig, use_container_width=True)

# ---------------------------------------------------
# GRUP ANALİZİ
# ---------------------------------------------------

st.subheader("👥 Grup Analizi")

grup_sayim = df.groupby("Grup")["Eczane"].count().reset_index()

fig2 = px.bar(
    grup_sayim,
    x="Grup",
    y="Eczane",
    title="Grup Nöbet Sayıları"
)

st.plotly_chart(fig2, use_container_width=True)

# ---------------------------------------------------
# TAKVİM OLUŞTURMA
# ---------------------------------------------------

st.subheader("📅 Nöbet Takvimi")

events = []

for i, row in df.iterrows():

    events.append(
        {
            "title": row["Eczane"],
            "start": str(row["Tarih"].date())
        }
    )

calendar_options = {
    "initialView": "dayGridMonth",
}

calendar(events=events, options=calendar_options)

# ---------------------------------------------------
# TARİHE GÖRE ARAMA
# ---------------------------------------------------

st.subheader("📆 Tarihe Göre Nöbet")

tarih = st.date_input("Tarih Seç")

sonuc = df[df["Tarih"] == pd.to_datetime(tarih)]

st.dataframe(sonuc)

# ---------------------------------------------------
# ECZANE ANALİZ
# ---------------------------------------------------

st.subheader("🏥 Eczane Detay")

eczane_sec = st.selectbox(
    "Eczane Seç",
    df["Eczane"].unique()
)

eczane_df = df[df["Eczane"] == eczane_sec]

st.write("Toplam Nöbet:", len(eczane_df))

st.dataframe(eczane_df)
