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
# TASARIM / CSS - AYÇA V2
# ==============================
st.markdown("""
<style>
:root {
    --bg: #f5f8fc;
    --surface: #ffffff;
    --surface2: #f8fbff;
    --primary: #155eef;
    --primary-dark: #0f3f9e;
    --accent: #16b8a6;
    --accent-soft: #e7fbf8;
    --text: #0f172a;
    --muted: #667085;
    --line: #d9e2ef;
    --soft: #eef5ff;
    --danger: #f04438;
    --warning: #f79009;
    --shadow: 0 18px 45px rgba(15, 23, 42, 0.08);
    --shadow-soft: 0 10px 28px rgba(15, 23, 42, 0.06);
    --radius: 22px;
}

html, body, [class*="css"] {
    font-family: "Inter", "Segoe UI", sans-serif;
}

.stApp {
    background:
      radial-gradient(circle at top left, rgba(21,94,239,0.10), transparent 32%),
      linear-gradient(180deg, #fbfdff 0%, #f3f7fc 100%);
    color: var(--text);
}

header[data-testid="stHeader"] {
    background: rgba(255,255,255,0);
}

.block-container {
    padding-top: 1.4rem;
    padding-bottom: 2.5rem;
    max-width: 1500px;
}

section[data-testid="stSidebar"] {
    background: rgba(255,255,255,0.94);
    border-right: 1px solid var(--line);
}

section[data-testid="stSidebar"] .block-container {
    padding-top: 1.1rem;
}

section[data-testid="stSidebar"] label {
    font-weight: 650;
}

div[role="radiogroup"] label {
    padding: 4px 0;
}

.main-title {
    font-size: 2.35rem;
    font-weight: 900;
    color: var(--text);
    letter-spacing: -0.04em;
    margin-bottom: 0.25rem;
}

.main-subtitle {
    color: var(--muted);
    font-size: 1.02rem;
    margin-bottom: 1rem;
}

.hero-box {
    position: relative;
    overflow: hidden;
    background:
        linear-gradient(135deg, rgba(21,94,239,0.11), rgba(22,184,166,0.10)),
        #ffffff;
    border: 1px solid #dce7f7;
    border-radius: 30px;
    padding: 28px 30px;
    box-shadow: var(--shadow);
    margin-bottom: 1.3rem;
}

.hero-box:after {
    content: "";
    position: absolute;
    width: 280px;
    height: 280px;
    right: -95px;
    top: -130px;
    background: radial-gradient(circle, rgba(22,184,166,0.24), rgba(22,184,166,0));
}

.hero-badge {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    background: #ffffff;
    color: var(--primary-dark);
    border: 1px solid #cfe0ff;
    border-radius: 999px;
    padding: 8px 14px;
    font-size: 0.82rem;
    font-weight: 800;
    margin-bottom: 15px;
    box-shadow: var(--shadow-soft);
}

.hero-headline {
    font-size: 2.05rem;
    line-height: 1.08;
    font-weight: 900;
    color: var(--text);
    margin-bottom: 10px;
    letter-spacing: -0.04em;
}

.hero-headline .blue { color: var(--primary); }
.hero-headline .green { color: var(--accent); }

.hero-text {
    color: var(--muted);
    font-size: 1rem;
    line-height: 1.7;
    max-width: 940px;
}

.card, .metric-card, .ai-card, .duty-card {
    background: rgba(255,255,255,0.92);
    border: 1px solid var(--line);
    border-radius: var(--radius);
    box-shadow: var(--shadow-soft);
}

.card {
    padding: 18px 18px;
}

.card-title {
    font-size: 1.04rem;
    font-weight: 850;
    color: var(--text);
    margin-bottom: 0.35rem;
}

.card-desc {
    color: var(--muted);
    line-height: 1.62;
    font-size: 0.94rem;
}

.metric-card {
    padding: 18px 18px;
    min-height: 118px;
    transition: transform .18s ease, box-shadow .18s ease;
}

.metric-card:hover {
    transform: translateY(-2px);
    box-shadow: var(--shadow);
}

.metric-top {
    display:flex;
    align-items:center;
    justify-content:space-between;
    gap:12px;
    margin-bottom: 10px;
}

.metric-icon {
    width: 38px;
    height: 38px;
    display:flex;
    align-items:center;
    justify-content:center;
    border-radius: 14px;
    background: var(--soft);
    color: var(--primary);
    font-size: 1.15rem;
}

.metric-label {
    color: var(--muted);
    font-size: 0.9rem;
    font-weight: 700;
}

.metric-value {
    color: var(--text);
    font-size: 2rem;
    font-weight: 900;
    letter-spacing: -0.035em;
}

.metric-delta {
    margin-top: 6px;
    color: var(--accent);
    font-size: 0.82rem;
    font-weight: 800;
}

.ai-card {
    padding: 18px 20px;
    margin: 12px 0 18px 0;
    background:
      linear-gradient(135deg, rgba(21,94,239,0.08), rgba(22,184,166,0.08)),
      #ffffff;
}

.ai-title {
    font-size: 1rem;
    font-weight: 900;
    color: var(--text);
    margin-bottom: 7px;
}

.ai-text {
    color: #344054;
    line-height: 1.65;
    font-size: 0.96rem;
}

.section-title {
    font-size: 1.18rem;
    font-weight: 900;
    color: var(--text);
    margin: 1rem 0 0.75rem 0;
    letter-spacing: -0.025em;
}

.small-note {
    color: var(--muted);
    font-size: 0.9rem;
    line-height: 1.6;
}

.duty-card {
    padding: 16px 16px;
    min-height: 118px;
    border-left: 5px solid var(--primary);
}

.duty-group {
    color: var(--primary-dark);
    font-weight: 900;
    font-size: 0.88rem;
    margin-bottom: 8px;
}

.duty-name {
    color: var(--text);
    font-weight: 900;
    font-size: 1.25rem;
    letter-spacing: -0.03em;
}

.duty-meta {
    color: var(--muted);
    font-size: 0.88rem;
    margin-top: 8px;
}

.timeline {
    display:flex;
    flex-wrap:wrap;
    gap:10px;
    margin: 10px 0 18px 0;
}

.timeline-item {
    display:inline-flex;
    align-items:center;
    gap:8px;
    background:#fff;
    border:1px solid var(--line);
    border-radius:999px;
    padding:8px 12px;
    color:var(--text);
    font-size:0.87rem;
    font-weight:750;
    box-shadow: var(--shadow-soft);
}

.timeline-dot {
    width:9px;
    height:9px;
    border-radius:999px;
    background:var(--accent);
}

.logo-wrap { margin-bottom: 0.8rem; }
.logo-title {
    font-size: 1.15rem;
    font-weight: 900;
    color: var(--text);
    margin-top: 0.3rem;
}
.logo-subtitle {
    color: var(--muted);
    font-size: 0.85rem;
    margin-top: 0.1rem;
    margin-bottom: 1rem;
}

.stButton > button,
.stDownloadButton > button {
    background: linear-gradient(135deg, var(--primary), var(--accent));
    color: white;
    border: none;
    border-radius: 14px;
    padding: 0.68rem 1.1rem;
    font-weight: 800;
}

.stSelectbox > div > div,
.stTextInput > div > div > input,
.stDateInput > div > div input,
div[data-testid="stFileUploader"] section {
    border-radius: 16px !important;
}

div[data-testid="stDataFrame"] {
    border-radius: 18px;
    overflow: hidden;
    border: 1px solid var(--line);
    box-shadow: var(--shadow-soft);
}

.chip-wrap {
    display: flex;
    flex-wrap: wrap;
    gap: 7px;
    margin-top: 8px;
}
.mini-chip {
    display: inline-block;
    background: #eef5ff;
    color: #1447a6;
    border: 1px solid #d6e4ff;
    border-radius: 999px;
    padding: 6px 10px;
    font-size: 0.82rem;
    font-weight: 800;
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
def show_metric_card(label, value, icon="📌", delta=""):
    delta_html = f'<div class="metric-delta">{delta}</div>' if delta else ""
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-top">
                <div class="metric-label">{label}</div>
                <div class="metric-icon">{icon}</div>
            </div>
            <div class="metric-value">{value}</div>
            {delta_html}
        </div>
        """,
        unsafe_allow_html=True
    )


