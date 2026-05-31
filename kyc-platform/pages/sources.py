import streamlit as st
import pandas as pd

def show():
    st.markdown("## 📊 Sources de données intégrées")
    st.markdown("<div style='color: #7A8BA6; margin-bottom: 1.5rem;'>Catalogue complet des sources OSINT, registres officiels, listes de sanctions et APIs utilisées dans le pipeline KYC</div>", unsafe_allow_html=True)

    tabs = st.tabs(["🏛️ Registres officiels", "⚖️ Sanctions & PPE", "📰 Adverse Media & OSINT", "🔌 APIs techniques", "🇫🇷 Sources françaises spécifiques"])

    with tabs[0]:
        st.markdown("### Registres officiels & sources réglementaires")
        sources = [
            {
                "name": "Pappers API",
                "url": "https://api.pappers.fr",
                "pays": "🇫🇷 France",
                "data": "Kbis, dirigeants, actionnaires, procédures collectives, actes, bilans",
                "acces": "API payante",
                "update": "Temps réel",
                "usage": "Vérification SIREN, identité dirigeants, structure capital",
                "color": "#00D4AA"
            },
            {
                "name": "INPI — Registre des Bénéficiaires Effectifs",
                "url": "https://data.inpi.fr",
                "pays": "🇫🇷 France",
                "data": "Bénéficiaires effectifs déclarés, UBOs, seuil >25%",
                "acces": "Accès libre + API",
                "update": "Batch hebdomadaire",
                "usage": "Identification UBOs, contrôle déclaration obligatoire",
                "color": "#00D4AA"
            },
            {
                "name": "BODACC",
                "url": "https://bodacc.fr",
                "pays": "🇫🇷 France",
                "data": "Avis légaux, ventes fonds, procédures collectives, modifications",
                "acces": "API publique gratuite",
                "update": "Quotidien",
                "usage": "Détection procédures collectives, changements significatifs",
                "color": "#00D4AA"
            },
            {
                "name": "INSEE — Base SIRENE",
                "url": "https://api.insee.fr/entreprises/sirene",
                "pays": "🇫🇷 France",
                "data": "Identification établissements, code NAF, statut actif/inactif",
                "acces": "API publique (token requis)",
                "update": "Quotidien",
                "usage": "Vérification existence juridique, activité réelle",
                "color": "#00D4AA"
            },
            {
                "name": "AMF — Info-Financière",
                "url": "https://data.gouv.fr/dataservices/api-info-financiere",
                "pays": "🇫🇷 France",
                "data": "Informations réglementées, déclarations franchissements de seuils",
                "acces": "API publique",
                "update": "Temps réel",
                "usage": "Contrôle entités réglementées, déclarations émetteurs",
                "color": "#00D4AA"
            },
            {
                "name": "Registre du Commerce Européen (EBR)",
                "url": "https://www.ebr.org",
                "pays": "🇪🇺 UE",
                "data": "Registres de commerce des 28 États membres",
                "acces": "API payante",
                "update": "Variable par pays",
                "usage": "Vérification sociétés européennes, cross-border",
                "color": "#7A8BA6"
            },
            {
                "name": "Luxembourg Business Registers",
                "url": "https://www.lbr.lu",
                "pays": "🇱🇺 Luxembourg",
                "data": "RCS, RCSL, RBE luxembourgeois",
                "acces": "API publique partielle",
                "update": "Temps réel",
                "usage": "Holdings luxembourgeoises, structures de détention",
                "color": "#7A8BA6"
            },
            {
                "name": "Companies House (UK)",
                "url": "https://api.company-information.service.gov.uk",
                "pays": "🇬🇧 UK",
                "data": "Sociétés britanniques, PSC (Persons with Significant Control)",
                "acces": "API publique gratuite",
                "update": "Temps réel",
                "usage": "Entités UK, bénéficiaires effectifs",
                "color": "#7A8BA6"
            },
        ]
        _render_source_cards(sources)

    with tabs[1]:
        st.markdown("### Listes de sanctions & bases PPE")
        sources_sanctions = [
            {
                "name": "OpenSanctions",
                "url": "https://opensanctions.org",
                "pays": "🌍 International",
                "data": "70 000+ entités, consolide ONU, UE, OFAC, HMT, SECO et 100+ listes",
                "acces": "Base téléchargeable + API",
                "update": "Quotidien",
                "usage": "Screening sanctions, PPE, adverse media consolidé",
                "color": "#FF6B35"
            },
            {
                "name": "UE — Registre des sanctions PESC",
                "url": "https://data.europa.eu/data/datasets/eu-financial-sanctions",
                "pays": "🇪🇺 UE",
                "data": "Personnes et entités sous sanctions européennes",
                "acces": "Téléchargement XML/CSV gratuit",
                "update": "Temps réel lors des mises à jour",
                "usage": "Obligation réglementaire UE, AMLD6",
                "color": "#FF6B35"
            },
            {
                "name": "OFAC — SDN List (USA)",
                "url": "https://ofac.treasury.gov/sanctions-list-service",
                "pays": "🇺🇸 USA",
                "data": "Specially Designated Nationals, CAATSA, Cuba, Iran...",
                "acces": "Téléchargement gratuit",
                "update": "Temps réel",
                "usage": "Correspondants USD, entités américaines exposées",
                "color": "#FF6B35"
            },
            {
                "name": "ONU — Comité des sanctions",
                "url": "https://scsanctions.un.org",
                "pays": "🌍 ONU",
                "data": "Listes consolidées ONU (Al-Qaïda, Daesh, DPRK...)",
                "acces": "XML gratuit",
                "update": "Variable",
                "usage": "Financement terrorisme, prolifération",
                "color": "#FF6B35"
            },
            {
                "name": "HMT — Financial Sanctions (UK)",
                "url": "https://www.gov.uk/government/publications/financial-sanctions-consolidated-list",
                "pays": "🇬🇧 UK",
                "data": "Liste consolidée His Majesty's Treasury",
                "acces": "Téléchargement CSV/XML gratuit",
                "update": "Quotidien",
                "usage": "Entités sous sanctions britanniques post-Brexit",
                "color": "#FF6B35"
            },
            {
                "name": "DGT — Gels d'avoirs (France)",
                "url": "https://gels-avoirs.dgtresor.gouv.fr",
                "pays": "🇫🇷 France",
                "data": "Gels d'avoirs français, mesures nationales",
                "acces": "Téléchargement + API",
                "update": "Temps réel",
                "usage": "Obligation légale française, L.562-4-1 CMF",
                "color": "#FF6B35"
            },
            {
                "name": "SECO — Sanctions (Suisse)",
                "url": "https://www.seco.admin.ch/seco/fr/home/Aussenwirtschaftspolitik_Wirtschaftliche_Zusammenarbeit/Wirtschaftsbeziehungen/exportkontrollen-und-sanktionen/sanktionen-embargos.html",
                "pays": "🇨🇭 Suisse",
                "data": "Sanctions suisses, embargos",
                "acces": "Téléchargement XML",
                "update": "Variable",
                "usage": "Entités suisses, correspondants CHF",
                "color": "#FF6B35"
            },
            {
                "name": "ComplyAdvantage",
                "url": "https://complyadvantage.com",
                "pays": "🌍 International",
                "data": "PPE, sanctions, adverse media, 120M+ profils, mise à jour 24h/24",
                "acces": "API payante (Mesh)",
                "update": "Temps réel (15-min refresh)",
                "usage": "Screening industriel, coverage globale PPE & adverse media",
                "color": "#FF6B35"
            },
            {
                "name": "WorldCheck (Refinitiv/LSEG)",
                "url": "https://www.refinitiv.com/en/financial-crime/world-check-kyc-screening",
                "pays": "🌍 International",
                "data": "3M+ profils, PPE, sanctions, adverse media structuré",
                "acces": "API payante",
                "update": "Continue",
                "usage": "Screening haut volume, faux positifs réduits",
                "color": "#FF6B35"
            },
        ]
        _render_source_cards(sources_sanctions)

    with tabs[2]:
        st.markdown("### Sources OSINT & Adverse Media")
        st.markdown("""<div class='info-box'>
        <div style='font-weight: 600; color: #00D4AA;'>ℹ️ Adverse Media Screening</div>
        <div style='font-size: 0.85rem; color: #7A8BA6; margin-top: 0.3rem;'>
        L'adverse media screening consiste à surveiller les sources d'information publiques pour détecter des actualités défavorables 
        (crimes financiers, fraudes, sanctions, condamnations) sur les clients et leurs bénéficiaires effectifs. 
        Requis par AMLD5/6 et les lignes directrices ACPR.
        </div></div>""", unsafe_allow_html=True)

        sources_osint = [
            {
                "name": "Légifrance",
                "url": "https://legifrance.gouv.fr",
                "pays": "🇫🇷 France",
                "data": "Textes de loi, décisions judiciaires, JORF, BOSP",
                "acces": "API publique",
                "update": "Quotidien",
                "usage": "Condamnations, arrêtés, textes réglementaires",
                "color": "#9B59B6"
            },
            {
                "name": "ACPR — Sanctions publiées",
                "url": "https://acpr.banque-france.fr/sanctions",
                "pays": "🇫🇷 France",
                "data": "Sanctions disciplinaires, avertissements, interdictions",
                "acces": "Web scraping / manuel",
                "update": "Variable",
                "usage": "Entités du secteur financier sanctionnées",
                "color": "#9B59B6"
            },
            {
                "name": "AMF — Décisions et sanctions",
                "url": "https://www.amf-france.org/fr/sanctions-et-transactions",
                "pays": "🇫🇷 France",
                "data": "Sanctions AMF, transactions, mises en demeure",
                "acces": "Web / API partielle",
                "update": "Variable",
                "usage": "Acteurs marchés financiers sanctionnés",
                "color": "#9B59B6"
            },
            {
                "name": "TRACFIN — Publications",
                "url": "https://www.economie.gouv.fr/tracfin",
                "pays": "🇫🇷 France",
                "data": "Typologies de blanchiment, rapports annuels",
                "acces": "Public",
                "update": "Annuel",
                "usage": "Référentiels typologies, formation analystes",
                "color": "#9B59B6"
            },
            {
                "name": "ICIJ — Offshore Leaks",
                "url": "https://offshoreleaks.icij.org",
                "pays": "🌍 International",
                "data": "Panama Papers, Pandora Papers, Paradise Papers — 800 000+ entités",
                "acces": "Interface publique + API",
                "update": "Ponctuel (nouvelles fuites)",
                "usage": "Structures offshore, opacité actionnariale",
                "color": "#9B59B6"
            },
            {
                "name": "OpenCorporates",
                "url": "https://opencorporates.com",
                "pays": "🌍 International",
                "data": "200M+ sociétés dans 130 pays",
                "acces": "API freemium",
                "update": "Variable",
                "usage": "Mapping structures corporate internationales",
                "color": "#9B59B6"
            },
            {
                "name": "OCCRP — Aleph",
                "url": "https://aleph.occrp.org",
                "pays": "🌍 International",
                "data": "Bases de données leaked, registres, documents judiciaires",
                "acces": "Interface publique + API",
                "update": "Continue",
                "usage": "Journalisme d'investigation, due diligence approfondie",
                "color": "#9B59B6"
            },
            {
                "name": "Infogreffe",
                "url": "https://www.infogreffe.fr",
                "pays": "🇫🇷 France",
                "data": "Kbis officiels, actes déposés, comptes annuels",
                "acces": "Payant à l'acte / API",
                "update": "Temps réel",
                "usage": "Documents officiels opposables",
                "color": "#9B59B6"
            },
        ]
        _render_source_cards(sources_osint)

    with tabs[3]:
        st.markdown("### APIs techniques & intégrations")

        col1, col2 = st.columns(2)
        apis = [
            ("Pappers", "https://api.pappers.fr/v2", "Bearer token", "Python `requests`", "pip install pappers"),
            ("OpenSanctions", "https://api.opensanctions.org", "API key header", "REST JSON", "Base locale ou API"),
            ("ComplyAdvantage", "https://api.complyadvantage.com", "Bearer token", "REST JSON", "pip install complyadvantage"),
            ("INSEE SIRENE", "https://api.insee.fr/entreprises/sirene/V3", "Bearer OAuth2", "REST JSON", "Token gratuit sur insee.fr"),
            ("AMF Info-Financière", "https://api.info-financiere.fr/api/v1", "Aucune (publique)", "REST JSON", "Accès libre"),
            ("BODACC", "https://bodacc.fr/api", "Aucune (publique)", "REST JSON", "Accès libre"),
            ("DGT Gels d'avoirs", "https://gels-avoirs.dgtresor.gouv.fr/api", "Aucune (publique)", "REST XML/JSON", "Accès libre"),
            ("Mistral AI", "https://api.mistral.ai/v1", "Bearer token", "OpenAI-compatible", "pip install mistralai"),
        ]

        for i, (name, url, auth, format_, note) in enumerate(apis):
            col = col1 if i % 2 == 0 else col2
            with col:
                st.markdown(f"""
                <div style='background: #0F1F3D; border: 1px solid #1E3055; border-radius: 8px; padding: 1rem; margin-bottom: 0.8rem;'>
                    <div style='font-weight: 600; color: #00D4AA; margin-bottom: 0.5rem;'>🔌 {name}</div>
                    <div style='font-family: IBM Plex Mono, monospace; font-size: 0.72rem; color: #7A8BA6; background: rgba(0,0,0,0.3); padding: 4px 8px; border-radius: 4px; margin-bottom: 0.5rem;'>{url}</div>
                    <div style='font-size: 0.8rem; color: #E8EDF5;'>Auth: <span style='color: #FFB347;'>{auth}</span></div>
                    <div style='font-size: 0.8rem; color: #E8EDF5;'>Format: <span style='color: #FFB347;'>{format_}</span></div>
                    <div style='font-size: 0.75rem; color: #7A8BA6; margin-top: 0.3rem;'>{note}</div>
                </div>
                """, unsafe_allow_html=True)

        st.markdown("### Exemple d'appel API — Pappers")
        st.code("""import requests

# Interroger Pappers pour obtenir les infos d'une société
def get_company_pappers(siren: str, api_key: str) -> dict:
    url = f"https://api.pappers.fr/v2/entreprise"
    params = {
        "siren": siren,
        "api_token": api_key,
        "extrait_kbis": True,
        "beneficiaires_effectifs": True,
        "dirigeants": True,
        "procedures_collectives": True
    }
    response = requests.get(url, params=params)
    return response.json()

# Usage
data = get_company_pappers("952744167", "votre_api_key")
print(data["denomination"])  # → "Early Consulting"
print(data["dirigeants"])    # → liste des dirigeants
""", language="python")

    with tabs[4]:
        st.markdown("### 🇫🇷 Spécificités françaises")

        st.markdown("""<div class='info-box' style='margin-bottom: 1.5rem;'>
        <div style='font-weight: 700; color: #00D4AA; font-size: 1rem;'>France Identité — Pièce d'identité numérique souveraine</div>
        <div style='font-size: 0.85rem; color: #E8EDF5; margin-top: 0.5rem;'>
        Porté par France Titres (ANTS), le justificatif France Identité est signé électroniquement par le ministère de l'Intérieur. 
        Il contient les données d'identité strictement nécessaires, pour un destinataire et une durée définis.
        </div></div>""", unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**Avantages KYC**")
            advantages = [
                "✅ Signature cryptographique ministère de l'Intérieur",
                "✅ Usage unique par destinataire et durée",
                "✅ Minimisation des données (pas de numéro de carte)",
                "✅ Traçabilité du consentement intégrée",
                "✅ Vérification via QR code service public",
                "✅ Fraude documentaire quasiment éliminée",
            ]
            for a in advantages:
                st.markdown(f"<div style='font-size: 0.85rem; color: #E8EDF5; margin: 0.3rem 0;'>{a}</div>", unsafe_allow_html=True)

        with col2:
            st.markdown("**Limitations actuelles**")
            limits = [
                "⚠️ Pas d'API publique pour raccordement automatique",
                "⚠️ Modes de raccordement (OIDC/OID4VP) sur invitation",
                "⚠️ Coercition du titulaire reste un vecteur de fraude",
                "⚠️ Ne couvre pas l'ensemble des pièces acceptées (passeport...)",
                "⚠️ Intégration manuelle dans pipeline actuel",
            ]
            for l in limits:
                st.markdown(f"<div style='font-size: 0.85rem; color: #E8EDF5; margin: 0.3rem 0;'>{l}</div>", unsafe_allow_html=True)

        st.markdown("---")
        st.markdown("**Registre des Bénéficiaires Effectifs (INPI/RBE)**")
        st.markdown("""<div style='font-size: 0.85rem; color: #7A8BA6;'>
        Depuis la loi SAPIN II et les directives AMLD4/5, toute société française doit déclarer ses bénéficiaires effectifs (UBOs) 
        détenant directement ou indirectement plus de 25% du capital ou des droits de vote. La déclaration est consultable sur 
        le site de l'INPI. Une déclaration absente ou incohérente est un signal d'alerte KYC.
        </div>""", unsafe_allow_html=True)


def _render_source_cards(sources):
    for s in sources:
        with st.expander(f"**{s['name']}** — {s['pays']} — {s['acces']}", expanded=False):
            col1, col2 = st.columns([2, 1])
            with col1:
                st.markdown(f"**URL :** `{s['url']}`")
                st.markdown(f"**Données :** {s['data']}")
                st.markdown(f"**Usage KYC :** {s['usage']}")
            with col2:
                st.markdown(f"**Mise à jour :** {s['update']}")
                st.markdown(f"**Accès :** {s['acces']}")


def show_data_explorer():
    """Standalone tab for CSV data explorer - called from sources page"""
    import pandas as pd
    import os
    DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
    
    CSV_FILES = {
        "📋 Codes NAF / risque LCB-FT": "codes_naf_risque.csv",
        "🌍 Pays — risque GAFI / sanctions": "pays_risque_gafi.csv",
        "🇪🇺 Codes NACE Europe": "codes_nace_europe.csv",
        "🔍 Historique screenings": "historique_screenings.csv",
        "🗂️ Registre dossiers KYC": "registre_dossiers_kyc.csv",
        "⚠️ Typologies de blanchiment": "typologies_blanchiment.csv",
        "⚖️ Sources de sanctions": "sources_sanctions.csv",
        "📏 Règles de scoring LCB-FT": "regles_scoring_lcbft.csv",
    }
    
    st.markdown("## 🗄️ Explorateur de données — Bases de référence")
    st.markdown("<div style='color: #7A8BA6; margin-bottom: 1.5rem;'>Bases de données intégrées : codes sectoriels, pays, typologies, règles de scoring</div>", unsafe_allow_html=True)
    
    selected = st.selectbox("Sélectionner une base", list(CSV_FILES.keys()))
    filename = CSV_FILES[selected]
    filepath = os.path.join(DATA_DIR, filename)
    
    if os.path.exists(filepath):
        df = pd.read_csv(filepath, encoding="utf-8")
        
        col1, col2, col3 = st.columns(3)
        with col1: st.markdown(f"""<div class='metric-card'><div class='metric-value'>{len(df)}</div><div class='metric-label'>Entrées</div></div>""", unsafe_allow_html=True)
        with col2: st.markdown(f"""<div class='metric-card'><div class='metric-value'>{len(df.columns)}</div><div class='metric-label'>Colonnes</div></div>""", unsafe_allow_html=True)
        with col3: st.markdown(f"""<div class='metric-card'><div class='metric-value'>{filename.split('.')[0][:10]}</div><div class='metric-label'>Fichier source</div></div>""", unsafe_allow_html=True)

        # Filters
        search_col = st.text_input("🔍 Rechercher dans toutes les colonnes", "")
        if search_col:
            mask = df.astype(str).apply(lambda col: col.str.contains(search_col, case=False, na=False)).any(axis=1)
            df = df[mask]
            st.caption(f"{len(df)} résultat(s)")
        
        st.dataframe(df, use_container_width=True, hide_index=True)
        
        csv_bytes = df.to_csv(index=False, encoding="utf-8").encode("utf-8")
        st.download_button(f"⬇️ Télécharger {filename}", csv_bytes, filename, "text/csv")
    else:
        st.error(f"Fichier non trouvé : {filepath}")
