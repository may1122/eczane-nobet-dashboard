import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_calendar import calendar


st.set_page_config(page_title="Eczane Nöbet Takip Sistemi", layout="wide")

@st.cache_data
def load_excel(file):
    xls = pd.ExcelFile(file)
    all_data = []
    for sheet in xls.sheet_names:
        if "GENEL" in sheet.upper():
            continue
        df = pd.read_excel(file, sheet_name=sheet)
        if "Tarih" not in df.columns:
            continue
        df_long = df.melt(id_vars=["Tarih","Gün"], var_name="Grup", value_name="Eczane")
        df_long = df_long.dropna(subset=["Eczane"])
        df_long["Ay"] = sheet
        all_data.append(df_long)
    return pd.concat(all_data, ignore_index=True)

st.title("💊 Eczane Nöbet Takip Sistemi")

file = st.file_uploader("Excel dosyasını yükleyin", type=["xlsx"])

if not file:
    st.info("Başlamak için Excel dosyasını yükleyin.")
    st.stop()

df = load_excel(file)

menu = st.sidebar.radio("Menü",[
    "Genel Özet",
    "Tarih Seç",
    "Aylık Takvim",
    "Grup Analizi",
    "Eczane Analizi"
])

if menu == "Genel Özet":

    col1,col2,col3,col4 = st.columns(4)

    col1.metric("Toplam Nöbet", len(df))
    col2.metric("Toplam Eczane", df["Eczane"].nunique())
    col3.metric("Toplam Ay", df["Ay"].nunique())
    col4.metric("Ortalama Nöbet", round(len(df)/df["Eczane"].nunique(),2))

    # Pasta grafik
    st.subheader("Gün Dağılımı")

    gun_sayim = df["Gün"].value_counts().reset_index()
    gun_sayim.columns = ["Gün", "Sayı"]

    fig = px.pie(
        gun_sayim,
        names="Gün",
        values="Sayı",
        hole=0.4
    )

    st.plotly_chart(fig, use_container_width=True)

if df["Tarih"].dtype != "datetime64[ns]":
    df["Tarih"] = pd.to_datetime(
        df["Tarih"],
        dayfirst=True,
        errors="coerce"
    )


elif menu == "Tarih Seç":

    st.title("Tarih Seçerek Nöbetçi Bul")

    df["Tarih"] = pd.to_datetime(df["Tarih"])

    # Takvim event formatı
    events = []

    for tarih in df["Tarih"].unique():
        events.append({
            "title": "Nöbet Var",
            "start": tarih.strftime("%Y-%m-%d"),
            "allDay": True
        })

    calendar_options = {
        "initialView": "dayGridMonth",
        "locale": "tr",
        "height": 600,
    }

    selected = calendar(events=events, options=calendar_options)

    if selected and "dateClick" in selected:
        secilen_tarih = pd.to_datetime(selected["dateClick"]["date"])

        sonuc = df[df["Tarih"] == secilen_tarih]

        st.write(sonuc)


elif menu == "Aylık Takvim":

    ay = st.selectbox(
        "Ay seç",
        sorted(df["Ay"].unique())
    )

    sonuc = df[df["Ay"] == ay]

    pivot = sonuc.pivot(
        index="Tarih",
        columns="Grup",
        values="Eczane"
    )

    pivot = pivot.fillna("")

    def highlight_cells(val):
        if val == "":
            return "background-color: #eeeeee"
        else:
            return "background-color: #d4edda"

    styled = pivot.style.applymap(highlight_cells)

    st.dataframe(styled, use_container_width=True)


elif menu == "Grup Analizi":

    grup = st.selectbox(
        "Grup seç",
        sorted(df["Grup"].unique())
    )

    sonuc = df[df["Grup"] == grup]

    st.bar_chart(sonuc["Eczane"].value_counts())

elif menu == "Grup Analizi":
    grup = st.selectbox("Grup", sorted(df["Grup"].unique()))
    sonuc = df[df["Grup"]==grup]
    st.bar_chart(sonuc["Eczane"].value_counts())

elif menu == "Eczane Analizi":
    eczane = st.selectbox("Eczane", sorted(df["Eczane"].unique()))
    sonuc = df[df["Eczane"]==eczane]
    st.metric("Toplam Nöbet", len(sonuc))
    st.dataframe(sonuc.sort_values("Tarih"))
