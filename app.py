import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Eczane Nöbet Takip Sistemi",
    page_icon="💊",
    layout="wide"
)

# ---------------------------------------------------
# CSS TASARIM
# ---------------------------------------------------

st.markdown("""
<style>

.main-title{
font-size:40px;
font-weight:700;
color:#0f172a;
}

.metric-card{
background-color:#f8fafc;
padding:20px;
border-radius:12px;
box-shadow:0 2px 6px rgba(0,0,0,0.05);
}

</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------
# EXCEL OKUMA
# ---------------------------------------------------

@st.cache_data
def load_excel(file):

    xls = pd.ExcelFile(file)

    all_data = []
    genel = None

    for sheet in xls.sheet_names:

        df = pd.read_excel(file, sheet_name=sheet)

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


# ---------------------------------------------------
# BAŞLIK
# ---------------------------------------------------

st.markdown('<p class="main-title">💊 Eczane Nöbet Takip Sistemi</p>', unsafe_allow_html=True)

file = st.file_uploader("Excel dosyasını yükleyin", type=["xlsx"])

if not file:
    st.info("Başlamak için Excel dosyasını yükleyin.")
    st.stop()

df, genel = load_excel(file)

# ---------------------------------------------------
# SIDEBAR
# ---------------------------------------------------

st.sidebar.title("📊 Menü")

menu = st.sidebar.radio(
    "",
    [
        "Genel Özet",
        "Tarih Seç",
        "Aylık Takvim",
        "Grup Analizi",
        "Eczane Analizi"
    ]
)

gun_sira = ["Pzt","Salı","Çarş","Perş","Cuma","Ctesi","Pazar"]

# ---------------------------------------------------
# GENEL ÖZET
# ---------------------------------------------------

if menu == "Genel Özet":

    col1,col2,col3,col4 = st.columns(4)

    col1.metric("Toplam Nöbet", len(df))
    col2.metric("Toplam Eczane", df["Eczane"].nunique())
    col3.metric("Toplam Ay", df["Ay"].nunique())
    col4.metric("Ortalama Nöbet", round(len(df)/df["Eczane"].nunique(),2))

    st.divider()

    col1,col2 = st.columns(2)

    with col1:

        st.subheader("📊 Gün Dağılımı")

        gun_sayim = df["Gün"].value_counts().reset_index()
        gun_sayim.columns = ["Gün","Sayı"]

        fig = px.pie(
            gun_sayim,
            names="Gün",
            values="Sayı",
            hole=0.5
        )

        st.plotly_chart(fig,use_container_width=True)

    with col2:

        st.subheader("📈 Günlere Göre Nöbet")

        fig = px.bar(
            gun_sayim,
            x="Gün",
            y="Sayı",
            color="Gün"
        )

        st.plotly_chart(fig,use_container_width=True)

    st.divider()

    st.subheader("📋 Özet Tablo")

    gun_pivot = pd.pivot_table(
        df,
        index=["Eczane","Grup"],
        columns="Gün",
        aggfunc="size",
        fill_value=0
    ).reset_index()

    mevcut_gunler = [g for g in gun_sira if g in gun_pivot.columns]

    gun_pivot = gun_pivot[["Eczane","Grup"] + mevcut_gunler]

    ozet = genel.merge(gun_pivot,on=["Eczane","Grup"],how="left")

    ozet.fillna(0,inplace=True)

    st.dataframe(ozet,use_container_width=True,height=500)

# ---------------------------------------------------
# TARİH SEÇ
# ---------------------------------------------------

elif menu == "Tarih Seç":

    st.subheader("📅 Tarihe Göre Nöbet")

    tarih = st.selectbox("Tarih",sorted(df["Tarih"].unique()))

    sonuc = df[df["Tarih"]==tarih]

    st.dataframe(
        sonuc[["Tarih","Gün","Grup","Eczane"]],
        use_container_width=True
    )

# ---------------------------------------------------
# AYLIK TAKVİM
# ---------------------------------------------------

elif menu == "Aylık Takvim":

    st.subheader("📆 Aylık Nöbet Listesi")

    ay = st.selectbox("Ay seç",sorted(df["Ay"].unique()))

    sonuc = df[df["Ay"]==ay]

    pivot = sonuc.pivot_table(
        index="Tarih",
        columns="Grup",
        values="Eczane",
        aggfunc="first"
    )

    pivot = pivot.sort_index()

    pivot = pivot.fillna("")

    st.dataframe(
        pivot,
        use_container_width=True,
        height=600
    )

# ---------------------------------------------------
# GRUP ANALİZİ
# ---------------------------------------------------

elif menu == "Grup Analizi":

    st.subheader("🏥 Grup Analizi")

    grup = st.selectbox(
        "Grup seç",
        sorted(genel["Grup"].unique())
    )

    sonuc = df[df["Grup"]==grup]

    st.subheader(f"{grup} Gün Dağılımı")

    sayim = sonuc.groupby(["Gün","Eczane"]).size().reset_index(name="Nöbet")

    sayim["Gün"] = pd.Categorical(
        sayim["Gün"],
        categories=gun_sira,
        ordered=True
    )

    fig = px.bar(
        sayim,
        x="Gün",
        y="Nöbet",
        color="Eczane",
        barmode="group"
    )

    st.plotly_chart(fig,use_container_width=True)

# ---------------------------------------------------
# ECZANE ANALİZİ
# ---------------------------------------------------

elif menu == "Eczane Analizi":

    st.subheader("💊 Eczane Analizi")

    col1,col2 = st.columns([4,1])

    with col1:
        eczane = st.selectbox(
            "Eczane seç",
            sorted(df["Eczane"].unique())
        )

    with col2:
        ara = st.button("🔎 Ara")

    if ara:

        sonuc = df[df["Eczane"]==eczane]

        col1,col2,col3 = st.columns(3)

        col1.metric("Toplam Nöbet",len(sonuc))
        col2.metric("Grup",sonuc["Grup"].iloc[0])
        col3.metric("Toplam Ay",sonuc["Ay"].nunique())

        st.divider()

        st.subheader("📊 Günlere Göre Nöbet Dağılımı")

        gun_sayim = sonuc["Gün"].value_counts().reset_index()
        gun_sayim.columns = ["Gün","Sayı"]

        gun_sayim["Gün"] = pd.Categorical(
            gun_sayim["Gün"],
            categories=gun_sira,
            ordered=True
        )

        fig = px.bar(
            gun_sayim,
            x="Gün",
            y="Sayı",
            color="Gün",
            text="Sayı"
        )

        st.plotly_chart(fig,use_container_width=True)

        st.subheader("📅 Nöbet Zaman Çizelgesi")

        fig = px.scatter(
            sonuc,
            x="Tarih",
            y="Grup",
            color="Gün"
        )

        st.plotly_chart(fig,use_container_width=True)

        st.subheader("📋 Nöbet Listesi")

        st.dataframe(
            sonuc.sort_values("Tarih"),
            use_container_width=True
        )
