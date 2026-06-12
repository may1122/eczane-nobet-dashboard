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


@st.cache_data
def load_monthly_excel(file):
    """aylik_nobet_data.xlsx dosyasını okur."""
    xls = pd.ExcelFile(file)

    def read_sheet(name):
        if name not in xls.sheet_names:
            return pd.DataFrame()
        df_sheet = pd.read_excel(file, sheet_name=name)
        df_sheet = df_sheet.loc[:, ~df_sheet.columns.astype(str).str.contains("^Unnamed")]
        return df_sheet

    aylik_detay = read_sheet("AYLIK DETAY")
    periyot_ozet = read_sheet("PERIYOT OZET")
    debug_ozet = read_sheet("DEBUG OZET")
    aylik_zero = read_sheet("AYLIK 0 NOBET")
    aylik_two = read_sheet("AYLIK 2+ NOBET")

    for df_sheet in [aylik_detay, periyot_ozet, debug_ozet, aylik_zero, aylik_two]:
        if not df_sheet.empty:
            df_sheet.columns = [str(c).strip() for c in df_sheet.columns]

    if not aylik_detay.empty and {"Yıl", "Ay"}.issubset(aylik_detay.columns):
        aylik_detay["Ay Etiketi"] = aylik_detay.apply(
            lambda r: f"{int(r['Yıl'])}-{int(r['Ay']):02d}", axis=1
        )
        aylik_detay["Hafta İçi"] = (
            aylik_detay.get("Pazartesi", 0) +
            aylik_detay.get("Salı", 0) +
            aylik_detay.get("Çarşamba", 0) +
            aylik_detay.get("Perşembe", 0) +
            aylik_detay.get("Cuma", 0)
        )
        aylik_detay["Hafta Sonu"] = aylik_detay.get("Cumartesi", 0) + aylik_detay.get("Pazar", 0)
        aylik_detay["Toplam Nöbet"] = aylik_detay["Hafta İçi"] + aylik_detay["Hafta Sonu"] + aylik_detay.get("Bayram", 0) + aylik_detay.get("Arefe", 0)

    if not debug_ozet.empty and {"Yıl", "Ay"}.issubset(debug_ozet.columns):
        debug_ozet["Ay Etiketi"] = debug_ozet.apply(
            lambda r: f"{int(r['Yıl'])}-{int(r['Ay']):02d}", axis=1
        )

    for df_sheet in [aylik_zero, aylik_two]:
        if not df_sheet.empty and {"Yıl", "Ay"}.issubset(df_sheet.columns):
            df_sheet["Ay Etiketi"] = df_sheet.apply(
                lambda r: f"{int(r['Yıl'])}-{int(r['Ay']):02d}", axis=1
            )

    return {
        "AYLIK DETAY": aylik_detay,
        "PERIYOT OZET": periyot_ozet,
        "DEBUG OZET": debug_ozet,
        "AYLIK 0 NOBET": aylik_zero,
        "AYLIK 2+ NOBET": aylik_two,
    }

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
    st.sidebar.image(logo_path, width=360)
else:
    st.sidebar.markdown('<div class="logo-wrap">', unsafe_allow_html=True)
    st.sidebar.markdown('<div class="logo-title">AYÇA Paneli</div>', unsafe_allow_html=True)
    st.sidebar.markdown('<div class="logo-subtitle">Akıllı Yazılım Çözüm Asistanı</div>', unsafe_allow_html=True)

# ==============================
# ÜST ALAN
# ==============================
render_header()

