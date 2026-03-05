import streamlit as st
import pandas as pd
import plotly.express as px
import calendar

st.set_page_config(page_title="Eczane Nöbet Takip", layout="wide")

st.title("💊 Eczane Nöbet Takip Sistemi")

# Excel yükleme
file = st.file_uploader("Excel Dosyası Yükle", type=["xlsx"])

@st.cache_data
def load_excel(file):

    df = pd.read_excel(file)

    # Unnamed kolonları temizle
    df = df.loc[:, ~df.columns.str.contains("^Unnamed")]

    # İlk kolon grup olsun
    df.rename(columns={df.columns[0]: "Grup"}, inplace=True)

    # Long format
    df_long = df.melt(
        id_vars=["Grup"],
        var_name="Tarih",
        value_name="Eczane"
    )

    df_long["Tarih"] = pd.to_datetime(df_long["Tarih"], errors="coerce")

    df_long = df_long.dropna(subset=["Tarih","Eczane"])

    df_long["Gun"] = df_long["Tarih"].dt.day
    df_long["Ay"] = df_long["Tarih"].dt.month
    df_long["Yil"] = df_long["Tarih"].dt.year
    df_long["HaftaGunu"] = df_long["Tarih"].dt.day_name()

    return df_long


if file:

    df = load_excel(file)

    tab1, tab2, tab3, tab4 = st.tabs(
        ["📊 Genel Özet","📅 Aylık Takvim","👥 Grup Görünümü","🔎 Eczane Ara"]
    )

# ---------------------------------------------------
# GENEL ÖZET
# ---------------------------------------------------

    with tab1:

        st.subheader("Genel Nöbet Dağılımı")

        toplam = df["Eczane"].value_counts().reset_index()
        toplam.columns = ["Eczane","Toplam"]

        fig = px.bar(
            toplam,
            x="Eczane",
            y="Toplam",
            title="Eczanelere Göre Nöbet Sayısı"
        )

        st.plotly_chart(fig,use_container_width=True)


# ---------------------------------------------------
# AYLIK TAKVİM
# ---------------------------------------------------

    with tab2:

        st.subheader("Aylık Takvim")

        yil = int(st.selectbox("Yıl", sorted(df["Yil"].unique())))
        ay = int(st.selectbox("Ay", sorted(df["Ay"].unique())))

        # HATA DÜZELTME
        if ay < 1 or ay > 12:
            st.error("Geçersiz ay değeri")
        else:

            ay_gun = calendar.monthrange(yil, ay)[1]

            ay_df = df[(df["Yil"]==yil) & (df["Ay"]==ay)]

            gunler = []

            for i in range(1, ay_gun+1):

                gun_df = ay_df[ay_df["Gun"]==i]

                if len(gun_df) > 0:

                    eczaneler = ", ".join(gun_df["Eczane"].tolist())

                else:

                    eczaneler = "-"

                gunler.append({
                    "Gün":i,
                    "Eczaneler":eczaneler
                })

            takvim_df = pd.DataFrame(gunler)

            st.dataframe(takvim_df,use_container_width=True)


# ---------------------------------------------------
# GRUP GÖRÜNÜMÜ
# ---------------------------------------------------

    with tab3:

        st.subheader("Grup Bazlı Nöbet")

        grup = st.selectbox("Grup Seç", df["Grup"].unique())

        grup_df = df[df["Grup"]==grup]

        sayim = grup_df["Eczane"].value_counts().reset_index()
        sayim.columns = ["Eczane","Toplam"]

        fig = px.bar(
            sayim,
            x="Eczane",
            y="Toplam",
            title=f"{grup} Grubu Nöbet Dağılımı"
        )

        st.plotly_chart(fig,use_container_width=True)


# ---------------------------------------------------
# ECZANE ARAMA
# ---------------------------------------------------

    with tab4:

        st.subheader("🔎 Eczane Ara")

        col1,col2 = st.columns([4,1])

        with col1:
            eczane_input = st.text_input("Eczane Adı Yaz")

        with col2:
            ara_btn = st.button("Ara")

        if ara_btn:

            sonuc = df[df["Eczane"].str.contains(eczane_input,case=False,na=False)]

            if len(sonuc)==0:

                st.warning("Eczane bulunamadı")

            else:

                eczane = sonuc["Eczane"].iloc[0]

                st.subheader(f"📍 {eczane}")

                col1,col2,col3 = st.columns(3)

                with col1:
                    st.metric("Toplam Nöbet", len(sonuc))

                with col2:
                    st.metric("Grup", sonuc["Grup"].iloc[0])

                with col3:
                    st.metric("Farklı Gün", sonuc["HaftaGunu"].nunique())

                st.subheader("📊 Günlere Göre Nöbet Dağılımı")

                grafik = sonuc.groupby("HaftaGunu").size().reset_index(name="Nöbet")

                fig = px.bar(
                    grafik,
                    x="HaftaGunu",
                    y="Nöbet",
                    color="HaftaGunu"
                )

                st.plotly_chart(fig,use_container_width=True)

                st.subheader("📋 Nöbet Günleri")

                st.dataframe(
                    sonuc[["Tarih","Grup","Eczane"]],
                    use_container_width=True
                )
