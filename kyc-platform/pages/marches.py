import streamlit as st
import random
import io
from datetime import datetime

# ── Case types for market surveillance ───────────────────────────────────────
CASE_TYPES = {
    "📈 Délit d'initié — Insider Trading": {
        "regime": "MAR Art. 7-8 · L.465-1 Code pénal · L.621-14 CMF",
        "sanction_max": "7 ans emprisonnement + 100 M€ ou 10× le profit",
        "desc": "Transaction sur instrument financier en utilisant une information précise, non publique, susceptible d'influencer significativement le cours.",
        "signaux": [
            "Volume anormalement élevé sur le titre avant une annonce réglementée",
            "Intervenant figurant sur la liste d'initiés de l'émetteur",
            "Achat d'options call juste avant une OPA ou résultats positifs",
            "Vente massive avant un profit warning ou événement négatif",
            "Transaction via un compte de proche (conjoint, enfant, associé)",
            "Changement radical de profil de trading sur le titre concerné",
        ],
        "checklist": [
            "1. Identifier l'annonce réglementée déclenchante (résultats, OPA, accord...)",
            "2. Calculer la fenêtre suspecte (J-5 à J-30 avant l'annonce)",
            "3. Analyser les transactions sur action ET dérivés (options, CFD)",
            "4. Croiser avec la liste d'initiés (Art. 18 MAR, L.621-18-4 CMF)",
            "5. Vérifier les transactions de l'entourage (Art. 19 MAR)",
            "6. Calculer le profit/perte évité (élément constitutif)",
            "7. Évaluer si seuil STOR atteint → déclaration immédiate AMF",
            "8. Documenter même si décision de ne pas déclarer (Art. 16 MAR)",
        ],
        "stor_obligatoire": True,
        "articles": ["MAR Art. 7", "MAR Art. 8", "MAR Art. 16", "L.465-1 CP", "L.621-14 CMF", "Art. 18 MAR (liste initiés)"],
        "sources": [
            ("AMF — Décisions insider trading", "https://www.amf-france.org/fr/sanctions-et-transactions"),
            ("ESMA — Guidelines MAR", "https://www.esma.europa.eu/document/guidelines-mar-market-soundings"),
            ("Portail ROSA (STOR)", "https://www.amf-france.org/fr/formulaires-et-declarations/professionnels-de-la-finance/declarations-de-transactions-suspectes"),
        ],
        "color": "#FF4757",
    },
    "🔄 Manipulation de cours — Layering / Spoofing": {
        "regime": "MAR Art. 12 · L.465-3-1 CMF · CFTC (USA)",
        "sanction_max": "5 ans emprisonnement + 100 M€",
        "desc": "Placement d'ordres sans intention d'exécution pour créer une fausse impression de liquidité ou d'intérêt, puis annulation avant exécution.",
        "signaux": [
            "Ratio annulation/exécution > 90% sur une valeur",
            "Ordres de gros volumes placés puis annulés en millisecondes",
            "Pattern répété : ordres côté offre → achat côté demande → annulation offre",
            "Activité concentrée en période de faible liquidité (ouverture/clôture)",
            "Déséquilibre artificiel persistant du carnet d'ordres",
            "Corrélation entre mouvements de cours et annulations massives",
        ],
        "checklist": [
            "1. Extraire le carnet d'ordres complet sur la période suspecte",
            "2. Calculer le ratio ordre/annulation par intervenant",
            "3. Analyser le timing microstructurel (millisecondes à secondes)",
            "4. Identifier le pattern directionnel (spoofing côté achat ou vente)",
            "5. Mesurer l'impact cours des faux ordres",
            "6. Vérifier si l'intervenant a profité du mouvement artificiel",
            "7. Cross-market : vérifier les dérivés liés (futures, options)",
            "8. Évaluer STOR — déclaration AMF si soupçon raisonnable",
        ],
        "stor_obligatoire": True,
        "articles": ["MAR Art. 12", "MAR Art. 12(1)(a)", "L.465-3-1 CMF", "RTS 6 (algorithmes)"],
        "sources": [
            ("ESMA — Indicateurs manipulation MAR Annexe I", "https://www.esma.europa.eu/document/guidelines-mar-market-manipulation"),
            ("AMF — Études de cas layering", "https://www.amf-france.org/fr/actualites-et-publications/publications/etudes-et-analyses"),
            ("Directive 2014/57/UE (MAD II)", "https://eur-lex.europa.eu/legal-content/FR/TXT/?uri=CELEX:32014L0057"),
        ],
        "color": "#FF6B35",
    },
    "📊 Marking the Close": {
        "regime": "MAR Art. 12(1)(a) · Annexe I MAR",
        "sanction_max": "5 ans + 100 M€ ou 10× profit",
        "desc": "Transactions en fin de séance visant à influencer artificiellement le cours de clôture, utilisé comme référence pour des produits dérivés, fonds ou contrats.",
        "signaux": [
            "Pic de volume anormal dans les 5-15 dernières minutes de séance",
            "Impact cours disproportionné par rapport au volume normal",
            "Intervenant avec position significative sur dérivés liés au fixing",
            "Pattern répété sur plusieurs jours consécutifs en fin de séance",
            "Cours de clôture systématiquement au-dessus/dessous des niveaux intraday",
            "Intérêt économique identifiable dans le fixing (options expirant, NAV fonds)",
        ],
        "checklist": [
            "1. Analyser les volumes des 15 dernières minutes vs moyenne historique",
            "2. Calculer l'impact cours des transactions suspects",
            "3. Identifier les produits dérivés ou contrats référencés sur ce cours",
            "4. Vérifier l'intérêt économique de l'intervenant dans le fixing",
            "5. Analyser si le pattern est répété (plusieurs jours/semaines)",
            "6. Comparer avec la volatilité intraday normale",
            "7. Déclarer STOR si soupçon raisonnable",
        ],
        "stor_obligatoire": True,
        "articles": ["MAR Art. 12(1)(a)", "MAR Annexe I §1", "ESMA Guidelines on MAR"],
        "sources": [
            ("ESMA — Indicateurs abus de marché", "https://www.esma.europa.eu/document/guidelines-mar-delayed-disclosure"),
            ("AMF — Rapport annuel surveillance marchés", "https://www.amf-france.org/fr/actualites-et-publications/rapports-annuels"),
        ],
        "color": "#FFB347",
    },
    "🔁 Wash Trading": {
        "regime": "MAR Art. 12(1)(a) · Art. 12(2)(a)",
        "sanction_max": "5 ans + 100 M€",
        "desc": "Transactions réalisées entre parties liées ou contrôlées par le même bénéficiaire effectif, créant un volume artificiel sans transfert de risque réel.",
        "signaux": [
            "Transactions croisées entre comptes ayant le même bénéficiaire effectif",
            "Volume élevé sans évolution significative du cours",
            "Ordres miroirs : achat et vente simultanés au même prix",
            "Contreparties dans des entités liées (filiales, associés)",
            "Fréquence anormale sur titres peu liquides",
            "Coïncidence parfaite de prix et de volume entre deux intervenants",
        ],
        "checklist": [
            "1. Identifier les deux parties à la transaction",
            "2. Analyser les liens entre les entités (capital, dirigeants, UBOs)",
            "3. Vérifier l'absence de transfert de risque réel",
            "4. Calculer l'impact sur le volume affiché du titre",
            "5. Rechercher un motif : manipulation cours, gonflement volume, fraude fiscale",
            "6. Tracer les flux financiers associés (LCB-FT possible)",
            "7. STOR si soupçon + signalement TRACFIN si origine suspecte des fonds",
        ],
        "stor_obligatoire": True,
        "articles": ["MAR Art. 12(1)(a)", "MAR Art. 12(2)(a)", "L.465-3-1 CMF"],
        "sources": [
            ("IOSCO — Report on Wash Trading", "https://www.iosco.org"),
            ("ESMA — Q&A MAR", "https://www.esma.europa.eu/document/qa-mar"),
        ],
        "color": "#9B59B6",
    },
    "📰 Divulgation d'information privilégiée": {
        "regime": "MAR Art. 10 · L.465-2 CP",
        "sanction_max": "5 ans + 100 M€",
        "desc": "Communication d'une information privilégiée à une tierce personne en dehors du cadre normal de l'exercice de ses fonctions.",
        "signaux": [
            "Transactions suspectes sur titre par des personnes proches d'un initié",
            "Leak d'information avant annonce officielle dans la presse/réseaux sociaux",
            "Échanges de communications entre initié et intervenant avant transaction",
            "Diffusion sélective à certains investisseurs avant publication officielle",
            "Analyste financier obtenant des informations non publiques lors de réunions",
        ],
        "checklist": [
            "1. Identifier la source de l'information (émetteur, conseil, auditeur...)",
            "2. Tracer les flux d'information : qui savait quoi et quand ?",
            "3. Analyser les communications (emails, messages) si disponibles",
            "4. Vérifier les transactions des personnes en contact avec la source",
            "5. Évaluer si la divulgation était dans le cadre normal des fonctions",
            "6. Documenter la chaîne causale information → transaction",
            "7. STOR sur les transactions suspectes résultantes",
        ],
        "stor_obligatoire": True,
        "articles": ["MAR Art. 10", "MAR Art. 11 (sondage de marché)", "L.465-2 CP", "L.621-14 CMF"],
        "sources": [
            ("AMF — Sondage de marché (market sounding)", "https://www.amf-france.org/fr/reglementation/dossiers-thematiques/sondage-de-marche"),
            ("ESMA — Market sounding guidelines", "https://www.esma.europa.eu/document/guidelines-mar-market-soundings"),
        ],
        "color": "#3498DB",
    },
    "🤖 Manipulation algorithmique": {
        "regime": "MAR Art. 12 · RTS 6 · MiFID II Art. 17",
        "sanction_max": "5 ans + 100 M€ + suspension agrément",
        "desc": "Utilisation d'algorithmes de trading à haute fréquence pour manipuler les marchés : quote stuffing, momentum ignition, cross-venue manipulation.",
        "signaux": [
            "Flood de messages d'ordres saturant les systèmes (quote stuffing)",
            "Série d'ordres designed à déclencher des stop-loss (momentum ignition)",
            "Exploitation des latences inter-marchés (cross-venue)",
            "Ordres fantômes à des prix extrêmes pour tester la liquidité",
            "Patterns répétés en microsecondes impossibles à exécuter manuellement",
            "Ratio messages/transactions > 100:1",
        ],
        "checklist": [
            "1. Analyser les données tick-by-tick (pas uniquement les trades)",
            "2. Calculer le ratio messages/transactions de l'algorithme",
            "3. Identifier le type de manipulation (quote stuffing, momentum ignition...)",
            "4. Vérifier la conformité du système algo (RTS 6 : tests, kill switch)",
            "5. Analyser l'impact sur la stabilité du marché",
            "6. Vérifier l'agrément algo trading (MiFID II Art. 17)",
            "7. STOR + signalement autorité compétente pour les algorithmes",
        ],
        "stor_obligatoire": True,
        "articles": ["MAR Art. 12", "MiFID II Art. 17", "RTS 6 (algo trading)", "Règlement (UE) 600/2014 (MiFIR)"],
        "sources": [
            ("ESMA — Guidelines algo trading", "https://www.esma.europa.eu/document/guidelines-systems-and-controls-algorithmic-trading"),
            ("AMF — Algo trading", "https://www.amf-france.org/fr/reglementation/dossiers-thematiques/trading-algorithmique"),
            ("RTS 6 — Commission européenne", "https://eur-lex.europa.eu/legal-content/FR/TXT/?uri=CELEX:32017R0589"),
        ],
        "color": "#1ABC9C",
    },
}

