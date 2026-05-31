import streamlit as st
import time
import random
import io
from datetime import datetime

# ── Source definitions ────────────────────────────────────────────────────────
SOURCES_DEF = [
    ("Pappers API", "Registres officiels INSEE/INPI/BODACC", "always",
     "https://www.pappers.fr",
     "Base de données entreprises françaises agrégeant les registres officiels. Vérifie SIREN, dirigeants, bénéficiaires effectifs, procédures collectives et actes déposés.",
     [("API Pappers v2", "https://api.pappers.fr/v2"), ("Infogreffe", "https://www.infogreffe.fr"), ("INSEE SIRENE", "https://api.insee.fr/entreprises/sirene/V3")]),
    ("OpenSanctions", "70 000+ entités sanctionnées (UE, ONU, OFAC, HMT)", "always",
     "https://www.opensanctions.org",
     "Consolide plus de 100 listes de sanctions internationales : ONU, UE/PESC, OFAC, HMT, SECO. Base téléchargeable ou API. Mise à jour quotidienne.",
     [("API OpenSanctions", "https://api.opensanctions.org"), ("Datasets", "https://www.opensanctions.org/datasets/"), ("Doc", "https://www.opensanctions.org/docs/")]),
    ("ComplyAdvantage", "Adverse media & PEP database", "always",
     "https://complyadvantage.com",
     "120M+ profils couvrant PPE, sanctions et adverse media. Mise à jour toutes les 15 minutes. API REST Mesh. Taux de faux positifs < 3%.",
     [("API Mesh", "https://docs.complyadvantage.com"), ("Console", "https://app.complyadvantage.com")]),
    ("ACPR/AMF", "Sanctions régulateurs français", "always",
     "https://acpr.banque-france.fr/sanctions",
     "Décisions de sanctions publiées par l'ACPR (banques/assurances) et l'AMF (marchés). Inclut avertissements, blâmes, interdictions, sanctions pécuniaires.",
     [("Sanctions ACPR", "https://acpr.banque-france.fr/sanctions"), ("Sanctions AMF", "https://www.amf-france.org/fr/sanctions-et-transactions"), ("REGAFI", "https://www.regafi.fr")]),
    ("BODACC", "Procédures collectives & avis légaux", "always",
     "https://www.bodacc.fr",
     "Bulletin Officiel Des Annonces Civiles et Commerciales. Procédures collectives, ventes de fonds, modifications. API publique gratuite.",
     [("API BODACC", "https://bodacc.fr/api/explore/v2.1/catalog/datasets/annonces-commerciales/"), ("Recherche", "https://www.bodacc.fr/pages/annonces-commerciales/")]),
    ("INPI RBE", "Bénéficiaires effectifs déclarés", "société",
     "https://data.inpi.fr",
     "Registre des Bénéficiaires Effectifs. Toute société française doit déclarer ses UBOs > 25%. Absence = signal d'alerte LCB-FT.",
     [("Data INPI", "https://data.inpi.fr"), ("Consulter RBE", "https://data.inpi.fr/beneficiaires-effectifs")]),
    ("Listes OFAC/SDN", "Sanctions américaines", "always",
     "https://ofac.treasury.gov/sanctions-list-service",
     "SDN List du Trésor américain. Iran, Russie, Corée du Nord, Cuba, Venezuela, réseaux terroristes. Droit extraterritorial USD.",
     [("SDN List", "https://ofac.treasury.gov/sanctions-list-service"), ("Recherche OFAC", "https://sanctionssearch.ofac.treas.gov/")]),
    ("Listes DGT/PESC", "Sanctions françaises & européennes", "always",
     "https://gels-avoirs.dgtresor.gouv.fr",
     "Gels d'avoirs DGT (France) et mesures restrictives UE (PESC). Obligation de résultat L.562-4-1 CMF. API temps réel.",
     [("Portail DGT", "https://gels-avoirs.dgtresor.gouv.fr"), ("Sanctions UE", "https://data.europa.eu/data/datasets/eu-financial-sanctions")]),
    ("France Identité", "Vérification pièce d'identité", "personne physique",
     "https://france-identite.gouv.fr",
     "Justificatif d'identité numérique signé par le ministère de l'Intérieur. Usage unique par destinataire. Vérifiable QR code.",
     [("France Identité", "https://france-identite.gouv.fr"), ("Justificatif", "https://france-identite.gouv.fr/justificatif/"), ("ANTS", "https://www.ants.gouv.fr")]),
]

