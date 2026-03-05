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

        df_long["Tarih"] = pd.to_datetime(df_long["Tarih"])

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

    st.dataframe(ozet, use_container_width=True)



# TARİH SEÇ
elif menu == "Tarih Seç":

    st.subheader("📅 Tarih Seçerek Nöbetçi Bul")

    tarih = st.date_input("Tarih Seç")

    tarih = pd.to_datetime(tarih)

    sonuc = df[df["Tarih"] == tarih]

    if sonuc.empty:

        st.warning("Bu tarihte nöbetçi bulunamadı")

    else:

        st.success(f"{tarih.date()} nöbetçileri")

        cols = st.columns(len(sonuc))

        for i, (_, row) in enumerate(sonuc.iterrows()):

            with cols[i]:

                st.markdown(
                    f"""
                    <div style="
                    background:linear-gradient(135deg,#667eea,#764ba2);
                    padding:25px;
                    border-radius:15px;
                    text-align:center;
                    color:white;
                    font-size:24px;
                    font-weight:bold;
                    ">
                    {row['Eczane']}
                    <br>
                    <span style='font-size:16px'>Grup {row['Grup']}</span>
                    </div>
                    """,
                    unsafe_allow_html=True
                )



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

    st.dataframe(pivot, use_container_width=True)



# GRUP ANALİZİ
elif menu == "Grup Analizi":

    st.subheader("Grup Görünümü")

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

    ozet = genel.merge(gun_pivot, on=["Eczane","Grup"], how="left")

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

    fig = px.bar(
        sayim,
        x="Gün",
        y="Nöbet Sayısı",
        color="Eczane",
        barmode="group",
        title=f"{grup} Günlere Göre Nöbet Dağılımı"
    )

    st.plotly_chart(fig, use_container_width=True)



# ECZANE ANALİZİ
elif menu == "Eczane Analizi":

    st.subheader("🔎 Eczane Ara")

    arama = st.text_input("Eczane adı yaz")

    eczaneler = sorted(df["Eczane"].unique())

    if arama:
        eczaneler = [e for e in eczaneler if arama.lower() in e.lower()]

    eczane = st.selectbox("Eczane seç", eczaneler)

    sonuc = df[df["Eczane"] == eczane]

    st.metric("Toplam Nöbet", len(sonuc))

    st.dataframe(sonuc.sort_values("Tarih"))
