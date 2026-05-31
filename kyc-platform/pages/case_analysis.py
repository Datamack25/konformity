import streamlit as st

CASES = {
    "🏢 Onboarding société standard": {
        "desc": "Entrée en relation avec une SAS/SARL française, activité standard, dirigeants résidents français.",
        "risk_factors": [
            "Secteur d'activité (code NAF) — certains secteurs surexposés",
            "Ancienneté de la société (< 6 mois = signal d'alerte)",
            "Cohérence capital social vs activité déclarée",
            "Présence/absence déclaration RBE INPI",
            "Procédures collectives ou incidents BODACC",
        ],
        "documents": [
            "Extrait Kbis de moins de 3 mois",
            "Extrait RBE (INPI)",
            "Statuts à jour",
            "CNI/Passeport dirigeants + UBOs > 25%",
            "Justificatif domicile personne morale",
            "Justificatif origine des fonds (si > 10 000€)",
        ],
        "checks": [
            "1. Vérifier cohérence SIREN / Pappers / Kbis fourni",
            "2. Identifier tous les UBOs > 25% via RBE + Pappers",
            "3. Screening sanctions ONU/UE/OFAC sur société ET dirigeants",
            "4. Screening PPE sur dirigeants et UBOs",
            "5. Adverse media screening (derniers 24 mois)",
            "6. Vérifier absence procédures collectives (BODACC)",
            "7. Cohérence activité déclarée vs mouvements attendus",
            "8. Identifier toute structure d'actionnariat intermédiaire (holdings)",
        ],
        "red_flags": [
            "🔴 Capital social symbolique (1€) pour activité à fort CA attendu",
            "🔴 Dirigeant ou UBO absent du RBE",
            "🔴 Adresse siège = domicile particulier sans justification",
            "🔴 Changement récent de dirigeant sans explication",
            "🔴 Société créée < 3 mois pour une opération significative",
            "🟡 Actionnaire intermédiaire dans pays à fiscalité privilégiée",
            "🟡 Objet social très large, non distinctif",
        ],
        "articles": ["L.561-5 CMF (identification)", "L.561-6 CMF (vérification)", "L.561-4-1 CMF (classification risques)"],
        "regime": "Vigilance standard (art. L.561-8 CMF)"
    },
    "👤 Onboarding personne physique": {
        "desc": "Entrée en relation avec un client particulier, opérations bancaires ou financières.",
        "risk_factors": [
            "Nationalité et pays de résidence",
            "Profession et source des revenus",
            "Statut PPE (politique, judiciaire, militaire)",
            "Montants et nature des opérations prévues",
            "Cohérence revenus déclarés / patrimoine",
        ],
        "documents": [
            "CNI/Passeport en cours de validité",
            "Justificatif de domicile < 3 mois",
            "Justificatif de revenus (3 derniers bulletins ou avis imposition)",
            "Déclaration origine des fonds si investissement significatif",
            "Questionnaire PPE signé",
        ],
        "checks": [
            "1. Vérification pièce d'identité (authenticité, validité)",
            "2. Screening sanctions toutes listes sur nom + date naissance",
            "3. Vérification statut PPE (+ entourage proche si déclaré PPE)",
            "4. Adverse media screening",
            "5. Cohérence géographique (pays résidence vs opérations)",
            "6. Vérification domicile (pays tiers à risque = vigilance renforcée)",
        ],
        "red_flags": [
            "🔴 Incohérence entre revenus déclarés et opérations envisagées",
            "🔴 PPE déclaré sans due diligence renforcée",
            "🔴 Pièce d'identité expirée ou suspecte",
            "🔴 Adresse dans pays sous embargo",
            "🟡 Transactions fréquentes juste sous seuils déclaratifs",
            "🟡 Refus de justifier origine des fonds",
            "🟡 Utilisation de multiples comptes ou entités",
        ],
        "articles": ["L.561-5 CMF", "L.561-7 CMF (PPE)", "L.561-10 CMF (vigilance renforcée)"],
        "regime": "Vigilance standard ou renforcée si PPE/pays tiers risqué"
    },
    "⚠️ PPE — Personne Politiquement Exposée": {
        "desc": "Client identifié comme PPE ou membre proche/associé d'une PPE. Régime de vigilance renforcée systématique.",
        "risk_factors": [
            "Niveau de la fonction (national vs local vs international)",
            "Pays de la fonction (régimes à risque élevé de corruption)",
            "Durée depuis la fin de la fonction (règle des 12 mois AMLD5, souplesse AMLD6)",
            "Nature des opérations (immobilier, placements, crédit...)",
            "Composition et localisation du patrimoine",
        ],
        "documents": [
            "Identité PPE ET personnes de l'entourage proche impliquées",
            "Justificatif détaillé origine des fonds et du patrimoine",
            "Déclarations de patrimoine publiques si disponibles",
            "Attestation employeur / mandat électif",
            "Statuts sociétés détenues par la PPE",
        ],
        "checks": [
            "1. Confirmation statut PPE : quelle fonction, quel pays, depuis quand",
            "2. Identification entourage proche (conjoint, enfants, parents, associés proches)",
            "3. Screening étendu : tous membres famille + sociétés liées",
            "4. Adverse media approfondi (presse locale pays fonction)",
            "5. Vérification déclarations de patrimoine publiques",
            "6. Analyse détaillée justificatifs origine des fonds",
            "7. Approbation de la direction avant entrée en relation (exigence AMLD5/6)",
            "8. Surveillance continue renforcée post-entrée en relation",
        ],
        "red_flags": [
            "🔴 Pas de justification plausible des fonds par rapport à la rémunération publique connue",
            "🔴 Interposition de sociétés-écrans pour masquer l'origine des fonds",
            "🔴 PPE de pays à forte corruption (indice CPI < 40)",
            "🔴 Adverse media : soupçons de corruption, procédures judiciaires",
            "🟡 Activité immobilière intense sans justification",
            "🟡 Mandats croisés avec entités privées pendant la fonction",
        ],
        "articles": ["L.561-7 CMF (définition PPE)", "L.561-10 CMF (VR PPE)", "Art. 20 AMLD4"],
        "regime": "Vigilance renforcée systématique (art. L.561-10 CMF)"
    },
    "🌐 Structure offshore / holding complexe": {
        "desc": "Groupe avec entités dans plusieurs juridictions, actionnariat à travers holdings, trusts ou véhicules fiduciaires.",
        "risk_factors": [
            "Présence de juridictions listées GAFI non-coopératives",
            "Imbrication de couches d'actionnariat (> 2-3 couches = signal)",
            "Trusts ou fondations sans transparence des bénéficiaires",
            "Séparation entre bénéficiaire effectif déclaré et contrôle effectif",
            "Pays d'incorporation sans registre public des bénéficiaires",
        ],
        "documents": [
            "Organigramme certifié de la structure complète",
            "Registres de sociétés de chaque entité intermédiaire",
            "Acte de trust / déclaration de fiducie si applicable",
            "Attestation du trustee/fiduciaire identifiant les bénéficiaires",
            "Justificatif de substance économique dans chaque pays",
            "Déclarations fiscales ou attestations de résidence fiscale",
        ],
        "checks": [
            "1. Reconstituer l'intégralité de la chaîne de détention jusqu'aux UBOs personnes physiques",
            "2. Vérifier cohérence organigramme déclaré vs sources officielles (Companies House, EBR...)",
            "3. Identifier chaque pays d'incorporation et évaluer le risque de chaque juridiction (GAFI, EU)",
            "4. Screening sur chaque entité intermédiaire ET chaque UBO",
            "5. Adverse media sur groupe et dirigeants historiques",
            "6. Recherche ICIJ / OCCRP Aleph pour entités offshore",
            "7. Évaluation de la substance économique (employés locaux? activité réelle?)",
            "8. Demande d'explication de la rationale économique de la structure",
        ],
        "red_flags": [
            "🔴 Entité dans liste GAFI pays non-coopératif (Iran, Corée du Nord, Myanmar...)",
            "🔴 UBO déclaré mais contrôle effectif exercé par une autre personne",
            "🔴 Plus de 3 couches d'interposition sans justification économique",
            "🔴 Trust ou fondation discrétionnaire sans liste des bénéficiaires",
            "🔴 Résultats ICIJ / Panama Papers / Pandora Papers sur des entités du groupe",
            "🟡 Holding dans pays à fiscalité privilégiée (Luxembourg, Îles Caïmans...)",
            "🟡 Nominees (prête-noms) comme dirigeants officiels",
        ],
        "articles": ["L.561-5 CMF (UBO)", "L.561-12 CMF (conservation)", "AMLD5 Art.13 (UBO trust)"],
        "regime": "Vigilance renforcée + escalade systématique"
    },
    "💸 Opération suspecte — Signaux typologiques": {
        "desc": "Détection d'opérations ou comportements atypiques sur un client en relation. Évaluation du soupçon TRACFIN.",
        "risk_factors": [
            "Rupture de profil comportemental",
            "Opérations sans justification économique apparente",
            "Structuration (fractionnement pour passer sous seuils)",
            "Rapidité des mouvements (in / out)",
            "Pays d'origine ou de destination à risque",
        ],
        "documents": [
            "Relevés de compte analysés sur période suspecte",
            "Justificatifs demandés pour les opérations atypiques",
            "Dossier KYC initial pour comparaison profil",
            "Échanges client sur les opérations (mail, courrier)",
        ],
        "checks": [
            "1. Identifier précisément l'opération ou le pattern atypique",
            "2. Comparer avec le profil de risque initial et les opérations habituelles",
            "3. Demander justification au client si cohérent avec la relation (sans alerter)",
            "4. Analyser la chaîne de flux : origine et destination des fonds",
            "5. Vérifier si les contreparties apparaissent dans des listes de surveillance",
            "6. Documenter l'analyse et les diligences effectuées",
            "7. Escalader au responsable conformité + déclarant désigné",
            "8. Décider de la déclaration TRACFIN (L.561-15 CMF)",
        ],
        "red_flags": [
            "🔴 Structuration manifeste (plusieurs virements juste sous 10 000€)",
            "🔴 Fonds transitant par pays sous embargo puis entrant",
            "🔴 Refus répété du client de justifier l'origine des fonds",
            "🔴 Opérations sans lien avec l'activité déclarée",
            "🔴 Utilisation intensive d'espèces dans un secteur non-espèces",
            "🟡 Multiplication de bénéficiaires sans lien apparent",
            "🟡 Horaires inhabituels ou urgence injustifiée",
        ],
        "articles": ["L.561-15 CMF (déclaration soupçon)", "L.561-16 CMF (confidentialité)", "Art. R.561-38 CMF"],
        "regime": "Examen renforcé + évaluation déclaration TRACFIN"
    },
    "📈 Abus de marché — Insider trading": {
        "desc": "Détection d'opérations pouvant constituer un délit d'initié ou une manipulation de cours. Périmètre AMF / MAR.",
        "risk_factors": [
            "Proximité temporelle avec annonces réglementées",
            "Profil inhabituel de l'intervenant sur le titre",
            "Accès potentiel à des informations privilégiées (liste d'initiés)",
            "Volume et timing des ordres anormaux",
        ],
        "documents": [
            "Carnet d'ordres sur le titre concerné",
            "Journal des transactions de l'intervenant",
            "Liste d'initiés de l'émetteur (si accès)",
            "Calendrier des annonces réglementées",
            "Communications internes potentiellement liées",
        ],
        "checks": [
            "1. Identifier l'annonce réglementée (résultats, OPA, accord significatif...)",
            "2. Analyser les transactions sur le titre dans les 5 à 30 jours précédant l'annonce",
            "3. Identifier les personnes ayant accès à l'information (liste d'initiés L.621-18-4 CMF)",
            "4. Corréler les transactions suspectes avec les personnes listées",
            "5. Analyser les options et dérivés en plus des actions",
            "6. Vérifier les transactions de l'entourage (famille, associés)",
            "7. Évaluer si seuil STOR atteint : déclaration immédiate à l'AMF",
            "8. Documentation obligatoire même si décision de ne pas déclarer",
        ],
        "red_flags": [
            "🔴 Achat massif inhabituel avant annonce positive",
            "🔴 Vente inhabituelle avant annonce négative (profit warning)",
            "🔴 Intervenant figurant dans la liste d'initiés",
            "🔴 Utilisation d'un compte tiers ou d'un proche",
            "🟡 Changement de profil de trading radical",
            "🟡 Timing suspicieux même si personne non-initiée",
        ],
        "articles": ["MAR (UE 596/2014)", "L.621-14 CMF", "L.465-1 Code pénal", "Art. 16 MAR (STOR)"],
        "regime": "STOR obligatoire si soupçon raisonnable (Art. 16 MAR)"
    },
}

