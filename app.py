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

.chip-wrap {
    display: flex;
    flex-wrap: wrap;
    gap: 7px;
    margin-top: 8px;
}

.mini-chip {
    display: inline-block;
    background: #eef4ff;
    color: #1f4b99;
    border: 1px solid #d6e4ff;
    border-radius: 999px;
    padding: 6px 10px;
    font-size: 0.82rem;
    font-weight: 700;
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
                "Bayram",
                "Pzt",
                "Salı",
                "Çarş",
                "Perş",
                "Cuma",
                "Ctesi",
                "Pazar"
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


@st.cache_data
def load_detayli_rapor(file):
    """aylik_nobet_data.xlsx dosyasını okur."""
    xls = pd.ExcelFile(file)

    def read_sheet(sheet_name):
        if sheet_name not in xls.sheet_names:
            return pd.DataFrame()
        df_sheet = pd.read_excel(file, sheet_name=sheet_name)
        df_sheet = df_sheet.loc[:, ~df_sheet.columns.astype(str).str.contains("^Unnamed")]
        return df_sheet

    aylik_detay = read_sheet("AYLIK DETAY")
    periyot_ozet = read_sheet("PERIYOT OZET")
    debug_ozet = read_sheet("DEBUG OZET")

    # Eski dosyalarda O harfiyle yazılmış olabilir; ikisini de destekle.
    aylik_sifir = read_sheet("AYLIK 0 NOBET")
    if aylik_sifir.empty:
        aylik_sifir = read_sheet("AYLIK O NOBET")

    aylik_iki_plus = read_sheet("AYLIK 2+ NOBET")

    return {
        "aylik_detay": aylik_detay,
        "periyot_ozet": periyot_ozet,
        "debug_ozet": debug_ozet,
        "aylik_sifir": aylik_sifir,
        "aylik_iki_plus": aylik_iki_plus,
    }


def _safe_cell_text(value):
    if pd.isna(value):
        return ""
    return str(value).strip()


def _render_list_card(title, count, names_text):
    names_text = _safe_cell_text(names_text)
    if not names_text:
        names_html = '<div class="card-desc">Kayıt yok.</div>'
    else:
        names = [x.strip() for x in names_text.split(",") if x.strip()]
        if names:
            chips = "".join([f'<span class="mini-chip">{name}</span>' for name in names])
            names_html = f'<div class="chip-wrap">{chips}</div>'
        else:
            names_html = '<div class="card-desc">Kayıt yok.</div>'

    st.markdown(
        f"""
        <div class="card" style="margin-bottom:12px; min-height:150px;">
            <div class="card-title">{title}</div>
            <div class="metric-value" style="font-size:2.1rem; margin-bottom:10px;">{count}</div>
            {names_html}
        </div>
        """,
        unsafe_allow_html=True
    )


def _split_names_text(names_text):
    names_text = _safe_cell_text(names_text)
    if not names_text:
        return []
    return [x.strip() for x in names_text.split(",") if x.strip()]


def _render_group_list(group_name, names):
    temiz_names = [str(name).strip() for name in names if str(name).strip()]

    # Boş grup hiç gösterilmez.
    if not temiz_names:
        return

    chips = "".join([f'<span class="mini-chip">{name}</span>' for name in temiz_names])

    st.markdown(
        f"""
        <div style="margin-bottom:10px; padding-bottom:8px; border-bottom:1px solid #eef2f7;">
            <div style="font-weight:800; color:#1b2430; margin-bottom:6px;">{group_name}</div>
            <div class="chip-wrap">{chips}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


def _render_grouped_debug_card(title, debug_df, year, month, list_column, count_column):
    st.markdown(
        f"""
        <div class="card" style="margin-bottom:12px;">
            <div class="card-title">{title}</div>
            <div class="card-desc">{year}-{month:02d} ayı grup bazlı görünüm</div>
        </div>
        """,
        unsafe_allow_html=True
    )

    required_cols = {"Yıl", "Ay", "Grup", list_column, count_column}
    if debug_df.empty or not required_cols.issubset(debug_df.columns):
        st.info("DEBUG OZET sekmesinde gerekli kolonlar bulunamadı.")
        return

    view = debug_df[(debug_df["Yıl"] == year) & (debug_df["Ay"] == month)].copy()
    if view.empty:
        st.info("Seçilen ay için grup bazlı kayıt bulunamadı.")
        return

    view = view.sort_values("Grup")
    for _, row in view.iterrows():
        names = _split_names_text(row.get(list_column, ""))
        temiz_names = [str(name).strip() for name in names if str(name).strip()]

        # 0 kayıtlı gruplar ekranda hiç görünmez.
        if not temiz_names:
            continue

        group_name = row.get("Grup", "-")
        label = f"{group_name} — {len(temiz_names)} eczane"
        _render_group_list(label, temiz_names)


def build_hafta_ici_sonu_table(df, genel):
    """Genel özetten veya ana nöbet verisinden hafta içi / hafta sonu tablosu hazırlar."""
    if genel is not None and {"Eczane", "Grup"}.issubset(genel.columns):
        kaynak = genel.copy()
    else:
        kaynak, _ = prepare_ozet_table(df, genel)

    gun_kolonlari = ["Pzt", "Salı", "Çarş", "Perş", "Cuma", "Ctesi", "Pazar"]
    for col in gun_kolonlari:
        if col not in kaynak.columns:
            kaynak[col] = 0
        kaynak[col] = pd.to_numeric(kaynak[col], errors="coerce").fillna(0).astype(int)

    if "Bayram" not in kaynak.columns:
        kaynak["Bayram"] = 0
    kaynak["Bayram"] = pd.to_numeric(kaynak["Bayram"], errors="coerce").fillna(0).astype(int)

    kaynak["Hafta İçi"] = (
        kaynak["Pzt"] +
        kaynak["Salı"] +
        kaynak["Çarş"] +
        kaynak["Perş"] +
        kaynak["Cuma"]
    )

    kaynak["Cumartesi"] = kaynak["Ctesi"]
    kaynak["Pazar"] = kaynak["Pazar"]
    kaynak["Hafta Sonu"] = kaynak["Cumartesi"] + kaynak["Pazar"]
    kaynak["Toplam"] = kaynak["Hafta İçi"] + kaynak["Hafta Sonu"]
    kaynak["Hafta Sonu Oranı"] = kaynak.apply(
        lambda r: round(r["Hafta Sonu"] / r["Toplam"], 4) if r["Toplam"] else 0,
        axis=1
    )

    return kaynak


def render_hafta_ici_sonu_metrics(kaynak):
    toplam_hafta_ici = int(kaynak["Hafta İçi"].sum()) if not kaynak.empty else 0
    toplam_hafta_sonu = int(kaynak["Hafta Sonu"].sum()) if not kaynak.empty else 0
    toplam = toplam_hafta_ici + toplam_hafta_sonu
    hafta_sonu_orani = round((toplam_hafta_sonu / toplam) * 100, 2) if toplam else 0

    c1, c2, c3 = st.columns(3)
    with c1:
        show_metric_card("Toplam Hafta İçi", toplam_hafta_ici)
    with c2:
        show_metric_card("Toplam Hafta Sonu", toplam_hafta_sonu)
    with c3:
        show_metric_card("Hafta Sonu Oranı", f"%{hafta_sonu_orani}")


def render_hafta_ici_sonu_grafik(kaynak, baslik):
    st.markdown(f'<div class="section-title">{baslik}</div>', unsafe_allow_html=True)

    if kaynak.empty:
        st.warning("Grafik için kayıt bulunamadı.")
        return

    grafik = kaynak.copy()
    grafik = grafik.sort_values(["Grup", "Eczane"])

    grafik_kolonlari = ["Hafta İçi", "Cumartesi", "Pazar"]
    if "Bayram" in grafik.columns and grafik["Bayram"].sum() > 0:
        grafik_kolonlari.append("Bayram")

    long_df = grafik.melt(
        id_vars=["Eczane", "Grup"],
        value_vars=grafik_kolonlari,
        var_name="Nöbet Tipi",
        value_name="Nöbet Sayısı"
    )

    fig = px.bar(
        long_df,
        x="Eczane",
        y="Nöbet Sayısı",
        color="Nöbet Tipi",
        barmode="stack",
        hover_data=["Grup"],
        color_discrete_sequence=["#9bbb59", "#c0504d", "#4f81bd", "#8064a2"]
    )
    fig.update_layout(
        height=520,
        margin=dict(l=10, r=10, t=20, b=120),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        legend_title_text="",
        xaxis_title="Eczane",
        yaxis_title="Nöbet Sayısı",
        xaxis_tickangle=-90
    )
    st.plotly_chart(fig, use_container_width=True)


def render_genel_hafta_ici_sonu(df, genel):
    st.markdown('<div class="section-title">Genel Hafta İçi / Hafta Sonu</div>', unsafe_allow_html=True)
    st.markdown(
        """
        <div class="card" style="margin-bottom:14px;">
            <div class="card-title">Eczane bazlı hafta içi / hafta sonu dağılımı</div>
            <div class="card-desc">
                Bu alan ilk yüklenen ana nöbet Excel dosyasındaki GENEL OZET sayfasından hesaplanır.
                Hem tüm eczaneleri toplu olarak, hem de grup bazında filtreleyerek görebilirsiniz.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    kaynak = build_hafta_ici_sonu_table(df, genel)

    tab1, tab2 = st.tabs(["Tüm Eczaneler", "Grup Bazlı Görünüm"])

    goster_kolonlari = [
        "Eczane",
        "Grup",
        "Hafta İçi",
        "Cumartesi",
        "Pazar",
        "Hafta Sonu",
        "Toplam",
        "Bayram",
        "Hafta Sonu Oranı"
    ]
    goster_kolonlari = [c for c in goster_kolonlari if c in kaynak.columns]

    with tab1:
        render_hafta_ici_sonu_metrics(kaynak)
        render_hafta_ici_sonu_grafik(kaynak, "Tüm Eczaneler Grafiksel Görünüm")

        st.markdown('<div class="section-title">Eczane Bazlı Liste</div>', unsafe_allow_html=True)
        goster = kaynak[goster_kolonlari].copy()
        if {"Hafta Sonu", "Hafta İçi"}.issubset(goster.columns):
            goster = goster.sort_values(["Hafta Sonu", "Hafta İçi"], ascending=[False, False])
        st.dataframe(goster, use_container_width=True, height=620)

    with tab2:
        grup_listesi = sorted(kaynak["Grup"].dropna().unique()) if "Grup" in kaynak.columns else []
        if not grup_listesi:
            st.warning("Grup bilgisi bulunamadı.")
            return

        secili_grup = st.selectbox("Grup seç", grup_listesi, key="hafta_ici_sonu_grup_sec")
        grup_df = kaynak[kaynak["Grup"] == secili_grup].copy()

        st.markdown(
            f"""
            <div class="card" style="margin-bottom:12px;">
                <div class="card-title">{secili_grup} grubu hafta içi / hafta sonu görünümü</div>
                <div class="card-desc">Bu alanda sadece seçilen gruptaki eczanelerin dağılımı gösterilir.</div>
            </div>
            """,
            unsafe_allow_html=True
        )

        render_hafta_ici_sonu_metrics(grup_df)
        render_hafta_ici_sonu_grafik(grup_df, f"{secili_grup} Grubu Grafiksel Görünüm")

        st.markdown('<div class="section-title">Grup Eczane Listesi</div>', unsafe_allow_html=True)
        grup_goster = grup_df[goster_kolonlari].copy()
        grup_goster = grup_goster.sort_values(["Hafta Sonu", "Hafta İçi"], ascending=[False, False])
        st.dataframe(grup_goster, use_container_width=True, height=520)

def render_detayli_rapor():
    st.markdown('<div class="section-title">Detaylı Rapor</div>', unsafe_allow_html=True)
    st.markdown(
        """
        <div class="card" style="margin-bottom:14px;">
            <div class="card-title">Aylık data raporu</div>
            <div class="card-desc">
                Bu alan opsiyoneldir. Sadece detaylı analiz görmek istediğinizde aylik_nobet_data.xlsx dosyasını buraya yükleyin.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    detay_file = st.file_uploader(
        "Detaylı rapor Excel dosyasını yükleyin",
        type=["xlsx"],
        key="detayli_rapor_excel"
    )

    if detay_file is None:
        st.info("Detaylı rapor için aylik_nobet_data.xlsx dosyasını yükleyin.")
        return

    rapor = load_detayli_rapor(detay_file)
    periyot = rapor["periyot_ozet"]
    debug = rapor["debug_ozet"]
    sifir = rapor["aylik_sifir"]
    iki_plus = rapor["aylik_iki_plus"]

    if periyot.empty and debug.empty and sifir.empty and iki_plus.empty:
        st.error("Bu dosyada beklenen detay rapor sekmeleri bulunamadı.")
        return

    # Ay seçimi kartları filtrelemek için kullanılır.
    ay_options = []
    for kaynak in [debug, sifir, iki_plus]:
        if not kaynak.empty and {"Yıl", "Ay"}.issubset(kaynak.columns):
            ay_options += kaynak[["Yıl", "Ay"]].drop_duplicates().apply(
                lambda r: f"{int(r['Yıl'])}-{int(r['Ay']):02d}", axis=1
            ).tolist()

    ay_options = sorted(set(ay_options))
    secili_yil, secili_ay_no = None, None

    if ay_options:
        secili_ay = st.selectbox("Ay seç", ay_options)
        secili_yil, secili_ay_no = map(int, secili_ay.split("-"))

    # PERIYOT OZET
    st.markdown('<div class="section-title">Periyodik Özet</div>', unsafe_allow_html=True)

    if not periyot.empty:
        kolonlar = [
            "Eczane", "Grup", "Periyot Toplam Katsayı", "Periyot Bayram",
            "Hafta İçi", "Hafta Sonu", "Hafta Sonu Oranı",
            "Pazartesi", "Salı", "Çarşamba", "Perşembe", "Cuma", "Cumartesi", "Pazar", "Arefe"
        ]
        mevcut_kolonlar = [c for c in kolonlar if c in periyot.columns]
        st.dataframe(periyot[mevcut_kolonlar], use_container_width=True, height=420)
    else:
        st.info("PERIYOT OZET sekmesi bulunamadı.")

    # AYLIK 0 / 2+ KARTLARI - DEBUG OZET grup bazlı
    st.markdown('<div class="section-title">Aylık Kritik Kartlar</div>', unsafe_allow_html=True)

    if secili_yil is None:
        st.info("Kartlar için detay raporda Yıl/Ay bilgisi bulunamadı.")
        return

    col1, col2 = st.columns(2)

    with col1:
        _render_grouped_debug_card(
            title="Aylık 0 Nöbet",
            debug_df=debug,
            year=secili_yil,
            month=secili_ay_no,
            list_column="0 Nöbetliler",
            count_column="0 Nöbet Sayısı"
        )

    with col2:
        _render_grouped_debug_card(
            title="Aylık 2+ Nöbet",
            debug_df=debug,
            year=secili_yil,
            month=secili_ay_no,
            list_column="2+ Nöbetliler",
            count_column="2+ Nöbet Sayısı"
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

    # Gün isimleri farklı gelirse yine de kırılmasın.
    gun_alias = {
        "Pazartesi": "Pzt",
        "Pzt": "Pzt",
        "Salı": "Salı",
        "Sali": "Salı",
        "Çarşamba": "Çarş",
        "Çarş": "Çarş",
        "Carsamba": "Çarş",
        "Perşembe": "Perş",
        "Perş": "Perş",
        "Persembe": "Perş",
        "Cuma": "Cuma",
        "Cumartesi": "Ctesi",
        "Ctesi": "Ctesi",
        "Pazar": "Pazar",
    }

    gun_pivot = gun_pivot.rename(columns={c: gun_alias.get(str(c), c) for c in gun_pivot.columns})

    # Aynı güne denk gelen olası duplicate kolonları birleştir.
    for g in gun_sira:
        same_cols = [c for c in gun_pivot.columns if c == g]
        if len(same_cols) > 1:
            gun_pivot[g] = gun_pivot[same_cols].sum(axis=1)

    keep_cols = ["Eczane", "Grup"] + [g for g in gun_sira if g in gun_pivot.columns]
    gun_pivot = gun_pivot.loc[:, ~gun_pivot.columns.duplicated()].copy()
    gun_pivot = gun_pivot[[c for c in keep_cols if c in gun_pivot.columns]]

    if genel is not None and {"Eczane", "Grup"}.issubset(genel.columns):
        ozet = genel.merge(gun_pivot, on=["Eczane", "Grup"], how="left", suffixes=("_genel", ""))
    else:
        ozet = gun_pivot.copy()

    # Merge sonrası oluşabilecek _genel / _x / _y kolon karmaşasını temizle.
    for g in gun_sira:
        candidates = [
            g,
            f"{g}_y",
            f"{g}_x",
            f"{g}_genel",
        ]
        found = [c for c in candidates if c in ozet.columns]

        if found:
            ozet[g] = ozet[found].apply(pd.to_numeric, errors="coerce").fillna(0).sum(axis=1)
        else:
            ozet[g] = 0

    sabit_kolonlar = [
        "Eczane",
        "Grup",
        "Geçmiş Katsayı",
        "Geçmiş Bayram",
        "Toplam Katsayı",
        "Bayram"
    ]

    mevcut_sabitler = [c for c in sabit_kolonlar if c in ozet.columns]

    # KeyError oluşmaması için sadece gerçekten var olan kolonları al.
    final_cols = mevcut_sabitler + gun_sira
    final_cols = [c for c in final_cols if c in ozet.columns]

    ozet = ozet[final_cols].copy()

    for g in gun_sira:
        if g in ozet.columns:
            ozet[g] = pd.to_numeric(ozet[g], errors="coerce").fillna(0).astype(int)

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

# ==============================
# ANA BÖLÜM SEÇİMİ
# ==============================
st.sidebar.markdown("### Bölüm")
ana_bolum = st.sidebar.radio(
    "",
    [
        "Ana Panel",
        "Detaylı Rapor"
    ]
)

st.sidebar.markdown("---")

# ==============================
# DETAYLI RAPOR ANA BÖLÜMÜ
# ==============================
if ana_bolum == "Detaylı Rapor":
    st.sidebar.markdown(
        """
        <div class="small-note">
        Detaylı rapor alanı ayrı Excel ile çalışır. Ana nöbet planı Excel'i yüklemenize gerek yoktur.
        </div>
        """,
        unsafe_allow_html=True
    )
    render_detayli_rapor()
    st.stop()

# ==============================
# ANA PANEL DOSYA YÜKLEME
# ==============================
file = st.file_uploader("Ana nöbet planı Excel dosyasını yükleyin", type=["xlsx"])

if not file:
    st.info("Başlamak için ana nöbet planı Excel dosyasını yükleyin.")
    st.stop()

df, genel = load_excel(file)

if df.empty:
    st.error("Excel dosyasında okunabilir nöbet verisi bulunamadı.")
    st.stop()

# ==============================
# ANA PANEL MENÜ
# ==============================
st.sidebar.markdown("### Ana Panel Menü")

menu = st.sidebar.radio(
    "",
    [
        "Genel Özet",
        "Tarih Seç",
        "Aylık Takvim",
        "Grup Analizi",
        "Eczane Analizi",
        "Genel Hafta İçi / Hafta Sonu"
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

# ==============================
# GENEL HAFTA İÇİ / HAFTA SONU
# ==============================
elif menu == "Genel Hafta İçi / Hafta Sonu":
    render_genel_hafta_ici_sonu(df, genel)