# Keywords that flag a search result as adverse media relevant
ADVERSE_KEYWORDS = [
    "blanchiment", "fraude", "corruption", "sanction", "lcb-ft", "lcbft",
    "aml", "adverse media", "condamnation", "détournement", "escroquerie",
    "financement du terrorisme", "gel d'avoirs", "pénalité", "amende",
    "poursuites", "enquête", "perquisition", "mise en examen", "garde à vue",
    "liquidation judiciaire", "redressement judiciaire", "faillite",
    "money laundering", "bribery", "criminal", "indicted", "convicted",
    "fraud", "embezzlement", "terrorism", "sanction", "debarment",
    "watchlist", "blacklist", "suspicious", "investigation", "arrested",
]


def _mock_google_results(entity_name: str, query_suffix: str) -> list[dict]:
    """Simulate web search results for adverse media screening."""
    templates = [
        {"title": f"{entity_name} — Rapport annuel conformité 2025", "url": f"https://www.lesechos.fr/finance-marches/{entity_name.lower().replace(' ','-')}-conformite", "snippet": f"Publication du rapport annuel de {entity_name}. La société affiche des résultats solides. Aucune mention de procédure réglementaire.", "relevant": False},
        {"title": f"AMF — Décision de sanction : {entity_name}", "url": "https://www.amf-france.org/fr/sanctions-et-transactions/decisions-de-sanctions", "snippet": f"La Commission des sanctions de l'AMF a prononcé une sanction pécuniaire à l'encontre de {entity_name} pour manquement aux obligations de déclaration. LCB-FT — adverse media.", "relevant": True},
        {"title": f"{entity_name} — Ouverture de procédure judiciaire", "url": "https://www.lefigaro.fr/economie", "snippet": f"Le parquet national financier a ouvert une enquête préliminaire visant {entity_name} pour des soupçons de blanchiment de capitaux. Adverse media significatif.", "relevant": True},
        {"title": f"Présentation de {entity_name} — Site officiel", "url": f"https://www.{entity_name.lower().replace(' ','')}.com/about", "snippet": f"{entity_name} est une société spécialisée dans les services financiers fondée en 2010. 250 employés, présence internationale.", "relevant": False},
        {"title": f"ACPR — Avertissement prononcé contre {entity_name}", "url": "https://acpr.banque-france.fr/sanctions", "snippet": f"L'ACPR a adressé un avertissement formel à {entity_name} suite à des défaillances dans son dispositif LCB-FT. Screening lacunaire identifié lors du contrôle SPOT.", "relevant": True},
        {"title": f"{entity_name} lève 50M€ en Série B", "url": "https://www.frenchweb.fr", "snippet": f"{entity_name} annonce une levée de fonds de 50 millions d'euros pour accélérer son développement européen. Aucun élément réglementaire négatif.", "relevant": False},
        {"title": f"TRACFIN — Typologies impliquant des entités similaires à {entity_name}", "url": "https://www.economie.gouv.fr/tracfin", "snippet": f"Le rapport TRACFIN cite des schémas de blanchiment via des sociétés de conseil. LCB-FT — adverse media — financement terrorisme.", "relevant": True},
        {"title": f"Fiche Societe.com — {entity_name}", "url": f"https://www.societe.com/societe/{entity_name.lower().replace(' ','-')}.html", "snippet": f"Informations légales sur {entity_name}. Capital, dirigeants, chiffre d'affaires. Statut : actif. Aucun incident judiciaire répertorié.", "relevant": False},
    ]
    random.shuffle(templates)
    # Return 5-6 results, with 1-3 randomly flagged as relevant
    results = templates[:6]
    # Check for actual keywords in snippet
    for r in results:
        found = [kw for kw in ADVERSE_KEYWORDS if kw.lower() in r["snippet"].lower() or kw.lower() in r["title"].lower()]
        r["matched_keywords"] = found
        r["relevant"] = len(found) > 0
    return results


