import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import random

try:
    import plotly.graph_objects as go
    HAS_PLOTLY = True
except ImportError:
    HAS_PLOTLY = False

def show():
    st.markdown("""
    <div class='main-header'>
        <div style='font-size: 1.8rem; font-weight: 700; color: #E8EDF5;'>Tableau de bord <span style='color: #00D4AA;'>KYC / LCB-FT</span></div>
        <div style='font-size: 0.85rem; color: #7A8BA6; margin-top: 0.3rem;'>Vue consolidée · Conformité financière · """ + datetime.now().strftime('%d %B %Y') + """</div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3, col4, col5 = st.columns(5)
    metrics = [
        ("47", "Dossiers en cours"),
        ("3", "Escalades actives"),
        ("92%", "Taux de complétion"),
        ("12", "Alertes sanctions"),
        ("2.1%", "Taux faux positifs"),
    ]
    for col, (val, label) in zip([col1, col2, col3, col4, col5], metrics):
        with col:
            st.markdown(f"""
            <div class='metric-card'>
                <div class='metric-value'>{val}</div>
                <div class='metric-label'>{label}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    col_left, col_right = st.columns([3, 2])

    with col_left:
        st.markdown("<div class='section-title'>Activité des dossiers — 30 jours</div>", unsafe_allow_html=True)
        dates = [datetime.now() - timedelta(days=i) for i in range(29, -1, -1)]
        vals = [random.randint(2, 12) for _ in dates]
        escalades = [random.randint(0, 3) for _ in dates]

        if HAS_PLOTLY:
            import plotly.graph_objects as go
            fig = go.Figure()
            fig.add_trace(go.Bar(x=dates, y=vals, name='Dossiers traités',
                marker_color='rgba(0,212,170,0.6)', marker_line_color='#00D4AA', marker_line_width=1))
            fig.add_trace(go.Scatter(x=dates, y=escalades, name='Escalades',
                line=dict(color='#FF6B35', width=2), mode='lines+markers', marker=dict(size=4)))
            fig.update_layout(
                plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
                font_color='#7A8BA6', height=280,
                margin=dict(t=10, b=10, l=10, r=10),
                legend=dict(bgcolor='rgba(0,0,0,0)', font=dict(color='#E8EDF5', size=11)),
                xaxis=dict(gridcolor='#1E3055', linecolor='#1E3055'),
                yaxis=dict(gridcolor='#1E3055', linecolor='#1E3055'),
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            df_chart = pd.DataFrame({'Date': dates, 'Dossiers': vals, 'Escalades': escalades})
            st.line_chart(df_chart.set_index('Date'))

    with col_right:
        st.markdown("<div class='section-title'>Répartition des risques</div>", unsafe_allow_html=True)
        if HAS_PLOTLY:
            import plotly.graph_objects as go
            fig2 = go.Figure(data=[go.Pie(
                labels=['Risque FAIBLE', 'Risque MOYEN', 'Risque ÉLEVÉ', 'En attente'],
                values=[28, 12, 4, 3], hole=0.65,
                marker=dict(colors=['#00D4AA', '#FFB347', '#FF4757', '#7A8BA6']),
                textfont=dict(color='white'),
            )])
            fig2.update_layout(
                plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
                font_color='#E8EDF5', height=280,
                margin=dict(t=10, b=10, l=10, r=10),
                legend=dict(bgcolor='rgba(0,0,0,0)', font=dict(color='#E8EDF5', size=10)),
                annotations=[dict(text='47<br>dossiers', x=0.5, y=0.5, font_size=14,
                    showarrow=False, font_color='#E8EDF5')]
            )
            st.plotly_chart(fig2, use_container_width=True)
        else:
            st.dataframe(pd.DataFrame({
                'Niveau': ['FAIBLE','MOYEN','ÉLEVÉ','En attente'],
                'Dossiers': [28, 12, 4, 3]
            }), hide_index=True, use_container_width=True)

    st.markdown("<div class='section-title'>Derniers dossiers traités</div>", unsafe_allow_html=True)
    df = pd.DataFrame({
        'Société': ['Alpha Invest SAS', 'BetaCorp SARL', 'Gamma Holdings', 'Delta Finance SA', 'Epsilon Conseil'],
        'SIREN': ['842156789', '731245678', '912345678', '654321987', '789456123'],
        'Date': ['30/05/2026', '29/05/2026', '28/05/2026', '27/05/2026', '26/05/2026'],
        'Risque': ['🟡 MOYEN', '🟢 FAIBLE', '🔴 ÉLEVÉ', '🟡 MOYEN', '🟢 FAIBLE'],
        'Statut': ['En cours', 'Validé', 'Escalade', 'Validé', 'Validé'],
        'Analyste': ['M. Dupont', 'S. Martin', 'A. Leblanc', 'M. Dupont', 'S. Martin'],
        'Screening': ['✅ Clear', '✅ Clear', '⚠️ Hit potentiel', '✅ Clear', '✅ Clear'],
    })
    st.dataframe(df, use_container_width=True, hide_index=True)

    st.markdown("<br>", unsafe_allow_html=True)
    col_a, col_b = st.columns(2)

    with col_a:
        st.markdown("<div class='section-title'>⚠️ Alertes actives</div>", unsafe_allow_html=True)
        for icon, title, desc in [
            ("🔴", "Gamma Holdings — Hit sanctions ONU", "Examen renforcé requis — L.561-10 CMF"),
            ("🟡", "3 dossiers — Bénéficiaires effectifs manquants", "Délai de relance dépassé"),
            ("🟡", "Alpha Invest — Origine des fonds non justifiée", "En attente de pièces complémentaires"),
        ]:
            color = "#FF4757" if icon == "🔴" else "#FFB347"
            st.markdown(f"""
            <div style='background:rgba(255,255,255,0.03);border-left:3px solid {color};border-radius:0 8px 8px 0;padding:0.8rem 1rem;margin-bottom:0.5rem;'>
                <div style='font-size:0.9rem;font-weight:600;color:#E8EDF5;'>{icon} {title}</div>
                <div style='font-size:0.78rem;color:#7A8BA6;margin-top:0.2rem;'>{desc}</div>
            </div>""", unsafe_allow_html=True)

    with col_b:
        st.markdown("<div class='section-title'>📋 Actions requises</div>", unsafe_allow_html=True)
        for entity, action, deadline, color in [
            ("Gamma Holdings", "Décision TRACFIN", "Urgent", "#FF4757"),
            ("Alpha Invest", "Relance pièces KYC", "Cette semaine", "#FFB347"),
            ("7 dossiers", "Revue annuelle due diligence", "Ce mois", "#7A8BA6"),
            ("Dispositif LCB-FT", "Mise à jour grille scoring ACPR", "Q3 2026", "#7A8BA6"),
        ]:
            st.markdown(f"""
            <div style='background:rgba(255,255,255,0.03);border-radius:8px;padding:0.8rem 1rem;margin-bottom:0.5rem;'>
                <div style='font-size:0.88rem;font-weight:600;color:#E8EDF5;'>{entity}</div>
                <div style='font-size:0.78rem;color:#7A8BA6;'>{action} — <span style='color:{color};font-weight:600;'>{deadline}</span></div>
            </div>""", unsafe_allow_html=True)