# ── 80 concepts marchés financiers ───────────────────────────────────────────
CONCEPTS_MARCHES = [
    # Fondamentaux réglementaires
    ("MAR — Market Abuse Regulation", "reglementation",
     "Règlement (UE) 596/2014 sur les abus de marché. Remplace la directive MAD (2003/6/CE). Couvre les opérations d'initiés, la manipulation de marché et la divulgation illicite d'informations privilégiées. S'applique à tous les marchés réglementés, MTF et OTF de l'UE. Base légale principale de la surveillance des marchés."),
    ("MiFID II / MiFIR", "reglementation",
     "Directive 2014/65/UE et Règlement (UE) 600/2014. Cadre réglementaire des marchés d'instruments financiers. MiFID II régit les prestataires, MiFIR la transparence des transactions. Introduit la catégorie OTF, les obligations de reporting (EMIR), et le trading algorithmique réglementé (Art. 17)."),
    ("STOR — Suspicious Transaction and Order Report", "surveillance",
     "Déclaration d'opération ou d'ordre suspect sur les marchés financiers, adressée à l'AMF via le portail ROSA. Obligation issue de l'Art. 16 MAR. Délai : immédiat dès naissance du soupçon raisonnable. Distinct de la déclaration de soupçon TRACFIN. Doit être effectuée même en l'absence de certitude."),
    ("Listing Act (UE 2024/2809)", "reglementation",
     "Règlement européen modifiant MAR, adopté en 2024. Relève le seuil de déclaration des transactions des dirigeants (Art. 19 MAR) de 5 000€ à 20 000€, puis 50 000€ à horizon 2026. Allège certaines obligations pour les PME cotées. Entrée en vigueur progressive."),
    ("MAD II — Market Abuse Directive", "reglementation",
     "Directive 2014/57/UE définissant les sanctions pénales minimales pour les abus de marché dans l'UE. Impose aux États membres des peines d'emprisonnement minimales : 4 ans pour délit d'initié et manipulation de marché, 2 ans pour divulgation illicite."),
    ("EMIR — Règlement sur les dérivés OTC", "reglementation",
     "Règlement (UE) 648/2012. Obligations de compensation centrale, de reporting et de mitigation des risques pour les dérivés OTC. Les transactions sont reportées aux référentiels centraux (trade repositories), source clé pour la surveillance de la manipulation cross-product."),
    ("DORA — Digital Operational Resilience Act", "reglementation",
     "Règlement (UE) 2022/2554. En vigueur depuis janvier 2025. Impose des exigences de résilience opérationnelle numérique aux acteurs financiers, incluant les systèmes de surveillance des marchés. Tests de pénétration TLPT, gestion des prestataires TIC tiers."),
    ("Règlement (UE) 2016/957 — RTS STOR", "reglementation",
     "Regulatory Technical Standard précisant le format, le contenu et les procédures de soumission des STOR à l'AMF. Définit l'Annex 1 (formulaire STOR) et les délais. Adopté par la Commission européenne sur proposition d'ESMA."),
    ("CSDR — Central Securities Depositories Regulation", "reglementation",
     "Règlement (UE) 909/2014 sur les dépositaires centraux de titres. Encadre le règlement-livraison des transactions. Les pénalités de règlement (buy-in) introduites affectent la liquidité et les stratégies de court selling."),
    ("MiCA — Markets in Crypto-Assets", "reglementation",
     "Règlement (UE) 2023/1114. Premier cadre réglementaire harmonisé pour les crypto-actifs dans l'UE. Les CASP (Crypto-Asset Service Providers) sont soumis à des règles anti-manipulation de marché similaires à MAR. L'ESMA et les ANCs supervisent."),
    # Infractions
    ("Délit d'initié", "infractions",
     "Art. 7-8 MAR et L.465-1 Code pénal. Utilisation d'une information privilégiée pour effectuer une transaction. Trois éléments : (1) information privilégiée, (2) connaissance de son caractère privilégié, (3) utilisation pour transacter. Le recel de délit d'initié est également sanctionné."),
    ("Information privilégiée", "infractions",
     "Art. 7 MAR. Information : (1) précise, (2) non publique, (3) concernant un émetteur ou instrument, (4) susceptible d'influencer significativement le cours si rendue publique. Test : l'investisseur raisonnable l'utiliserait-il ? Doit être évaluée ex ante."),
    ("Manipulation de marché", "infractions",
     "Art. 12 MAR. Trois formes : (1) transactions créant une fausse impression (layering, wash trading, marking the close), (2) recours à des procédés fictifs (squeeze, cornering), (3) diffusion d'informations fausses (rumeurs, recommandations biaisées). Liste indicative à l'Annexe I MAR."),
    ("Divulgation illicite", "infractions",
     "Art. 10 MAR et L.465-2 Code pénal. Communication d'une information privilégiée hors du cadre normal de l'exercice de ses fonctions. Exception : sondage de marché conforme à l'Art. 11 MAR. Délit distinct du délit d'initié, sanctionné séparément."),
    ("Tentative d'abus de marché", "infractions",
     "Art. 14-15 MAR. La tentative de manipulation ou d'opération d'initié est sanctionnée même en l'absence de consommation de l'infraction. Important pour les ordres annulés avant exécution dans les cas de layering."),
    ("Recommandations d'investissement biaisées", "infractions",
     "Art. 20 MAR. Les personnes produisant ou diffusant des recommandations doivent les présenter objectivement et révéler leurs conflits d'intérêts. Une recommandation délibérément biaisée pour manipuler le cours constitue une manipulation de marché."),
    ("Squeeze et cornering", "infractions",
     "Manipulation par acquisition d'une position dominante sur un instrument ou sa sous-jacente, permettant d'imposer un prix. Classique sur les marchés de matières premières. Signaux : position très concentrée, prime anormale, difficultés de livraison."),
    ("Front running", "infractions",
     "Pratique d'un intermédiaire consistant à transacter pour son propre compte avant d'exécuter un ordre client dont il anticipe l'impact de cours. Conflit d'intérêts et potentiellement manipulation. Interdit par MiFID II Art. 24 et constitutif d'abus de marché si intentionnel."),
    ("Pump and dump", "infractions",
     "Schéma classique sur les petites valeurs : acquisition silencieuse d'une position, diffusion d'informations positives fausses pour gonfler le cours, vente au plus haut. Très fréquent sur les penny stocks et les crypto-actifs. Constitue une manipulation de marché (Art. 12 MAR)."),
    ("Bear raid", "infractions",
     "Ventes massives coordonnées visant à faire baisser artificiellement le cours d'un titre, souvent accompagnées de rumeurs négatives. Inverse du pump and dump. Peut s'appuyer sur des positions short. Infraction sous MAR Art. 12."),
    # Instruments et marchés
    ("Marché réglementé", "marches",
     "Système multilatéral géré par un opérateur de marché, admettant des instruments financiers à la négociation selon des règles non discrétionnaires. En France : Euronext Paris (Eurolist). Soumis à la surveillance de l'AMF. Pleine application de MAR."),
    ("MTF — Multilateral Trading Facility", "marches",
     "Système multilatéral permettant de confronter des intérêts acheteurs et vendeurs, géré par une entreprise d'investissement ou un opérateur de marché. Ex : Euronext Growth. MAR s'applique intégralement. Moins régulé qu'un marché réglementé mais même obligations anti-manipulation."),
    ("OTF — Organised Trading Facility", "marches",
     "Catégorie créée par MiFID II pour les plateformes non réglementées où sont négociés des instruments autres que des actions (obligations, dérivés). Soumis à MAR depuis 2016. Opérateur a une certaine discrétion dans l'exécution."),
    ("Instrument financier (MAR)", "marches",
     "Notion centrale de MAR. Inclut : valeurs mobilières (actions, obligations), instruments du marché monétaire, parts d'OPC, dérivés (sur actions, taux, change, matières premières), quotas d'émission, et depuis MiCA les crypto-actifs significatifs."),
    ("Dérivés OTC", "marches",
     "Instruments dérivés négociés de gré à gré, hors marchés organisés. Soumis à MAR si leur cours peut affecter un instrument financier admis à la négociation. EMIR impose leur reporting aux référentiels centraux, facilitant la surveillance de la manipulation cross-product."),
    ("Short selling (vente à découvert)", "marches",
     "Règlement (UE) 236/2012. La vente d'instruments non détenus est autorisée mais encadrée. Obligation de déclaration des positions courtes nettes > 0,1% du capital à l'AMF. > 0,5% : publication publique. Suspension possible par l'AMF en cas de volatilité excessive (Art. 20)."),
    ("Carnet d'ordres (order book)", "marches",
     "Registre en temps réel des ordres d'achat et de vente en attente d'exécution sur un marché. Source de données principale pour la détection du layering et du spoofing. L'analyse de la profondeur de carnet et des annulations est clé en surveillance des marchés."),
    ("Dark pool", "marches",
     "Système de négociation alternatif où les ordres ne sont pas visibles avant exécution. Autorisés par MiFID II mais encadrés (caps de volumes). Vecteur potentiel de manipulation cross-venue si utilisés en combinaison avec des marchés lit pour manipuler les prix de référence."),
    ("Programme de rachat d'actions", "marches",
     "MAR Art. 5 et Règlement délégué 2016/1052. Safe harbour : exemption des règles anti-manipulation pour les rachats d'actions réalisés dans des conditions strictes (volumes, prix, timing, reporting). Conditions à respecter précisément pour bénéficier de l'exemption."),
    ("Stabilisation de cours", "marches",
     "MAR Art. 5. Pratique autorisée d'intervention sur le cours d'un instrument en période de distribution publique (IPO, augmentation de capital) pour soutenir le prix. Conditions strictes : période limitée, prix plafond, transparence. Safe harbour si respect des conditions."),
    # Surveillance et outils
    ("ROSA — Reporting et Surveillance AMF", "surveillance",
     "Portail extranet de l'AMF pour la soumission des STOR (déclarations de transactions suspectes). Accessible aux prestataires de services d'investissement assujettis. Les STOR soumis via ROSA alimentent le système de triage MATA (Market Triage Allocation Tool) de l'AMF."),
    ("MATA — Market Triage Allocation Tool", "surveillance",
     "Outil interne de l'AMF pour le triage et l'allocation des cas suspects. Chaque STOR reçu est analysé et classé : cas ouvert pour investigation, cas fermé (soupçon non confirmé), ou transmis à la Division des Enquêtes. Processus en 15-20 minutes pour les cas prioritaires."),
    ("SAMIR — Système de surveillance AMF", "surveillance",
     "Système informatique de surveillance des marchés de l'AMF. Analyse en temps réel les transactions sur les marchés français. Génère des alertes sur des patterns suspects. Alimenté par les données de transaction reportées sous MiFIR (transaction reporting)."),
    ("Transaction reporting (MiFIR Art. 26)", "surveillance",
     "Obligation pour les PSI de reporter chaque transaction à l'autorité compétente le jour suivant (T+1). Inclut : instrument, prix, volume, contreparties, identifiants (LEI, ISIN). Données analysées par l'AMF pour la détection des abus de marché."),
    ("LEI — Legal Entity Identifier", "surveillance",
     "Identifiant à 20 caractères identifiant de manière unique les personnes morales parties à des transactions financières. Obligatoire pour le transaction reporting MiFIR. Géré par le GLEIF. Clé pour le suivi des transactions cross-border et la détection du wash trading."),
    ("ISIN — International Securities Identification Number", "surveillance",
     "Code à 12 caractères identifiant un instrument financier. Structure : pays (2 lettres) + code national (9 chiffres) + check digit. Standard universel pour le reporting. Utilisé dans tous les reportings réglementaires (EMIR, MiFIR, STOR)."),
    ("Liste d'initiés (insider list)", "surveillance",
     "Art. 18 MAR. Liste tenue par l'émetteur et ses conseils identifiant toutes les personnes ayant accès à des informations privilégiées. Doit être mise à jour en temps réel, conservée 5 ans, communiquée à l'AMF sur demande. Outil clé des investigations insider trading."),
    ("PDMR — Persons Discharging Managerial Responsibilities", "surveillance",
     "Art. 19 MAR. Dirigeants et personnes exerçant des responsabilités dirigeantes, ainsi que leurs personnes liées, doivent notifier à l'émetteur et à l'AMF toutes leurs transactions sur les titres de l'émetteur dans les 3 jours ouvrables. Seuil de déclaration : 20 000€ (puis 50 000€ post-Listing Act)."),
    ("Fenêtre négoire (blackout period)", "surveillance",
     "Art. 19(11) MAR. Interdiction pour les PDMR de transacter sur les titres de l'émetteur pendant les 30 jours précédant la publication des résultats financiers. Les émetteurs peuvent étendre cette période. Exceptions limitées (nécessité financière urgente)."),
    ("Market sounding (sondage de marché)", "surveillance",
     "Art. 11 MAR. Communication d'informations à des investisseurs potentiels avant annonce d'une opération. Safe harbour si procédures strictes : évaluation préalable du caractère privilégié, information du destinataire, documentation. Hors cadre = divulgation illicite."),
    # Acteurs et responsabilités
    ("PSI — Prestataire de Services d'Investissement", "acteurs",
     "Entité agréée pour fournir des services d'investissement (réception-transmission d'ordres, exécution, gestion de portefeuille, conseil). Soumis à MAR Art. 16 : obligation de détection et déclaration STOR. Doit disposer de systèmes et procédures de surveillance adaptés."),
    ("Opérateur de marché", "acteurs",
     "Entité gérant un marché réglementé (ex : Euronext). Soumis à MAR Art. 16(2) : doit notifier à l'autorité compétente tout ordre ou transaction susceptible de constituer un abus de marché. Première ligne de surveillance des marchés organisés."),
    ("AMF — Autorité des Marchés Financiers", "acteurs",
     "Régulateur indépendant des marchés financiers français. Supervise les émetteurs, PSI, sociétés de gestion, PSAN. Pouvoirs d'investigation (inspection, perquisition, audition), de sanction (jusqu'à 100 M€ ou 10× profit) et d'injonction. Membre de l'ESMA."),
    ("ESMA — European Securities and Markets Authority", "acteurs",
     "Autorité européenne des marchés financiers. Émet les guidelines et Q&A d'application de MAR. Coordonne la surveillance cross-border entre ANCs. Peut prendre des mesures d'urgence (Art. 28 ESMA Regulation). Publie les orientations sur les STOR et les indicateurs de manipulation."),
    ("Déclarant obligatoire STOR", "acteurs",
     "Toute personne qui effectue ou organise des transactions à titre professionnel (PSI, opérateurs de marché, gestionnaires...). Obligation pesant sur la personne morale et ses dirigeants. La défaillance dans la déclaration STOR est elle-même sanctionnable sous MAR Art. 16."),
    ("Compliance officer marchés", "acteurs",
     "RCCI/RCSI responsable de la surveillance des marchés au sein du PSI. Décide de la soumission des STOR. Doit disposer d'une indépendance suffisante et d'un accès aux données de trading. Peut être personnellement sanctionné en cas de manquement grave (MAR Art. 16)."),
    ("Émetteur", "acteurs",
     "Entité dont les instruments financiers sont admis à la négociation. Obligations MAR : publication d'informations réglementées (Art. 17), liste d'initiés (Art. 18), notifications PDMR (Art. 19), programmes de rachat (Art. 5). Première responsable de la prévention du délit d'initié interne."),
    ("Analyste financier", "acteurs",
     "Produit des recommandations d'investissement. Soumis à MAR Art. 20 : objectivité des recommandations, révélation des conflits d'intérêts. Potentiellement initié s'il reçoit des informations privilégiées lors de rencontres avec les émetteurs. Obligations MiFID II de transparence."),
    # Outils de détection
    ("Algorithme de détection layering", "detection",
     "Algorithme analysant le ratio ordres/annulations, la durée de vie des ordres, l'impact cours, et la corrélation entre annulations et exécutions en sens inverse. Machine learning supervisé (XGBoost, Random Forest) sur données labelisées par des cas AMF historiques."),
    ("Analyse de microstructure", "detection",
     "Étude des données tick-by-tick (chaque ordre, modification, annulation) pour détecter les manipulations algorithmiques. Requiert des données à la milliseconde. Permet de distinguer le market-making légitime de la manipulation. Utilisée par l'AMF dans ses investigations HFT."),
    ("Corrélation pré-annonce", "detection",
     "Méthode de détection du délit d'initié : analyse statistique des variations de cours, volume et volatilité dans les jours précédant une annonce réglementée. Un mouvement anormal corrélé avec une annonce ultérieure déclenche l'alerte et l'analyse de la liste d'initiés."),
    ("Réseau d'analyse des liens", "detection",
     "Graphe des relations entre intervenants (comptes, entités, personnes physiques) pour détecter les wash trading et les schémas coordonnés. Algorithmes de détection de communautés (community detection) sur les données de transactions cross-account."),
    ("Benchmark de liquidité", "detection",
     "Mesure de la liquidité normale d'un titre (spread bid-ask, profondeur de carnet, impact de marché) servant de référence pour détecter des comportements anormaux. Un écart significatif par rapport au benchmark déclenche une alerte de surveillance."),
    ("Cross-market surveillance", "detection",
     "Surveillance coordonnée entre marchés liés : action et ses dérivés, actif sous-jacent et produit dérivé, titre sur différentes plateformes. Nécessaire pour détecter les manipulations exploitant les écarts de surveillance entre marchés (ex : manipuler l'action pour profiter sur les options)."),
    ("Modèle d'alerte ESMA", "detection",
     "ESMA publie des indicateurs non exhaustifs de manipulation dans l'Annexe I de MAR, classés par type : (Section A) indicateurs pour toutes formes de manipulation, (Section B) manipulation cours, (Section C) manipulation via médias. Chaque indicateur est pondéré dans les systèmes de scoring."),
    ("Forensic data analysis", "detection",
     "Analyse forensique des données de trading pour reconstituer la chronologie précise des événements dans une investigation. Inclut la reconstruction du carnet d'ordres, l'analyse des latences, et la corrélation avec des événements externes (actualités, communications)."),
    # Procédure et sanctions
    ("Procédure de sanction AMF", "procedure",
     "Biphasique : (1) enquête/contrôle par la Direction des Enquêtes → notification de griefs → (2) Commission des sanctions (indépendante du Collège) statue. Droits de la défense garantis. Décision publiée (name and shame). Recours devant la Cour d'appel de Paris."),
    ("Commission des sanctions AMF", "procedure",
     "Organe indépendant du Collège de l'AMF statuant sur les manquements réglementaires. 12 membres. Peut prononcer : avertissement, blâme, interdiction temporaire ou définitive d'exercer, sanction pécuniaire jusqu'à 100 M€ ou 10× profit. Décisions publiées."),
    ("Transaction AMF", "procedure",
     "Procédure permettant à la personne mise en cause de conclure un accord avec le Collège AMF (similaire à la CJIP). Homologuée par la Commission des sanctions. Permet de clore la procédure sans reconnaissance de culpabilité. Montant fixé, publié."),
    ("PNF — Parquet National Financier", "procedure",
     "Juridiction spécialisée dans les infractions financières complexes. Compétent pour les délits d'initiés et manipulations de marché les plus graves (délit pénal). Travaille en coordination avec l'AMF (convention de coopération). Peut ouvrir une instruction indépendamment de l'AMF."),
    ("Cumul des poursuites AMF/PNF", "procedure",
     "La règle non bis in idem (ne pas être jugé deux fois pour les mêmes faits) s'applique entre la Commission des sanctions AMF et le PNF. Décision du Conseil constitutionnel 2014 : le cumul est possible mais les sanctions cumulées ne doivent pas dépasser le maximum légal le plus élevé."),
    ("Délai de prescription MAR", "procedure",
     "Manquement administratif (AMF) : 6 ans à compter des faits. Délit pénal (PNF) : 6 ans pour les délits d'initiés (Art. L.465-1 CP). Le délai commence à courir à partir du moment où les faits pouvaient être découverts. La prescription est suspendue pendant l'enquête."),
    ("Lanceur d'alerte marchés financiers", "procedure",
     "MAR Art. 32 et Directive 2019/1937. Obligation pour les États membres de mettre en place des canaux de signalement des violations de MAR. En France : portail AMF Infofraud et protection spécifique des lanceurs d'alerte (loi Sapin II). Récompense financière possible dans certains pays (USA : SEC whistleblower)."),
    # Concepts avancés
    ("High-Frequency Trading (HFT)", "avance",
     "Trading algorithmique caractérisé par des vitesses d'exécution en microsecondes, des positions intraday, des volumes élevés et des profits par transaction infimes. Légal en tant que tel mais source de manipulations potentielles (layering, quote stuffing). Encadré par MiFID II Art. 17 (registration, kill switch, tests)."),
    ("Dark liquidity et manipulation", "avance",
     "L'opacité des dark pools permet théoriquement de masquer des stratégies de manipulation cross-venue. Les caps de volumes MiFID II (DVC mechanism : 4% sur un dark pool unique, 8% global) limitent ce risque. L'AMF surveille les flux entre marchés lit et dark."),
    ("Crypto-actifs et manipulation MAR", "avance",
     "MiCA impose aux CASP des obligations de surveillance similaires à MAR. Les pratiques de manipulation dans le crypto (wash trading sur DEX, pump and dump de tokens, rug pull) sont désormais dans le périmètre réglementaire UE. ESMA élabore les guidelines d'application."),
    ("ESG washing et information privilégiée", "avance",
     "Les annonces ESG (notation, incident environnemental, retrait de notation) constituent potentiellement des informations privilégiées au sens MAR si leur impact cours est significatif. L'AMF surveille les transactions précédant des annonces ESG majeures."),
    ("SFDR et manipulation narrative", "avance",
     "Règlement (UE) 2019/2088 sur la divulgation en matière de finance durable. La classification trompeuse d'un fonds (Art. 8 vs Art. 9) peut constituer une manipulation via diffusion d'informations fausses (MAR Art. 12(1)(c)) si intentionnelle."),
    ("Quantum computing et surveillance", "avance",
     "Problématique émergente : les algorithmes quantiques pourraient permettre des manipulations de marché à des vitesses impossibles à détecter avec les outils actuels. L'ESMA et l'AMF anticipent cette évolution dans leurs programmes de transformation technologique."),
    ("Tokenisation des actifs et MAR", "avance",
     "Les security tokens (représentation numérique d'instruments financiers sur blockchain) tombent sous MAR dès lors qu'ils sont admis à la négociation sur une plateforme régulée. Le régime pilote DLT (Règlement UE 2022/858) ouvre la voie à des marchés réglementés tokenisés."),
    ("LIBOR manipulation et benchmarks", "avance",
     "Scandale de manipulation du LIBOR (2012) → Règlement Benchmarks (UE) 2016/1011. Encadre la production et l'utilisation des indices de référence financiers (EURIBOR, €STR). La manipulation d'un benchmark constitue une infraction distincte sous le Règlement."),
    ("Position limits (limites de position)", "avance",
     "MiFID II Art. 57. Limites imposées aux positions nettes sur les dérivés sur matières premières agricoles pour prévenir les manipulations de marché et le squeeze. Fixées par l'AMF et l'ESMA. Exemptions pour les couvertures commerciales (hedging)."),
    ("Suspicious activities reporting — SAR vs STOR", "avance",
     "Le SAR (Suspicious Activity Report, utilisé aux USA et UK pour LCB-FT) et le STOR (MAR) sont deux mécanismes distincts. Un même comportement peut déclencher les deux : ex. un schéma de wash trading servant aussi à blanchir des fonds déclenche un STOR AMF ET une déclaration TRACFIN."),
]

