import os
import streamlit as st
import pandas as pd
import plotly.express as px

# ==============================
# AY ADLARI
# ==============================
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

# ==============================
# SAYFA AYARI
# ==============================
st.set_page_config(
    page_title="AYÇA | Eczane Nöbet Takip Sistemi",
    page_icon="💊",
    layout="wide"
)

# ==============================
# TASARIM / CSS
# ==============================
st.markdown("""
<style>
:root {
    --bg: #f6f8fb;
    --surface: #ffffff;
    --primary: #1f4b99;
    --primary2: #2e6bdb;
    --accent: #22a06b;
    --text: #1b2430;
    --muted: #5e6b7a;
    --line: #dbe3ee;
    --soft: #eef4ff;
    --shadow: 0 12px 30px rgba(22, 34, 51, 0.08);
    --radius: 18px;
}

html, body, [class*="css"]  {
    font-family: "Inter", sans-serif;
}

.stApp {
    background: linear-gradient(180deg, #f9fbff 0%, #f3f6fb 100%);
}

header[data-testid="stHeader"] {
    background: rgba(0, 0, 0, 0);
}

section[data-testid="stSidebar"] {
    background: #ffffff;
    border-right: 1px solid var(--line);
}

section[data-testid="stSidebar"] .block-container {
    padding-top: 1.2rem;
}

.block-container {
    padding-top: 2.4rem;
    padding-bottom: 2rem;
}

.main-title {
    font-size: 2.2rem;
    font-weight: 800;
    color: var(--text);
    margin-top: 0.2rem;
    margin-bottom: 0.35rem;
    line-height: 1.2;
    letter-spacing: -0.02em;
}

.main-subtitle {
    color: var(--muted);
    font-size: 1rem;
    margin-bottom: 1.2rem;
}

.hero-box {
    background: linear-gradient(135deg, rgba(31,75,153,0.08), rgba(34,160,107,0.08));
    border: 1px solid var(--line);
    border-radius: 24px;
    padding: 24px 28px;
    box-shadow: var(--shadow);
    margin-bottom: 1.2rem;
}

.hero-badge {
    display: inline-block;
    background: #e9f1ff;
    color: var(--primary);
    border: 1px solid #cfe0ff;
    border-radius: 999px;
    padding: 8px 14px;
    font-size: 0.82rem;
    font-weight: 700;
    margin-bottom: 14px;
}

.hero-headline {
    font-size: 2rem;
    line-height: 1.08;
    font-weight: 800;
    color: var(--text);
    margin-bottom: 10px;
    letter-spacing: -0.02em;
}

.hero-headline .blue {
    color: var(--primary2);
}

.hero-headline .green {
    color: var(--accent);
}

.hero-text {
    color: var(--muted);
    font-size: 1rem;
    line-height: 1.75;
    max-width: 900px;
}

.card {
    background: var(--surface);
    border: 1px solid var(--line);
    border-radius: var(--radius);
    padding: 18px 18px;
    box-shadow: var(--shadow);
}

.card-title {
    font-size: 1.05rem;
    font-weight: 800;
    color: var(--text);
    margin-bottom: 0.4rem;
}

.card-desc {
    color: var(--muted);
    line-height: 1.6;
    font-size: 0.95rem;
}

.metric-card {
    background: #ffffff;
    border: 1px solid var(--line);
    border-radius: 18px;
    padding: 14px 16px;
    box-shadow: var(--shadow);
}

.metric-label {
    color: var(--muted);
    font-size: 0.9rem;
    margin-bottom: 6px;
    font-weight: 600;
}

.metric-value {
    color: var(--text);
    font-size: 1.8rem;
    font-weight: 800;
}

.section-title {
    font-size: 1.15rem;
    font-weight: 800;
    color: var(--text);
    margin: 0.4rem 0 0.8rem 0;
}

.small-note {
    color: var(--muted);
    font-size: 0.9rem;
}

.logo-wrap {
    margin-bottom: 0.8rem;
}

.logo-title {
    font-size: 1.15rem;
    font-weight: 800;
    color: var(--text);
    margin-top: 0.3rem;
}

.logo-subtitle {
    color: var(--muted);
    font-size: 0.85rem;
    margin-top: 0.1rem;
    margin-bottom: 1rem;
}

div[data-testid="metric-container"] {
    background: #ffffff;
    border: 1px solid var(--line);
    padding: 14px;
    border-radius: 18px;
    box-shadow: var(--shadow);
}

div[data-testid="metric-container"] label {
    color: var(--muted) !important;
    font-weight: 600 !important;
}

.stButton > button {
    background: linear-gradient(135deg, var(--primary), var(--primary2));
    color: white;
    border: none;
    border-radius: 12px;
    padding: 0.65rem 1.1rem;
    font-weight: 700;
}

.stDownloadButton > button {
    background: linear-gradient(135deg, var(--primary), var(--primary2));
    color: white;
    border: none;
    border-radius: 12px;
    padding: 0.65rem 1.1rem;
    font-weight: 700;
}

.stSelectbox > div > div,
.stTextInput > div > div > input,
.stDateInput > div > div input {
    border-radius: 12px !important;
}
</style>
""", unsafe_allow_html=True)

