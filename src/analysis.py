"""
Module d'analyse statistique pour les systèmes éducatifs.

Ce module contient les fonctions d'analyse statistique avancée
pour explorer les données éducatives.
"""

import pandas as pd
import numpy as np
from scipy import stats
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
import warnings
warnings.filterwarnings('ignore')


class EducationAnalyzer:
    """Classe pour l'analyse statistique des données éducatives."""
    
    def __init__(self):
        """Initialise l'analyseur."""
        self.scaler = StandardScaler()
        self.pca = None
        self.kmeans = None
        
    def descriptive_statistics(self, df: pd.DataFrame, group_by: str = None) -> pd.DataFrame:
        """
        Calcule les statistiques descriptives.
        
        Args:
            df (pd.DataFrame): Dataset à analyser
            group_by (str): Colonne pour grouper les statistiques
            
        Returns:
            pd.DataFrame: Statistiques descriptives
        """
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        
        if group_by and group_by in df.columns:
            stats_df = df.groupby(group_by)[numeric_cols].agg([
                'count', 'mean', 'median', 'std', 'min', 'max'
            ]).round(2)
        else:
            stats_df = df[numeric_cols].describe().round(2)
            
        return stats_df
    
    def correlation_analysis(self, df: pd.DataFrame, threshold: float = 0.5) -> dict:
        """
        Analyse les corrélations entre variables.
        
        Args:
            df (pd.DataFrame): Dataset à analyser
            threshold (float): Seuil de corrélation significative
            
        Returns:
            dict: Résultats de l'analyse de corrélation
        """
        numeric_df = df.select_dtypes(include=[np.number])
        corr_matrix = numeric_df.corr()
        
        # Trouver les corrélations fortes
        strong_correlations = []
        for i in range(len(corr_matrix.columns)):
            for j in range(i+1, len(corr_matrix.columns)):
                corr_value = corr_matrix.iloc[i, j]
                if abs(corr_value) >= threshold:
                    strong_correlations.append({
                        'Variable_1': corr_matrix.columns[i],
                        'Variable_2': corr_matrix.columns[j],
                        'Correlation': round(corr_value, 3),
                        'Strength': 'Forte' if abs(corr_value) >= 0.7 else 'Modérée'
                    })
        
        return {
            'correlation_matrix': corr_matrix,
            'strong_correlations': pd.DataFrame(strong_correlations),
            'summary': {
                'total_variables': len(numeric_df.columns),
                'strong_correlations_count': len(strong_correlations),
                'max_correlation': corr_matrix.abs().max().max() if not corr_matrix.empty else 0
            }
        }
    
    def perform_pca(self, df: pd.DataFrame, n_components: int = None) -> dict:
        """
        Effectue une Analyse en Composantes Principales.
        
        Args:
            df (pd.DataFrame): Dataset à analyser
            n_components (int): Nombre de composantes à conserver
            
        Returns:
            dict: Résultats de l'ACP
        """
        numeric_df = df.select_dtypes(include=[np.number]).dropna()
        
        if numeric_df.empty:
            return {'error': 'Aucune donnée numérique valide pour l\'ACP'}
        
        # Standardiser les données
        scaled_data = self.scaler.fit_transform(numeric_df)
        
        # Déterminer le nombre optimal de composantes si non spécifié
        if n_components is None:
            n_components = min(len(numeric_df.columns), len(numeric_df))
        
        # Effectuer l'ACP
        self.pca = PCA(n_components=n_components)
        pca_result = self.pca.fit_transform(scaled_data)
        
        # Créer un DataFrame avec les résultats
        pca_df = pd.DataFrame(
            pca_result,
            columns=[f'PC{i+1}' for i in range(n_components)]
        )
        
        # Calculer la variance expliquée cumulative
        cumulative_variance = np.cumsum(self.pca.explained_variance_ratio_)
        
        return {
            'pca_data': pca_df,
            'explained_variance_ratio': self.pca.explained_variance_ratio_,
            'cumulative_variance': cumulative_variance,
            'components': pd.DataFrame(
                self.pca.components_.T,
                columns=[f'PC{i+1}' for i in range(n_components)],
                index=numeric_df.columns
            ),
            'summary': {
                'total_variance_explained': cumulative_variance[-1],
                'components_for_80_percent': np.argmax(cumulative_variance >= 0.8) + 1,
                'components_for_95_percent': np.argmax(cumulative_variance >= 0.95) + 1
            }
        }
    
    def cluster_analysis(self, df: pd.DataFrame, max_clusters: int = 10) -> dict:
        """
        Effectue une analyse de clustering.
        
        Args:
            df (pd.DataFrame): Dataset à analyser
            max_clusters (int): Nombre maximum de clusters à tester
            
        Returns:
            dict: Résultats du clustering
        """
        numeric_df = df.select_dtypes(include=[np.number]).dropna()
        
        if numeric_df.empty or len(numeric_df) < 2:
            return {'error': 'Données insuffisantes pour le clustering'}
        
        # Standardiser les données
        scaled_data = self.scaler.fit_transform(numeric_df)
        
        # Tester différents nombres de clusters
        max_clusters = min(max_clusters, len(numeric_df) - 1)
        inertias = []
        silhouette_scores = []
        
        for k in range(2, max_clusters + 1):
            kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
            cluster_labels = kmeans.fit_predict(scaled_data)
            
            inertias.append(kmeans.inertia_)
            silhouette_scores.append(silhouette_score(scaled_data, cluster_labels))
        
        # Trouver le nombre optimal de clusters
        optimal_k = np.argmax(silhouette_scores) + 2
        
        # Effectuer le clustering final
        self.kmeans = KMeans(n_clusters=optimal_k, random_state=42, n_init=10)
        final_clusters = self.kmeans.fit_predict(scaled_data)
        
        # Ajouter les clusters au DataFrame original
        result_df = numeric_df.copy()
        result_df['Cluster'] = final_clusters
        
        return {
            'clustered_data': result_df,
            'cluster_centers': pd.DataFrame(
                self.scaler.inverse_transform(self.kmeans.cluster_centers_),
                columns=numeric_df.columns
            ),
            'inertias': inertias,
            'silhouette_scores': silhouette_scores,
            'optimal_clusters': optimal_k,
            'cluster_summary': result_df.groupby('Cluster').agg(['count', 'mean']).round(2)
        }
    
    def statistical_tests(self, df: pd.DataFrame, group_col: str, value_col: str) -> dict:
        """
        Effectue des tests statistiques entre groupes.
        
        Args:
            df (pd.DataFrame): Dataset à analyser
            group_col (str): Colonne des groupes
            value_col (str): Colonne des valeurs à comparer
            
        Returns:
            dict: Résultats des tests statistiques
        """
        # Préparer les données
        clean_df = df[[group_col, value_col]].dropna()
        groups = clean_df[group_col].unique()
        
        if len(groups) < 2:
            return {'error': 'Au moins 2 groupes nécessaires pour les tests'}
        
        # Séparer les données par groupe
        group_data = [clean_df[clean_df[group_col] == group][value_col].values 
                     for group in groups]
        
        # Test de normalité (Shapiro-Wilk pour chaque groupe)
        normality_tests = {}
        for i, group in enumerate(groups):
            if len(group_data[i]) >= 3:  # Minimum pour Shapiro-Wilk
                stat, p_value = stats.shapiro(group_data[i])
                normality_tests[group] = {
                    'statistic': stat,
                    'p_value': p_value,
                    'is_normal': p_value > 0.05
                }
        
        # Test d'égalité des variances (Levene)
        levene_stat, levene_p = stats.levene(*group_data)
        equal_variances = levene_p > 0.05
        
        # Choisir le test approprié
        if len(groups) == 2:
            # Test t ou Mann-Whitney U
            if all(normality_tests[g]['is_normal'] for g in groups if g in normality_tests) and equal_variances:
                # Test t de Student
                stat, p_value = stats.ttest_ind(group_data[0], group_data[1], equal_var=True)
                test_used = "Test t de Student"
            else:
                # Test de Mann-Whitney U
                stat, p_value = stats.mannwhitneyu(group_data[0], group_data[1], alternative='two-sided')
                test_used = "Test de Mann-Whitney U"
        else:
            # ANOVA ou Kruskal-Wallis
            if all(normality_tests[g]['is_normal'] for g in groups if g in normality_tests) and equal_variances:
                # ANOVA
                stat, p_value = stats.f_oneway(*group_data)
                test_used = "ANOVA"
            else:
                # Kruskal-Wallis
                stat, p_value = stats.kruskal(*group_data)
                test_used = "Test de Kruskal-Wallis"
        
        return {
            'test_used': test_used,
            'statistic': stat,
            'p_value': p_value,
            'is_significant': p_value < 0.05,
            'normality_tests': normality_tests,
            'levene_test': {
                'statistic': levene_stat,
                'p_value': levene_p,
                'equal_variances': equal_variances
            },
            'group_statistics': clean_df.groupby(group_col)[value_col].agg(['count', 'mean', 'std']).round(3)
        }
    
    def trend_analysis(self, df: pd.DataFrame, time_col: str, value_col: str) -> dict:
        """
        Analyse les tendances temporelles.
        
        Args:
            df (pd.DataFrame): Dataset à analyser
            time_col (str): Colonne temporelle
            value_col (str): Colonne des valeurs
            
        Returns:
            dict: Résultats de l'analyse de tendance
        """
        # Préparer les données
        clean_df = df[[time_col, value_col]].dropna().sort_values(time_col)
        
        if len(clean_df) < 3:
            return {'error': 'Données insuffisantes pour l\'analyse de tendance'}
        
        x = np.arange(len(clean_df))
        y = clean_df[value_col].values
        
        # Régression linéaire
        slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
        
        # Test de Mann-Kendall pour la tendance
        def mann_kendall_test(data):
            n = len(data)
            s = 0
            for i in range(n-1):
                for j in range(i+1, n):
                    s += np.sign(data[j] - data[i])
            
            var_s = n * (n-1) * (2*n+5) / 18
            
            if s > 0:
                z = (s - 1) / np.sqrt(var_s)
            elif s < 0:
                z = (s + 1) / np.sqrt(var_s)
            else:
                z = 0
            
            p_mk = 2 * (1 - stats.norm.cdf(abs(z)))
            
            return s, z, p_mk
        
        mk_s, mk_z, mk_p = mann_kendall_test(y)
        
        return {
            'linear_regression': {
                'slope': slope,
                'intercept': intercept,
                'r_squared': r_value**2,
                'p_value': p_value,
                'std_error': std_err
            },
            'mann_kendall': {
                'statistic': mk_s,
                'z_score': mk_z,
                'p_value': mk_p,
                'trend': 'Croissante' if mk_s > 0 and mk_p < 0.05 else 
                        'Décroissante' if mk_s < 0 and mk_p < 0.05 else 'Pas de tendance'
            },
            'summary': {
                'data_points': len(clean_df),
                'time_span': f"{clean_df[time_col].min()} - {clean_df[time_col].max()}",
                'mean_value': np.mean(y),
                'trend_direction': 'Positive' if slope > 0 else 'Négative' if slope < 0 else 'Stable'
            }
        }


if __name__ == "__main__":
    # Test du module
    print("📊 Module d'analyse statistique chargé avec succès!")
    
    # Créer des données de test
    np.random.seed(42)
    test_data = pd.DataFrame({
        'Country': ['France', 'Germany', 'Spain', 'Italy'] * 5,
        'Year': list(range(2016, 2021)) * 4,
        'Education_Index': np.random.normal(80, 10, 20),
        'GDP_per_capita': np.random.normal(40000, 8000, 20),
        'Region': ['Europe'] * 20
    })
    
    analyzer = EducationAnalyzer()
    print("✅ Analyseur initialisé avec succès!")