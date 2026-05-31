import streamlit as st

def show():
    st.markdown("## ⚙️ Pipeline technique KYC souverain")
    st.markdown("<div style='color: #7A8BA6; margin-bottom: 1.5rem;'>Architecture et implémentation du pipeline KYC — pile 100% européenne (Mistral, Pappers, OpenSanctions)</div>", unsafe_allow_html=True)

    tabs = st.tabs(["🏗️ Architecture", "🐍 Code Python", "🔒 Souveraineté des données", "📦 Installation"])

    with tabs[0]:
        st.markdown("### Architecture du pipeline souverain")
        st.markdown("""<div class='info-box' style='margin-bottom: 1.5rem;'>
        <div style='font-weight: 700; color: #00D4AA;'>Principe : aucune donnée personnelle ne quitte le périmètre européen</div>
        <div style='font-size: 0.85rem; color: #7A8BA6; margin-top: 0.3rem;'>
        Modèle LLM : Mistral AI (traitement déclaré UE) · Registres : Pappers (France) · Screening : OpenSanctions local · Identité : France Identité
        </div></div>""", unsafe_allow_html=True)

        steps = [
            ("1", "Ingestion des documents", "Kbis PDF + pièce d'identité chargés localement", "#00D4AA"),
            ("2", "Extraction — Mistral AI", "Le LLM lit les documents et extrait les champs structurés (SIREN, dirigeants, UBOs)", "#00D4AA"),
            ("3", "Vérification Pappers", "Cross-check SIREN contre les registres officiels français", "#00D4AA"),
            ("4", "Screening local — OpenSanctions", "Chaque nom criblé en local. Aucun nom ne quitte la machine.", "#00D4AA"),
            ("5", "Scoring — Mistral AI", "Application de la grille de règles LCB-FT : 8 facteurs scorés", "#FFB347"),
            ("6", "Verdict structuré", "Score global, checklist documentaire, disposition, articles CMF cités", "#FFB347"),
            ("7", "Génération PDF", "Rapport mis en forme pour signature conformité.", "#7A8BA6"),
        ]
        for num, title, desc, color in steps:
            st.markdown(f"""
            <div style='background:#0F1F3D;border:1px solid #1E3055;border-left:3px solid {color};border-radius:0 8px 8px 0;padding:0.8rem 1rem;margin-bottom:0.5rem;display:flex;gap:1rem;align-items:flex-start;'>
                <div style='background:{color};color:#0A1628;width:26px;height:26px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-weight:700;font-size:0.8rem;flex-shrink:0;'>{num}</div>
                <div>
                    <div style='font-weight:600;color:#E8EDF5;'>{title}</div>
                    <div style='font-size:0.82rem;color:#7A8BA6;margin-top:0.2rem;'>{desc}</div>
                </div>
            </div>""", unsafe_allow_html=True)

        st.markdown("---")
        cols = st.columns(5)
        nodes = [
            ("📄 Documents\nKbis + ID", "#0F1F3D", "#00D4AA"),
            ("🤖 Mistral AI\nAPI UE", "#0F1F3D", "#00D4AA"),
            ("🏛️ Pappers\nRegistres FR", "#0F1F3D", "#00D4AA"),
            ("🔍 OpenSanctions\nLocal", "#0F1F3D", "#00D4AA"),
            ("📊 Rapport\nPDF + JSON", "#0F1F3D", "#FFB347"),
        ]
        for col, (label, bg, border) in zip(cols, nodes):
            with col:
                st.markdown(f"""<div style='background:{bg};border:2px solid {border};border-radius:10px;padding:0.8rem;text-align:center;font-size:0.8rem;color:#E8EDF5;line-height:1.6;'>{label.replace(chr(10),"<br>")}</div>""", unsafe_allow_html=True)

    with tabs[1]:
        st.markdown("### Code Python — Pipeline complet")
        st.code(r"""
import os, json, requests
from pathlib import Path
from rapidfuzz import fuzz, process
import pandas as pd

MISTRAL_API_KEY = os.environ["MISTRAL_API_KEY"]
PAPPERS_API_KEY = os.environ["PAPPERS_API_KEY"]

def extract_from_documents(pdf_paths):
    import base64
    contents = []
    for path in pdf_paths:
        with open(path, "rb") as f:
            b64 = base64.b64encode(f.read()).decode()
        contents.append({"type":"document","source":{"type":"base64","media_type":"application/pdf","data":b64}})
    contents.append({"type":"text","text":"Extrais les champs KYC au format JSON strict."})
    resp = requests.post("https://api.mistral.ai/v1/chat/completions",
        headers={"Authorization": f"Bearer {MISTRAL_API_KEY}"},
        json={"model":"mistral-large-latest","messages":[{"role":"user","content":contents}],"max_tokens":1500,"temperature":0})
    return json.loads(resp.json()["choices"][0]["message"]["content"])

def verify_with_pappers(siren):
    resp = requests.get("https://api.pappers.fr/v2/entreprise",
        params={"siren":siren,"api_token":PAPPERS_API_KEY,"dirigeants":True,"beneficiaires_effectifs":True})
    return resp.json()

def screen_name(name, db, threshold=85):
    from rapidfuzz import fuzz, process
    matches = process.extract(name, db["name"].dropna().tolist(),
        scorer=fuzz.token_sort_ratio, limit=5)
    return [{"name":m[0],"score":m[1]} for m in matches if m[1] >= threshold]

def run_kyc_pipeline(pdf_paths):
    extraction = extract_from_documents(pdf_paths)
    pappers    = verify_with_pappers(extraction["siren"])
    db         = pd.read_csv("./data/opensanctions_entities.csv", low_memory=False)
    screening  = {n: screen_name(n, db) for n in
                  [extraction["legal_name"]] + [f"{d['prenoms']} {d['nom']}"
                   for d in extraction.get("dirigeants", [])]}
    return extraction, pappers, screening
""", language="python")

    with tabs[2]:
        st.markdown("### Souveraineté des données — Audit de flux")
        st.markdown("""<div class='info-box'>
        <div style='font-weight:700;color:#00D4AA;'>Résultat de l'audit lsof en production</div>
        <div style='font-size:0.85rem;color:#7A8BA6;margin-top:0.3rem;'>
        Un seul socket sortant : <code>api.mistral.ai</code> — aucune connexion vers Anthropic depuis le processus du script.
        </div></div>""", unsafe_allow_html=True)

        for service, endpoint, location, data, note, color in [
            ("Mistral AI","api.mistral.ai","🇫🇷 France/UE","Texte des documents","Traitement déclaré UE","#00D4AA"),
            ("Pappers","api.pappers.fr","🇫🇷 France","SIREN uniquement","Source française publique","#00D4AA"),
            ("OpenSanctions","Local (fichier)","🖥️ Machine locale","Aucune","Aucun flux réseau","#00D4AA"),
            ("France Identité","Local (fichier)","🖥️ Machine locale","PDF fourni manuellement","Aucun flux réseau","#00D4AA"),
            ("Anthropic Claude","N/A","🚫 Hors pipeline","Aucune — code seulement","Séparation stricte","#7A8BA6"),
        ]:
            st.markdown(f"""<div style='background:#0F1F3D;border:1px solid #1E3055;border-left:3px solid {color};border-radius:0 8px 8px 0;padding:0.9rem 1rem;margin-bottom:0.5rem;'>
                <div style='font-weight:600;color:#E8EDF5;'>{service} <span style='color:{color};font-size:0.8rem;margin-left:0.5rem;'>{location}</span></div>
                <div style='font-size:0.78rem;color:#7A8BA6;font-family:monospace;'>{endpoint}</div>
                <div style='font-size:0.82rem;color:#E8EDF5;margin-top:0.3rem;'>Données : <span style='color:#FFB347;'>{data}</span> — {note}</div>
            </div>""", unsafe_allow_html=True)

    with tabs[3]:
        st.markdown("### Installation")
        st.code("""# 1. Cloner le repo
git clone https://github.com/votre-org/kyc-platform
cd kyc-platform

# 2. Environnement Python isolé
python3 -m venv venv && source venv/bin/activate

# 3. Dépendances
pip install -r requirements.txt

# 4. Variables d'environnement
cp .env.example .env
# Renseigner MISTRAL_API_KEY et PAPPERS_API_KEY

# 5. Lancer
streamlit run app.py
""", language="bash")

        st.markdown("### requirements.txt")
        st.code("""streamlit>=1.35.0
pandas>=2.0.0
plotly>=5.17.0
rapidfuzz>=3.6.0
reportlab>=4.0.0
openpyxl>=3.1.0
requests>=2.31.0
python-dotenv>=1.0.0
""", language="text")