# ==============================
# EXCEL OKUMA
# ==============================
@st.cache_data
def load_excel(file):
    xls = pd.ExcelFile(file)
    all_data = []
    genel = None

    for sheet in xls.sheet_names:
        df_sheet = pd.read_excel(file, sheet_name=sheet)
        df_sheet = df_sheet.loc[:, ~df_sheet.columns.astype(str).str.contains("^Unnamed")]

        if "GENEL" in sheet.upper():
            genel_cols = [
                "Eczane",
                "Grup",
                "Geçmiş Katsayı",
                "Geçmiş Bayram",
                "Toplam Katsayı",
                "Bayram"
            ]
            mevcut_genel_cols = [c for c in genel_cols if c in df_sheet.columns]
            if len(mevcut_genel_cols) >= 2:
                genel = df_sheet[mevcut_genel_cols].copy()
            continue

        if "Tarih" not in df_sheet.columns or "Gün" not in df_sheet.columns:
            continue

        df_long = df_sheet.melt(
            id_vars=["Tarih", "Gün"],
            var_name="Grup",
            value_name="Eczane"
        )

        df_long = df_long.dropna(subset=["Eczane"]).copy()
        df_long["Tarih"] = pd.to_datetime(df_long["Tarih"], dayfirst=True, errors="coerce")
        df_long = df_long.dropna(subset=["Tarih"]).copy()
        df_long["Ay"] = sheet
        all_data.append(df_long)

    if not all_data:
        return pd.DataFrame(), genel

    df = pd.concat(all_data, ignore_index=True)
    return df, genel

# ==============================
# YARDIMCI FONKSİYONLAR
# ==============================
def show_metric_card(label, value):
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">{label}</div>
            <div class="metric-value">{value}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

def prepare_ozet_table(df, genel):
    gun_sira = ["Pzt", "Salı", "Çarş", "Perş", "Cuma", "Ctesi", "Pazar"]

    gun_pivot = pd.pivot_table(
        df,
        index=["Eczane", "Grup"],
        columns="Gün",
        aggfunc="size",
        fill_value=0
    ).reset_index()

    mevcut_gunler = [g for g in gun_sira if g in gun_pivot.columns]
    gun_pivot = gun_pivot[["Eczane", "Grup"] + mevcut_gunler]

    if genel is not None and {"Eczane", "Grup"}.issubset(genel.columns):
        ozet = genel.merge(gun_pivot, on=["Eczane", "Grup"], how="left")
    else:
        ozet = gun_pivot.copy()

    for g in gun_sira:
        if g in ozet.columns:
            ozet[g] = ozet[g].fillna(0)

    sabit_kolonlar = [
        "Eczane",
        "Grup",
        "Geçmiş Katsayı",
        "Geçmiş Bayram",
        "Toplam Katsayı",
        "Bayram"
    ]
    mevcut_sabitler = [c for c in sabit_kolonlar if c in ozet.columns]
    ozet = ozet[mevcut_sabitler + mevcut_gunler]

    return ozet, gun_sira

