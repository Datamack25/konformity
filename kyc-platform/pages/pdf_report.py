import streamlit as st
import io
from datetime import datetime

def show():
    st.markdown("## 📄 Générateur de rapports KYC")
    st.markdown("<div style='color: #7A8BA6; margin-bottom: 1.5rem;'>Produire une note d'escalade ou une fiche KYC au format PDF — prêt pour signature conformité</div>", unsafe_allow_html=True)

    tab1, tab2 = st.tabs(["📝 Saisie du dossier", "👁️ Aperçu & Téléchargement"])

    with tab1:
        st.markdown("### Informations société")
        col1, col2 = st.columns(2)
        with col1:
            nom_societe = st.text_input("Raison sociale *", value="Étoile Conseil SAS")
            siren = st.text_input("SIREN *", value="123456789")
            forme = st.selectbox("Forme juridique", ["SAS", "SARL", "SA", "SCI", "GIE"])
            capital = st.text_input("Capital social", value="10 000 €")
        with col2:
            adresse = st.text_input("Adresse siège", value="24 rue de la Paix, 75002 Paris")
            naf = st.text_input("Code NAF / Activité", value="7022Z — Conseil pour les affaires et autres conseils")
            date_creation = st.date_input("Date de création")
            analyste = st.text_input("Analyste KYC", value="M. Dupont")

        st.markdown("### Dirigeants et bénéficiaires effectifs")
        col3, col4 = st.columns(2)
        with col3:
            dirigeant1 = st.text_input("Dirigeant 1 — Nom & Fonction", value="Hélène Müller — Présidente (60%)")
        with col4:
            dirigeant2 = st.text_input("Dirigeant 2 — Nom & Fonction", value="François Dubois — DG (40%)")

        st.markdown("### Résultats du screening")
        col5, col6 = st.columns(2)
        with col5:
            screening_societe = st.selectbox("Screening société", ["✅ Clear — Aucun hit", "⚠️ Hit potentiel — À qualifier", "🔴 Hit confirmé"])
            screening_dirigeants = st.selectbox("Screening dirigeants", ["✅ Clear — Aucun hit", "⚠️ Hit potentiel — À qualifier", "🔴 Hit confirmé"])
        with col6:
            ppe_check = st.selectbox("Statut PPE", ["Non-PPE vérifié", "PPE déclaré — VR appliquée", "À vérifier"])
            adverse_media = st.selectbox("Adverse media", ["✅ Aucun résultat négatif", "⚠️ Résultats à qualifier", "🔴 Adverse media significatif"])

        st.markdown("### Checklist documentaire")
        docs = {
            "Extrait Kbis (< 3 mois)": st.checkbox("Kbis reçu", value=True),
            "Registre des Bénéficiaires Effectifs": st.checkbox("RBE reçu"),
            "Statuts à jour": st.checkbox("Statuts reçus"),
            "Pièce d'identité dirigeant(s)": st.checkbox("CNI/Passeport reçu", value=True),
            "Justificatif d'origine des fonds": st.checkbox("Justificatif origine reçu"),
            "Justificatif domicile personne morale": st.checkbox("Justificatif domicile reçu", value=True),
        }

        st.markdown("### Scoring et disposition")
        col7, col8 = st.columns(2)
        with col7:
            score = st.select_slider("Score de risque global", ["FAIBLE", "MOYEN", "ÉLEVÉ"], value="MOYEN")
            regime = st.selectbox("Régime de vigilance", ["Vigilance standard (L.561-8 CMF)", "Vigilance renforcée (L.561-10 CMF)", "Vigilance allégée (L.561-9 CMF)"])
        with col8:
            disposition = st.selectbox("Disposition", [
                "VALIDATION — Entrée en relation autorisée",
                "DEMANDE DE COMPLÉMENTS — Dossier incomplet",
                "ESCALADE — Examen renforcé requis",
                "REFUS — Entrée en relation refusée"
            ])
            tracfin = st.checkbox("Évaluer opportunité déclaration TRACFIN")

        motifs = st.text_area("Motifs et observations", value="Screening sanctions négatif. Bénéficiaires effectifs non déclarés au RBE. Origine des fonds non justifiée pour les montants envisagés. Examen complémentaire requis avant validation.")

        st.session_state['report_data'] = {
            'nom_societe': nom_societe, 'siren': siren, 'forme': forme, 'capital': capital,
            'adresse': adresse, 'naf': naf, 'date_creation': str(date_creation), 'analyste': analyste,
            'dirigeant1': dirigeant1, 'dirigeant2': dirigeant2,
            'screening_societe': screening_societe, 'screening_dirigeants': screening_dirigeants,
            'ppe_check': ppe_check, 'adverse_media': adverse_media,
            'docs': docs, 'score': score, 'regime': regime,
            'disposition': disposition, 'tracfin': tracfin, 'motifs': motifs,
        }

    with tab2:
        if 'report_data' not in st.session_state:
            st.info("Remplissez d'abord le formulaire dans l'onglet 'Saisie du dossier'")
            return

        d = st.session_state['report_data']
        score_color = {"FAIBLE": "#00D4AA", "MOYEN": "#FFB347", "ÉLEVÉ": "#FF4757"}.get(d['score'], "#7A8BA6")
        disp_color = "#FF4757" if "REFUS" in d['disposition'] or "ESCALADE" in d['disposition'] else "#FFB347" if "COMPLÉMENTS" in d['disposition'] else "#00D4AA"

        # Preview
        st.markdown(f"""
        <div style='background: white; color: #1a1a1a; border-radius: 12px; padding: 2rem; font-family: Georgia, serif; max-width: 800px; margin: 0 auto;'>
            <div style='border-bottom: 3px solid #0A1628; padding-bottom: 1rem; margin-bottom: 1.5rem;'>
                <div style='font-size: 1.4rem; font-weight: 700; color: #0A1628;'>NOTE D'ESCALADE KYC</div>
                <div style='font-size: 0.85rem; color: #666; margin-top: 0.3rem;'>CONFIDENTIEL — Dossier de conformité LCB-FT</div>
                <div style='font-size: 0.8rem; color: #888; margin-top: 0.2rem;'>Généré le {datetime.now().strftime('%d/%m/%Y à %H:%M')} · Analyste : {d['analyste']}</div>
            </div>
            
            <div style='background: #f8f9fa; border-left: 4px solid {disp_color}; padding: 1rem; margin-bottom: 1.5rem; border-radius: 0 8px 8px 0;'>
                <div style='font-size: 1.1rem; font-weight: 700; color: #0A1628;'>DISPOSITION : {d['disposition']}</div>
                <div style='font-size: 0.85rem; color: #444; margin-top: 0.3rem;'>Score de risque : <strong style='color: {score_color};'>{d['score']}</strong> · {d['regime']}</div>
            </div>
            
            <div style='margin-bottom: 1.5rem;'>
                <div style='font-size: 1rem; font-weight: 700; color: #0A1628; border-bottom: 1px solid #e0e0e0; padding-bottom: 0.3rem; margin-bottom: 0.8rem;'>1. IDENTIFICATION</div>
                <table style='width: 100%; border-collapse: collapse; font-size: 0.85rem;'>
                    <tr><td style='padding: 4px 8px; color: #666; width: 40%;'>Raison sociale</td><td style='padding: 4px 8px; font-weight: 600;'>{d['nom_societe']}</td></tr>
                    <tr style='background: #f8f9fa;'><td style='padding: 4px 8px; color: #666;'>SIREN</td><td style='padding: 4px 8px; font-family: monospace;'>{d['siren']}</td></tr>
                    <tr><td style='padding: 4px 8px; color: #666;'>Forme juridique</td><td style='padding: 4px 8px;'>{d['forme']}</td></tr>
                    <tr style='background: #f8f9fa;'><td style='padding: 4px 8px; color: #666;'>Capital social</td><td style='padding: 4px 8px;'>{d['capital']}</td></tr>
                    <tr><td style='padding: 4px 8px; color: #666;'>Siège social</td><td style='padding: 4px 8px;'>{d['adresse']}</td></tr>
                    <tr style='background: #f8f9fa;'><td style='padding: 4px 8px; color: #666;'>Activité (NAF)</td><td style='padding: 4px 8px;'>{d['naf']}</td></tr>
                </table>
            </div>
            
            <div style='margin-bottom: 1.5rem;'>
                <div style='font-size: 1rem; font-weight: 700; color: #0A1628; border-bottom: 1px solid #e0e0e0; padding-bottom: 0.3rem; margin-bottom: 0.8rem;'>2. DIRIGEANTS & BÉNÉFICIAIRES EFFECTIFS</div>
                <div style='font-size: 0.85rem; color: #333;'>{d['dirigeant1']}</div>
                <div style='font-size: 0.85rem; color: #333; margin-top: 0.3rem;'>{d['dirigeant2']}</div>
            </div>
            
            <div style='margin-bottom: 1.5rem;'>
                <div style='font-size: 1rem; font-weight: 700; color: #0A1628; border-bottom: 1px solid #e0e0e0; padding-bottom: 0.3rem; margin-bottom: 0.8rem;'>3. RÉSULTATS SCREENING</div>
                <div style='font-size: 0.85rem; color: #333;'>Société : {d['screening_societe']}</div>
                <div style='font-size: 0.85rem; color: #333; margin-top: 0.3rem;'>Dirigeants : {d['screening_dirigeants']}</div>
                <div style='font-size: 0.85rem; color: #333; margin-top: 0.3rem;'>PPE : {d['ppe_check']}</div>
                <div style='font-size: 0.85rem; color: #333; margin-top: 0.3rem;'>Adverse media : {d['adverse_media']}</div>
            </div>
            
            <div style='margin-bottom: 1.5rem;'>
                <div style='font-size: 1rem; font-weight: 700; color: #0A1628; border-bottom: 1px solid #e0e0e0; padding-bottom: 0.3rem; margin-bottom: 0.8rem;'>4. CHECKLIST DOCUMENTAIRE</div>
                {"".join([f'<div style="font-size: 0.85rem; color: #333; margin-bottom: 0.3rem;">{"✓" if checked else "✗"} {doc}</div>' for doc, checked in d['docs'].items()])}
            </div>
            
            <div style='margin-bottom: 1.5rem;'>
                <div style='font-size: 1rem; font-weight: 700; color: #0A1628; border-bottom: 1px solid #e0e0e0; padding-bottom: 0.3rem; margin-bottom: 0.8rem;'>5. MOTIFS & OBSERVATIONS</div>
                <div style='font-size: 0.85rem; color: #333; line-height: 1.7;'>{d['motifs']}</div>
                {"<div style='margin-top: 0.8rem; font-size: 0.85rem; color: #d32f2f; font-weight: 600;'>⚠️ Déclaration TRACFIN (L.561-15 CMF) : à évaluer par le responsable conformité et le déclarant désigné.</div>" if d['tracfin'] else ""}
            </div>
            
            <div style='border-top: 1px solid #e0e0e0; padding-top: 1rem; margin-top: 2rem; font-size: 0.75rem; color: #888;'>
                Base légale : L.561-1 et suivants CMF · Arrêté 6 janvier 2021 · Lignes directrices ACPR<br>
                Document confidentiel — Usage interne conformité uniquement
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        if st.button("📥 Générer le PDF"):
            try:
                from reportlab.lib.pagesizes import A4
                from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
                from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
                from reportlab.lib import colors
                from reportlab.lib.units import mm

                buffer = io.BytesIO()
                doc = SimpleDocTemplate(buffer, pagesize=A4,
                    leftMargin=25*mm, rightMargin=25*mm, topMargin=20*mm, bottomMargin=20*mm)

                styles = getSampleStyleSheet()
                story = []

                title_style = ParagraphStyle('Title', fontName='Helvetica-Bold', fontSize=16, spaceAfter=4)
                sub_style = ParagraphStyle('Sub', fontName='Helvetica', fontSize=9, textColor=colors.grey, spaceAfter=12)
                section_style = ParagraphStyle('Section', fontName='Helvetica-Bold', fontSize=11, spaceBefore=12, spaceAfter=6)
                body_style = ParagraphStyle('Body', fontName='Helvetica', fontSize=9.5, spaceAfter=4, leading=14)

                story.append(Paragraph("NOTE D'ESCALADE KYC — CONFIDENTIEL", title_style))
                story.append(Paragraph(f"Généré le {datetime.now().strftime('%d/%m/%Y à %H:%M')} · Analyste : {d['analyste']}", sub_style))

                disp_color_rl = colors.HexColor("#D32F2F") if "REFUS" in d['disposition'] or "ESCALADE" in d['disposition'] else colors.HexColor("#F57C00") if "COMPLÉMENTS" in d['disposition'] else colors.HexColor("#2E7D32")
                story.append(Paragraph(f"DISPOSITION : {d['disposition']}", ParagraphStyle('Disp', fontName='Helvetica-Bold', fontSize=12, textColor=disp_color_rl, spaceAfter=4)))
                story.append(Paragraph(f"Score de risque : {d['score']} · {d['regime']}", body_style))
                story.append(Spacer(1, 6*mm))

                story.append(Paragraph("1. IDENTIFICATION", section_style))
                table_data = [
                    ["Raison sociale", d['nom_societe']],
                    ["SIREN", d['siren']],
                    ["Forme juridique", d['forme']],
                    ["Capital social", d['capital']],
                    ["Siège social", d['adresse']],
                    ["Activité (NAF)", d['naf']],
                ]
                t = Table(table_data, colWidths=[55*mm, 120*mm])
                t.setStyle(TableStyle([
                    ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
                    ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
                    ('FONTSIZE', (0, 0), (-1, -1), 9),
                    ('ROWBACKGROUNDS', (0, 0), (-1, -1), [colors.white, colors.HexColor('#F5F5F5')]),
                    ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#E0E0E0')),
                    ('TOPPADDING', (0, 0), (-1, -1), 4),
                    ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
                    ('LEFTPADDING', (0, 0), (-1, -1), 6),
                ]))
                story.append(t)

                story.append(Paragraph("2. MOTIFS & OBSERVATIONS", section_style))
                story.append(Paragraph(d['motifs'], body_style))
                if d['tracfin']:
                    story.append(Spacer(1, 3*mm))
                    story.append(Paragraph("⚠ Déclaration TRACFIN (L.561-15 CMF) : à évaluer par le responsable conformité.", ParagraphStyle('Warning', fontName='Helvetica-Bold', fontSize=9.5, textColor=colors.HexColor('#D32F2F'))))

                story.append(Spacer(1, 8*mm))
                story.append(Paragraph("Base légale : L.561-1 et suivants CMF · Arrêté 6 janvier 2021 · Lignes directrices ACPR", ParagraphStyle('Footer', fontName='Helvetica', fontSize=8, textColor=colors.grey)))

                doc.build(story)
                buffer.seek(0)

                st.download_button(
                    label="⬇️ Télécharger le PDF",
                    data=buffer,
                    file_name=f"note_kyc_{d['nom_societe'].replace(' ', '_')}_{datetime.now().strftime('%Y%m%d')}.pdf",
                    mime="application/pdf"
                )
                st.success("PDF généré avec succès !")
            except ImportError:
                st.error("Installez reportlab : `pip install reportlab`")
                st.info("En attendant, vous pouvez imprimer l'aperçu ci-dessus depuis votre navigateur (Ctrl+P).")
