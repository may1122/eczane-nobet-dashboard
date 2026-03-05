import streamlit as st
import pandas as pd
import plotly.express as px

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
    
    st.divider()
    st.subheader("Özet Tablo")

    # Gün bazlı dağılım
    gun_pivot = pd.pivot_table(
        df,
        index=["Eczane","Grup"],
        columns="Gün",
        aggfunc="size",
        fill_value=0
    ).reset_index()

    # Toplam nöbet
    toplam_nobet = df.groupby("Eczane").size().reset_index(name="Toplam Nöbet")

    # Bayram sayısı (Gün içinde "Bayram" varsa)
    if "Bayram" in df["Gün"].unique():
        bayram = df[df["Gün"]=="Bayram"].groupby("Eczane").size().reset_index(name="Bayram")
    else:
        bayram = pd.DataFrame(columns=["Eczane","Bayram"])

    # Merge
    ozet = gun_pivot.merge(toplam_nobet, on="Eczane", how="left")
    ozet = ozet.merge(bayram, on="Eczane", how="left")

    ozet["Bayram"] = ozet["Bayram"].fillna(0)

    # Kolon sırası düzeni
    sabit_kolonlar = ["Eczane","Grup","Toplam Nöbet","Bayram"]
    diger_kolonlar = [col for col in ozet.columns if col not in sabit_kolonlar]

    ozet = ozet[sabit_kolonlar + diger_kolonlar]

    st.dataframe(ozet, use_container_width=True)
    
elif menu == "Tarih Seç":
    tarih = st.selectbox("Tarih", sorted(df["Tarih"].unique()))
    sonuc = df[df["Tarih"]==tarih]
    st.dataframe(sonuc)


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

    st.subheader("Grup Günlere Göre Nöbet Dağılımı")

    grup = st.selectbox(
        "Grup seç",
        sorted(df["Grup"].unique())
    )

    sonuc = df[df["Grup"] == grup]

    # Gün + Eczane bazlı sayım
    sayim = (
        sonuc
        .groupby(["Gün","Eczane"])
        .size()
        .reset_index(name="Nöbet Sayısı")
    )

    # Gün sırası (doğru sırada görünmesi için)
    gun_sira = ["Pzt","Salı","Çarş","Perş","Cuma","Ctesi","Pazar"]
    sayim["Gün"] = pd.Categorical(sayim["Gün"], categories=gun_sira, ordered=True)

    # Grafik
    fig = px.bar(
        sayim,
        x="Gün",
        y="Nöbet Sayısı",
        color="Eczane",
        barmode="group",
        title=f"{grup} Günlere Göre Nöbet Dağılımı"
    )

    st.plotly_chart(fig, use_container_width=True)




elif menu == "Eczane Analizi":
    eczane = st.selectbox("Eczane", sorted(df["Eczane"].unique()))
    sonuc = df[df["Eczane"]==eczane]
    st.metric("Toplam Nöbet", len(sonuc))
    st.dataframe(sonuc.sort_values("Tarih"))
