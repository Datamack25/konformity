# 🛡️ KYC Compliance Platform

Pipeline KYC souverain · LCB-FT · Marchés Financiers

## Installation

```bash
git clone <votre-repo>
cd kyc-platform
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

## Variables d'environnement (`.env`)

```
MISTRAL_API_KEY=votre_clé_mistral
PAPPERS_API_KEY=votre_clé_pappers
```

## Structure

```
kyc-platform/
├── app.py                    # Point d'entrée Streamlit
├── requirements.txt
├── pages/
│   ├── dashboard.py          # Tableau de bord
│   ├── screening.py          # Screening KYC interactif
│   ├── sources.py            # Catalogue sources OSINT + explorateur CSV
│   ├── case_analysis.py      # Méthodes d'analyse par type de cas
│   ├── concepts.py           # 100 concepts LCB-FT / marchés
│   ├── pipeline.py           # Architecture technique pipeline souverain
│   └── pdf_report.py         # Générateur note d'escalade PDF
└── data/
    ├── codes_naf_risque.csv         # 68 codes NAF avec scoring risque
    ├── pays_risque_gafi.csv         # 57 pays avec statut GAFI / sanctions
    ├── codes_nace_europe.csv        # 23 codes NACE harmonisés UE
    ├── historique_screenings.csv    # Log des recherches effectuées
    ├── registre_dossiers_kyc.csv    # Registre des dossiers ouverts
    ├── typologies_blanchiment.csv   # 15 typologies TRACFIN/GAFI
    ├── sources_sanctions.csv        # 14 sources de sanctions référencées
    └── regles_scoring_lcbft.csv     # 12 règles de scoring CMF
```

## Sources intégrées

- **Pappers** — Registres officiels INSEE/INPI/BODACC
- **OpenSanctions** — 70 000+ entités sanctionnées (local)
- **ComplyAdvantage** — PPE + adverse media
- **DGT Gels d'avoirs** — Sanctions françaises
- **OFAC SDN** — Sanctions américaines
- **UE PESC** — Sanctions européennes
- **France Identité** — Justificatif d'identité numérique souverain
- **ICIJ Offshore Leaks** — Panama/Pandora Papers

## Licence

Apache-2.0 — Inspiré du template KYC Screener d'Anthropic
