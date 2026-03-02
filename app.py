import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Eczane Nöbet Takip Sistemi", layout="wide")

# ================= CSS =================
st.markdown("""
<style>
.card-container {
    display: flex;
    flex-wrap: wrap;
    gap: 20px;
    margin-top: 20px;
}

.card {
    background: linear-gradient(135deg, #5f72ff, #9b23ea);
    padding: 25px;
    border-radius: 15px;
    color: white;
    width: 200px;
    text-align: center;
    box-shadow: 0 6px 18px rgba(0,0,0,0.2);
    transition: 0.3s;
}

.card:hover {
    transform: translateY(-5px);
}

.eczane {
    font-size: 22px;
    font-weight: bold;
}

.grup {
    font-size: 16px;
    margin-top: 8px;
}
</style>
""", unsafe_allow_html=True)


# ================= EXCEL OKUMA =================
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

        df_long = df.melt(
            id_vars=["Tarih","Gün"],
            var_name="Grup",
            value_name="Eczane"
        )

        df_long = df_long.dropna(subset=["Eczane"])

        df_long["Ay"] = sheet

        all_data.append(df_long)

    return pd.concat(all_data, ignore_index=True)


# ================= BAŞLIK =================
st.title("💊 Eczane Nöbet Takip Sistemi")


# ================= DOSYA =================
file = st.file_uploader("Excel dosyasını yükleyin", type=["xlsx"])

if not file:
    st.info("Excel dosyası yükleyin.")
    st.stop()

df = load_excel(file)


# ================= TARİH FORMAT =================
df["Tarih"] = pd.to_datetime(df["Tarih"], dayfirst=True)


# ================= MENÜ =================
menu = st.sidebar.radio("Menü",[
    "Genel Özet",
    "Tarih Seç",
    "Aylık Takvim",
    "Grup Analizi",
    "Eczane Analizi"
])


# ================= GENEL ÖZET =================
if menu == "Genel Özet":

    col1,col2,col3,col4 = st.columns(4)

    col1.metric("Toplam Nöbet", len(df))
    col2.metric("Toplam Eczane", df["Eczane"].nunique())
    col3.metric("Toplam Ay", df["Ay"].nunique())
    col4.metric("Ortalama Nöbet", round(len(df)/df["Eczane"].nunique(),2))

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


# ================= TARİH SEÇ (KARTLI) =================
elif menu == "Tarih Seç":

    tarih = st.selectbox(
        "Tarih seç",
        sorted(df["Tarih"].unique())
    )

    sonuc = df[df["Tarih"] == tarih]

    if sonuc.empty:

        st.warning("Nöbetçi yok")

    else:

        html = '<div class="card-container">'

        for _, row in sonuc.iterrows():

            html += f"""
            <div class="card">
                <div class="eczane">
                    {row['Eczane']}
                </div>
                <div class="grup">
                    Grup {row['Grup']}
                </div>
            </div>
            """

        html += "</div>"

        st.markdown(html, unsafe_allow_html=True)


# ================= AYLIK TAKVİM =================
elif menu == "Aylık Takvim":

    ay = st.selectbox("Ay seç", sorted(df["Ay"].unique()))

    sonuc = df[df["Ay"] == ay]

    pivot = sonuc.pivot(
        index="Tarih",
        columns="Grup",
        values="Eczane"
    )

    pivot = pivot.fillna("")

    def highlight(val):

        if val == "":
            return "background-color:#eeeeee"

        return "background-color:#d4edda"

    styled = pivot.style.applymap(highlight)

    st.dataframe(styled, use_container_width=True)


# ================= GRUP ANALİZ =================
elif menu == "Grup Analizi":

    grup = st.selectbox(
        "Grup seç",
        sorted(df["Grup"].unique())
    )

    sonuc = df[df["Grup"] == grup]

    st.bar_chart(
        sonuc["Eczane"].value_counts()
    )


# ================= ECZANE ANALİZ =================
elif menu == "Eczane Analizi":

    eczane = st.selectbox(
        "Eczane seç",
        sorted(df["Eczane"].unique())
    )

    sonuc = df[df["Eczane"] == eczane]

    st.metric("Toplam Nöbet", len(sonuc))

    st.dataframe(
        sonuc.sort_values("Tarih")
    )