def render_ai_card(text, title="AYÇA AI Değerlendirmesi"):
    st.markdown(
        f"""
        <div class="ai-card">
            <div class="ai-title">🤖 {title}</div>
            <div class="ai-text">{text}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


def render_duty_cards(rows):
    if rows.empty:
        return
    cols = st.columns(min(4, len(rows)))
    for i, (_, row) in enumerate(rows.iterrows()):
        with cols[i % len(cols)]:
            tarih_text = pd.to_datetime(row["Tarih"]).strftime("%d.%m.%Y") if "Tarih" in row else ""
            gun_text = row.get("Gün", "")
            st.markdown(
                f"""
                <div class="duty-card">
                    <div class="duty-group">{row.get("Grup", "-")}</div>
                    <div class="duty-name">{row.get("Eczane", "-")}</div>
                    <div class="duty-meta">{gun_text} · {tarih_text}</div>
                </div>
                """,
                unsafe_allow_html=True
            )


def style_plotly(fig):
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter, Segoe UI, sans-serif", color="#344054"),
        margin=dict(l=10, r=10, t=45, b=40),
        legend_title_text=""
    )
    fig.update_xaxes(showgrid=False, zeroline=False)
    fig.update_yaxes(gridcolor="rgba(102,112,133,0.16)", zeroline=False)
    return fig


def safe_num(series, default=0):
    return pd.to_numeric(series, errors="coerce").fillna(default)


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


def render_genel_hafta_ici_sonu(df, genel):
    st.markdown('<div class="section-title">Genel Hafta İçi / Hafta Sonu</div>', unsafe_allow_html=True)
    st.markdown(
        """
        <div class="card" style="margin-bottom:14px;">
            <div class="card-title">Hafta içi / Cumartesi / Pazar dağılımı</div>
            <div class="card-desc">
                Bu alan GENEL OZET verisinden çalışır. Mevcut eczane bazlı görünüm korunur;
                ek olarak hafta içi, cumartesi ve pazar bilgilerini gösteren dikey grafik eklenmiştir.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    if genel is not None and {"Eczane", "Grup"}.issubset(genel.columns):
        kaynak = genel.copy()
    else:
        kaynak, _ = prepare_ozet_table(df, genel)

    gun_kolonlari = ["Pzt", "Salı", "Çarş", "Perş", "Cuma", "Ctesi", "Pazar"]
    for col in gun_kolonlari:
        if col not in kaynak.columns:
            kaynak[col] = 0
        kaynak[col] = pd.to_numeric(kaynak[col], errors="coerce").fillna(0).astype(int)

    kaynak["Hafta İçi"] = (
        kaynak["Pzt"] +
        kaynak["Salı"] +
        kaynak["Çarş"] +
        kaynak["Perş"] +
        kaynak["Cuma"]
    )
    kaynak["Toplam Cumartesi"] = kaynak["Ctesi"]
    kaynak["Toplam Pazar"] = kaynak["Pazar"]
    kaynak["Hafta Sonu"] = kaynak["Toplam Cumartesi"] + kaynak["Toplam Pazar"]
    kaynak["Toplam"] = kaynak["Hafta İçi"] + kaynak["Hafta Sonu"]
    kaynak["Hafta Sonu Oranı"] = kaynak.apply(
        lambda r: round((r["Hafta Sonu"] / r["Toplam"]) * 100, 2) if r["Toplam"] else 0,
        axis=1
    )

    toplam_hafta_ici = int(kaynak["Hafta İçi"].sum())
    toplam_cumartesi = int(kaynak["Toplam Cumartesi"].sum())
    toplam_pazar = int(kaynak["Toplam Pazar"].sum())
    toplam_hafta_sonu = toplam_cumartesi + toplam_pazar
    toplam = toplam_hafta_ici + toplam_hafta_sonu
    hafta_sonu_orani = round((toplam_hafta_sonu / toplam) * 100, 2) if toplam else 0

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        show_metric_card("Toplam Hafta İçi", toplam_hafta_ici)
    with c2:
        show_metric_card("Toplam Cumartesi", toplam_cumartesi)
    with c3:
        show_metric_card("Toplam Pazar", toplam_pazar)
    with c4:
        show_metric_card("Hafta Sonu Oranı", f"%{hafta_sonu_orani}")

    # Grup bazlı özet: A1, A2, B1 gibi her grup ayrı toplamlanır.
    grup_ozet = (
        kaynak.groupby("Grup", dropna=False)
        .agg({
            "Eczane": "count",
            "Hafta İçi": "sum",
            "Toplam Cumartesi": "sum",
            "Toplam Pazar": "sum",
            "Hafta Sonu": "sum",
            "Toplam": "sum"
        })
        .reset_index()
        .rename(columns={"Eczane": "Eczane Sayısı"})
    )
    grup_ozet["Hafta Sonu Oranı"] = grup_ozet.apply(
        lambda r: round((r["Hafta Sonu"] / r["Toplam"]) * 100, 2) if r["Toplam"] else 0,
        axis=1
    )
    grup_ozet = grup_ozet.sort_values("Grup")

    tab1, tab2 = st.tabs([
        "Eczane Bazlı Liste",
        "Dikey Grafik"
    ])

    with tab1:
        st.markdown('<div class="section-title">Eczane Bazlı Liste</div>', unsafe_allow_html=True)
        goster_kolonlari = [
            "Eczane",
            "Grup",
            "Hafta İçi",
            "Toplam Cumartesi",
            "Toplam Pazar",
            "Hafta Sonu",
            "Toplam",
            "Hafta Sonu Oranı"
        ]
        goster_kolonlari = [c for c in goster_kolonlari if c in kaynak.columns]
        goster = kaynak[goster_kolonlari].copy()
        goster = goster.sort_values(["Grup", "Eczane"])
        st.dataframe(goster, use_container_width=True, height=620)

    with tab2:
        st.markdown('<div class="section-title">Dikey Grafik</div>', unsafe_allow_html=True)

        grafik_modu = st.radio(
            "Grafik görünümü",
            ["Seçili Grup Eczaneleri", "Tüm Gruplar Özeti"],
            horizontal=True
        )

        if grafik_modu == "Seçili Grup Eczaneleri":
            grup_listesi = sorted(kaynak["Grup"].dropna().unique())
            secili_grup = st.selectbox("Grafikte gösterilecek grup", grup_listesi)
            grafik_df = kaynak[kaynak["Grup"] == secili_grup].copy()
            grafik_df = grafik_df.sort_values("Eczane")
            x_col = "Eczane"
            baslik = f"{secili_grup} grubu hafta içi / cumartesi / pazar dağılımı"
        else:
            grafik_df = grup_ozet.copy()
            x_col = "Grup"
            baslik = "Tüm gruplar hafta içi / cumartesi / pazar dağılımı"

        grafik_long = grafik_df.melt(
            id_vars=[x_col],
            value_vars=["Hafta İçi", "Toplam Cumartesi", "Toplam Pazar"],
            var_name="Nöbet Türü",
            value_name="Sayı"
        )

        fig = px.bar(
            grafik_long,
            x=x_col,
            y="Sayı",
            color="Nöbet Türü",
            barmode="stack",
            category_orders={"Nöbet Türü": ["Hafta İçi", "Toplam Cumartesi", "Toplam Pazar"]},
            color_discrete_map={
                "Hafta İçi": "#8BC34A",
                "Toplam Cumartesi": "#D64545",
                "Toplam Pazar": "#2F7DD1"
            },
            text="Sayı"
        )
        # V4.8: Küçük değerlerde (1-2 gibi) yazıların bazen dikey bazen yatay görünmesini engeller.
        # Tüm bar içi etiketler yatay ve ortalı gösterilir.
        fig.update_traces(
            textposition="inside",
            textangle=0,
            insidetextanchor="middle",
            cliponaxis=False
        )
        fig.update_layout(
            title=baslik,
            xaxis_title="",
            yaxis_title="Nöbet Sayısı",
            legend_title_text="",
            margin=dict(l=10, r=10, t=55, b=120),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            xaxis_tickangle=-90,
            uniformtext_minsize=9,
            uniformtext_mode="show"
        )
        st.plotly_chart(fig, use_container_width=True)

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
    st.markdown('<div class="main-title">AYÇA Nöbet Yönetim Paneli</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="main-subtitle">Eczane nöbet planlarını analiz eden, dengeyi görünür kılan ve karar desteği sunan akıllı panel.</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="hero-box">
            <div class="hero-badge">✨ AYÇA V2 · Akıllı nöbet analizi</div>
            <div class="hero-headline">
                Nöbet listesi sadece tablo değil; <span class="blue">ölçülebilir</span>, <span class="green">anlaşılır</span> ve yönetilebilir olmalı.
            </div>
            <div class="hero-text">
                Tarih, grup, eczane, hafta içi / hafta sonu ve bayram dağılımlarını tek panelde izleyerek oda yönetimi için daha şeffaf bir karar zemini oluşturur.
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
    toplam_grup = df["Grup"].nunique()
    ortalama_nobet = round(toplam_nobet / toplam_eczane, 2) if toplam_eczane else 0

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        show_metric_card("Toplam Nöbet", toplam_nobet, "📅", "Plan genel yükü")
    with c2:
        show_metric_card("Toplam Eczane", toplam_eczane, "🏥")
    with c3:
        show_metric_card("Toplam Ay", toplam_ay, "🗓️")
    with c4:
        show_metric_card("Ortalama Nöbet", ortalama_nobet, "⚖️", f"{toplam_grup} grup izleniyor")

    gun_sayim = df["Gün"].value_counts().reset_index()
    gun_sayim.columns = ["Gün", "Sayı"]

    gun_sira = ["Pzt", "Salı", "Çarş", "Perş", "Cuma", "Ctesi", "Pazar"]
    gun_sayim["Gün"] = pd.Categorical(gun_sayim["Gün"], categories=gun_sira, ordered=True)
    gun_sayim = gun_sayim.sort_values("Gün")

    en_yogun = gun_sayim.sort_values("Sayı", ascending=False).iloc[0]
    en_dusuk = gun_sayim.sort_values("Sayı", ascending=True).iloc[0]
    fark = int(en_yogun["Sayı"] - en_dusuk["Sayı"])

    render_ai_card(
        f"Gün dağılımında en yoğun gün <b>{en_yogun['Gün']}</b> ({int(en_yogun['Sayı'])} nöbet), "
        f"en düşük gün <b>{en_dusuk['Gün']}</b> ({int(en_dusuk['Sayı'])} nöbet). "
        f"Aradaki fark <b>{fark}</b>. Bu değer oda yönetimi için hızlı denge kontrolü sağlar."
    )

    st.markdown('<div class="section-title">Gün Dağılımı</div>', unsafe_allow_html=True)

    chart_col, insight_col = st.columns([2.2, 1])

    with chart_col:
        fig = px.pie(
            gun_sayim,
            names="Gün",
            values="Sayı",
            hole=0.58,
            color="Gün",
            color_discrete_sequence=[
                "#123f8c", "#155eef", "#528bff", "#7ba7ff", "#16a276", "#45c49b", "#9be0c5"
            ]
        )
        fig.update_traces(textposition="inside", textinfo="percent+label", marker=dict(line=dict(color="#ffffff", width=2)))
        fig.update_layout(margin=dict(l=10, r=10, t=10, b=10), paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", legend_title_text="")
        st.plotly_chart(fig, use_container_width=True)

    with insight_col:
        show_metric_card("En Yoğun Gün", f"{en_yogun['Gün']}", "🔥", f"{int(en_yogun['Sayı'])} nöbet")
        show_metric_card("En Düşük Gün", f"{en_dusuk['Gün']}", "🌿", f"{int(en_dusuk['Sayı'])} nöbet")
        show_metric_card("Gün Farkı", fark, "📊", "Denge göstergesi")

    st.markdown('<div class="section-title">Özet Tablo</div>', unsafe_allow_html=True)
    ozet, _ = prepare_ozet_table(df, genel)

    tablo_arama = st.text_input("Tabloda eczane / grup ara", key="genel_ozet_arama")
    ozet_goster = ozet.copy()
    if tablo_arama:
        q = tablo_arama.lower()
        ozet_goster = ozet_goster[
            ozet_goster.astype(str).apply(lambda row: row.str.lower().str.contains(q).any(), axis=1)
        ]

    st.dataframe(ozet_goster, use_container_width=True, height=520)


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
    gun_adi = sonuc["Gün"].iloc[0] if not sonuc.empty else "-"

    with col2:
        st.markdown(
            f"""
            <div class="card">
                <div class="card-title">Seçilen Tarih</div>
                <div class="metric-value" style="font-size:2rem;">{secilen_tarih.day} {aylar_tr[secilen_tarih.month]} {secilen_tarih.year}</div>
                <div class="card-desc">{gun_adi} · Bu tarihte {len(sonuc)} eczane nöbetçi görünüyor.</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    render_ai_card(
        f"Seçilen günde <b>{len(sonuc)}</b> nöbet kaydı var. Kart görünümü sahada hızlı kontrol, tablo görünümü ise resmi rapor takibi için kullanılabilir.",
        "Günlük Nöbet Kontrolü"
    )

    st.markdown('<div class="section-title">O gün nöbetçi olan eczaneler</div>', unsafe_allow_html=True)

    if sonuc.empty:
        st.warning("Seçilen tarihte kayıt bulunamadı.")
    else:
        render_duty_cards(sonuc[["Tarih", "Gün", "Grup", "Eczane"]])
        st.markdown('<div class="section-title">Tablo Görünümü</div>', unsafe_allow_html=True)
        st.dataframe(sonuc[["Tarih", "Gün", "Grup", "Eczane"]], use_container_width=True, height=330)


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

    st.markdown('<div class="section-title">Grup Analizi</div>', unsafe_allow_html=True)
    grup = st.selectbox("Grup seç", grup_listesi)

    ozet, gun_sira = prepare_ozet_table(df, genel)
    grup_ozet = ozet[ozet["Grup"] == grup].copy()
    sonuc = df[df["Grup"] == grup].copy()

    toplam_grup_nobet = len(sonuc)
    eczane_sayisi = grup_ozet["Eczane"].nunique() if "Eczane" in grup_ozet.columns else sonuc["Eczane"].nunique()
    toplam_bayram = int(safe_num(grup_ozet["Bayram"]).sum()) if "Bayram" in grup_ozet.columns else 0
    toplam_katsayi = round(safe_num(grup_ozet["Toplam Katsayı"]).sum(), 2) if "Toplam Katsayı" in grup_ozet.columns else toplam_grup_nobet

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        show_metric_card("Grup", grup, "👥")
    with c2:
        show_metric_card("Eczane Sayısı", eczane_sayisi, "🏥")
    with c3:
        show_metric_card("Toplam Nöbet", toplam_grup_nobet, "📅")
    with c4:
        show_metric_card("Toplam Katsayı", toplam_katsayi, "⚖️", f"Bayram: {toplam_bayram}")

    render_ai_card(
        f"<b>{grup}</b> grubunda {eczane_sayisi} eczane ve {toplam_grup_nobet} nöbet kaydı bulunuyor. "
        f"Bu ekran grup içi gün yükünü ve eczane bazlı dağılımı beraber kontrol etmek için düzenlendi.",
        "Grup Denge Yorumu"
    )

    st.markdown('<div class="section-title">Grup Eczaneleri</div>', unsafe_allow_html=True)
    st.dataframe(grup_ozet, use_container_width=True, height=360)

    st.markdown('<div class="section-title">Grup Günlere Göre Nöbet Dağılımı</div>', unsafe_allow_html=True)

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
        color_discrete_sequence=px.colors.sequential.Blues_r
    )
    fig.update_traces(marker_line_width=0)
    fig = style_plotly(fig)
    st.plotly_chart(fig, use_container_width=True)


# ==============================
# ECZANE ANALİZİ
# ==============================
elif menu == "Eczane Analizi":
    st.markdown('<div class="section-title">Eczane Analizi</div>', unsafe_allow_html=True)

    arama = st.text_input("Eczane adı ara")
    eczane_listesi = sorted(df["Eczane"].dropna().unique())

    if arama:
        eczane_listesi = [e for e in eczane_listesi if arama.lower() in e.lower()]

    if not eczane_listesi:
        st.warning("Arama kriterine uygun eczane bulunamadı.")
        st.stop()

    eczane = st.selectbox("Eczane seç", eczane_listesi)
    sonuc = df[df["Eczane"] == eczane].copy().sort_values("Tarih")
    ozet, _ = prepare_ozet_table(df, genel)
    eczane_ozet = ozet[ozet["Eczane"] == eczane].copy()

    grup_bilgisi = sonuc["Grup"].iloc[0] if not sonuc.empty else "-"
    toplam_nobet = len(sonuc)
    bayram = int(safe_num(eczane_ozet["Bayram"]).sum()) if not eczane_ozet.empty and "Bayram" in eczane_ozet.columns else 0
    toplam_katsayi = round(safe_num(eczane_ozet["Toplam Katsayı"]).sum(), 2) if not eczane_ozet.empty and "Toplam Katsayı" in eczane_ozet.columns else toplam_nobet
    hafta_sonu = int(sonuc[sonuc["Gün"].isin(["Ctesi", "Pazar"])].shape[0])

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        show_metric_card("Eczane", eczane, "🏥")
    with c2:
        show_metric_card("Grup", grup_bilgisi, "👥")
    with c3:
        show_metric_card("Toplam Nöbet", toplam_nobet, "📅")
    with c4:
        show_metric_card("Katsayı", toplam_katsayi, "⚖️", f"Bayram: {bayram} · Hafta sonu: {hafta_sonu}")

    render_ai_card(
        f"<b>{eczane}</b> için {toplam_nobet} nöbet kaydı bulunuyor. "
        f"Hafta sonu nöbet sayısı <b>{hafta_sonu}</b>, bayram kaydı <b>{bayram}</b>. "
        f"Bu özet, tek eczane bazında adalet kontrolü için hızlı izleme sağlar.",
        "Eczane Bazlı İçgörü"
    )

    if not sonuc.empty:
        timeline_items = ""
        for _, row in sonuc.iterrows():
            t = pd.to_datetime(row["Tarih"])
            timeline_items += f"""
            <span class="timeline-item">
                <span class="timeline-dot"></span>
                {t.day} {aylar_tr[t.month]} · {row["Gün"]}
            </span>
            """
        st.markdown(f'<div class="timeline">{timeline_items}</div>', unsafe_allow_html=True)

    col_chart, col_table = st.columns([1, 1.3])

    with col_chart:
        st.markdown('<div class="section-title">Gün Dağılımı</div>', unsafe_allow_html=True)
        gun_df = sonuc["Gün"].value_counts().reset_index()
        gun_df.columns = ["Gün", "Sayı"]
        if not gun_df.empty:
            fig = px.pie(
                gun_df,
                names="Gün",
                values="Sayı",
                hole=0.55,
                color_discrete_sequence=["#155eef", "#528bff", "#16b8a6", "#98dcca", "#0f3f9e", "#7ba7ff", "#45c49b"]
            )
            fig.update_traces(textposition="inside", textinfo="label+value")
            fig.update_layout(margin=dict(l=10, r=10, t=10, b=10), paper_bgcolor="rgba(0,0,0,0)", legend_title_text="")
            st.plotly_chart(fig, use_container_width=True)

    with col_table:
        st.markdown('<div class="section-title">Eczane Nöbet Geçmişi</div>', unsafe_allow_html=True)
        st.dataframe(sonuc[["Tarih", "Gün", "Grup", "Ay"]], use_container_width=True, height=420)


# ==============================
# GENEL HAFTA İÇİ / HAFTA SONU
# ==============================
elif menu == "Genel Hafta İçi / Hafta Sonu":
    render_genel_hafta_ici_sonu(df, genel)
