"""
🚀 Enhanced UI Components - Phoenix CV
Composants modernes alignés avec Phoenix Letters
"""

import streamlit as st
from typing import Dict, List, Optional, Any
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime

class PhoenixCVUI:
    """Composants UI modernes pour Phoenix CV"""
    
    @staticmethod
    def render_modern_header():
        """Header moderne aligné avec Phoenix Letters"""
        st.markdown("""
        <div style="background: linear-gradient(90deg, #ff7a00 0%, #ff0040 100%); padding: 20px; border-radius: 10px; margin-bottom: 30px;">
            <div style="text-align: center; color: white;">
                <h1 style="margin: 0; font-size: 3em; text-shadow: 2px 2px 4px rgba(0,0,0,0.3);">
                    🔥 PHOENIX CV
                </h1>
                <h3 style="margin: 10px 0 0 0; opacity: 0.9;">
                    Générateur CV IA pour Reconversions Professionnelles
                </h3>
                <div style="margin-top: 15px;">
                    <span style="background: rgba(255,255,255,0.2); padding: 5px 15px; border-radius: 20px; margin: 0 5px; font-size: 0.9em;">
                        🤖 IA Avancée
                    </span>
                    <span style="background: rgba(255,255,255,0.2); padding: 5px 15px; border-radius: 20px; margin: 0 5px; font-size: 0.9em;">
                        🎯 ATS Optimisé
                    </span>
                    <span style="background: rgba(255,255,255,0.2); padding: 5px 15px; border-radius: 20px; margin: 0 5px; font-size: 0.9em;">
                        🛡️ Sécurisé
                    </span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    @staticmethod
    def render_progress_indicator(current_step: int, total_steps: int, step_names: List[str]):
        """Indicateur de progression moderne"""
        progress = current_step / total_steps
        
        st.markdown("""
        <style>
        .progress-container {
            background: #f0f2f6;
            border-radius: 10px;
            padding: 20px;
            margin: 20px 0;
        }
        .progress-bar {
            background: linear-gradient(90deg, #ff7a00, #ff0040);
            height: 8px;
            border-radius: 4px;
            transition: width 0.3s ease;
        }
        .step-indicator {
            display: flex;
            justify-content: space-between;
            margin-top: 10px;
        }
        .step {
            text-align: center;
            flex: 1;
        }
        .step.active {
            color: #ff7a00;
            font-weight: bold;
        }
        .step.completed {
            color: #28a745;
        }
        </style>
        """, unsafe_allow_html=True)
        
        progress_html = f"""
        <div class="progress-container">
            <div style="background: #e9ecef; height: 8px; border-radius: 4px;">
                <div class="progress-bar" style="width: {progress*100}%;"></div>
            </div>
            <div class="step-indicator">
        """
        
        for i, step_name in enumerate(step_names):
            if i < current_step:
                class_name = "step completed"
                icon = "✅"
            elif i == current_step:
                class_name = "step active"
                icon = "🔄"
            else:
                class_name = "step"
                icon = "⏳"
            
            progress_html += f'<div class="{class_name}">{icon} {step_name}</div>'
        
        progress_html += """
            </div>
        </div>
        """
        
        st.markdown(progress_html, unsafe_allow_html=True)
    
    @staticmethod
    def render_feature_card(title: str, description: str, icon: str, is_premium: bool = False):
        """Carte de fonctionnalité moderne"""
        premium_badge = """
        <span style="background: linear-gradient(45deg, #ffd700, #ffed4e); color: #000; padding: 2px 8px; border-radius: 10px; font-size: 0.7em; font-weight: bold; margin-left: 10px;">
            ⭐ PREMIUM
        </span>
        """ if is_premium else ""
        
        st.markdown(f"""
        <div style="background: white; border: 2px solid #e9ecef; border-radius: 15px; padding: 20px; margin: 10px 0; box-shadow: 0 4px 6px rgba(0,0,0,0.1); transition: transform 0.2s;">
            <h4 style="margin: 0 0 10px 0; color: #333;">
                {icon} {title} {premium_badge}
            </h4>
            <p style="margin: 0; color: #666; line-height: 1.5;">
                {description}
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    @staticmethod
    def render_stats_dashboard(stats: Dict[str, Any]):
        """Dashboard de statistiques avec graphiques"""
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                label="🎯 Score ATS",
                value=f"{stats.get('ats_score', 0)}/100",
                delta=f"+{stats.get('ats_improvement', 0)}"
            )
        
        with col2:
            st.metric(
                label="📊 Sections Complétées",
                value=f"{stats.get('completed_sections', 0)}/8",
                delta=f"{stats.get('completion_rate', 0)}%"
            )
        
        with col3:
            st.metric(
                label="🔍 Mots-clés Détectés",
                value=stats.get('keywords_found', 0),
                delta=f"+{stats.get('keywords_added', 0)} ajoutés"
            )
        
        with col4:
            st.metric(
                label="⚡ Temps Génération",
                value=f"{stats.get('generation_time', 0)}s",
                delta=f"-{stats.get('time_saved', 0)}s optimisé"
            )
    
    @staticmethod
    def render_ats_analysis_chart(ats_data: Dict[str, float]):
        """Graphique d'analyse ATS moderne"""
        if not ats_data:
            return
        
        fig = go.Figure()
        
        categories = list(ats_data.keys())
        values = list(ats_data.values())
        
        # Graphique radar pour l'analyse ATS
        fig.add_trace(go.Scatterpolar(
            r=values,
            theta=categories,
            fill='toself',
            name='Score ATS',
            line_color='#ff7a00',
            fillcolor='rgba(255, 122, 0, 0.2)'
        ))
        
        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 100]
                )
            ),
            showlegend=False,
            title="📊 Analyse ATS - Compatibilité CV",
            title_x=0.5
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    @staticmethod
    def render_skill_distribution(skills_data: Dict[str, List[str]]):
        """Graphique de distribution des compétences"""
        if not skills_data:
            return
        
        # Préparation des données
        categories = []
        counts = []
        
        for category, skills in skills_data.items():
            categories.append(category)
            counts.append(len(skills))
        
        # Graphique en barres horizontal
        fig = px.bar(
            x=counts,
            y=categories,
            orientation='h',
            title="🎯 Distribution des Compétences par Catégorie",
            color=counts,
            color_continuous_scale='Oranges'
        )
        
        fig.update_layout(
            showlegend=False,
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    @staticmethod
    def render_success_message(message: str, details: Optional[str] = None):
        """Message de succès moderne"""
        details_html = f"<p style='margin: 10px 0 0 0; color: #666; font-size: 0.9em;'>{details}</p>" if details else ""
        
        st.markdown(f"""
        <div style="background: linear-gradient(45deg, #28a745, #34ce57); color: white; padding: 20px; border-radius: 10px; margin: 20px 0; box-shadow: 0 4px 6px rgba(40, 167, 69, 0.3);">
            <div style="display: flex; align-items: center;">
                <div style="font-size: 2em; margin-right: 15px;">🎉</div>
                <div>
                    <h4 style="margin: 0; font-weight: bold;">{message}</h4>
                    {details_html}
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    @staticmethod
    def render_warning_message(message: str, details: Optional[str] = None):
        """Message d'avertissement moderne"""
        details_html = f"<p style='margin: 10px 0 0 0; color: #856404; font-size: 0.9em;'>{details}</p>" if details else ""
        
        st.markdown(f"""
        <div style="background: linear-gradient(45deg, #ffc107, #ffed4a); color: #856404; padding: 20px; border-radius: 10px; margin: 20px 0; box-shadow: 0 4px 6px rgba(255, 193, 7, 0.3);">
            <div style="display: flex; align-items: center;">
                <div style="font-size: 2em; margin-right: 15px;">⚠️</div>
                <div>
                    <h4 style="margin: 0; font-weight: bold; color: #856404;">{message}</h4>
                    {details_html}
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    @staticmethod
    def render_info_panel(title: str, content: str, icon: str = "💡"):
        """Panneau d'information moderne"""
        st.markdown(f"""
        <div style="background: linear-gradient(45deg, #17a2b8, #20c997); color: white; padding: 20px; border-radius: 10px; margin: 15px 0;">
            <h4 style="margin: 0 0 10px 0; display: flex; align-items: center;">
                <span style="margin-right: 10px; font-size: 1.5em;">{icon}</span>
                {title}
            </h4>
            <p style="margin: 0; line-height: 1.6; opacity: 0.95;">
                {content}
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    @staticmethod
    def render_modern_footer():
        """Footer moderne aligné avec Phoenix Letters"""
        st.markdown("---")
        
        col1, col2, col3 = st.columns([2, 2, 1])
        
        with col1:
            st.markdown("""
            **🚀 Phoenix CV - Générateur Professionnel**
            
            • 🤖 IA de dernière génération
            • 🎯 Optimisation ATS avancée
            • 🛡️ Sécurité enterprise
            • 🔄 Support reconversions
            """)
        
        with col2:
            st.markdown("""
            **🌟 Fonctionnalités Premium**
            
            • 📊 Analyse détaillée
            • 🎨 Templates exclusifs  
            • ⚡ Génération rapide
            • 📈 Suivi performances
            """)
        
        with col3:
            if st.button("🚀 Upgrade Premium", type="primary", use_container_width=True):
                st.balloons()
                st.success("🎉 Redirection vers Phoenix Premium!")
        
        # Footer avec style moderne
        st.markdown("""
        <div style="text-align: center; margin-top: 40px; padding: 30px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 15px; color: white;">
            <h3 style="margin: 0 0 15px 0;">🔥 Phoenix Ecosystem</h3>
            <p style="margin: 0; opacity: 0.9;">
                La suite complète pour réussir votre reconversion professionnelle
            </p>
            <div style="margin-top: 20px;">
                <span style="background: rgba(255,255,255,0.2); padding: 8px 16px; border-radius: 20px; margin: 0 5px; font-size: 0.9em;">
                    🔥 Phoenix Letters
                </span>
                <span style="background: rgba(255,255,255,0.3); padding: 8px 16px; border-radius: 20px; margin: 0 5px; font-size: 0.9em;">
                    📄 Phoenix CV
                </span>
                <span style="background: rgba(255,255,255,0.2); padding: 8px 16px; border-radius: 20px; margin: 0 5px; font-size: 0.9em;">
                    🚀 Phoenix Rise
                </span>
            </div>
        </div>
        """, unsafe_allow_html=True)