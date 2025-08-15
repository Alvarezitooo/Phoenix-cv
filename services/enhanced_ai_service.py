"""
🚀 Enhanced AI Service - Phoenix CV
Service IA enrichi aligné avec Phoenix Letters
"""

import google.generativeai as genai
import streamlit as st
from typing import Dict, List, Optional, Any, Tuple
import json
import re
from datetime import datetime
import time
from models.cv_data import CVProfile, ATSAnalysis, CVTier
from utils.secure_validator import SecureValidator
from utils.secure_logging import SecureLogger

class EnhancedAIService:
    """Service IA enrichi pour Phoenix CV avec fonctionnalités avancées"""
    
    def __init__(self):
        self.logger = SecureLogger()
        self.validator = SecureValidator()
        self._initialize_gemini()
        
        # Compteurs pour analytics
        self.generation_stats = {
            'total_requests': 0,
            'successful_generations': 0,
            'failed_generations': 0,
            'avg_response_time': 0
        }
    
    def _initialize_gemini(self):
        """Initialise Gemini avec configuration sécurisée"""
        try:
            api_key = st.secrets.get("GEMINI_API_KEY")
            if not api_key:
                raise ValueError("GEMINI_API_KEY non configurée")
            
            genai.configure(api_key=api_key)
            self.model = genai.GenerativeModel('gemini-1.5-flash')
            
            # Configuration de sécurité
            self.safety_settings = [
                {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
                {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
                {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
                {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"}
            ]
            
        except Exception as e:
            self.logger.log_error(f"Erreur initialisation Gemini: {e}")
            raise
    
    def enhance_professional_summary(self, cv_profile: CVProfile, target_position: str = "") -> str:
        """Améliore le résumé professionnel avec IA"""
        start_time = time.time()
        self.generation_stats['total_requests'] += 1
        
        try:
            # Construction du prompt sécurisé
            prompt = self._build_summary_prompt(cv_profile, target_position)
            
            # Validation anti-injection
            if not self.validator.validate_prompt_safety(prompt):
                raise ValueError("Prompt non sécurisé détecté")
            
            # Génération avec retry
            response = self._generate_with_retry(prompt)
            
            # Post-traitement sécurisé
            enhanced_summary = self._clean_and_validate_response(response)
            
            # Mise à jour stats
            response_time = time.time() - start_time
            self._update_stats(True, response_time)
            
            return enhanced_summary
            
        except Exception as e:
            self.logger.log_error(f"Erreur génération résumé: {e}")
            self._update_stats(False, time.time() - start_time)
            return cv_profile.professional_summary  # Fallback
    
    def optimize_for_ats(self, cv_profile: CVProfile, job_description: str) -> Tuple[CVProfile, ATSAnalysis]:
        """Optimise le CV pour les systèmes ATS"""
        start_time = time.time()
        
        try:
            # Analyse des mots-clés
            keywords_analysis = self._extract_job_keywords(job_description)
            
            # Optimisation du contenu
            optimized_profile = self._optimize_cv_content(cv_profile, keywords_analysis)
            
            # Analyse ATS finale
            ats_analysis = self._perform_ats_analysis(optimized_profile, job_description)
            
            self.logger.log_info(f"Optimisation ATS réussie - Score: {ats_analysis.score}")
            
            return optimized_profile, ats_analysis
            
        except Exception as e:
            self.logger.log_error(f"Erreur optimisation ATS: {e}")
            # Retour du profil original avec analyse basique
            basic_analysis = ATSAnalysis(
                score=50,
                level="Moyen",
                recommendations=["Optimisation non disponible temporairement"]
            )
            return cv_profile, basic_analysis
    
    def generate_achievement_suggestions(self, experience_description: str, position: str) -> List[str]:
        """Génère des suggestions de réalisations pour une expérience"""
        try:
            prompt = f"""
            En tant qu'expert en rédaction CV, améliore cette description d'expérience pour le poste de {position}.
            
            Description actuelle:
            {experience_description}
            
            Génère 3 réalisations spécifiques et quantifiées qui pourraient correspondre à ce poste.
            Utilise des verbes d'action et des métriques concrètes.
            
            Format: Liste numérotée simple, une réalisation par ligne.
            """
            
            response = self._generate_with_retry(prompt)
            achievements = self._parse_achievements_list(response)
            
            return achievements[:3]  # Maximum 3 suggestions
            
        except Exception as e:
            self.logger.log_error(f"Erreur génération réalisations: {e}")
            return ["Optimisé les processus de l'équipe", "Atteint les objectifs fixés", "Collaboré efficacement"]
    
    def analyze_skill_gaps(self, cv_profile: CVProfile, job_description: str) -> Dict[str, List[str]]:
        """Analyse les lacunes en compétences par rapport à l'offre"""
        try:
            current_skills = [skill.name.lower() for skill in cv_profile.skills]
            
            # Extraction des compétences requises
            required_skills = self._extract_required_skills(job_description)
            
            # Identification des lacunes
            missing_skills = [skill for skill in required_skills if skill.lower() not in current_skills]
            matching_skills = [skill for skill in required_skills if skill.lower() in current_skills]
            
            return {
                'missing_skills': missing_skills,
                'matching_skills': matching_skills,
                'suggestions': self._generate_skill_suggestions(missing_skills)
            }
            
        except Exception as e:
            self.logger.log_error(f"Erreur analyse compétences: {e}")
            return {'missing_skills': [], 'matching_skills': [], 'suggestions': []}
    
    def get_generation_stats(self) -> Dict[str, Any]:
        """Retourne les statistiques de génération"""
        success_rate = 0
        if self.generation_stats['total_requests'] > 0:
            success_rate = (self.generation_stats['successful_generations'] / 
                          self.generation_stats['total_requests']) * 100
        
        return {
            'total_requests': self.generation_stats['total_requests'],
            'success_rate': round(success_rate, 2),
            'avg_response_time': round(self.generation_stats['avg_response_time'], 2),
            'last_updated': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
    
    # Méthodes privées
    
    def _build_summary_prompt(self, cv_profile: CVProfile, target_position: str) -> str:
        """Construit un prompt sécurisé pour le résumé professionnel"""
        experiences_summary = ""
        for exp in cv_profile.experiences[:3]:  # Top 3 expériences
            experiences_summary += f"- {exp.position} chez {exp.company}\n"
        
        skills_summary = ", ".join([skill.name for skill in cv_profile.skills[:8]])
        
        prompt = f"""
        En tant qu'expert en rédaction de CV pour reconversions professionnelles, 
        créez un résumé professionnel percutant pour ce profil.
        
        Profil candidat:
        - Expériences clés: {experiences_summary}
        - Compétences: {skills_summary}
        - Poste visé: {target_position or "Évolution de carrière"}
        
        Créez un résumé de 3-4 lignes qui:
        1. Met en valeur les compétences transférables
        2. Montre la motivation pour la reconversion
        3. Utilise des mots-clés du domaine visé
        4. Reste concis et impactant
        
        Réponse: paragraphe unique sans formatage.
        """
        
        return prompt
    
    def _generate_with_retry(self, prompt: str, max_retries: int = 3) -> str:
        """Génère du contenu avec système de retry"""
        for attempt in range(max_retries):
            try:
                response = self.model.generate_content(
                    prompt,
                    safety_settings=self.safety_settings,
                    generation_config=genai.types.GenerationConfig(
                        max_output_tokens=1000,
                        temperature=0.7
                    )
                )
                
                if response.text:
                    return response.text.strip()
                else:
                    raise ValueError("Réponse vide du modèle")
                    
            except Exception as e:
                if attempt == max_retries - 1:
                    raise e
                time.sleep(2 ** attempt)  # Backoff exponentiel
    
    def _clean_and_validate_response(self, response: str) -> str:
        """Nettoie et valide la réponse IA"""
        # Suppression des caractères indésirables
        cleaned = re.sub(r'[^\w\s\-\.,;:()\[\]{}]', '', response)
        
        # Validation longueur
        if len(cleaned) > 2000:
            cleaned = cleaned[:2000] + "..."
        
        # Validation contenu offensant (basique)
        forbidden_words = ['hack', 'exploit', 'malicious', 'attack']
        for word in forbidden_words:
            if word.lower() in cleaned.lower():
                raise ValueError("Contenu potentiellement dangereux détecté")
        
        return cleaned
    
    def _extract_job_keywords(self, job_description: str) -> List[str]:
        """Extrait les mots-clés importants de l'offre d'emploi"""
        try:
            prompt = f"""
            Extrais les 15 mots-clés les plus importants de cette offre d'emploi.
            Concentre-toi sur les compétences techniques, outils, et qualifications.
            
            Offre d'emploi:
            {job_description[:1500]}
            
            Format: Liste séparée par des virgules, un mot-clé par élément.
            """
            
            response = self._generate_with_retry(prompt)
            keywords = [kw.strip() for kw in response.split(',') if kw.strip()]
            
            return keywords[:15]
            
        except Exception as e:
            self.logger.log_error(f"Erreur extraction mots-clés: {e}")
            return []
    
    def _optimize_cv_content(self, cv_profile: CVProfile, keywords: List[str]) -> CVProfile:
        """Optimise le contenu CV avec les mots-clés identifiés"""
        # Copie du profil pour modification
        optimized_profile = cv_profile
        
        # Optimisation du résumé professionnel
        if keywords and cv_profile.professional_summary:
            summary_with_keywords = self._integrate_keywords_in_summary(
                cv_profile.professional_summary, keywords[:5]
            )
            optimized_profile.professional_summary = summary_with_keywords
        
        return optimized_profile
    
    def _integrate_keywords_in_summary(self, summary: str, keywords: List[str]) -> str:
        """Intègre naturellement des mots-clés dans le résumé"""
        try:
            prompt = f"""
            Améliore ce résumé professionnel en intégrant naturellement ces mots-clés: {', '.join(keywords)}
            
            Résumé actuel:
            {summary}
            
            Consignes:
            - Garde le sens et le style original
            - Intègre 2-3 mots-clés maximum
            - Reste naturel et fluide
            - Maximum 4 lignes
            
            Résumé optimisé:
            """
            
            response = self._generate_with_retry(prompt)
            return self._clean_and_validate_response(response)
            
        except Exception as e:
            self.logger.log_error(f"Erreur intégration mots-clés: {e}")
            return summary  # Retour original si erreur
    
    def _perform_ats_analysis(self, cv_profile: CVProfile, job_description: str) -> ATSAnalysis:
        """Effectue une analyse ATS du CV"""
        score = 75  # Score de base
        recommendations = []
        missing_keywords = []
        
        # Analyse basique des sections
        sections_score = 0
        if cv_profile.professional_summary:
            sections_score += 20
        if cv_profile.experiences:
            sections_score += 25
        if cv_profile.skills:
            sections_score += 20
        if cv_profile.education:
            sections_score += 15
        
        final_score = min(100, sections_score + 20)  # Score bonus pour complétude
        
        # Recommandations basées sur le score
        if final_score < 60:
            recommendations.append("Complétez toutes les sections principales du CV")
        if not cv_profile.professional_summary:
            recommendations.append("Ajoutez un résumé professionnel accrocheur")
        if len(cv_profile.skills) < 5:
            recommendations.append("Enrichissez la section compétences")
        
        return ATSAnalysis(
            score=final_score,
            level="",  # Sera déterminé automatiquement
            missing_keywords=missing_keywords,
            recommendations=recommendations,
            keyword_density={},
            sections_analyzed=["summary", "experience", "skills", "education"]
        )
    
    def _parse_achievements_list(self, response: str) -> List[str]:
        """Parse la réponse pour extraire une liste de réalisations"""
        lines = response.split('\n')
        achievements = []
        
        for line in lines:
            # Nettoie et filtre les lignes valides
            cleaned = line.strip()
            if cleaned and (cleaned[0].isdigit() or cleaned.startswith('-') or cleaned.startswith('•')):
                # Supprime les numéros/puces du début
                achievement = re.sub(r'^[\d\-•.\s]+', '', cleaned).strip()
                if achievement and len(achievement) > 10:
                    achievements.append(achievement)
        
        return achievements[:5]  # Maximum 5 achievements
    
    def _extract_required_skills(self, job_description: str) -> List[str]:
        """Extrait les compétences requises de l'offre d'emploi"""
        # Méthode simplifiée - dans un vrai projet, utiliser NLP plus avancé
        common_skills = [
            'Python', 'JavaScript', 'React', 'Angular', 'Vue.js', 'Node.js',
            'Java', 'C++', 'SQL', 'PostgreSQL', 'MySQL', 'MongoDB',
            'AWS', 'Azure', 'Docker', 'Kubernetes', 'Git', 'Jenkins',
            'Agile', 'Scrum', 'Leadership', 'Management', 'Communication'
        ]
        
        found_skills = []
        job_lower = job_description.lower()
        
        for skill in common_skills:
            if skill.lower() in job_lower:
                found_skills.append(skill)
        
        return found_skills
    
    def _generate_skill_suggestions(self, missing_skills: List[str]) -> List[str]:
        """Génère des suggestions pour acquérir les compétences manquantes"""
        suggestions = []
        
        for skill in missing_skills[:3]:  # Top 3 compétences manquantes
            suggestion = f"Développez vos compétences en {skill} via des formations en ligne"
            suggestions.append(suggestion)
        
        return suggestions
    
    def _update_stats(self, success: bool, response_time: float):
        """Met à jour les statistiques de génération"""
        if success:
            self.generation_stats['successful_generations'] += 1
        else:
            self.generation_stats['failed_generations'] += 1
        
        # Calcul de la moyenne mobile du temps de réponse
        current_avg = self.generation_stats['avg_response_time']
        total_requests = self.generation_stats['total_requests']
        
        self.generation_stats['avg_response_time'] = (
            (current_avg * (total_requests - 1) + response_time) / total_requests
        )