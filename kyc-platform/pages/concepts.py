import streamlit as st

CONCEPTS = [
    # LCB-FT Fondamentaux
    ("LCB-FT", "lcb-ft", "Lutte Contre le Blanchiment de Capitaux et le Financement du Terrorisme. Ensemble des obligations légales imposées aux établissements assujettis pour détecter et signaler les opérations suspectes. Cadre légal : L.561-1 et suivants du CMF."),
    ("KYC — Know Your Customer", "lcb-ft", "Processus d'identification et de vérification de l'identité du client, avant et pendant la relation d'affaires. Inclut l'identification de la personne, la vérification des documents, et la compréhension de l'objet et de la nature de la relation."),
    ("CDD — Customer Due Diligence", "lcb-ft", "Diligence client standard : mesures de connaissance client de base. S'oppose à la vigilance simplifiée (SDD) et à la vigilance renforcée (EDD). Définie à l'article L.561-8 du CMF."),
    ("EDD — Enhanced Due Diligence", "lcb-ft", "Vigilance renforcée, applicable aux PPE, aux relations avec des pays tiers à risque, et à toute situation de risque élevé. Implique une connaissance approfondie de l'origine des fonds et une approbation du management. Art. L.561-10 CMF."),
    ("UBO — Ultimate Beneficial Owner", "lcb-ft", "Bénéficiaire effectif ultime : personne physique détenant in fine plus de 25% du capital ou des droits de vote, ou exerçant un contrôle de fait. La déclaration au RBE (INPI) est obligatoire en France depuis 2017."),
    ("PPE — Personne Politiquement Exposée", "lcb-ft", "Toute personne exerçant ou ayant exercé une fonction publique importante (chef d'État, ministre, député, dirigeant d'entreprise publique...). Régime de vigilance renforcée systématique. Périmètre étendu à l'entourage proche (AMLD5)."),
    ("Blanchiment de capitaux", "lcb-ft", "Processus consistant à dissimuler l'origine illicite de fonds (produits du crime) pour les réintégrer dans l'économie légale. Trois phases classiques : placement, empilage, intégration. Infraction pénale : L.324-1 Code pénal."),
    ("Financement du terrorisme", "lcb-ft", "Fait de fournir, collecter ou gérer des fonds destinés à financer des actes terroristes, même si les fonds sont d'origine licite. Art. 421-2-2 Code pénal. Particularité : les montants peuvent être très faibles."),
    ("TRACFIN", "lcb-ft", "Traitement du renseignement et action contre les circuits financiers clandestins. Cellule de renseignement financier française rattachée au ministère de l'Économie. Destinataire des déclarations de soupçon (L.561-15 CMF)."),
    ("Déclaration de soupçon", "lcb-ft", "Obligation légale de signaler à TRACFIN toute opération portant sur des fonds dont on soupçonne l'origine illicite ou liée au financement du terrorisme. Art. L.561-15 CMF. Strictement confidentielle (L.561-16 CMF)."),
    # Réglementation
    ("AMLD — Anti-Money Laundering Directive", "reglementation", "Directive européenne anti-blanchiment. AMLD1 (1991) à AMLD6 (2021). L'AMLD6 introduit la liste harmonisée des infractions sous-jacentes, l'extension de la responsabilité pénale aux personnes morales, et renforce les exigences sur les PPE."),
    ("GAFI — Groupe d'Action Financière", "reglementation", "Organisation intergouvernementale créée en 1989 fixant les standards internationaux LCB-FT. Ses 40 Recommandations sont la référence mondiale. Publie des évaluations mutuelles et des listes de pays à risque (liste noire / liste grise)."),
    ("CMF — Code Monétaire et Financier", "reglementation", "Code regroupant les dispositions législatives et réglementaires françaises applicables aux acteurs financiers. Livre V (L.500 et suivants) contient les dispositions LCB-FT. Articles clés : L.561-1 à L.561-50."),
    ("ACPR — Autorité de Contrôle Prudentiel et de Résolution", "reglementation", "Superviseur français des banques et assurances. Contrôle le respect des obligations LCB-FT par les entités assujetties. Peut prononcer des sanctions disciplinaires et pécuniaires. Publie des lignes directrices et positions."),
    ("AMF — Autorité des Marchés Financiers", "reglementation", "Régulateur français des marchés financiers. Compétent pour la conformité marchés (abus de marché, information réglementée). Destinataire des STOR (déclarations d'opérations suspectes sur les marchés). Site : amf-france.org."),
    ("MAR — Market Abuse Regulation", "reglementation", "Règlement européen (UE) 596/2014 sur les abus de marché. Couvre les opérations d'initiés, la manipulation de marché, la divulgation illicite d'informations privilégiées. S'applique à tous les marchés réglementés, MTF et OTF de l'UE."),
    ("STOR — Suspicious Transaction and Order Report", "reglementation", "Déclaration d'opération ou d'ordre suspect sur les marchés financiers, adressée à l'AMF via le portail ROSA. Obligation issue de l'article 16 MAR. Délai : immédiat après naissance du soupçon raisonnable."),
    ("Listing Act (UE 2024/2809)", "reglementation", "Règlement européen modifiant MAR, adopté en 2024. Relève le seuil de déclaration des transactions des dirigeants de 5 000€ à 20 000€, puis 50 000€. Allège certaines obligations de divulgation pour les émetteurs."),
    ("DORA — Digital Operational Resilience Act", "reglementation", "Règlement européen (UE) 2022/2554 sur la résilience opérationnelle numérique du secteur financier. En vigueur depuis janvier 2025. Impose des exigences sur la gestion des risques TIC, les tests de résilience, et la surveillance des prestataires tiers."),
    ("RGPD — Règlement Général sur la Protection des Données", "reglementation", "Règlement (UE) 2016/679. Applicable au traitement des données personnelles dans le cadre KYC. Crée des obligations de minimisation, de sécurité, et limite les transferts vers pays tiers. Tension avec l'obligation LCB-FT de conservation 5 ans."),
    # Opérations et typologies
    ("Smurfing / Structuration", "typologies", "Technique de blanchiment consistant à fractionner une somme importante en multiples petites transactions pour rester sous les seuils de déclaration (en France : 10 000€ pour espèces, 1 000€ pour change manuel). Signal d'alerte majeur."),
    ("Layering (empilage)", "typologies", "Deuxième phase du blanchiment : multiplication des transactions et des intermédiaires pour brouiller la trace des fonds illicites. Utilisation typique de virements internationaux, échanges de cryptomonnaies, sociétés-écrans successives."),
    ("Trade-based money laundering (TBML)", "typologies", "Blanchiment par le commerce international : sur ou sous-facturation de biens/services, fausses transactions commerciales pour justifier des flux de fonds. Parmi les méthodes les plus difficiles à détecter."),
    ("Shell company / Société-écran", "typologies", "Société sans activité économique réelle, utilisée pour masquer l'identité des bénéficiaires effectifs ou la trace des fonds. Signal d'alerte : capital minimal, objet social vague, pas d'employés, adresse de domiciliation."),
    ("Nominee / Prête-nom", "typologies", "Personne physique ou morale figurant comme dirigeant ou actionnaire official au lieu du véritable bénéficiaire. Pratique courante dans les structures offshore. Indicateur d'opacité actionnariale."),
    ("Correspondent banking", "typologies", "Relations entre banques correspondantes permettant d'effectuer des paiements internationaux. Vecteur historique de blanchiment (cas BCCI, Riggs Bank). Obligations renforcées sous AMLD et FATF Rec. 13."),
    ("Hawalas", "typologies", "Système de transfert de fonds informel, fondé sur la confiance et un réseau de courtiers (hawaladars), sans mouvement physique d'argent. Utilisé légitimement pour remises familiales, aussi vecteur de financement du terrorisme."),
    ("Mules financières", "typologies", "Personnes recrutées pour transférer des fonds illicites sur leurs comptes personnels, en échange d'une commission. Souvent recrutées via des arnaques emploi. Victimes ET complices juridiquement selon les circonstances."),
    ("Real estate money laundering", "typologies", "Blanchiment par l'immobilier : achat/vente de biens pour réinjecter des fonds illicites. Secteur à risque élevé en France. Exige des vérifications renforcées sur l'origine des fonds dans les transactions immobilières significatives."),
    ("Crypto-asset related ML", "typologies", "Blanchiment via actifs numériques : mixers, chain hopping, DEX non-KYC. Le cadre MiCA et la directive TFR imposent des obligations LCB-FT aux PSAN/CASP. Technique d'analyse : blockchain analytics (Chainalysis, Elliptic)."),
    # Marchés financiers
    ("Délit d'initié", "marches", "Infraction consistant à utiliser une information privilégiée pour effectuer ou faire effectuer des transactions sur des instruments financiers. Art. L.465-1 Code pénal, Art. 7-8 MAR. Peine : 2 à 7 ans d'emprisonnement + amendes."),
    ("Information privilégiée", "marches", "Information précise, non publique, susceptible d'avoir une influence significative sur le cours d'un instrument financier. Les personnes y ayant accès sont des initiés et doivent s'abstenir de toute transaction sur l'instrument concerné."),
    ("Liste d'initiés", "marches", "Liste des personnes ayant accès aux informations privilégiées d'un émetteur, tenue à jour par ce dernier et ses conseils. Obligation légale (Art. 18 MAR, Art. L.621-18-4 CMF). Doit être communiquée à l'AMF sur demande."),
    ("Manipulation de cours", "marches", "Comportements artificiellement influençant le cours d'un instrument : diffusion d'informations fausses, transactions fictives, spoofing, layering. Art. 12 MAR. Infraction pénale : L.465-3-1 CMF."),
    ("Spoofing", "marches", "Technique de manipulation consistant à placer de gros ordres sans intention de les exécuter pour créer une fausse impression de liquidité ou d'intérêt, puis les annuler. Infraction sous MAR et CFTC (USA)."),
    ("Layering (marchés)", "marches", "Sur les marchés financiers, technique consistant à placer plusieurs ordres à des niveaux de prix différents pour créer un carnet d'ordres artificiel, puis les annuler après avoir exécuté une transaction en sens inverse. Forme de spoofing."),
    ("Marking the close", "marches", "Manipulation de cours en fin de séance pour influencer le cours de clôture, utilisé comme référence pour des évaluations ou des produits dérivés. Signal détectable par analyse de volume et impact cours en fin de session."),
    ("Front running", "marches", "Pratique consistant, pour un intermédiaire, à effectuer des transactions pour son propre compte avant d'exécuter un ordre client dont il connaît l'impact probable sur le cours. Infraction et conflit d'intérêts."),
    ("Pump and dump", "marches", "Schéma de manipulation : acheter massivement un titre peu liquide, diffuser des informations positives fausses pour en faire monter le cours, puis vendre avec profit. Fréquent sur les penny stocks et cryptomonnaies."),
    ("Cross-market manipulation", "marches", "Manipulation utilisant deux marchés liés (ex : action + dérivé sur l'action) : manipuler le cours de l'action pour influencer un produit dérivé ou vice versa. Nécessite une surveillance cross-market coordonnée."),
    # Surveillance et contrôles
    ("Approche fondée sur les risques (Risk-Based Approach)", "controles", "Principe fondateur LCB-FT : adapter l'intensité des mesures de vigilance au niveau de risque identifié. Les ressources sont concentrées là où le risque est le plus élevé. Base de l'ensemble des recommandations GAFI et directives AMLD."),
    ("Profil de risque client", "controles", "Évaluation documentée du risque présenté par un client, combinant risque pays, risque sectoriel, risque lié au type de client, et risque lié aux opérations attendues. Mis à jour périodiquement et lors d'événements déclencheurs."),
    ("Classification des risques", "controles", "Obligation pour les entités assujetties de classer leurs clients en niveaux de risque (standard/élevé) selon des critères définis. En France, encadrée par l'art. L.561-4-1 CMF et l'arrêté du 6 janvier 2021."),
    ("Surveillance continue (ongoing monitoring)", "controles", "Obligation de surveiller en permanence la relation d'affaires, de vérifier la cohérence des opérations avec le profil client, et de mettre à jour les informations KYC. Art. L.561-8 CMF. Fréquence proportionnelle au risque."),
    ("Scoring de risque", "controles", "Attribution d'un score numérique de risque à un client ou une opération, sur la base de critères pondérés. Permet d'automatiser la priorisation des dossiers. Le modèle doit être documenté, expliqué, et révisé régulièrement."),
    ("Fuzzy matching / Correspondance floue", "controles", "Algorithme permettant d'identifier des correspondances approximatives entre des noms (tolérant erreurs orthographiques, translittérations, variations). Clé pour le screening de sanctions. Distance de Levenshtein, algorithme de Jaro-Winkler fréquemment utilisés."),
    ("Faux positif (false positive)", "controles", "Alerte générée par le système de screening sur une entité qui n'est pas en réalité dans une liste de sanctions ou une base PPE. Le traitement des faux positifs consomme des ressources importantes. Taux cible : < 3%."),
    ("Vrai positif (true positive)", "controles", "Hit confirmé : correspondance identifiée par le screening qui s'avère réelle après analyse manuelle. Chaque vrai positif doit faire l'objet d'une action documentée (gel d'avoirs, refus, escalade, déclaration soupçon)."),
    ("STOR — Suspicious Transaction Report", "controles", "Rapport d'opération suspecte sur les marchés financiers, adressé à l'AMF. Distinct de la déclaration de soupçon TRACFIN. Obligation issue de l'Art. 16 MAR. Le délai est immédiat dès le soupçon raisonnable."),
    ("Gel d'avoirs", "controles", "Mesure préventive consistant à bloquer les fonds et ressources économiques d'une personne ou entité sanctionnée. En France : art. L.562-4-1 CMF. Obligation de résultat : tout manquement expose l'établissement à des sanctions."),
    # Structures et instruments
    ("Trust / Fiducie", "structures", "Structure juridique par laquelle un constituant transfère des actifs à un trustee pour le bénéfice de bénéficiaires. Risque LCB-FT élevé car peut masquer les bénéficiaires effectifs. AMLD5 impose l'identification des bénéficiaires des trusts."),
    ("Fondation privée", "structures", "Personne morale sans associés, avec un patrimoine dédié à un but. Utilisée dans la planification successorale et patrimoniale mais peut être vecteur d'opacité. Régimes varient (Liechtenstein, Panama, Suisse)."),
    ("SPV — Special Purpose Vehicle", "structures", "Entité créée pour un objet limité (titrisation, financement de projet). Pas d'activité opérationnelle. Le suivi LCB-FT requiert d'identifier le groupe initiateur et les investisseurs bénéficiaires."),
    ("Free zones / Zones franches", "structures", "Zones géographiques à régulation allégée (fiscalité, douanes). Certaines zones franches sont des vecteurs reconnus de TBML et de financement de la prolifération. GAFI les identifie comme zones à risque élevé."),
    ("Compte de passage (Payable Through Account)", "structures", "Compte de correspondant bancaire permettant à des sous-clients étrangers d'accéder directement aux services. Vecteur à risque élevé, limité sous AMLD et FATF Rec. 13."),
    ("Netting / Compensation multilatérale", "structures", "Mécanisme de compensation entre flux financiers réciproques. Dans le contexte TBML, le netting informel entre hawaladars est un vecteur classique. Dans les marchés : mécanisme légitime mais nécessitant surveillance."),
    # Technologies et outils
    ("Blockchain analytics", "tech", "Analyse des transactions sur les blockchains publiques pour tracer les flux de cryptomonnaies. Outils : Chainalysis, Elliptic, Crystal. Permet d'identifier les wallets associés à des exchanges non-KYC, mixers, darknets."),
    ("Transaction Monitoring System (TMS)", "tech", "Système informatique surveillant les transactions en temps réel ou batch pour détecter des patterns suspects. Génère des alertes soumises aux analystes. Paramétrage des règles crucial pour éviter sur/sous-détection."),
    ("RegTech", "tech", "Technologies appliquées à la conformité réglementaire. Inclut l'automatisation du KYC (eKYC), le monitoring, le reporting réglementaire. Marché en forte croissance sous pression des exigences réglementaires croissantes."),
    ("eKYC — Electronic KYC", "tech", "Processus KYC dématérialisé : vérification d'identité à distance via vidéo, OCR de documents, face matching, signature électronique. Encadré par la réglementation eIDAS en Europe."),
    ("NLP — Natural Language Processing", "tech", "Traitement automatique du langage naturel, utilisé en LCB-FT pour l'adverse media screening (analyse automatique de milliers d'articles de presse), la classification de risque, et l'extraction d'entités nommées."),
    ("Machine Learning en LCB-FT", "tech", "Algorithmes supervisés (classification fraude/non-fraude) et non supervisés (détection d'anomalies) pour améliorer la détection. Réduit les faux positifs vs règles statiques. Exige gouvernance, auditabilité, et recette avant mise en production."),
    ("OCR — Optical Character Recognition", "tech", "Reconnaissance optique de caractères pour extraire les données de documents scannnés (Kbis, CNI, passeports). Brique technique du pipeline KYC pour automatiser la saisie et la vérification des données."),
    ("API REST en compliance", "tech", "Interface de programmation permettant d'interroger des bases de données en temps réel (sanctions, registres, adverse media). Architecture standard des pipelines KYC modernes. Permet l'intégration dans le SI de l'établissement."),
    # Gouvernance
    ("Responsable conformité (RCCI/RCSI)", "gouvernance", "Responsable du Contrôle de la Conformité et des Investissements (RCCI pour sociétés de gestion) ou des Services d'Investissement (RCSI). Dirige le dispositif LCB-FT, est le garant de la conformité réglementaire auprès du superviseur."),
    ("Déclarant désigné TRACFIN", "gouvernance", "Personne physique désignée par l'entité assujettie pour effectuer les déclarations de soupçon auprès de TRACFIN. Art. R.561-23 CMF. Distinct du responsable conformité (peut être la même personne)."),
    ("Correspondant LCB-FT", "gouvernance", "Personne désignée dans chaque entité ou agence pour être l'interlocuteur du dispositif LCB-FT. Obligatoire dans les groupes. Art. L.561-4-2 CMF."),
    ("Tone from the top", "gouvernance", "Culture de conformité impulsée par la direction générale et le conseil d'administration. Le GAFI et les superviseurs considèrent que l'implication active du management est un facteur clé d'efficacité du dispositif."),
    ("Contrôle permanent", "gouvernance", "Contrôle exercé en continu sur les procédures et opérations, par les opérationnels eux-mêmes (contrôle de 1er niveau) et par la fonction conformité (contrôle de 2ème niveau). Distinct du contrôle périodique (audit interne)."),
    ("Contrôle périodique", "gouvernance", "Contrôle exercé par l'audit interne (3ème niveau) sur l'efficacité du dispositif de conformité. Revue indépendante, périodicité définie par la réglementation et la cartographie des risques."),
    ("Cartographie des risques LCB-FT", "gouvernance", "Document fondamental du dispositif : identification et évaluation des risques de blanchiment et de financement du terrorisme pesant sur l'entité. Base de la classification des clients et du paramétrage du monitoring. Art. L.561-4-1 CMF."),
    ("MLA — Mutual Legal Assistance", "gouvernance", "Entraide judiciaire internationale permettant l'échange d'informations entre autorités de pays différents dans le cadre d'enquêtes financières. Essentielle pour les affaires cross-border."),
    # Sanctions et pénalités
    ("Sanctions ACPR", "sanctions", "L'ACPR peut prononcer : avertissement, blâme, interdiction d'exercer, sanction pécuniaire jusqu'à 100 M€ ou 10% du CA. Les décisions sont publiées (name and shame). Revue des décisions ACPR : source clé de typologies."),
    ("Name and shame", "sanctions", "Publication des décisions de sanctions par les régulateurs (ACPR, AMF, CNIL). Outil de dissuasion. En France, l'ACPR publie systématiquement ses décisions sur son site. Les établissements y sont très sensibles."),
    ("DPA — Deferred Prosecution Agreement", "sanctions", "Accord entre le parquet et une personne morale suspendant les poursuites en échange d'engagements (amende, programme de mise en conformité, moniteur indépendant). Pratique américaine (DOJ) qui se répand en Europe (CJIP en France)."),
    ("CJIP — Convention Judiciaire d'Intérêt Public", "sanctions", "Équivalent français du DPA. Permet au Parquet National Financier (PNF) de conclure avec une personne morale un accord incluant amendes, indemnisation des victimes, programme de conformité. Cas emblématiques : Airbus, Total, Goldman Sachs."),
    ("Correspondant monitor", "sanctions", "Expert indépendant nommé dans le cadre d'un DPA/CJIP pour superviser la mise en œuvre du programme de conformité imposé à l'entreprise. Reporte directement aux autorités."),
    ("FATF/GAFI grey list", "sanctions", "Liste des pays sous surveillance renforcée du GAFI pour insuffisances dans leur dispositif LCB-FT. Les établissements doivent appliquer une vigilance renforcée sur les relations avec ces pays. Mise à jour 3 fois par an."),
    ("FATF/GAFI black list", "sanctions", "Liste des pays à haut risque (Iran, Corée du Nord). Appelle des contre-mesures renforcées. Les établissements doivent appliquer des mesures proportionnelles aux risques spécifiques."),
    # Produits et secteurs à risque
    ("PSAN — Prestataire de Services sur Actifs Numériques", "secteurs", "Catégorie réglementaire française (Loi PACTE 2019) pour les acteurs du secteur crypto. Soumis aux obligations LCB-FT depuis 2020 (enregistrement ACPR obligatoire). En cours d'harmonisation avec MiCA au niveau européen."),
    ("MiCA — Markets in Crypto-Assets Regulation", "secteurs", "Règlement européen (UE) 2023/1114 encadrant les émetteurs d'actifs numériques et les CASP (Crypto-Asset Service Providers). En vigueur depuis 2024. Impose des exigences LCB-FT harmonisées au niveau UE."),
    ("Secteur immobilier (obligations LCB-FT)", "secteurs", "Notaires, agents immobiliers, et autres acteurs sont assujettis LCB-FT depuis AMLD3. Obligés de vérifier l'identité des parties et l'origine des fonds. Secteur à risque élevé selon TRACFIN."),
    ("Jeux et paris (obligations LCB-FT)", "secteurs", "Casinos et opérateurs de jeux en ligne assujettis LCB-FT. Seuils de déclaration spécifiques. FDJ et PMU soumis à des obligations adaptées. Risque lié à l'utilisation de gains légaux pour justifier des fonds illicites."),
    ("Financement du commerce (Trade Finance)", "secteurs", "Crédits documentaires, lettres de crédit. Vecteur à risque de TBML. Le GAFI a publié des orientations spécifiques. Nécessite une vigilance sur les factures, les biens, et la cohérence des prix avec les standards du marché."),
    # Concepts avancés
    ("De-risking", "avance", "Pratique par laquelle des banques mettent fin à des relations d'affaires avec certaines catégories de clients jugées trop risquées (MSB, correspondants dans certains pays, ONG...). Phénomène préoccupant car il pousse certains flux vers des canaux non surveillés."),
    ("Correspondent banking de-risking", "avance", "Retrait de grandes banques internationales des relations de correspondant avec des banques de pays à risque élevé. Impact sur les remises de la diaspora, le financement du commerce. Thème de discussion au GAFI et FSB."),
    ("FinCEN Files", "avance", "Investigation journalistique (2020) basée sur des SARs (Suspicious Activity Reports) américains ayant fuité. A révélé que certaines grandes banques continuaient à traiter des transactions suspectes malgré des signaux d'alerte. Impact sur les exigences de surveillance."),
    ("Évaluation nationale des risques (ENR)", "avance", "Exercice conduit par les États pour identifier et évaluer les risques de blanchiment et de financement du terrorisme sur leur territoire. La France publie régulièrement son ENR. Sert de référence pour les cartographies des risques sectorielles."),
    ("Prédiction conforme (Conformal Prediction)", "avance", "Méthode statistique permettant de quantifier l'incertitude des prédictions d'un modèle ML avec des garanties théoriques. Appliquée au scoring LCB-FT, elle fournit des intervalles de confiance sur les scores de risque, améliorant l'auditabilité."),
    ("Explication des décisions IA (XAI)", "avance", "Ensemble de méthodes permettant de rendre interprétables les décisions de modèles ML (SHAP values, LIME). Crucial en LCB-FT : les régulateurs exigent que les décisions automatisées soient explicables et auditables."),
    ("Regulatory sandbox", "avance", "Environnement contrôlé permettant à des innovateurs (fintech, regtech) de tester de nouveaux produits ou services en bénéficiant d'un régime réglementaire allégé. L'ACPR et l'AMF disposent d'un programme conjoint (Fintech Forum)."),
    ("SecNumCloud", "avance", "Qualification française (ANSSI) pour les services cloud destinés aux données sensibles. Assure une immunité au droit extra-européen. Certains établissements exigent un hébergement SecNumCloud pour les données de KYC. Mistral AI propose cette option."),
    ("eIDAS 2.0 / EUDI Wallet", "avance", "Révision du règlement européen sur l'identité numérique. Le portefeuille européen d'identité numérique (EUDI Wallet) permettra à chaque citoyen de présenter ses attributs d'identité de manière sélective. Impact majeur attendu sur le KYC à distance d'ici 2026-2027."),
    ("OID4VP — OpenID for Verifiable Presentations", "avance", "Protocole permettant à un portefeuille d'identité numérique de présenter des attestations vérifiables à un service en ligne. Standard ouvert pour le raccordement entre wallet citoyen (France Identité, EUDI) et pipeline KYC d'un établissement."),
]

