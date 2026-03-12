aylar_tr = {
    1: "Ocak",
    2: "Şubat",
    3: "Mart",
    4: "Nisan",
    5: "Mayıs",
    6: "Haziran",
    7: "Temmuz",
    8: "Ağustos",
    9: "Eylül",
    10: "Ekim",
    11: "Kasım",
    12: "Aralık"
}


import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Eczane Nöbet Takip Sistemi", layout="wide")

@st.cache_data
def load_excel(file):

    xls = pd.ExcelFile(file)

    all_data = []
    genel = None

    for sheet in xls.sheet_names:

        df = pd.read_excel(file, sheet_name=sheet)

        # Unnamed sütunlarını kaldır
        df = df.loc[:, ~df.columns.str.contains('^Unnamed')]

        # GENEL sayfasını oku
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

        df_long = df.melt(
            id_vars=["Tarih", "Gün"],
            var_name="Grup",
            value_name="Eczane"
        )

        df_long = df_long.dropna(subset=["Eczane"])

        # TARİHİ GERÇEK TARİHE ÇEVİR
        df_long["Tarih"] = pd.to_datetime(
        df_long["Tarih"],
        dayfirst=True,
        errors="coerce"
)

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

    gun_sira = ["Pzt","Salı","Çarş","Perş","Cuma","Ctesi","Pazar"]

    mevcut_gunler = [g for g in gun_sira if g in gun_pivot.columns]

    gun_pivot = gun_pivot[["Eczane","Grup"] + mevcut_gunler]

    ozet = genel.merge(gun_pivot, on=["Eczane","Grup"], how="left")

    for g in gun_sira:
        if g in ozet.columns:
            ozet[g] = ozet[g].fillna(0)

    ozet = ozet[
        [
            "Eczane",
            "Grup",
            "Geçmiş Katsayı",
            "Geçmiş Bayram",
            "Toplam Nöbet",
            "Toplam Katsayı",
            "Bayram"
        ] + mevcut_gunler
    ]

    st.dataframe(ozet, use_container_width=True)


# TARİH SEÇ
elif menu == "Tarih Seç":

    min_tarih = df["Tarih"].min().date()
    max_tarih = df["Tarih"].max().date()

    # Tarih widget
    tarih = st.date_input(
        "Tarih seçin",
        value=min_tarih,
        min_value=min_tarih,
        max_value=max_tarih
    )

    # Eğer tarih pandas.Timestamp ise .date() ile datetime.date dönüştür
    if hasattr(tarih, "to_pydatetime"):
        secilen_tarih = tarih.to_pydatetime().date()
    else:
        secilen_tarih = tarih

    # Seçilen tarihe göre filtrele
    sonuc = df[df["Tarih"].dt.date == secilen_tarih]

    st.subheader(f"Seçilen Tarih: {secilen_tarih.day} {aylar_tr[secilen_tarih.month]} {secilen_tarih.year}")
    st.dataframe(sonuc.sort_values("Tarih"), use_container_width=True)



# AYLIK TAKVİM
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


# GRUP ANALİZİ
elif menu == "Grup Analizi":

    st.subheader("Grup Görünümü")

    grup = st.selectbox(
        "Grup seç",
        sorted(genel["Grup"].unique())
    )

    # Gün pivot oluştur
    gun_pivot = pd.pivot_table(
        df,
        index=["Eczane","Grup"],
        columns="Gün",
        aggfunc="size",
        fill_value=0
    ).reset_index()

    gun_sira = ["Pzt","Salı","Çarş","Perş","Cuma","Ctesi","Pazar"]

    mevcut_gunler = [g for g in gun_sira if g in gun_pivot.columns]

    gun_pivot = gun_pivot[["Eczane","Grup"] + mevcut_gunler]

    ozet = genel.merge(gun_pivot, on=["Eczane","Grup"], how="left")

    for g in gun_sira:
        if g in ozet.columns:
            ozet[g] = ozet[g].fillna(0)

    grup_ozet = ozet[ozet["Grup"] == grup]

    st.subheader(f"{grup} Eczaneleri")

    st.dataframe(grup_ozet, use_container_width=True)

    st.divider()

    st.subheader("Grup Günlere Göre Nöbet Dağılımı")

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
        title=f"{grup} Günlere Göre Nöbet Dağılımı",
        category_orders={"Gün": gun_sira}
    )

    st.plotly_chart(fig, use_container_width=True)


# ECZANE ANALİZİ
elif menu == "Eczane Analizi":

    st.subheader("Eczane Arama")

    # 🔎 Arama kutusu
    arama = st.text_input("Eczane adı ara")

    eczane_listesi = sorted(df["Eczane"].unique())

    # Arama varsa filtrele
    if arama:
        eczane_listesi = [
            e for e in eczane_listesi
            if arama.lower() in e.lower()
        ]

    # Scroll + seçim
    eczane = st.selectbox(
        "Eczane seç",
        eczane_listesi
    )

    sonuc = df[df["Eczane"] == eczane]

    st.metric("Toplam Nöbet", len(sonuc))

    st.dataframe(
        sonuc.sort_values("Tarih"),
        use_container_width=True
    )

    sonuc = df[df["Eczane"] == eczane]

    st.metric("Toplam Nöbet", len(sonuc))

    st.dataframe(sonuc.sort_values("Tarih"))
