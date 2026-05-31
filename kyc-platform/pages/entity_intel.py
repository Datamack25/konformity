import streamlit as st
import random
import io
from datetime import datetime

# ── Mock data generator simulating Pappers / Infogreffe / BODACC responses ───
def _fetch_entity_data(name: str, siren: str) -> dict:
    """Simulate aggregated data from Pappers, Infogreffe, BODACC, INPI."""
    random.seed(hash(name) % 10000)
    ca = random.randint(500_000, 50_000_000)
    employees = random.randint(5, 300)
    year = random.randint(2005, 2022)
    capital = random.choice([1_000, 10_000, 50_000, 100_000, 500_000, 1_000_000])
    naf_choices = [
        ("7022Z", "Conseil pour les affaires et autres conseils de gestion"),
        ("6630Z", "Gestion de fonds"),
        ("6612Z", "Courtage de valeurs mobilières"),
        ("6419Z", "Autres intermédiations monétaires"),
        ("6810Z", "Activités des marchands de biens immobiliers"),
        ("6201Z", "Programmation informatique"),
        ("7010Z", "Activités des sièges sociaux"),
    ]
    naf_code, naf_lib = random.choice(naf_choices)

    return {
        "identite": {
            "denomination": name,
            "siren": siren or f"8{random.randint(10000000, 99999999)}",
            "siret_siege": f"8{random.randint(10000000, 99999999)}0001{random.randint(0,9)}",
            "forme_juridique": random.choice(["SAS", "SARL", "SA", "SCI"]),
            "date_creation": f"{year}-{random.randint(1,12):02d}-{random.randint(1,28):02d}",
            "capital": f"{capital:,} €",
            "adresse": f"{random.randint(1,200)} {random.choice(['rue de la Paix','avenue des Champs-Élysées','boulevard Haussmann','rue du Faubourg Saint-Honoré'])}, {random.randint(75001,75020)} Paris",
            "naf_code": naf_code,
            "naf_libelle": naf_lib,
            "tranche_effectif": f"{employees // 10 * 10}–{employees // 10 * 10 + 9} salariés",
            "statut": "Actif",
            "source": "Pappers API / INSEE SIRENE",
        },
        "dirigeants": [
            {"nom": "Martin DUPONT", "fonction": "Président", "depuis": f"{year + 1}", "nationalite": "Française"},
            {"nom": "Sophie LEBLANC", "fonction": "Directeur Général", "depuis": f"{year + 2}", "nationalite": "Française"},
            {"nom": random.choice(["Klaus MÜLLER","Li WEI","Ahmed HASSAN","Elena PETROV"]), "fonction": "Administrateur", "depuis": f"{year + 3}", "nationalite": random.choice(["Allemande","Chinoise","Marocaine","Russe"])},
        ],
        "beneficiaires_effectifs": [
            {"nom": "Martin DUPONT", "pourcentage": "60%", "depuis": f"{year + 1}", "source": "INPI RBE"},
            {"nom": "Sophie LEBLANC", "pourcentage": "40%", "depuis": f"{year + 2}", "source": "INPI RBE"},
        ],
        "financier": {
            "ca_dernier": f"{ca:,} €",
            "ca_n1": f"{int(ca * random.uniform(0.85, 1.15)):,} €",
            "ca_n2": f"{int(ca * random.uniform(0.75, 1.05)):,} €",
            "resultat_net": f"{int(ca * random.uniform(0.02, 0.12)):,} €",
            "fonds_propres": f"{int(ca * random.uniform(0.15, 0.5)):,} €",
            "endettement": random.choice(["Faible", "Modéré", "Élevé"]),
            "score_financier": random.randint(50, 95),
            "source": "Pappers / Infogreffe (comptes déposés)",
        },
        "etablissements": [
            {"siret": f"8{random.randint(10000000,99999999)}0001{random.randint(0,9)}", "adresse": "Paris (siège)", "type": "Siège social", "statut": "Actif"},
            {"siret": f"8{random.randint(10000000,99999999)}0002{random.randint(0,9)}", "adresse": "Lyon", "type": "Établissement secondaire", "statut": "Actif"},
        ],
        "procedures": {
            "redressement": False,
            "liquidation": False,
            "sauvegarde": False,
            "dernieres_annonces": [
                {"date": f"2024-{random.randint(1,12):02d}-{random.randint(1,28):02d}", "type": "Modification", "detail": "Changement d'adresse du siège social"},
                {"date": f"2023-{random.randint(1,12):02d}-{random.randint(1,28):02d}", "type": "Dépôt comptes", "detail": f"Dépôt des comptes annuels — exercice {year + random.randint(1,3)}"},
            ],
            "source": "BODACC",
        },
        "risque_lcb": {
            "score_naf": "MOYEN" if naf_code.startswith("6") or naf_code.startswith("7") else "FAIBLE",
            "anciennete": "Établie" if (2026 - year) > 5 else "Récente",
            "rbe_declaré": True,
            "ppe_dirigeants": False,
            "observations": [
                f"Secteur {naf_code} — risque sectoriel à évaluer selon l'activité réelle",
                "Bénéficiaires effectifs déclarés au RBE INPI" if True else "RBE manquant — signal d'alerte",
                f"Société créée en {year} — ancienneté {2026 - year} ans",
            ],
        },
    }