def render_header():
    st.markdown('<div class="main-title">AYÇA | Eczane Nöbet Takip Sistemi</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="main-subtitle">Nöbet planını yalnızca görüntülemek değil, daha şeffaf ve daha yönetilebilir hale getirmek için tasarlandı.</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="hero-box">
            <div class="hero-badge">Akıllı kontrol paneli</div>
            <div class="hero-headline">
                Nöbet planı hazır. <span class="blue">Peki gerçekten</span> <span class="green">adil mi?</span>
            </div>
            <div class="hero-text">
                AYÇA ile nöbet dağılımını tarih, grup ve eczane bazında izleyebilir; gün dengesi, dağılım görünümü ve özet tabloları tek ekranda takip edebilirsin.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

# ==============================
# SIDEBAR LOGO
# ==============================
logo_path = "logo.png"

if os.path.exists(logo_path):
    st.sidebar.image(logo_path, use_container_width=True)
else:
    st.sidebar.markdown('<div class="logo-wrap">', unsafe_allow_html=True)
    st.sidebar.markdown('<div class="logo-title">AYÇA Paneli</div>', unsafe_allow_html=True)
    st.sidebar.markdown('<div class="logo-subtitle">Akıllı Yazılım Çözüm Asistanı</div>', unsafe_allow_html=True)

# ==============================
# ÜST ALAN
# ==============================
render_header()

file = st.file_uploader("Excel dosyasını yükleyin", type=["xlsx"])

if not file:
    st.info("Başlamak için Excel dosyasını yükleyin.")
    st.stop()

df, genel = load_excel(file)

if df.empty:
    st.error("Excel dosyasında okunabilir nöbet verisi bulunamadı.")
    st.stop()

# ==============================
# SIDEBAR
# ==============================
st.sidebar.markdown("### Menü")

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

st.sidebar.markdown("---")
st.sidebar.markdown(
    """
    <div class="small-note">
    Bu panel; nöbet dağılımını daha anlaşılır, daha düzenli ve daha kurumsal şekilde takip etmeniz için düzenlenmiştir.
    </div>
    """,
    unsafe_allow_html=True
)

# ==============================
# GENEL ÖZET
# ==============================
if menu == "Genel Özet":
    toplam_nobet = len(df)
    toplam_eczane = df["Eczane"].nunique()
    toplam_ay = df["Ay"].nunique()
    ortalama_nobet = round(toplam_nobet / toplam_eczane, 2) if toplam_eczane else 0

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        show_metric_card("Toplam Nöbet", toplam_nobet)
    with c2:
        show_metric_card("Toplam Eczane", toplam_eczane)
    with c3:
        show_metric_card("Toplam Ay", toplam_ay)
    with c4:
        show_metric_card("Ortalama Nöbet", ortalama_nobet)

    st.markdown('<div class="section-title">Gün Dağılımı</div>', unsafe_allow_html=True)

    gun_sayim = df["Gün"].value_counts().reset_index()
    gun_sayim.columns = ["Gün", "Sayı"]

    gun_sira = ["Pzt", "Salı", "Çarş", "Perş", "Cuma", "Ctesi", "Pazar"]
    gun_sayim["Gün"] = pd.Categorical(gun_sayim["Gün"], categories=gun_sira, ordered=True)
    gun_sayim = gun_sayim.sort_values("Gün")

    fig = px.pie(
        gun_sayim,
        names="Gün",
        values="Sayı",
        hole=0.55,
        color="Gün",
        color_discrete_sequence=[
            "#1f4b99", "#2e6bdb", "#4d8af0", "#7bb0ff", "#22a06b", "#49c38a", "#9edcbf"
        ]
    )
    fig.update_traces(textposition="inside", textinfo="percent+label")
    fig.update_layout(
        margin=dict(l=10, r=10, t=10, b=10),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        legend_title_text=""
    )
    st.plotly_chart(fig, use_container_width=True)

    st.markdown('<div class="section-title">Özet Tablo</div>', unsafe_allow_html=True)
    ozet, _ = prepare_ozet_table(df, genel)
    st.dataframe(ozet, use_container_width=True, height=500)

# ==============================
# TARİH SEÇ
# ==============================
elif menu == "Tarih Seç":
    min_tarih = df["Tarih"].min().date()
    max_tarih = df["Tarih"].max().date()

    col1, col2 = st.columns([1, 2])

    with col1:
        tarih = st.date_input(
            "Tarih seçin",
            value=min_tarih,
            min_value=min_tarih,
            max_value=max_tarih
        )

    secilen_tarih = tarih.to_pydatetime().date() if hasattr(tarih, "to_pydatetime") else tarih
    sonuc = df[df["Tarih"].dt.date == secilen_tarih].copy().sort_values(["Grup", "Eczane"])

    with col2:
        st.markdown(
            f"""
            <div class="card">
                <div class="card-title">Seçilen Tarih</div>
                <div class="card-desc" style="font-size:1.15rem;">
                    {secilen_tarih.day} {aylar_tr[secilen_tarih.month]} {secilen_tarih.year}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown('<div class="section-title">O gün nöbetçi olan eczaneler</div>', unsafe_allow_html=True)

    if sonuc.empty:
        st.warning("Seçilen tarihte kayıt bulunamadı.")
    else:
        st.dataframe(sonuc[["Tarih", "Gün", "Grup", "Eczane"]], use_container_width=True, height=450)

# ==============================
# AYLIK TAKVİM
# ==============================
elif menu == "Aylık Takvim":
    ay = st.selectbox("Ay seç", sorted(df["Ay"].unique()))
    sonuc = df[df["Ay"] == ay].copy()

    st.markdown('<div class="section-title">Aylık nöbet takvimi</div>', unsafe_allow_html=True)

    if sonuc.empty:
        st.warning("Seçilen ay için veri bulunamadı.")
    else:
        pivot = pd.pivot_table(
            sonuc,
            index="Tarih",
            columns="Grup",
            values="Eczane",
            aggfunc="first"
        )

        pivot = pivot.fillna("")
        pivot = pivot.sort_index()
        pivot.index = pd.to_datetime(pivot.index).strftime("%d.%m.%Y")
        pivot = pivot.reset_index().rename(columns={"index": "Tarih"})

        st.dataframe(pivot, use_container_width=True, height=650)

# ==============================
# GRUP ANALİZİ
# ==============================
elif menu == "Grup Analizi":
    if genel is not None and "Grup" in genel.columns:
        grup_listesi = sorted(genel["Grup"].dropna().unique())
    else:
        grup_listesi = sorted(df["Grup"].dropna().unique())

    st.markdown('<div class="section-title">Grup görünümü</div>', unsafe_allow_html=True)
    grup = st.selectbox("Grup seç", grup_listesi)

    ozet, gun_sira = prepare_ozet_table(df, genel)
    grup_ozet = ozet[ozet["Grup"] == grup].copy()

    st.markdown(
        f"""
        <div class="card" style="margin-bottom:12px;">
            <div class="card-title">{grup} grubu eczaneleri</div>
            <div class="card-desc">Bu alanda ilgili grubun geçmiş ve gün bazlı nöbet dağılımını toplu olarak görebilirsin.</div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.dataframe(grup_ozet, use_container_width=True, height=400)

    st.markdown('<div class="section-title">Grup günlere göre nöbet dağılımı</div>', unsafe_allow_html=True)

    sonuc = df[df["Grup"] == grup].copy()

    sayim = (
        sonuc.groupby(["Gün", "Eczane"])
        .size()
        .reset_index(name="Nöbet Sayısı")
    )

    sayim["Gün"] = pd.Categorical(
        sayim["Gün"],
        categories=gun_sira,
        ordered=True
    )
    sayim = sayim.sort_values("Gün")

    fig = px.bar(
        sayim,
        x="Gün",
        y="Nöbet Sayısı",
        color="Eczane",
        barmode="group",
        category_orders={"Gün": gun_sira},
        color_discrete_sequence=px.colors.qualitative.Set2
    )
    fig.update_layout(
        margin=dict(l=10, r=10, t=30, b=10),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        legend_title_text=""
    )
    st.plotly_chart(fig, use_container_width=True)

# ==============================
# ECZANE ANALİZİ
# ==============================
elif menu == "Eczane Analizi":
    st.markdown('<div class="section-title">Eczane arama</div>', unsafe_allow_html=True)

    arama = st.text_input("Eczane adı ara")
    eczane_listesi = sorted(df["Eczane"].dropna().unique())

    if arama:
        eczane_listesi = [e for e in eczane_listesi if arama.lower() in e.lower()]

    if not eczane_listesi:
        st.warning("Arama kriterine uygun eczane bulunamadı.")
        st.stop()

    eczane = st.selectbox("Eczane seç", eczane_listesi)
    sonuc = df[df["Eczane"] == eczane].copy().sort_values("Tarih")

    c1, c2 = st.columns([1, 2])

    with c1:
        show_metric_card("Toplam Nöbet", len(sonuc))

    with c2:
        grup_bilgisi = sonuc["Grup"].iloc[0] if not sonuc.empty else "-"
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-label">Grup</div>
                <div class="metric-value" style="font-size:1.5rem;">{grup_bilgisi}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown('<div class="section-title">Eczane nöbet geçmişi</div>', unsafe_allow_html=True)
    st.dataframe(sonuc[["Tarih", "Gün", "Grup", "Ay"]], use_container_width=True, height=450)