CATEGORIES = {
    "lcb-ft": ("🏦 Fondamentaux LCB-FT", "#00D4AA"),
    "reglementation": ("⚖️ Réglementation", "#FF6B35"),
    "typologies": ("🔎 Typologies de blanchiment", "#9B59B6"),
    "marches": ("📈 Marchés financiers & abus", "#3498DB"),
    "controles": ("🛡️ Surveillance & contrôles", "#E74C3C"),
    "structures": ("🏗️ Structures & instruments", "#F39C12"),
    "tech": ("💻 Technologies & outils", "#1ABC9C"),
    "gouvernance": ("🏛️ Gouvernance", "#95A5A6"),
    "sanctions": ("⚠️ Sanctions & pénalités", "#E67E22"),
    "secteurs": ("🏭 Secteurs à risque", "#2ECC71"),
    "avance": ("🚀 Concepts avancés", "#8E44AD"),
}

def show():
    st.markdown("## 📚 100 Concepts essentiels LCB-FT & Marchés Financiers")
    st.markdown("<div style='color: #7A8BA6; margin-bottom: 1.5rem;'>Glossaire éducatif complet — De la définition de base aux concepts avancés de conformité</div>", unsafe_allow_html=True)

    # Stats
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"""<div class='metric-card'><div class='metric-value'>{len(CONCEPTS)}</div><div class='metric-label'>Concepts définis</div></div>""", unsafe_allow_html=True)
    with col2:
        st.markdown(f"""<div class='metric-card'><div class='metric-value'>{len(CATEGORIES)}</div><div class='metric-label'>Catégories</div></div>""", unsafe_allow_html=True)
    with col3:
        st.markdown(f"""<div class='metric-card'><div class='metric-value'>CMF</div><div class='metric-label'>Droit de référence</div></div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Search
    search = st.text_input("🔍 Rechercher un concept", placeholder="Ex: TRACFIN, PPE, spoofing, UBO...")

    # Category filter
    cat_options = ["Toutes les catégories"] + [v[0] for v in CATEGORIES.values()]
    cat_selected = st.selectbox("Filtrer par catégorie", cat_options, label_visibility="visible")

    # Filter concepts
    filtered = []
    for (title, cat, definition) in CONCEPTS:
        cat_label, _ = CATEGORIES[cat]
        if search and search.lower() not in title.lower() and search.lower() not in definition.lower():
            continue
        if cat_selected != "Toutes les catégories" and cat_label != cat_selected:
            continue
        filtered.append((title, cat, definition))

    st.markdown(f"<div style='font-size: 0.8rem; color: #7A8BA6; margin-bottom: 1rem;'>{len(filtered)} concept(s) affiché(s)</div>", unsafe_allow_html=True)

    # Group by category
    by_cat = {}
    for (title, cat, definition) in filtered:
        if cat not in by_cat:
            by_cat[cat] = []
        by_cat[cat].append((title, definition))

    num = 1
    for cat_key, items in by_cat.items():
        cat_label, cat_color = CATEGORIES[cat_key]
        st.markdown(f"<div style='font-size: 0.85rem; font-weight: 700; color: {cat_color}; text-transform: uppercase; letter-spacing: 1.5px; margin-top: 1.5rem; margin-bottom: 0.8rem; padding-bottom: 0.4rem; border-bottom: 1px solid #1E3055;'>{cat_label}</div>", unsafe_allow_html=True)

        for title, definition in items:
            with st.expander(f"**{num:03d}. {title}**"):
                st.markdown(f"""
                <div style='font-size: 0.88rem; color: #E8EDF5; line-height: 1.7;'>{definition}</div>
                <div style='margin-top: 0.8rem;'>
                    <span class='source-pill'>{CATEGORIES[cat_key][0]}</span>
                </div>
                """, unsafe_allow_html=True)
            num += 1
