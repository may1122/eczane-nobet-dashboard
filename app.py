import streamlit as st
import pandas as pd
from streamlit_calendar import calendar

st.set_page_config(page_title="Eczane Nöbet", layout="wide")

st.title("💊 Eczane Nöbet Dashboard")

uploaded_file = st.file_uploader("Excel dosyası yükle", type=["xlsx"])


@st.cache_data
def load_excel(file):

    df = pd.read_excel(file)

    # Unnamed kolon temizleme
    df = df.loc[:, ~df.columns.str.contains("Unnamed")]

    # Grup kolonunu bul
    grup_col = df.columns[0]
    df.rename(columns={grup_col: "Grup"}, inplace=True)

    # Uzun formata çevir
    df_long = df.melt(
        id_vars=["Grup"],
        var_name="Tarih",
        value_name="Eczane"
    )

    df_long["Tarih"] = pd.to_datetime(df_long["Tarih"], errors="coerce")

    df_long = df_long.dropna(subset=["Tarih"])
    df_long = df_long[df_long["Eczane"].notna()]

    return df_long


if uploaded_file:

    df = load_excel(uploaded_file)

    tab1, tab2 = st.tabs(["📅 Takvim", "📊 Grup Görünümü"])


    # ---------------------------------------------------
    # TAKVİM
    # ---------------------------------------------------

    with tab1:

        st.subheader("📅 Aylık Nöbet Takvimi")

        events = []

        for _, row in df.iterrows():

            events.append({
                "title": row["Eczane"],
                "start": row["Tarih"].strftime("%Y-%m-%d"),
                "end": row["Tarih"].strftime("%Y-%m-%d")
            })

        calendar_options = {
            "initialView": "dayGridMonth",
            "locale": "tr",
        }

        calendar(events=events, options=calendar_options)


        st.divider()

        st.subheader("📅 Tarih Seç")

        secilen_tarih = st.date_input("Tarih seç")

        gun_df = df[df["Tarih"].dt.date == secilen_tarih]

        if not gun_df.empty:
            st.dataframe(gun_df[["Grup", "Eczane"]])
        else:
            st.info("Bu tarihte nöbetçi eczane yok")


        st.divider()

        st.subheader("🔎 Eczane Ara")

        arama = st.text_input("Eczane adı yaz")

        if arama:
            sonuc = df[df["Eczane"].str.contains(arama, case=False)]

            if not sonuc.empty:
                st.dataframe(sonuc)
            else:
                st.warning("Eczane bulunamadı")


    # ---------------------------------------------------
    # GRUP GÖRÜNÜMÜ
    # ---------------------------------------------------

    with tab2:

        st.subheader("📊 Grup Özet")

        gruplar = sorted(df["Grup"].unique())

        secilen_grup = st.selectbox("Grup seç", gruplar)

        grup_df = df[df["Grup"] == secilen_grup]

        st.metric("Toplam Nöbet", len(grup_df))

        st.dataframe(grup_df[["Tarih", "Eczane"]].sort_values("Tarih"))