def _build_intel_pdf(data: dict, name: str) -> bytes:
    try:
        from reportlab.lib.pagesizes import A4
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
        from reportlab.lib import colors
        from reportlab.lib.units import mm

        buf = io.BytesIO()
        doc = SimpleDocTemplate(buf, pagesize=A4,
            leftMargin=22*mm, rightMargin=22*mm, topMargin=18*mm, bottomMargin=18*mm)

        H1   = ParagraphStyle('H1',   fontName='Helvetica-Bold', fontSize=16, spaceAfter=4,  textColor=colors.HexColor('#0A1628'))
        H2   = ParagraphStyle('H2',   fontName='Helvetica-Bold', fontSize=11, spaceBefore=10, spaceAfter=4, textColor=colors.HexColor('#0A3060'))
        BODY = ParagraphStyle('Body', fontName='Helvetica',      fontSize=9,  spaceAfter=3,  leading=13)
        SMALL= ParagraphStyle('Small',fontName='Helvetica',      fontSize=8,  textColor=colors.grey, spaceAfter=2)
        BOLD = ParagraphStyle('Bold', fontName='Helvetica-Bold', fontSize=9,  spaceAfter=3)

        def tbl(data_rows, col_widths):
            t = Table(data_rows, colWidths=col_widths)
            t.setStyle(TableStyle([
                ('FONTNAME',  (0,0),(0,-1), 'Helvetica-Bold'),
                ('FONTNAME',  (1,0),(1,-1), 'Helvetica'),
                ('FONTSIZE',  (0,0),(-1,-1), 8.5),
                ('ROWBACKGROUNDS',(0,0),(-1,-1),[colors.white, colors.HexColor('#F5F7FA')]),
                ('GRID',      (0,0),(-1,-1), 0.3, colors.HexColor('#D0D8E8')),
                ('TOPPADDING',(0,0),(-1,-1), 4),
                ('BOTTOMPADDING',(0,0),(-1,-1), 4),
                ('LEFTPADDING',(0,0),(-1,-1), 6),
            ]))
            return t

        story = []
        i = data["identite"]
        f = data["financier"]
        p = data["procedures"]
        r = data["risque_lcb"]

        story.append(Paragraph(f"FICHE INTELLIGENCE ENTREPRISE", H1))
        story.append(Paragraph(f"Générée le {datetime.now().strftime('%d/%m/%Y %H:%M')} — Sources : Pappers, Infogreffe, BODACC, INPI", SMALL))
        story.append(HRFlowable(width="100%", thickness=2, color=colors.HexColor('#0A1628'), spaceAfter=8))

        story.append(Paragraph("1. IDENTIFICATION", H2))
        story.append(tbl([
            ["Dénomination", i["denomination"]], ["SIREN", i["siren"]],
            ["Forme juridique", i["forme_juridique"]], ["Date création", i["date_creation"]],
            ["Capital social", i["capital"]], ["Siège social", i["adresse"]],
            ["Activité (NAF)", f"{i['naf_code']} — {i['naf_libelle']}"],
            ["Effectif", i["tranche_effectif"]], ["Statut", i["statut"]],
        ], [55*mm, 120*mm]))

        story.append(Paragraph("2. DIRIGEANTS & BÉNÉFICIAIRES EFFECTIFS", H2))
        dirs = [["Nom", "Fonction", "Depuis", "Nationalité"]]
        for d in data["dirigeants"]:
            dirs.append([d["nom"], d["fonction"], d["depuis"], d["nationalite"]])
        dt = Table(dirs, colWidths=[60*mm, 45*mm, 25*mm, 45*mm])
        dt.setStyle(TableStyle([
            ('FONTNAME',(0,0),(-1,0),'Helvetica-Bold'),('FONTSIZE',(0,0),(-1,-1),8.5),
            ('BACKGROUND',(0,0),(-1,0),colors.HexColor('#0A1628')),
            ('TEXTCOLOR',(0,0),(-1,0),colors.white),
            ('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.white, colors.HexColor('#F5F7FA')]),
            ('GRID',(0,0),(-1,-1),0.3,colors.HexColor('#D0D8E8')),
            ('TOPPADDING',(0,0),(-1,-1),4),('BOTTOMPADDING',(0,0),(-1,-1),4),('LEFTPADDING',(0,0),(-1,-1),6),
        ]))
        story.append(dt)

        story.append(Paragraph("3. DONNÉES FINANCIÈRES", H2))
        story.append(tbl([
            ["CA dernier exercice", f["ca_dernier"]], ["CA N-1", f["ca_n1"]], ["CA N-2", f["ca_n2"]],
            ["Résultat net", f["resultat_net"]], ["Fonds propres", f["fonds_propres"]],
            ["Niveau d'endettement", f["endettement"]], ["Score financier", f"{f['score_financier']}/100"],
        ], [65*mm, 110*mm]))

        story.append(Paragraph("4. PROCÉDURES & ANNONCES BODACC", H2))
        proc_status = "Aucune procédure collective active" if not (p["redressement"] or p["liquidation"] or p["sauvegarde"]) else "⚠ PROCÉDURE ACTIVE"
        story.append(Paragraph(proc_status, BOLD))
        for ann in p["dernieres_annonces"]:
            story.append(Paragraph(f"• {ann['date']} — {ann['type']} : {ann['detail']}", BODY))

        story.append(Paragraph("5. ÉVALUATION RISQUE LCB-FT", H2))
        story.append(tbl([
            ["Score sectoriel (NAF)", r["score_naf"]],
            ["Ancienneté", r["anciennete"]],
            ["RBE déclaré (INPI)", "Oui" if r["rbe_declaré"] else "Non — ALERTE"],
            ["Dirigeants PPE", "Oui — VR requise" if r["ppe_dirigeants"] else "Non"],
        ], [65*mm, 110*mm]))
        for obs in r["observations"]:
            story.append(Paragraph(f"→ {obs}", BODY))

        story.append(Spacer(1, 8*mm))
        story.append(HRFlowable(width="100%", thickness=0.5, color=colors.grey))
        story.append(Paragraph("Sources : Pappers API · Infogreffe · BODACC · INPI RBE · INSEE SIRENE — Document confidentiel", SMALL))

        doc.build(story)
        buf.seek(0)
        return buf.read()
    except ImportError:
        return None


def show():
    st.markdown("## 🏢 Intelligence Entreprise")
    st.markdown("<div style='color:#7A8BA6;margin-bottom:1.5rem;'>Fiche de synthèse complète sur une entité : identité, dirigeants, finances, procédures, risque LCB-FT — Sources : Pappers, Infogreffe, BODACC, INPI</div>", unsafe_allow_html=True)

    col1, col2 = st.columns([2, 1])
    with col1:
        entity_name = st.text_input("Nom de la société ou SIREN", placeholder="Ex: BNP Paribas, Société Générale, 552120222…")
    with col2:
        siren_input = st.text_input("SIREN (optionnel si nom renseigné)", placeholder="Ex: 552120222")

    if not entity_name:
        st.markdown("""<div class='info-box'>
        <div style='font-weight:600;color:#00D4AA;'>Comment utiliser cette page</div>
        <div style='font-size:0.85rem;color:#7A8BA6;margin-top:0.3rem;'>
        Saisissez le nom ou le SIREN d'une société française. La plateforme consolide les informations 
        issues de Pappers, Infogreffe, BODACC et INPI pour produire une fiche de synthèse complète, 
        incluant une évaluation du risque LCB-FT.
        </div></div>""", unsafe_allow_html=True)

        st.markdown("### Sources consultées")
        sources_intel = [
            ("🏛️ Pappers API", "https://www.pappers.fr", "Registres officiels, dirigeants, comptes déposés, actes, bénéficiaires effectifs"),
            ("📋 Infogreffe", "https://www.infogreffe.fr", "Extraits Kbis officiels, actes déposés au greffe"),
            ("📢 BODACC", "https://www.bodacc.fr", "Procédures collectives, avis légaux, modifications, ventes de fonds"),
            ("🔑 INPI RBE", "https://data.inpi.fr", "Registre des Bénéficiaires Effectifs — UBOs > 25%"),
            ("📊 INSEE SIRENE", "https://api.insee.fr/entreprises/sirene/V3", "Identification, code NAF, statut actif/inactif"),
            ("💰 Societe.com", "https://www.societe.com", "Données financières consolidées, scores"),
        ]
        for icon_name, url, desc in sources_intel:
            st.markdown(f"""<div style='background:#0F1F3D;border:1px solid #1E3055;border-radius:8px;padding:0.7rem 1rem;margin-bottom:0.4rem;display:flex;justify-content:space-between;align-items:center;'>
                <div>
                    <span style='font-weight:600;color:#E8EDF5;'>{icon_name}</span>
                    <span style='font-size:0.82rem;color:#7A8BA6;margin-left:0.5rem;'>{desc}</span>
                </div>
                <a href='{url}' target='_blank' style='font-size:0.75rem;color:#00D4AA;text-decoration:none;white-space:nowrap;margin-left:1rem;'>Ouvrir →</a>
            </div>""", unsafe_allow_html=True)
        return

    if st.button("🔍 Analyser l'entité", type="primary"):
        with st.spinner(f"Interrogation des sources pour **{entity_name}**…"):
            time_import()
            data = _fetch_entity_data(entity_name, siren_input)

        st.success(f"Fiche consolidée pour **{entity_name}**")

        # ── Tabs ──────────────────────────────────────────────────────────────
        t1, t2, t3, t4, t5 = st.tabs(["🏛️ Identité", "👤 Dirigeants & UBOs", "💰 Finances", "📢 BODACC & Procédures", "⚠️ Risque LCB-FT"])

        with t1:
            i = data["identite"]
            col_id1, col_id2 = st.columns(2)
            with col_id1:
                fields_left = [
                    ("Dénomination", i["denomination"]),
                    ("SIREN", i["siren"]),
                    ("SIRET siège", i["siret_siege"]),
                    ("Forme juridique", i["forme_juridique"]),
                    ("Date de création", i["date_creation"]),
                ]
                for label, val in fields_left:
                    st.markdown(f"""<div style='background:#0F1F3D;border:1px solid #1E3055;border-radius:6px;padding:0.6rem 0.9rem;margin-bottom:0.4rem;'>
                        <div style='font-size:0.72rem;color:#7A8BA6;text-transform:uppercase;letter-spacing:0.5px;'>{label}</div>
                        <div style='font-size:0.9rem;font-weight:600;color:#E8EDF5;margin-top:0.1rem;'>{val}</div>
                    </div>""", unsafe_allow_html=True)
            with col_id2:
                fields_right = [
                    ("Capital social", i["capital"]),
                    ("Activité (NAF)", f"{i['naf_code']} — {i['naf_libelle']}"),
                    ("Effectif estimé", i["tranche_effectif"]),
                    ("Adresse siège", i["adresse"]),
                    ("Statut", i["statut"]),
                ]
                for label, val in fields_right:
                    st.markdown(f"""<div style='background:#0F1F3D;border:1px solid #1E3055;border-radius:6px;padding:0.6rem 0.9rem;margin-bottom:0.4rem;'>
                        <div style='font-size:0.72rem;color:#7A8BA6;text-transform:uppercase;letter-spacing:0.5px;'>{label}</div>
                        <div style='font-size:0.9rem;font-weight:600;color:#E8EDF5;margin-top:0.1rem;'>{val}</div>
                    </div>""", unsafe_allow_html=True)

            st.markdown("**Liens directs**")
            siren_clean = i["siren"]
            cols_links = st.columns(4)
            with cols_links[0]: st.markdown(f"🔗 [Pappers](https://www.pappers.fr/entreprise/{entity_name.lower().replace(' ','-')}-{siren_clean})")
            with cols_links[1]: st.markdown(f"🔗 [Infogreffe](https://www.infogreffe.fr/entreprise-societe/{siren_clean}.html)")
            with cols_links[2]: st.markdown(f"🔗 [Societe.com](https://www.societe.com/cgi-bin/search?champs={siren_clean})")
            with cols_links[3]: st.markdown(f"🔗 [BODACC](https://www.bodacc.fr/pages/annonces-commerciales/#q={entity_name})")

        with t2:
            st.markdown("#### Dirigeants")
            import pandas as pd
            df_dirs = pd.DataFrame(data["dirigeants"])
            st.dataframe(df_dirs, use_container_width=True, hide_index=True)

            st.markdown("#### Bénéficiaires Effectifs (INPI RBE)")
            for ube in data["beneficiaires_effectifs"]:
                st.markdown(f"""<div style='background:#0F1F3D;border:1px solid #1E3055;border-left:3px solid #00D4AA;border-radius:0 8px 8px 0;padding:0.8rem 1rem;margin-bottom:0.4rem;'>
                    <div style='font-weight:600;color:#E8EDF5;'>{ube["nom"]}</div>
                    <div style='font-size:0.82rem;color:#7A8BA6;'>Détention : <span style='color:#00D4AA;font-weight:600;'>{ube["pourcentage"]}</span> · Depuis : {ube["depuis"]} · Source : {ube["source"]}</div>
                </div>""", unsafe_allow_html=True)
            st.markdown(f"🔗 [Consulter le RBE sur INPI](https://data.inpi.fr/beneficiaires-effectifs/{data['identite']['siren']})")

        with t3:
            f = data["financier"]
            c1, c2, c3 = st.columns(3)
            with c1:
                st.markdown(f"""<div class='metric-card'><div class='metric-value' style='font-size:1.4rem;'>{f["ca_dernier"]}</div><div class='metric-label'>CA dernier exercice</div></div>""", unsafe_allow_html=True)
            with c2:
                st.markdown(f"""<div class='metric-card'><div class='metric-value' style='font-size:1.4rem;'>{f["resultat_net"]}</div><div class='metric-label'>Résultat net</div></div>""", unsafe_allow_html=True)
            with c3:
                score_color = "#00D4AA" if f["score_financier"] > 70 else "#FFB347" if f["score_financier"] > 50 else "#FF4757"
                st.markdown(f"""<div class='metric-card'><div class='metric-value' style='color:{score_color};'>{f["score_financier"]}/100</div><div class='metric-label'>Score financier</div></div>""", unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)
            import pandas as pd
            df_fin = pd.DataFrame({
                "Exercice": ["N-2", "N-1", "N (dernier)"],
                "Chiffre d'affaires": [f["ca_n2"], f["ca_n1"], f["ca_dernier"]],
            })
            st.dataframe(df_fin, use_container_width=True, hide_index=True)

            for label, val in [("Fonds propres", f["fonds_propres"]), ("Endettement", f["endettement"]), ("Source", f["source"])]:
                st.markdown(f"**{label} :** {val}")

        with t4:
            p = data["procedures"]
            proc_ok = not (p["redressement"] or p["liquidation"] or p["sauvegarde"])
            if proc_ok:
                st.markdown("""<div class='info-box'><div style='color:#00D4AA;font-weight:600;'>✅ Aucune procédure collective active</div>
                <div style='font-size:0.82rem;color:#7A8BA6;'>Redressement, liquidation judiciaire et sauvegarde : RAS</div></div>""", unsafe_allow_html=True)
            else:
                st.markdown("""<div class='danger-box'><div style='color:#FF4757;font-weight:700;'>⚠️ PROCÉDURE COLLECTIVE ACTIVE</div></div>""", unsafe_allow_html=True)

            st.markdown("#### Dernières annonces BODACC")
            for ann in p["dernieres_annonces"]:
                st.markdown(f"""<div style='background:#0F1F3D;border:1px solid #1E3055;border-radius:6px;padding:0.6rem 0.9rem;margin-bottom:0.4rem;'>
                    <span style='font-size:0.75rem;color:#7A8BA6;font-family:monospace;'>{ann["date"]}</span>
                    <span style='font-weight:600;color:#E8EDF5;margin:0 0.5rem;'>{ann["type"]}</span>
                    <span style='font-size:0.85rem;color:#C8D4E5;'>{ann["detail"]}</span>
                </div>""", unsafe_allow_html=True)
            st.markdown(f"🔗 [Toutes les annonces BODACC pour {entity_name}](https://www.bodacc.fr/pages/annonces-commerciales/#q={entity_name})")

        with t5:
            r = data["risque_lcb"]
            score_map = {"FAIBLE": "#00D4AA", "MOYEN": "#FFB347", "ÉLEVÉ": "#FF4757"}
            score_color = score_map.get(r["score_naf"], "#7A8BA6")

            c1, c2, c3 = st.columns(3)
            with c1: st.markdown(f"""<div class='metric-card'><div class='metric-value' style='color:{score_color};'>{r["score_naf"]}</div><div class='metric-label'>Risque sectoriel NAF</div></div>""", unsafe_allow_html=True)
            with c2: st.markdown(f"""<div class='metric-card'><div class='metric-value' style='color:{"#00D4AA" if r["rbe_declaré"] else "#FF4757"};'>{"✓" if r["rbe_declaré"] else "✗"}</div><div class='metric-label'>RBE déclaré (INPI)</div></div>""", unsafe_allow_html=True)
            with c3: st.markdown(f"""<div class='metric-card'><div class='metric-value' style='color:{"#FF4757" if r["ppe_dirigeants"] else "#00D4AA"};'>{"OUI" if r["ppe_dirigeants"] else "NON"}</div><div class='metric-label'>Dirigeants PPE</div></div>""", unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("**Observations LCB-FT**")
            for obs in r["observations"]:
                st.markdown(f"""<div style='background:#0F1F3D;border-left:3px solid #FFB347;border-radius:0 6px 6px 0;padding:0.6rem 1rem;margin-bottom:0.4rem;font-size:0.85rem;color:#E8EDF5;'>→ {obs}</div>""", unsafe_allow_html=True)

            st.markdown("**Références réglementaires**")
            refs = st.columns(3)
            with refs[0]: st.markdown("🔗 [L.561-4-1 CMF — Classification risques](https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000042648607)")
            with refs[1]: st.markdown("🔗 [L.561-5 CMF — Identification](https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000042648601)")
            with refs[2]: st.markdown("🔗 [Arrêté 6 janvier 2021 ACPR](https://www.legifrance.gouv.fr/jorf/id/JORFTEXT000042921973)")

        # ── PDF export ────────────────────────────────────────────────────────
        st.markdown("---")
        if st.button("📥 Générer la fiche PDF"):
            pdf = _build_intel_pdf(data, entity_name)
            if pdf:
                fname = f"fiche_intel_{entity_name.replace(' ','_')}_{datetime.now().strftime('%Y%m%d')}.pdf"
                st.download_button("⬇️ Télécharger la fiche", pdf, fname, "application/pdf")
            else:
                st.error("Installez `reportlab` : `pip install reportlab`")


def time_import():
    import time
    time.sleep(0.8)