file = st.file_uploader("Excel dosyasını yükleyin", type=["xlsx"], key="ana_plan")

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
        "Eczane Analizi",
        "Detaylı Rapor"
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
    if df.empty:
        st.warning("Genel özet için ana nöbet planı Excel dosyasını yükleyin.")
        st.stop()

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
    if df.empty:
        st.warning("Tarih seçimi için ana nöbet planı Excel dosyasını yükleyin.")
        st.stop()

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
    if df.empty:
        st.warning("Aylık takvim için ana nöbet planı Excel dosyasını yükleyin.")
        st.stop()

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
    if df.empty:
        st.warning("Grup analizi için ana nöbet planı Excel dosyasını yükleyin.")
        st.stop()

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
# AYLIK DATA ANALİZİ
# ==============================
elif menu == "Detaylı Rapor":
    if monthly_data is None:
        st.warning("Bu ekran için aylık_nobet_data.xlsx dosyasını yükleyin.")
        st.stop()

    aylik_detay = monthly_data["AYLIK DETAY"]
    periyot_ozet = monthly_data["PERIYOT OZET"]
    debug_ozet = monthly_data["DEBUG OZET"]
    aylik_zero = monthly_data["AYLIK 0 NOBET"]
    aylik_two = monthly_data["AYLIK 2+ NOBET"]

    if aylik_detay.empty:
        st.error("AYLIK DETAY sekmesi okunamadı.")
        st.stop()

    st.markdown('<div class="section-title">Detaylı Rapor</div>', unsafe_allow_html=True)
    st.markdown(
        """
        <div class="card" style="margin-bottom:14px;">
            <div class="card-title">Aylık nöbet dengesini kontrol et</div>
            <div class="card-desc">
                Bu ekranda hafta içi / hafta sonu yükünü, ayda 0 nöbet kalanları ve ayda 2+ nöbet alanları tek ekranda görebilirsin.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    ay_listesi = sorted(aylik_detay["Ay Etiketi"].dropna().unique())
    secilen_ay = st.selectbox("Ay seç", ay_listesi)

    secilen_detay = aylik_detay[aylik_detay["Ay Etiketi"] == secilen_ay].copy()
    secilen_debug = debug_ozet[debug_ozet["Ay Etiketi"] == secilen_ay].copy() if not debug_ozet.empty else pd.DataFrame()
    secilen_zero = aylik_zero[aylik_zero["Ay Etiketi"] == secilen_ay].copy() if not aylik_zero.empty else pd.DataFrame()
    secilen_two = aylik_two[aylik_two["Ay Etiketi"] == secilen_ay].copy() if not aylik_two.empty else pd.DataFrame()

    toplam_hafta_ici = int(secilen_detay["Hafta İçi"].sum())
    toplam_hafta_sonu = int(secilen_detay["Hafta Sonu"].sum())
    toplam_bayram = int(secilen_detay.get("Bayram", 0).sum())
    toplam_arefe = int(secilen_detay.get("Arefe", 0).sum())
    toplam_nobet = toplam_hafta_ici + toplam_hafta_sonu + toplam_bayram + toplam_arefe
    hafta_sonu_orani = round((toplam_hafta_sonu / (toplam_hafta_ici + toplam_hafta_sonu)) * 100, 1) if (toplam_hafta_ici + toplam_hafta_sonu) else 0

    zero_count = int(secilen_zero["0 Nöbet Sayısı"].iloc[0]) if not secilen_zero.empty and "0 Nöbet Sayısı" in secilen_zero.columns else 0
    two_count = int(secilen_two["2+ Nöbet Sayısı"].iloc[0]) if not secilen_two.empty and "2+ Nöbet Sayısı" in secilen_two.columns else 0

    c1, c2, c3, c4, c5 = st.columns(5)
    with c1:
        show_metric_card("Hafta İçi", toplam_hafta_ici)
    with c2:
        show_metric_card("Hafta Sonu", toplam_hafta_sonu)
    with c3:
        show_metric_card("Hafta Sonu Oranı", f"%{hafta_sonu_orani}")
    with c4:
        show_metric_card("0 Nöbet Kalan", zero_count)
    with c5:
        show_metric_card("2+ Nöbet Alan", two_count)

    st.markdown('<div class="section-title">Hafta içi / hafta sonu karşılaştırması</div>', unsafe_allow_html=True)

    karsilastirma = pd.DataFrame({
        "Tür": ["Hafta İçi", "Hafta Sonu", "Bayram", "Arefe"],
        "Nöbet Sayısı": [toplam_hafta_ici, toplam_hafta_sonu, toplam_bayram, toplam_arefe]
    })

    fig = px.bar(
        karsilastirma,
        x="Tür",
        y="Nöbet Sayısı",
        text="Nöbet Sayısı",
        color="Tür",
        color_discrete_sequence=["#1f4b99", "#22a06b", "#f59f00", "#845ef7"]
    )
    fig.update_traces(textposition="outside")
    fig.update_layout(
        margin=dict(l=10, r=10, t=30, b=10),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        legend_title_text=""
    )
    st.plotly_chart(fig, use_container_width=True)

    st.markdown('<div class="section-title">Ay bazında trend</div>', unsafe_allow_html=True)

    aylik_trend = aylik_detay.groupby("Ay Etiketi", as_index=False)[["Hafta İçi", "Hafta Sonu"]].sum()
    aylik_trend_long = aylik_trend.melt(
        id_vars="Ay Etiketi",
        value_vars=["Hafta İçi", "Hafta Sonu"],
        var_name="Tür",
        value_name="Nöbet Sayısı"
    )

    fig2 = px.bar(
        aylik_trend_long,
        x="Ay Etiketi",
        y="Nöbet Sayısı",
        color="Tür",
        barmode="group",
        text="Nöbet Sayısı",
        color_discrete_sequence=["#1f4b99", "#22a06b"]
    )
    fig2.update_traces(textposition="outside")
    fig2.update_layout(
        margin=dict(l=10, r=10, t=30, b=10),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        legend_title_text=""
    )
    st.plotly_chart(fig2, use_container_width=True)

    col_a, col_b = st.columns(2)

    with col_a:
        st.markdown('<div class="section-title">Ayda 0 nöbet kalanlar</div>', unsafe_allow_html=True)
        if secilen_zero.empty or pd.isna(secilen_zero.get("0 Nöbet Kalanlar", pd.Series([None])).iloc[0]):
            st.success("Bu ay 0 nöbet kalan eczane yok.")
        else:
            zero_text = str(secilen_zero["0 Nöbet Kalanlar"].iloc[0])
            zero_people = [x.strip() for x in zero_text.split(",") if x.strip()]
            zero_df = pd.DataFrame({"Eczane": zero_people})
            st.dataframe(zero_df, use_container_width=True, height=260)

    with col_b:
        st.markdown('<div class="section-title">Ayda 2+ nöbet alanlar</div>', unsafe_allow_html=True)
        if secilen_two.empty or pd.isna(secilen_two.get("2+ Nöbet Alanlar", pd.Series([None])).iloc[0]):
            st.success("Bu ay 2+ nöbet alan eczane yok.")
        else:
            two_text = str(secilen_two["2+ Nöbet Alanlar"].iloc[0])
            two_people = [x.strip() for x in two_text.split(",") if x.strip()]
            two_df = pd.DataFrame({"Eczane": two_people})
            st.dataframe(two_df, use_container_width=True, height=260)

    if not secilen_debug.empty:
        st.markdown('<div class="section-title">Grup bazında 0 ve 2+ nöbet görünümü</div>', unsafe_allow_html=True)

        debug_long = secilen_debug[["Grup", "0 Nöbet Sayısı", "2+ Nöbet Sayısı"]].melt(
            id_vars="Grup",
            value_vars=["0 Nöbet Sayısı", "2+ Nöbet Sayısı"],
            var_name="Durum",
            value_name="Eczane Sayısı"
        )

        fig3 = px.bar(
            debug_long,
            x="Grup",
            y="Eczane Sayısı",
            color="Durum",
            barmode="group",
            text="Eczane Sayısı",
            color_discrete_sequence=["#fa5252", "#1f4b99"]
        )
        fig3.update_traces(textposition="outside")
        fig3.update_layout(
            margin=dict(l=10, r=10, t=30, b=10),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            legend_title_text=""
        )
        st.plotly_chart(fig3, use_container_width=True)

        st.markdown('<div class="section-title">DEBUG detay tablosu</div>', unsafe_allow_html=True)
        st.dataframe(secilen_debug, use_container_width=True, height=420)

    st.markdown('<div class="section-title">Eczane bazlı aylık detay</div>', unsafe_allow_html=True)
    gosterilecek_kolonlar = [
        "Eczane", "Yıl", "Ay", "Toplam Nöbet", "Hafta İçi", "Hafta Sonu",
        "Bayram", "Arefe", "Pazartesi", "Salı", "Çarşamba", "Perşembe", "Cuma", "Cumartesi", "Pazar"
    ]
    mevcut_kolonlar = [c for c in gosterilecek_kolonlar if c in secilen_detay.columns]
    st.dataframe(secilen_detay[mevcut_kolonlar].sort_values(["Hafta Sonu", "Hafta İçi", "Eczane"], ascending=[False, False, True]), use_container_width=True, height=500)


# ==============================
# ECZANE ANALİZİ
# ==============================
elif menu == "Eczane Analizi":
    if df.empty:
        st.warning("Eczane analizi için ana nöbet planı Excel dosyasını yükleyin.")
        st.stop()

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