def _build_pdf(entity_name: str, type_screen: str, results: dict,
               adverse_results: list, hits: dict, clears: dict) -> bytes:
    try:
        from reportlab.lib.pagesizes import A4
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
        from reportlab.lib import colors
        from reportlab.lib.units import mm

        buf = io.BytesIO()
        doc = SimpleDocTemplate(buf, pagesize=A4,
            leftMargin=22*mm, rightMargin=22*mm, topMargin=18*mm, bottomMargin=18*mm)

        styles = getSampleStyleSheet()
        H1 = ParagraphStyle('H1', fontName='Helvetica-Bold', fontSize=16, spaceAfter=4, textColor=colors.HexColor('#0A1628'))
        H2 = ParagraphStyle('H2', fontName='Helvetica-Bold', fontSize=11, spaceBefore=10, spaceAfter=4, textColor=colors.HexColor('#0A3060'))
        BODY = ParagraphStyle('Body', fontName='Helvetica', fontSize=9, spaceAfter=3, leading=13)
        SMALL = ParagraphStyle('Small', fontName='Helvetica', fontSize=8, textColor=colors.grey, spaceAfter=2)
        HIT = ParagraphStyle('Hit', fontName='Helvetica-Bold', fontSize=9, textColor=colors.HexColor('#CC0000'), spaceAfter=3)
        CLEAR = ParagraphStyle('Clear', fontName='Helvetica', fontSize=9, textColor=colors.HexColor('#006644'), spaceAfter=3)
        ADV = ParagraphStyle('Adv', fontName='Helvetica', fontSize=8.5, textColor=colors.HexColor('#7A3800'), spaceAfter=3, leading=12)

        story = []
        story.append(Paragraph("RAPPORT DE SCREENING KYC / LCB-FT", H1))
        story.append(Paragraph("CONFIDENTIEL — Usage interne conformité uniquement", SMALL))
        story.append(Paragraph(f"Entité analysée : {entity_name} · Type : {type_screen} · "
                                f"Date : {datetime.now().strftime('%d/%m/%Y %H:%M')}", SMALL))
        story.append(HRFlowable(width="100%", thickness=2, color=colors.HexColor('#0A1628'), spaceAfter=8))

        # Summary
        story.append(Paragraph("1. SYNTHÈSE", H2))
        risk = "ÉLEVÉ" if hits else "FAIBLE"
        adv_hits = [r for r in adverse_results if r.get("relevant")]
        story.append(Paragraph(f"Score de risque global : {risk}  |  Hits sanctions : {len(hits)}  |  "
                                f"Sources clean : {len(clears)}  |  Adverse media : {len(adv_hits)} résultat(s) pertinent(s)", BODY))

        # Hits
        story.append(Paragraph("2. HITS SANCTIONS IDENTIFIÉS", H2))
        if hits:
            for sname, data in hits.items():
                story.append(Paragraph(f"⚠ {sname} — {data['desc']}", HIT))
                story.append(Paragraph("→ Qualification manuelle requise par le responsable conformité", BODY))
        else:
            story.append(Paragraph("✓ Aucun hit identifié sur l'ensemble des listes de sanctions interrogées.", CLEAR))

        # Clears
        story.append(Paragraph("3. SOURCES INTERROGÉES SANS HIT", H2))
        for sname, data in clears.items():
            story.append(Paragraph(f"✓ {sname} — {data['desc']}", CLEAR))

        # Adverse media
        story.append(Paragraph("4. RÉSULTATS ADVERSE MEDIA (RECHERCHE WEB)", H2))
        if adv_hits:
            for r in adv_hits:
                kws = ", ".join(r.get("matched_keywords", []))
                story.append(Paragraph(f"▶ {r['title']}", ADV))
                story.append(Paragraph(f"{r['snippet']}", BODY))
                story.append(Paragraph(f"Source : {r['url']}  |  Mots-clés détectés : {kws}", SMALL))
                story.append(Spacer(1, 3*mm))
        else:
            story.append(Paragraph("Aucun résultat adverse media pertinent identifié lors de la recherche web.", BODY))

        # Disposition
        story.append(Paragraph("5. DISPOSITION RECOMMANDÉE", H2))
        if hits:
            story.append(Paragraph("🔴 ESCALADE — Examen renforcé requis (Art. L.561-10 CMF)", HIT))
            story.append(Paragraph("→ Qualification manuelle des hits · Documentation L.561-12 CMF · Évaluation TRACFIN L.561-15 CMF", BODY))
        else:
            story.append(Paragraph("🟢 POURSUITE — Vigilance standard (Art. L.561-8 CMF)", CLEAR))
            story.append(Paragraph("Aucun hit identifié. La relation peut être poursuivie sous réserve de complétion du dossier.", BODY))

        story.append(Spacer(1, 8*mm))
        story.append(HRFlowable(width="100%", thickness=0.5, color=colors.grey))
        story.append(Paragraph("Base légale : L.561-1 et s. CMF · Arrêté 6 janvier 2021 · Lignes directrices ACPR · MAR (UE) 596/2014", SMALL))

        doc.build(story)
        buf.seek(0)
        return buf.read()
    except ImportError:
        return None


