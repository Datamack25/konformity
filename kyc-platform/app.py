import streamlit as st
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

st.set_page_config(
    page_title="KYC Compliance Platform",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;600&family=IBM+Plex+Sans:wght@300;400;500;600;700&display=swap');
    :root {
        --primary:#0A1628;--accent:#00D4AA;--accent2:#FF6B35;
        --surface:#0F1F3D;--surface2:#162440;--text:#E8EDF5;
        --text-muted:#7A8BA6;--border:#1E3055;
        --danger:#FF4757;--warning:#FFB347;--success:#00D4AA;
    }
    .stApp{background-color:var(--primary);color:var(--text);font-family:'IBM Plex Sans',sans-serif;}
    .main-header{background:linear-gradient(135deg,#0F1F3D 0%,#0A1628 50%,#0F2A4A 100%);border-bottom:1px solid var(--border);padding:1.5rem 2rem;margin-bottom:2rem;border-radius:0 0 12px 12px;}
    .metric-card{background:var(--surface);border:1px solid var(--border);border-radius:10px;padding:1.2rem;text-align:center;transition:all 0.2s ease;}
    .metric-card:hover{border-color:var(--accent);transform:translateY(-2px);}
    .metric-value{font-size:2rem;font-weight:700;color:var(--accent);font-family:'IBM Plex Mono',monospace;}
    .metric-label{font-size:0.75rem;color:var(--text-muted);text-transform:uppercase;letter-spacing:1px;margin-top:0.3rem;}
    .section-title{font-size:1.1rem;font-weight:600;color:var(--accent);text-transform:uppercase;letter-spacing:1.5px;margin-bottom:1rem;padding-bottom:0.5rem;border-bottom:1px solid var(--border);}
    .info-box{background:var(--surface2);border-left:3px solid var(--accent);border-radius:0 8px 8px 0;padding:1rem 1.2rem;margin:0.5rem 0;}
    .warning-box{background:rgba(255,179,71,0.08);border-left:3px solid var(--warning);border-radius:0 8px 8px 0;padding:1rem 1.2rem;margin:0.5rem 0;}
    .danger-box{background:rgba(255,71,87,0.08);border-left:3px solid var(--danger);border-radius:0 8px 8px 0;padding:1rem 1.2rem;margin:0.5rem 0;}
    [data-testid="stSidebar"]{background-color:var(--surface)!important;border-right:1px solid var(--border);}
    .stButton>button{background:var(--accent);color:var(--primary);font-weight:600;border:none;border-radius:6px;padding:0.5rem 1.5rem;font-family:'IBM Plex Sans',sans-serif;letter-spacing:0.5px;}
    .stButton>button:hover{background:#00F0C0;transform:translateY(-1px);}
    h1,h2,h3{color:var(--text)!important;font-family:'IBM Plex Sans',sans-serif!important;}
    .stTabs [data-baseweb="tab-list"]{background-color:var(--surface);border-radius:10px;padding:4px;gap:4px;}
    .stTabs [data-baseweb="tab"]{color:var(--text-muted);font-weight:500;}
    .stTabs [aria-selected="true"]{background:var(--accent)!important;color:var(--primary)!important;border-radius:7px;}
    .source-pill{display:inline-block;background:rgba(0,212,170,0.1);border:1px solid rgba(0,212,170,0.2);color:var(--accent);padding:3px 10px;border-radius:20px;font-size:0.7rem;font-weight:500;margin:2px;font-family:'IBM Plex Mono',monospace;}
</style>
""", unsafe_allow_html=True)

PAGES = [
    "🏠 Tableau de bord",
    "🔍 Screening KYC",
    "📊 Sources de données",
    "🗂️ Analyse de cas",
    "📚 100 Concepts LCB-FT",
    "⚙️ Pipeline technique",
    "📄 Générateur de rapports PDF",
    "🏢 Intelligence Entreprise",
    "📈 Marchés Financiers",
    "🗄️ Explorateur de données",
]

with st.sidebar:
    st.markdown("""
    <div style='padding:1rem 0;border-bottom:1px solid #1E3055;margin-bottom:1rem;'>
        <div style='font-size:1.3rem;font-weight:700;color:#00D4AA;font-family:IBM Plex Mono;'>🛡️ KYC PLATFORM</div>
        <div style='font-size:0.7rem;color:#7A8BA6;margin-top:0.2rem;letter-spacing:2px;'>COMPLIANCE INTELLIGENCE</div>
    </div>""", unsafe_allow_html=True)

    page_label = st.selectbox("Navigation", PAGES, label_visibility="collapsed")

    st.markdown("---")
    st.markdown("""<div style='font-size:0.7rem;color:#7A8BA6;line-height:1.8;'>
        <div style='margin-bottom:0.5rem;font-size:0.75rem;color:#00D4AA;font-weight:600;'>SOURCES INTÉGRÉES</div>
        <div>✓ Pappers API</div><div>✓ OpenSanctions</div><div>✓ ComplyAdvantage</div>
        <div>✓ ACPR/AMF</div><div>✓ France Identité</div><div>✓ BODACC</div>
        <div>✓ TRACFIN</div><div>✓ INPI RBE</div>
    </div>""", unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("""<div style='font-size:0.7rem;color:#7A8BA6;line-height:1.8;'>
        <div style='margin-bottom:0.5rem;font-size:0.75rem;color:#00D4AA;font-weight:600;'>BASES DE DONNÉES</div>
        <div>📋 68 codes NAF/risque</div>
        <div>🌍 57 pays GAFI scorés</div>
        <div>🇪🇺 23 codes NACE UE</div>
        <div>⚠️ 15 typologies TRACFIN</div>
        <div>⚖️ 14 sources sanctions</div>
        <div>📏 12 règles scoring CMF</div>
    </div>""", unsafe_allow_html=True)

if page_label == "🏠 Tableau de bord":
    import pages.dashboard as mod
    mod.show()
elif page_label == "🔍 Screening KYC":
    import pages.screening as mod
    mod.show()
elif page_label == "📊 Sources de données":
    import pages.sources as mod
    mod.show()
elif page_label == "🗂️ Analyse de cas":
    import pages.case_analysis as mod
    mod.show()
elif page_label == "📚 100 Concepts LCB-FT":
    import pages.concepts as mod
    mod.show()
elif page_label == "⚙️ Pipeline technique":
    import pages.pipeline as mod
    mod.show()
elif page_label == "📄 Générateur de rapports PDF":
    import pages.pdf_report as mod
    mod.show()
elif page_label == "🏢 Intelligence Entreprise":
    import pages.entity_intel as mod
    mod.show()
elif page_label == "📈 Marchés Financiers":
    import pages.marches as mod
    mod.show()
elif page_label == "🗄️ Explorateur de données":
    import pages.sources as mod
    mod.show_data_explorer()
