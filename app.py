import streamlit as st
import pandas as pd
import plotly.express as px
import calendar

st.set_page_config(page_title="Eczane Nöbet Takip Sistemi", layout="wide")

@st.cache_data
def load_excel(file):

    xls = pd.ExcelFile(file)

    all_data = []
    genel = None

    for sheet in xls.sheet_names:

        df = pd.read_excel(file, sheet_name=sheet)

        # Unnamed sütunları kaldır
        df = df.loc[:, ~df.columns.str.contains('^Unnamed')]

        if "GENEL" in sheet.upper():

            genel = df[[
                "Eczane",
                "Grup",
                "Geçmiş Katsayı",
                "Geçmiş Bayram",
                "Toplam Nöbet",
                "Toplam Katsayı",
                "Bayram"
            ]]

            continue

        if "Tarih" not in df.columns:
            continue

        df["Tarih"] = pd.to_datetime(df["Tarih"], errors="coerce")

        df_long = df.melt(
            id_vars=["Tarih", "Gün"],
            var_name="Grup",
            value_name="Eczane"
        )

        df_long = df_long.dropna(subset=["Eczane"])

        df_long["Ay"] = sheet

        all_data.append(df_long)

    df = pd.concat(all_data, ignore_index=True)

    return df, genel


st.title("💊 Eczane Nöbet Takip Sistemi")

file = st.file_uploader("Excel dosyasını yükleyin", type=["xlsx"])

if not file:
    st.info("Başlamak için Excel dosyasını yükleyin.")
    st.stop()

df, genel = load_excel(file)

menu = st.sidebar.radio("Menü", [
    "Genel Özet",
    "Tarih Seç",
    "Aylık Takvim",
    "Grup Analizi",
    "Eczane Analizi"
])

gun_sira = ["Pzt","Salı","Çarş","Perş","Cuma","Ctesi","Pazar"]


# GENEL ÖZET
if menu == "Genel Özet":

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Toplam Nöbet", len(df))
    col2.metric("Toplam Eczane", df["Eczane"].nunique())
    col3.metric("Toplam Ay", df["Ay"].nunique())
    col4.metric("Ortalama Nöbet", round(len(df) / df["Eczane"].nunique(), 2))

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

    st.divider()

    st.subheader("Özet Tablo")

    gun_pivot = pd.pivot_table(
        df,
        index=["Eczane","Grup"],
        columns="Gün",
        aggfunc="size",
        fill_value=0
    ).reset_index()

    mevcut_gunler = [g for g in gun_sira if g in gun_pivot.columns]

    gun_pivot = gun_pivot[["Eczane","Grup"] + mevcut_gunler]

    ozet = genel.merge(gun_pivot, on=["Eczane","Grup"], how="left")

    ozet.fillna(0, inplace=True)

    st.dataframe(ozet, use_container_width=True)


# TARİH SEÇ
elif menu == "Tarih Seç":

    tarih = st.selectbox(
        "Tarih seç",
        sorted(df["Tarih"].dropna().unique())
    )

    sonuc = df[df["Tarih"] == tarih]

    st.subheader("Nöbetçi Eczaneler")

    st.dataframe(
        sonuc[["Tarih","Gün","Grup","Eczane"]],
        use_container_width=True
    )


# AYLIK TAKVİM
elif menu == "Aylık Takvim":

    ay = st.selectbox(
        "Ay seç",
        sorted(df["Ay"].unique())
    )

    sonuc = df[df["Ay"] == ay]

    # Takvim pivot
    pivot = sonuc.pivot_table(
        index="Tarih",
        columns="Grup",
        values="Eczane",
        aggfunc="first"
    )

    pivot = pivot.fillna("")

    # AYIN TÜM GÜNLERİNİ OLUŞTUR
    min_date = sonuc["Tarih"].min()
    year = min_date.year
    month = min_date.month

    days_in_month = calendar.monthrange(year, month)[1]

    full_dates = pd.date_range(
        start=f"{year}-{month:02d}-01",
        end=f"{year}-{month:02d}-{days_in_month}"
    )

    pivot = pivot.reindex(full_dates)

    pivot.index.name = "Tarih"

    st.subheader("📅 Aylık Takvim")

    st.dataframe(
        pivot,
        use_container_width=True
    )

    st.divider()

    # 30-31 GÜNLÜK LİSTE
    st.subheader("📋 Aylık Nöbet Listesi")

    liste = sonuc.sort_values("Tarih")

    st.dataframe(
        liste[["Tarih","Gün","Grup","Eczane"]],
        use_container_width=True
    )


# GRUP ANALİZİ
elif menu == "Grup Analizi":

    grup = st.selectbox(
        "Grup seç",
        sorted(genel["Grup"].unique())
    )

    gun_pivot = pd.pivot_table(
        df,
        index=["Eczane","Grup"],
        columns="Gün",
        aggfunc="size",
        fill_value=0
    ).reset_index()

    mevcut_gunler = [g for g in gun_sira if g in gun_pivot.columns]

    gun_pivot = gun_pivot[["Eczane","Grup"] + mevcut_gunler]

    ozet = genel.merge(gun_pivot, on=["Eczane","Grup"], how="left")

    ozet.fillna(0, inplace=True)

    grup_ozet = ozet[ozet["Grup"] == grup]

    st.subheader(f"{grup} Eczaneleri")

    st.dataframe(grup_ozet, use_container_width=True)

    st.divider()

    sonuc = df[df["Grup"] == grup]

    sayim = (
        sonuc
        .groupby(["Gün","Eczane"])
        .size()
        .reset_index(name="Nöbet Sayısı")
    )

    sayim["Gün"] = pd.Categorical(
        sayim["Gün"],
        categories=gun_sira,
        ordered=True
    )

    fig = px.bar(
        sayim,
        x="Gün",
        y="Nöbet Sayısı",
        color="Eczane",
        barmode="group",
        category_orders={"Gün": gun_sira}
    )

    st.plotly_chart(fig, use_container_width=True)


# ECZANE ANALİZİ
elif menu == "Eczane Analizi":

    eczane = st.selectbox(
        "Eczane",
        sorted(df["Eczane"].unique())
    )

    sonuc = df[df["Eczane"] == eczane]

    st.metric("Toplam Nöbet", len(sonuc))

    st.dataframe(
        sonuc.sort_values("Tarih"),
        use_container_width=True
    )