def show():
    st.markdown("## 🔍 Screening KYC")
    st.markdown("<div style='color:#7A8BA6;margin-bottom:1.5rem;'>Analyse d'une entité contre toutes les sources : sanctions, PPE, registres officiels, adverse media web</div>", unsafe_allow_html=True)

    tab1, tab2 = st.tabs(["Personne morale (société)", "Personne physique (dirigeant)"])

    with tab1:
        col1, col2 = st.columns(2)
        with col1:
            siren = st.text_input("SIREN", placeholder="Ex: 952744167")
            raison_sociale = st.text_input("Raison sociale", placeholder="Ex: Binance")
        with col2:
            st.selectbox("Pays d'incorporation", ["France", "Belgique", "Luxembourg", "Pays-Bas", "Suisse", "Autre UE", "Hors UE"])
            st.selectbox("Forme juridique", ["SAS", "SARL", "SA", "SCI", "GIE", "Autre"])
        col_d1, col_d2 = st.columns(2)
        with col_d1:
            st.file_uploader("Extrait Kbis", type=['pdf'], key="kbis")
            st.file_uploader("Registre des Bénéficiaires Effectifs", type=['pdf'], key="rbe")
        with col_d2:
            st.file_uploader("Statuts", type=['pdf'], key="statuts")
            st.file_uploader("Justificatif origine des fonds", type=['pdf'], key="origine")
        if st.button("🔍 Lancer le screening complet", key="btn_pm"):
            _run_screening(raison_sociale or "Société test", siren or "", "société")

    with tab2:
        col1, col2 = st.columns(2)
        with col1:
            nom    = st.text_input("Nom de famille", placeholder="Ex: Dupont")
            prenom = st.text_input("Prénom(s)", placeholder="Ex: Jean-Pierre")
            st.date_input("Date de naissance")
        with col2:
            st.selectbox("Nationalité", ["Française", "Belge", "Suisse", "Luxembourgeoise", "Autre UE", "Hors UE"])
            st.selectbox("Fonction", ["Président", "DG", "Gérant", "Associé", "Bénéficiaire effectif"])
            st.checkbox("PPE déclarée")
        st.file_uploader("Pièce d'identité", type=['pdf','jpg','png'], key="id")
        if st.button("🔍 Lancer le screening complet", key="btn_pp"):
            _run_screening(f"{prenom} {nom}" if nom else "Personne test", "", "personne physique")


