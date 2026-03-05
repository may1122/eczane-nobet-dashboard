import streamlit as st
import pandas as pd
import calendar
from datetime import datetime
import plotly.express as px

st.set_page_config(
    page_title="Eczane Nöbet Dashboard",
    layout="wide"
)

# ---------------------------
# CSS TASARIM
# ---------------------------

st.markdown("""
<style>

.main-title{
font-size:40px;
font-weight:700;
color:#1f4e79;
}

.metric-card{
background:#f1f6fb;
padding:15px;
border-radius:10px;
text-align:center;
box-shadow:0 2px 6px rgba(0,0,0,0.1);
}

.calendar-day{
background:#ffffff;
padding:10px;
border-radius:10px;
min-height:90px;
box-shadow:0 1px 4px rgba(0,0,0,0.08);
}

.calendar-day:hover{
background:#eef4ff;
}

.day-number{
font-size:14px;
font-weight:bold;
color:#999;
}

.eczane{
font-size:15px;
font-weight:600;
color:#1f4e79;
}

</style>
""", unsafe_allow_html=True)

# ---------------------------
# BAŞLIK
# ---------------------------

st.markdown("<div class='main-title'>💊 Eczane Nöbet Dashboard</div>", unsafe_allow_html=True)

# ---------------------------
# DOSYA YÜKLEME
# ---------------------------

file = st.file_uploader("Excel Dosyası Yükle", type=["xlsx"])

# ---------------------------
# EXCEL OKUMA
# ---------------------------

@st.cache_data
def load_excel(file):

    df = pd.read_excel(file)

    # tarih kolonlarını al
    tarih_kolonlari = df.columns[1:]

    df_long = df.melt(
        id_vars=[df.columns[0]],
        value_vars=tarih_kolonlari,
        var_name="Tarih",
        value_name="Eczane"
    )

    df_long.columns = ["Grup","Tarih","Eczane"]

    df_long["Tarih"] = pd.to_datetime(df_long["Tarih"], errors="coerce")

    genel = df_long.groupby("Eczane").size().reset_index(name="Nobet Sayisi")

    return df_long, genel


# ---------------------------
# UYGULAMA
# ---------------------------

if file:

    df, genel = load_excel(file)

    ay = st.selectbox("Ay Seç", sorted(df["Tarih"].dt.month.unique()))

    yil = st.selectbox("Yıl", sorted(df["Tarih"].dt.year.unique()))

    df_filtered = df[
        (df["Tarih"].dt.month == ay) &
        (df["Tarih"].dt.year == yil)
    ]

    # ---------------------------
    # METRİKLER
    # ---------------------------

    col1,col2,col3 = st.columns(3)

    with col1:
        st.markdown(f"""
        <div class="metric-card">
        <h3>Toplam Nöbet</h3>
        <h2>{len(df_filtered)}</h2>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="metric-card">
        <h3>Eczane Sayısı</h3>
        <h2>{df_filtered['Eczane'].nunique()}</h2>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div class="metric-card">
        <h3>Gün Sayısı</h3>
        <h2>{df_filtered['Tarih'].dt.day.nunique()}</h2>
        </div>
        """, unsafe_allow_html=True)

    st.divider()

    # ---------------------------
    # AYLIK TAKVİM
    # ---------------------------

    st.subheader("📅 Aylık Nöbet Takvimi")

    ay_gun = calendar.monthrange(yil, ay)[1]

    hafta = st.columns(7)
    gunler = ["Pzt","Sal","Çar","Per","Cum","Cts","Paz"]

    for i,g in enumerate(gunler):
        hafta[i].markdown(f"**{g}**")

    gun_index = 0
    cols = st.columns(7)

    for gun in range(1, ay_gun + 1):

        tarih = datetime(yil, ay, gun)

        eczane = df_filtered[
            df_filtered["Tarih"].dt.day == gun
        ]["Eczane"]

        isim = ""

        if len(eczane) > 0:
            isim = "<br>".join(eczane.astype(str))

        cols[gun_index].markdown(f"""
        <div class="calendar-day">
        <div class="day-number">{gun}</div>
        <div class="eczane">{isim}</div>
        </div>
        """, unsafe_allow_html=True)

        gun_index += 1

        if gun_index == 7:
            cols = st.columns(7)
            gun_index = 0

    st.divider()

    # ---------------------------
    # TABLO
    # ---------------------------

    st.subheader("📋 Nöbet Listesi")

    st.dataframe(
        df_filtered.sort_values("Tarih"),
        use_container_width=True
    )

    # ---------------------------
    # GRAFİK
    # ---------------------------

    st.subheader("📊 Eczane Nöbet Dağılımı")

    fig = px.bar(
        genel,
        x="Eczane",
        y="Nobet Sayisi",
        color="Nobet Sayisi"
    )

    st.plotly_chart(fig, use_container_width=True)

else:

    st.info("Başlamak için Excel dosyanızı yükleyin.")
