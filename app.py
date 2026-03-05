import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Eczane Nöbet Dashboard", layout="wide")

st.title("💊 Eczane Nöbet Dashboard")

uploaded_file = st.file_uploader("Excel dosyasını yükleyin", type=["xlsx"])

if uploaded_file is not None:

    df = pd.read_excel(uploaded_file)

    # Gün sütunları
    gunler = ["Pzt","Salı","Çarş","Perş","Cuma","Ctesi","Pazar"]

    # Özet tablo oluştur
    ozet = df.groupby(["Eczane","Grup"]).agg(
        {
            "Geçmiş Katsayı":"sum",
            "Geçmiş Bayram":"sum",
            "Toplam Nöbet":"sum",
            "Toplam Katsayı":"sum",
            "Bayram":"sum",
            "Pzt":"sum",
            "Salı":"sum",
            "Çarş":"sum",
            "Perş":"sum",
            "Cuma":"sum",
            "Ctesi":"sum",
            "Pazar":"sum"
        }
    ).reset_index()

    menu = st.sidebar.selectbox(
        "Sayfa Seç",
        ["Genel Özet","Grup Analiz"]
    )

    # =========================
    # GENEL ÖZET
    # =========================

    if menu == "Genel Özet":

        st.header("Genel Özet")

        st.dataframe(ozet,use_container_width=True)

        fig = px.bar(
            ozet,
            x="Eczane",
            y="Toplam Nöbet",
            color="Grup",
            title="Eczanelerin Toplam Nöbet Sayısı"
        )

        st.plotly_chart(fig,use_container_width=True)


    # =========================
    # GRUP ANALİZ
    # =========================

    if menu == "Grup Analiz":

        st.header("Grup Görünümü")

        gruplar = sorted(df["Grup"].unique())

        grup_sec = st.selectbox("Grup Seçin", gruplar)

        grup_df = ozet[ozet["Grup"] == grup_sec]

        st.subheader(f"Grup {grup_sec} Eczaneleri")

        # TABLO (senin istediğin kısım)
        st.dataframe(grup_df,use_container_width=True)

        col1,col2 = st.columns(2)

        with col1:

            fig1 = px.bar(
                grup_df,
                x="Eczane",
                y="Toplam Nöbet",
                title="Toplam Nöbet Dağılımı"
            )

            st.plotly_chart(fig1,use_container_width=True)

        with col2:

            fig2 = px.bar(
                grup_df,
                x="Eczane",
                y="Toplam Katsayı",
                title="Toplam Katsayı Dağılımı"
            )

            st.plotly_chart(fig2,use_container_width=True)

        st.subheader("Haftanın Günlerine Göre Nöbet Dağılımı")

        gun_df = grup_df.melt(
            id_vars=["Eczane"],
            value_vars=gunler,
            var_name="Gün",
            value_name="Nöbet"
        )

        fig3 = px.bar(
            gun_df,
            x="Eczane",
            y="Nöbet",
            color="Gün",
            barmode="group"
        )

        st.plotly_chart(fig3,use_container_width=True)

else:

    st.info("Lütfen Excel dosyasını yükleyin.")