CATEGORIES_M = {
    "reglementation": ("⚖️ Réglementation UE & française", "#00D4AA"),
    "infractions":    ("🔴 Infractions & typologies", "#FF4757"),
    "marches":        ("📊 Instruments & marchés", "#3498DB"),
    "surveillance":   ("🛡️ Surveillance & reporting", "#FF6B35"),
    "acteurs":        ("👤 Acteurs & responsabilités", "#9B59B6"),
    "detection":      ("🔍 Outils de détection", "#1ABC9C"),
    "procedure":      ("⚖️ Procédures & sanctions", "#E67E22"),
    "avance":         ("🚀 Concepts avancés", "#F39C12"),
}


def show():
    st.markdown("## 📈 Conformité des Marchés Financiers")
    st.markdown("<div style='color:#7A8BA6;margin-bottom:1.5rem;'>Surveillance des abus de marché · MAR · STOR · Insider trading · Manipulation · MiFID II</div>", unsafe_allow_html=True)

    main_tabs = st.tabs([
        "🗂️ Analyse de cas",
        "📚 80 Concepts marchés",
        "📋 Workflow STOR",
        "📊 Sources & outils",
    ])

    # ── TAB 1 : Case analysis ─────────────────────────────────────────────────
    with main_tabs[0]:
        st.markdown("### Méthodologie d'analyse par type de cas")
        case_type = st.selectbox("Sélectionner un type de cas", list(CASE_TYPES.keys()), label_visibility="visible")
        case = CASE_TYPES[case_type]

        st.markdown(f"""<div style='background:rgba(255,255,255,0.03);border-left:4px solid {case["color"]};border-radius:0 10px 10px 0;padding:1rem 1.2rem;margin-bottom:1.2rem;'>
            <div style='font-size:1rem;font-weight:700;color:#E8EDF5;'>{case_type}</div>
            <div style='font-size:0.85rem;color:#C8D4E5;margin-top:0.3rem;line-height:1.6;'>{case["desc"]}</div>
            <div style='margin-top:0.8rem;'>
                <span style='font-size:0.75rem;color:#7A8BA6;'>Régime : </span>
                <span style='font-size:0.8rem;color:{case["color"]};font-weight:600;'>{case["regime"]}</span>
            </div>
            <div style='margin-top:0.3rem;'>
                <span style='font-size:0.75rem;color:#7A8BA6;'>Sanction max : </span>
                <span style='font-size:0.8rem;color:#FF4757;font-weight:600;'>{case["sanction_max"]}</span>
            </div>
            {'<div style="margin-top:0.5rem;"><span style="background:rgba(255,71,87,0.15);color:#FF4757;border:1px solid rgba(255,71,87,0.3);padding:2px 10px;border-radius:20px;font-size:0.72rem;font-weight:600;">STOR OBLIGATOIRE</span></div>' if case.get("stor_obligatoire") else ''}
        </div>""", unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            st.markdown("<div class='section-title'>🚩 Signaux d'alerte</div>", unsafe_allow_html=True)
            for s in case["signaux"]:
                st.markdown(f"""<div style='background:rgba(255,71,87,0.06);border:1px solid rgba(255,71,87,0.2);border-radius:6px;padding:0.6rem 0.9rem;margin-bottom:0.4rem;font-size:0.85rem;color:#E8EDF5;'>
                    <span style='color:#FF4757;'>◆</span> {s}</div>""", unsafe_allow_html=True)

        with col2:
            st.markdown("<div class='section-title'>✅ Étapes d'analyse</div>", unsafe_allow_html=True)
            for step in case["checklist"]:
                num = step.split(".")[0]
                text = ".".join(step.split(".")[1:]).strip()
                st.markdown(f"""<div style='display:flex;gap:0.8rem;align-items:flex-start;margin-bottom:0.6rem;'>
                    <div style='background:{case["color"]};color:#0A1628;width:22px;height:22px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-weight:700;font-size:0.7rem;flex-shrink:0;'>{num}</div>
                    <div style='font-size:0.85rem;color:#E8EDF5;line-height:1.5;'>{text}</div>
                </div>""", unsafe_allow_html=True)

        st.markdown("<div class='section-title'>📚 Articles et références</div>", unsafe_allow_html=True)
        cols_a = st.columns(min(len(case["articles"]), 4))
        for i, art in enumerate(case["articles"]):
            with cols_a[i % len(cols_a)]:
                st.markdown(f"<span class='source-pill'>{art}</span>", unsafe_allow_html=True)

        st.markdown("<div class='section-title' style='margin-top:1rem;'>🔗 Sources officielles</div>", unsafe_allow_html=True)
        for label, url in case["sources"]:
            st.markdown(f"🔗 [{label}]({url})")

    # ── TAB 2 : 80 concepts ───────────────────────────────────────────────────
    with main_tabs[1]:
        st.markdown("### 80 concepts essentiels — Conformité marchés financiers")

        c1, c2, c3 = st.columns(3)
        with c1: st.markdown(f"""<div class='metric-card'><div class='metric-value'>{len(CONCEPTS_MARCHES)}</div><div class='metric-label'>Concepts</div></div>""", unsafe_allow_html=True)
        with c2: st.markdown(f"""<div class='metric-card'><div class='metric-value'>{len(CATEGORIES_M)}</div><div class='metric-label'>Catégories</div></div>""", unsafe_allow_html=True)
        with c3: st.markdown(f"""<div class='metric-card'><div class='metric-value'>MAR</div><div class='metric-label'>Règlement central</div></div>""", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        search = st.text_input("🔍 Rechercher un concept", placeholder="Ex: STOR, insider, layering, ESMA, MiFID…")
        cat_opts = ["Toutes"] + [v[0] for v in CATEGORIES_M.values()]
        cat_sel = st.selectbox("Filtrer par catégorie", cat_opts, label_visibility="visible")

        filtered = [
            (title, cat, defn) for title, cat, defn in CONCEPTS_MARCHES
            if (not search or search.lower() in title.lower() or search.lower() in defn.lower())
            and (cat_sel == "Toutes" or CATEGORIES_M[cat][0] == cat_sel)
        ]
        st.caption(f"{len(filtered)} concept(s) affiché(s)")

        by_cat = {}
        for title, cat, defn in filtered:
            by_cat.setdefault(cat, []).append((title, defn))

        num = 1
        for cat_key, items in by_cat.items():
            label, color = CATEGORIES_M[cat_key]
            st.markdown(f"<div style='font-size:0.85rem;font-weight:700;color:{color};text-transform:uppercase;letter-spacing:1.5px;margin-top:1.5rem;margin-bottom:0.8rem;padding-bottom:0.4rem;border-bottom:1px solid #1E3055;'>{label}</div>", unsafe_allow_html=True)
            for title, defn in items:
                with st.expander(f"**{num:03d}. {title}**"):
                    st.markdown(f"<div style='font-size:0.88rem;color:#E8EDF5;line-height:1.7;'>{defn}</div>", unsafe_allow_html=True)
                    st.markdown(f"<span class='source-pill'>{label}</span>", unsafe_allow_html=True)
                num += 1

    # ── TAB 3 : STOR workflow ─────────────────────────────────────────────────
    with main_tabs[2]:
        st.markdown("### Workflow de déclaration STOR")
        st.markdown("""<div class='info-box'>
        <div style='font-weight:700;color:#00D4AA;'>Art. 16 MAR — Obligation de déclaration immédiate</div>
        <div style='font-size:0.85rem;color:#7A8BA6;margin-top:0.3rem;'>
        Toute personne effectuant des transactions à titre professionnel qui a un soupçon raisonnable qu'une transaction
        constitue un abus de marché DOIT le déclarer immédiatement à l'AMF. Le délai court dès la naissance du soupçon.
        </div></div>""", unsafe_allow_html=True)

        steps_stor = [
            ("Détection", "Alerte générée par le système de surveillance (TMS) ou par un analyste", "#00D4AA", "TMS, règles, ML"),
            ("Analyse initiale", "Analyste examine l'alerte : contexte, profil, historique. Délai cible : 15-20 min", "#00D4AA", "Données internes + marché"),
            ("Qualification", "Décision : soupçon raisonnable ou non ? Documentation obligatoire même si non-déclaration", "#FFB347", "Compliance officer"),
            ("Rédaction STOR", "Formulaire Annexe 1 du Règlement délégué (UE) 2016/957 : description, instruments, personnes, motifs", "#FFB347", "Portail ROSA AMF"),
            ("Envoi AMF", "Soumission via ROSA (extranet AMF). Accusé de réception automatique. IMMÉDIAT après qualification", "#FF6B35", "https://rosa.amf-france.org"),
            ("Triage MATA", "AMF trie le STOR : cas ouvert / fermé / transmis Division Enquêtes", "#FF6B35", "Interne AMF"),
            ("Confidentialité", "Art. 16(2) MAR : interdiction d'informer la personne concernée. Violation = infraction pénale", "#FF4757", "L.465-3-3 CMF"),
            ("Conservation", "Conserver la documentation pendant 5 ans minimum (Art. 16(2) MAR)", "#7A8BA6", "Archivage interne"),
        ]

        for i, (title, desc, color, note) in enumerate(steps_stor):
            st.markdown(f"""<div style='display:flex;gap:1rem;align-items:flex-start;margin-bottom:0.6rem;'>
                <div style='background:{color};color:#0A1628;width:28px;height:28px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-weight:700;font-size:0.82rem;flex-shrink:0;'>{i+1}</div>
                <div style='background:#0F1F3D;border:1px solid #1E3055;border-radius:8px;padding:0.7rem 1rem;flex:1;'>
                    <div style='font-weight:600;color:#E8EDF5;font-size:0.9rem;'>{title}</div>
                    <div style='font-size:0.82rem;color:#C8D4E5;margin-top:0.2rem;'>{desc}</div>
                    <div style='font-size:0.75rem;color:#7A8BA6;font-family:monospace;margin-top:0.2rem;'>{note}</div>
                </div>
            </div>""", unsafe_allow_html=True)

        st.markdown("---")
        st.markdown("### Liens directs")
        c1, c2, c3 = st.columns(3)
        with c1: st.markdown("🔗 [Portail ROSA AMF](https://www.amf-france.org/fr/formulaires-et-declarations/professionnels-de-la-finance/declarations-de-transactions-suspectes)")
        with c2: st.markdown("🔗 [Règlement délégué (UE) 2016/957](https://eur-lex.europa.eu/legal-content/FR/TXT/?uri=CELEX:32016R0957)")
        with c3: st.markdown("🔗 [Q&A ESMA sur MAR](https://www.esma.europa.eu/document/qa-mar)")

    # ── TAB 4 : Sources ───────────────────────────────────────────────────────
    with main_tabs[3]:
        st.markdown("### Sources officielles et outils de surveillance")
        sources_list = [
            ("AMF — Portail ROSA (STOR)", "https://www.amf-france.org/fr/formulaires-et-declarations/professionnels-de-la-finance/declarations-de-transactions-suspectes", "Soumission des déclarations STOR. Accès sécurisé PSI."),
            ("AMF — Sanctions et transactions", "https://www.amf-france.org/fr/sanctions-et-transactions", "Toutes les décisions de sanction AMF publiées. Source adverse media réglementaire."),
            ("ESMA — Guidelines MAR", "https://www.esma.europa.eu/document/guidelines-mar-market-manipulation", "Orientations officielles sur les indicateurs de manipulation. Annexe I MAR."),
            ("ESMA — Q&A MAR", "https://www.esma.europa.eu/document/qa-mar", "Questions-réponses sur l'application pratique de MAR. Mis à jour régulièrement."),
            ("Legifrance — MAR transposé", "https://www.legifrance.gouv.fr/codes/section_lc/LEGITEXT000006072026/LEGISCTA000006170538/", "Articles L.465-1 à L.465-3-7 du Code pénal (sanctions pénales MAR)."),
            ("Euronext — Données marché", "https://live.euronext.com", "Données temps réel et historiques sur les marchés Euronext Paris."),
            ("AMF — Infofraud (signalement)", "https://www.amf-france.org/fr/espace-epargnants/proteger-son-epargne/signaler-un-probleme", "Portail de signalement pour les investisseurs et lanceurs d'alerte."),
            ("GLEIF — LEI search", "https://search.gleif.org", "Recherche d'entités par LEI. Indispensable pour le transaction reporting MiFIR."),
            ("ESMA — FIRDS (ISIN/instruments)", "https://registers.esma.europa.eu/publication/searchRegister?core=esma_registers_firds", "Financial Instruments Reference Data System. Base de tous les instruments financiers UE."),
            ("AMF — Décisions et règlements", "https://www.amf-france.org/fr/reglementation/textes-applicables/reglement-general-de-lamf", "Règlement général de l'AMF et décisions de portée générale."),
            ("Autorités compétentes MAR par pays", "https://www.esma.europa.eu/sites/default/files/library/esma70-145-111_annex_ii_mar_competent_authorities.pdf", "Liste des ANCs (Autorités Nationales Compétentes) pour MAR dans chaque État membre UE."),
            ("PNF — Parquet National Financier", "https://www.justice.fr/article/parquet-national-financier", "Juridiction pénale spécialisée dans les infractions financières complexes."),
        ]
        for name, url, desc in sources_list:
            st.markdown(f"""<div style='background:#0F1F3D;border:1px solid #1E3055;border-radius:8px;padding:0.8rem 1rem;margin-bottom:0.5rem;display:flex;justify-content:space-between;align-items:center;'>
                <div>
                    <div style='font-weight:600;color:#E8EDF5;font-size:0.9rem;'>{name}</div>
                    <div style='font-size:0.8rem;color:#7A8BA6;margin-top:0.2rem;'>{desc}</div>
                </div>
                <a href='{url}' target='_blank' style='font-size:0.75rem;color:#00D4AA;text-decoration:none;white-space:nowrap;margin-left:1rem;border:1px solid rgba(0,212,170,0.3);padding:3px 10px;border-radius:20px;'>Ouvrir →</a>
            </div>""", unsafe_allow_html=True)