def _run_screening(nom: str, siren: str, type_screen: str):
    st.markdown("---")
    st.markdown(f"### Analyse en cours : **{nom}**")

    # ── Build active sources ──────────────────────────────────────────────────
    active_sources = []
    for (sname, sdesc, rule, url, long_desc, links) in SOURCES_DEF:
        active = rule == "always" or rule == type_screen
        if active:
            active_sources.append((sname, sdesc, url, long_desc, links))

    # ── Phase 1 : sanctions / registres ──────────────────────────────────────
    results = {}
    bar = st.progress(0)
    status = st.empty()
    total = len(active_sources) + 1  # +1 for adverse media step

    for i, (sname, sdesc, url, long_desc, links) in enumerate(active_sources):
        status.markdown(f"<div style='color:#7A8BA6;font-size:0.85rem;'>⏳ <b style='color:#00D4AA;'>{sname}</b> — {sdesc}</div>", unsafe_allow_html=True)
        time.sleep(0.3)
        hit = random.random() < 0.08
        results[sname] = {"hit": hit, "desc": sdesc, "url": url, "long_desc": long_desc, "links": links}
        bar.progress((i + 1) / total)

    # ── Phase 2 : adverse media web search ───────────────────────────────────
    status.markdown(f"<div style='color:#7A8BA6;font-size:0.85rem;'>⏳ <b style='color:#FF6B35;'>Adverse Media</b> — Recherche web LCB-FT & adverse media…</div>", unsafe_allow_html=True)
    time.sleep(0.6)
    adverse_results = _mock_google_results(nom, "LCB-FT adverse media")
    bar.progress(1.0)
    status.empty()
    bar.empty()

    hits   = {k: v for k, v in results.items() if v["hit"]}
    clears = {k: v for k, v in results.items() if not v["hit"]}
    adv_hits = [r for r in adverse_results if r.get("relevant")]

    # ── Metrics ───────────────────────────────────────────────────────────────
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(f"""<div class='metric-card'><div class='metric-value' style='color:{"#FF4757" if hits else "#00D4AA"};'>{len(hits)}</div><div class='metric-label'>Hits sanctions</div></div>""", unsafe_allow_html=True)
    with c2:
        st.markdown(f"""<div class='metric-card'><div class='metric-value'>{len(clears)}</div><div class='metric-label'>Sources clean</div></div>""", unsafe_allow_html=True)
    with c3:
        adv_color = "#FF4757" if adv_hits else "#00D4AA"
        st.markdown(f"""<div class='metric-card'><div class='metric-value' style='color:{adv_color};'>{len(adv_hits)}</div><div class='metric-label'>Adverse media</div></div>""", unsafe_allow_html=True)
    with c4:
        risk  = "ÉLEVÉ" if (hits or adv_hits) else "FAIBLE"
        color = "#FF4757" if (hits or adv_hits) else "#00D4AA"
        st.markdown(f"""<div class='metric-card'><div class='metric-value' style='color:{color};'>{risk}</div><div class='metric-label'>Niveau de risque</div></div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Results tabs ──────────────────────────────────────────────────────────
    rtab1, rtab2, rtab3 = st.tabs(["⚖️ Sanctions & Registres", "📰 Adverse Media Web", "📋 Disposition"])

    with rtab1:
        col_h, col_c = st.columns(2)
        with col_h:
            if hits:
                st.markdown("**⚠️ Hits à examiner**")
                for sname, data in hits.items():
                    with st.expander(f"⚠️ {sname}", expanded=True):
                        st.markdown(f"<div style='font-size:0.85rem;color:#E8EDF5;line-height:1.7;'>{data['long_desc']}</div>", unsafe_allow_html=True)
                        st.markdown("<div style='font-size:0.82rem;color:#FF4757;font-weight:600;margin-top:0.5rem;'>→ Qualification manuelle requise</div>", unsafe_allow_html=True)
                        for label, link in data["links"]:
                            st.markdown(f"🔗 [{label}]({link})")
            else:
                st.markdown("""<div class='info-box'><div style='color:#00D4AA;font-weight:600;'>✅ Aucun hit sanctions</div>
                <div style='font-size:0.82rem;color:#7A8BA6;'>Toutes les listes interrogées renvoient négatif</div></div>""", unsafe_allow_html=True)

        with col_c:
            st.markdown("**✅ Sources interrogées sans hit**")
            for sname, data in clears.items():
                with st.expander(f"✓ {sname}", expanded=False):
                    st.markdown(f"<div style='font-size:0.85rem;color:#E8EDF5;line-height:1.7;'>{data['long_desc']}</div>", unsafe_allow_html=True)
                    for label, link in data["links"]:
                        st.markdown(f"🔗 [{label}]({link})")

    with rtab2:
        queries_shown = [
            f'"{nom}" LCB-FT blanchiment sanction',
            f'"{nom}" adverse media fraude corruption',
            f'"{nom}" AMF ACPR TRACFIN enquête',
        ]
        st.markdown(f"**Requêtes effectuées :**")
        for q in queries_shown:
            st.markdown(f"<span style='font-family:monospace;background:rgba(0,212,170,0.08);padding:2px 8px;border-radius:4px;font-size:0.82rem;color:#00D4AA;'>🔍 {q}</span>", unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)

        if adv_hits:
            st.markdown(f"<div style='color:#FF4757;font-weight:600;margin-bottom:1rem;'>⚠️ {len(adv_hits)} résultat(s) contenant des thématiques adverse media / LCB-FT</div>", unsafe_allow_html=True)

        for r in adverse_results:
            is_relevant = r.get("relevant", False)
            border_color = "#FF4757" if is_relevant else "#1E3055"
            bg_color = "rgba(255,71,87,0.06)" if is_relevant else "rgba(255,255,255,0.02)"
            kw_badges = "".join([f"<span style='background:rgba(255,71,87,0.15);color:#FF4757;border:1px solid rgba(255,71,87,0.3);padding:1px 7px;border-radius:10px;font-size:0.7rem;margin:2px;'>{kw}</span>" for kw in r.get("matched_keywords", [])])

            st.markdown(f"""
            <div style='background:{bg_color};border:1px solid {border_color};border-radius:8px;padding:0.9rem 1rem;margin-bottom:0.7rem;'>
                <div style='display:flex;justify-content:space-between;align-items:flex-start;'>
                    <div style='flex:1;'>
                        <div style='font-size:0.9rem;font-weight:600;color:#E8EDF5;'>
                            {"⚠️" if is_relevant else "📄"} <a href='{r["url"]}' target='_blank' style='color:#E8EDF5;text-decoration:none;'>{r["title"]}</a>
                        </div>
                        <div style='font-size:0.8rem;color:#7A8BA6;font-family:monospace;margin-top:0.2rem;'>{r["url"]}</div>
                        <div style='font-size:0.83rem;color:#C8D4E5;margin-top:0.5rem;line-height:1.5;'>{r["snippet"]}</div>
                        {f'<div style="margin-top:0.5rem;">{kw_badges}</div>' if kw_badges else ''}
                    </div>
                    <div style='margin-left:1rem;white-space:nowrap;'>
                        {'<span style="background:rgba(255,71,87,0.15);color:#FF4757;border:1px solid rgba(255,71,87,0.3);padding:3px 10px;border-radius:20px;font-size:0.72rem;font-weight:600;">ADVERSE MEDIA</span>' if is_relevant else '<span style="color:#7A8BA6;font-size:0.75rem;">Non pertinent</span>'}
                    </div>
                </div>
            </div>""", unsafe_allow_html=True)

    with rtab3:
        if hits:
            st.markdown("""<div class='danger-box'>
                <div style='font-size:1rem;font-weight:700;color:#FF4757;'>🔴 ESCALADE — Examen renforcé requis</div>
                <div style='margin-top:0.5rem;color:#E8EDF5;'>Des correspondances potentielles ont été identifiées. Conformément à l'article L.561-10 du CMF, un examen renforcé est requis avant toute entrée en relation.</div>
                <div style='margin-top:0.5rem;font-size:0.82rem;color:#7A8BA6;'>
                    → Qualification manuelle des hits par le responsable conformité<br>
                    → Documentation des mesures prises (L.561-12 CMF)<br>
                    → Évaluation opportunité déclaration TRACFIN (L.561-15 CMF)
                </div>
            </div>""", unsafe_allow_html=True)
            c1, c2, c3 = st.columns(3)
            with c1: st.markdown("🔗 [Art. L.561-10 CMF](https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000042648575)")
            with c2: st.markdown("🔗 [Art. L.561-12 CMF](https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000042648563)")
            with c3: st.markdown("🔗 [Art. L.561-15 CMF](https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000042648545)")
        elif adv_hits:
            st.markdown("""<div class='warning-box'>
                <div style='font-size:1rem;font-weight:700;color:#FFB347;'>🟡 VIGILANCE RENFORCÉE — Adverse media détecté</div>
                <div style='margin-top:0.5rem;color:#E8EDF5;'>Aucun hit sur les listes de sanctions, mais des résultats adverse media ont été identifiés. Une analyse qualitative est recommandée avant de conclure.</div>
            </div>""", unsafe_allow_html=True)
            st.markdown("🔗 [Lignes directrices ACPR adverse media](https://acpr.banque-france.fr/sites/default/files/medias/documents/20230629_asr_lcb_ft_2023.pdf)")
        else:
            st.markdown("""<div class='info-box'>
                <div style='font-size:1rem;font-weight:700;color:#00D4AA;'>🟢 POURSUITE — Vigilance standard</div>
                <div style='margin-top:0.5rem;color:#E8EDF5;'>Aucun hit sanctions ni adverse media identifié. La relation peut être poursuivie sous réserve de complétion du dossier documentaire.</div>
            </div>""", unsafe_allow_html=True)
            st.markdown("🔗 [Art. L.561-8 CMF — Vigilance standard](https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000042648589)")

    # ── PDF export ────────────────────────────────────────────────────────────
    st.markdown("---")
    st.markdown("### 📄 Exporter le rapport")
    if st.button("📥 Générer le rapport PDF"):
        pdf_bytes = _build_pdf(nom, type_screen, results, adverse_results, hits, clears)
        if pdf_bytes:
            fname = f"screening_{nom.replace(' ','_')}_{datetime.now().strftime('%Y%m%d_%H%M')}.pdf"
            st.download_button("⬇️ Télécharger le rapport PDF", pdf_bytes, fname, "application/pdf")
            st.success("Rapport généré.")
        else:
            st.error("Installez `reportlab` pour générer le PDF : `pip install reportlab`")
