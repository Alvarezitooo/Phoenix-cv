"""
🚀 PHOENIX CV - VERSION PREMIUM ENRICHIE
Point d'entrée principal avec fonctionnalités avancées
Aligné avec Phoenix Letters - UI Moderne - Services Premium
"""

import os
import streamlit as st
from core.app_core import main_secure, render_security_dashboard, run_security_tests

# Configuration Streamlit moderne
st.set_page_config(
    page_title="🚀 Phoenix CV - Générateur IA Premium",
    page_icon="🔥",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://phoenix-ecosystem.com/support',
        'Report a bug': 'https://phoenix-ecosystem.com/bug-report',
        'About': "🚀 Phoenix CV - Générateur CV IA pour Reconversions Professionnelles"
    }
)

# CSS moderne aligné avec Phoenix Letters
st.markdown("""
<style>
    /* Thème Phoenix moderne */
    .main > div {
        padding-top: 2rem;
    }
    
    .stApp > header {
        background-color: transparent;
    }
    
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    .block-container {
        padding-top: 3rem;
        background: white;
        border-radius: 15px;
        margin: 1rem;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
    }
    
    /* Boutons Phoenix style */
    .stButton > button {
        background: linear-gradient(45deg, #ff7a00, #ff0040);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 0.5rem 2rem;
        font-weight: bold;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(255, 122, 0, 0.4);
    }
    
    /* Métriques modernes */
    div[data-testid="metric-container"] {
        background: linear-gradient(45deg, #f8f9fa, #ffffff);
        border: 1px solid #e9ecef;
        padding: 1rem;
        border-radius: 10px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    }
    
    /* Sidebar Phoenix */
    .css-1d391kg {
        background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
    }
    
    /* Success/Warning modernes */
    .stSuccess {
        background: linear-gradient(45deg, #28a745, #34ce57);
        border-radius: 10px;
    }
    
    .stWarning {
        background: linear-gradient(45deg, #ffc107, #ffed4a);
        border-radius: 10px;
    }
</style>
""", unsafe_allow_html=True)

if __name__ == "__main__":
    # Mode de développement avec fonctionnalités étendues
    mode = os.environ.get('PHOENIX_MODE', 'production')
    
    if mode == 'security_dashboard':
        render_security_dashboard()
    elif mode == 'security_tests':
        run_security_tests()
    elif mode == 'demo':
        st.info("🎯 Mode Démo - Fonctionnalités limitées pour présentation")
        main_secure()
    else:
        # Mode production avec UI moderne
        main_secure()