def show():
    st.markdown("## 🗂️ Analyse de cas — Guide méthodologique")
    st.markdown("<div style='color: #7A8BA6; margin-bottom: 1.5rem;'>Comment analyser les différents types de dossiers LCB-FT et abus de marché : signaux d'alerte, documents requis, étapes de vérification</div>", unsafe_allow_html=True)

    case_type = st.selectbox(
        "Sélectionner un type de cas",
        list(CASES.keys()),
        label_visibility="visible"
    )

    case = CASES[case_type]

    st.markdown(f"""<div class='info-box'>
        <div style='font-size: 1rem; font-weight: 600; color: #E8EDF5;'>{case_type}</div>
        <div style='font-size: 0.85rem; color: #7A8BA6; margin-top: 0.3rem;'>{case['desc']}</div>
        <div style='margin-top: 0.8rem;'>
            <span style='font-size: 0.75rem; color: #7A8BA6; margin-right: 0.5rem;'>Base légale :</span>
            {"".join([f"<span class='source-pill'>{a}</span>" for a in case['articles']])}
        </div>
        <div style='margin-top: 0.5rem; font-size: 0.82rem;'>
            <span style='color: #7A8BA6;'>Régime applicable : </span>
            <span style='color: #FFB347; font-weight: 600;'>{case['regime']}</span>
        </div>
    </div>""", unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("<div class='section-title'>📋 Étapes de vérification</div>", unsafe_allow_html=True)
        for step in case['checks']:
            num = step.split('.')[0].strip()
            text = '.'.join(step.split('.')[1:]).strip()
            st.markdown(f"""
            <div style='display: flex; gap: 0.8rem; align-items: flex-start; margin-bottom: 0.7rem;'>
                <div style='background: #00D4AA; color: #0A1628; width: 22px; height: 22px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-weight: 700; font-size: 0.7rem; flex-shrink: 0; margin-top: 1px;'>{num}</div>
                <div style='font-size: 0.85rem; color: #E8EDF5; line-height: 1.5;'>{text}</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("<div class='section-title'>📄 Documents requis</div>", unsafe_allow_html=True)
        for doc in case['documents']:
            st.markdown(f"<div style='font-size: 0.85rem; color: #E8EDF5; margin-bottom: 0.4rem;'>→ {doc}</div>", unsafe_allow_html=True)

    with col2:
        st.markdown("<div class='section-title'>⚠️ Facteurs de risque clés</div>", unsafe_allow_html=True)
        for factor in case['risk_factors']:
            st.markdown(f"""<div style='background: rgba(255,179,71,0.06); border: 1px solid rgba(255,179,71,0.15); border-radius: 6px; padding: 0.6rem 0.9rem; margin-bottom: 0.4rem; font-size: 0.85rem; color: #E8EDF5;'>
                <span style='color: #FFB347;'>◆</span> {factor}</div>""", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("<div class='section-title'>🚩 Signaux d'alerte (Red Flags)</div>", unsafe_allow_html=True)
        for flag in case['red_flags']:
            is_red = flag.startswith("🔴")
            color = "#FF4757" if is_red else "#FFB347"
            bg = "rgba(255,71,87,0.08)" if is_red else "rgba(255,179,71,0.08)"
            border = "rgba(255,71,87,0.25)" if is_red else "rgba(255,179,71,0.25)"
            st.markdown(f"""<div style='background: {bg}; border: 1px solid {border}; border-radius: 6px; padding: 0.6rem 0.9rem; margin-bottom: 0.4rem; font-size: 0.85rem; color: #E8EDF5;'>
                {flag}</div>""", unsafe_allow_html=True)

    # Decision tree
    st.markdown("---")
    st.markdown("<div class='section-title'>🌳 Arbre de décision</div>", unsafe_allow_html=True)

    col_tree1, col_tree2, col_tree3 = st.columns(3)
    scenarios = [
        ("Dossier complet\nAucun red flag\nScreening négatif", "🟢 VALIDATION\nVigilance standard\nSurveillance continue", "#00D4AA"),
        ("Dossier incomplet\nOu red flags mineurs\nOu hits potentiels", "🟡 ESCALADE\nDemande compléments\nExamen renforcé", "#FFB347"),
        ("Red flags majeurs\nHit confirmé\nIncohérences graves", "🔴 REFUS ou TRACFIN\nEntée en relation refusée\nOu déclaration soupçon", "#FF4757"),
    ]
    for col, (cond, result, color) in zip([col_tree1, col_tree2, col_tree3], scenarios):
        with col:
            st.markdown(f"""<div style='background: rgba(255,255,255,0.03); border: 2px solid {color}; border-radius: 10px; padding: 1rem; text-align: center;'>
                <div style='font-size: 0.8rem; color: #7A8BA6; margin-bottom: 0.8rem; line-height: 1.6;'>{cond.replace(chr(10), "<br>")}</div>
                <div style='font-size: 0.85rem; font-weight: 700; color: {color}; line-height: 1.6;'>{result.replace(chr(10), "<br>")}</div>
            </div>""", unsafe_allow_html=True)
