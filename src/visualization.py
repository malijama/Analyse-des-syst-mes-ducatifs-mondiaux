"""
Module de visualisation pour l'analyse des systèmes éducatifs.

Ce module contient les fonctions pour créer des visualisations attractives
et informatives des données éducatives.
"""

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import warnings
warnings.filterwarnings('ignore')

# Configuration du style
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")

class EducationVisualizer:
    """Classe pour créer des visualisations des données éducatives."""
    
    def __init__(self, figsize=(12, 8), style='seaborn-v0_8'):
        """
        Initialise le visualiseur.
        
        Args:
            figsize (tuple): Taille par défaut des figures
            style (str): Style matplotlib à utiliser
        """
        self.figsize = figsize
        plt.style.use(style)
        
        # Palette de couleurs personnalisée
        self.colors = {
            'primary': '#2E86AB',
            'secondary': '#A23B72',
            'accent': '#F18F01',
            'success': '#C73E1D',
            'info': '#7209B7',
            'light': '#F2F2F2',
            'dark': '#2D3748'
        }
    
    def plot_missing_data_heatmap(self, df: pd.DataFrame, title: str = "Données Manquantes") -> None:
        """
        Crée une heatmap des données manquantes.
        
        Args:
            df (pd.DataFrame): Dataset à analyser
            title (str): Titre du graphique
        """
        plt.figure(figsize=self.figsize)
        
        # Calculer le pourcentage de données manquantes
        missing_data = df.isnull().sum() / len(df) * 100
        missing_data = missing_data[missing_data > 0].sort_values(ascending=False)
        
        if len(missing_data) > 0:
            sns.barplot(x=missing_data.values, y=missing_data.index, 
                       palette='viridis')
            plt.title(f'{title}\nPourcentage de Données Manquantes par Colonne', 
                     fontsize=16, fontweight='bold', pad=20)
            plt.xlabel('Pourcentage de Données Manquantes (%)', fontsize=12)
            plt.ylabel('Colonnes', fontsize=12)
            
            # Ajouter les valeurs sur les barres
            for i, v in enumerate(missing_data.values):
                plt.text(v + 0.5, i, f'{v:.1f}%', va='center', fontsize=10)
        else:
            plt.text(0.5, 0.5, 'Aucune donnée manquante détectée', 
                    ha='center', va='center', transform=plt.gca().transAxes,
                    fontsize=14, fontweight='bold')
            plt.title(title, fontsize=16, fontweight='bold')
        
        plt.tight_layout()
        plt.show()
    
    def plot_top_countries(self, df: pd.DataFrame, indicator_name: str, 
                          year: int, top_n: int = 10) -> None:
        """
        Crée un graphique en barres des top pays pour un indicateur.
        
        Args:
            df (pd.DataFrame): Dataset filtré avec pays et valeurs
            indicator_name (str): Nom de l'indicateur
            year (int): Année de référence
            top_n (int): Nombre de pays à afficher
        """
        if df.empty:
            print(f"❌ Aucune donnée disponible pour {indicator_name} en {year}")
            return
        
        plt.figure(figsize=(14, 8))
        
        # Préparer les données
        df_plot = df.head(top_n).copy()
        year_col = str(year)
        
        # Créer le graphique
        bars = plt.barh(range(len(df_plot)), df_plot[year_col], 
                       color=plt.cm.viridis(np.linspace(0, 1, len(df_plot))))
        
        # Personnaliser
        plt.yticks(range(len(df_plot)), df_plot['Country Name'])
        plt.xlabel(f'Valeur de l\'indicateur ({year})', fontsize=12)
        plt.title(f'Top {top_n} - {indicator_name}\nAnnée: {year}', 
                 fontsize=16, fontweight='bold', pad=20)
        
        # Ajouter les valeurs sur les barres
        for i, (bar, value) in enumerate(zip(bars, df_plot[year_col])):
            plt.text(bar.get_width() + max(df_plot[year_col]) * 0.01, 
                    bar.get_y() + bar.get_height()/2, 
                    f'{value:.1f}', va='center', fontsize=10)
        
        plt.gca().invert_yaxis()
        plt.tight_layout()
        plt.show()
    
    def plot_correlation_matrix(self, df: pd.DataFrame, title: str = "Matrice de Corrélation") -> None:
        """
        Crée une matrice de corrélation interactive.
        
        Args:
            df (pd.DataFrame): Dataset avec variables numériques
            title (str): Titre du graphique
        """
        # Sélectionner uniquement les colonnes numériques
        numeric_df = df.select_dtypes(include=[np.number])
        
        if numeric_df.empty:
            print("❌ Aucune variable numérique trouvée pour la corrélation")
            return
        
        # Calculer la matrice de corrélation
        corr_matrix = numeric_df.corr()
        
        plt.figure(figsize=(12, 10))
        
        # Créer la heatmap
        mask = np.triu(np.ones_like(corr_matrix, dtype=bool))
        sns.heatmap(corr_matrix, mask=mask, annot=True, cmap='RdYlBu_r', 
                   center=0, square=True, linewidths=0.5, 
                   cbar_kws={"shrink": .8}, fmt='.2f')
        
        plt.title(title, fontsize=16, fontweight='bold', pad=20)
        plt.tight_layout()
        plt.show()
    
    def plot_time_series(self, df: pd.DataFrame, countries: list, 
                        indicator_name: str, start_year: int = 2000, 
                        end_year: int = 2020) -> None:
        """
        Crée un graphique de séries temporelles pour plusieurs pays.
        
        Args:
            df (pd.DataFrame): Dataset des indicateurs
            countries (list): Liste des pays à afficher
            indicator_name (str): Nom de l'indicateur
            start_year (int): Année de début
            end_year (int): Année de fin
        """
        plt.figure(figsize=(14, 8))
        
        # Filtrer les années
        year_columns = [str(year) for year in range(start_year, end_year + 1) 
                       if str(year) in df.columns]
        
        if not year_columns:
            print(f"❌ Aucune donnée disponible pour la période {start_year}-{end_year}")
            return
        
        # Tracer chaque pays
        for i, country in enumerate(countries):
            country_data = df[df['Country Name'] == country]
            if not country_data.empty:
                values = country_data[year_columns].iloc[0]
                years = [int(year) for year in year_columns]
                
                # Supprimer les valeurs NaN
                valid_data = [(year, val) for year, val in zip(years, values) 
                             if pd.notna(val)]
                
                if valid_data:
                    years_clean, values_clean = zip(*valid_data)
                    plt.plot(years_clean, values_clean, marker='o', 
                            linewidth=2, label=country, markersize=6)
        
        plt.title(f'Évolution de {indicator_name}\nPériode: {start_year}-{end_year}', 
                 fontsize=16, fontweight='bold', pad=20)
        plt.xlabel('Année', fontsize=12)
        plt.ylabel('Valeur de l\'indicateur', fontsize=12)
        plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.show()
    
    def plot_regional_comparison(self, df: pd.DataFrame, region_col: str, 
                               value_col: str, title: str = "Comparaison Régionale") -> None:
        """
        Crée un boxplot pour comparer les régions.
        
        Args:
            df (pd.DataFrame): Dataset avec régions et valeurs
            region_col (str): Nom de la colonne des régions
            value_col (str): Nom de la colonne des valeurs
            title (str): Titre du graphique
        """
        plt.figure(figsize=(14, 8))
        
        # Supprimer les valeurs NaN
        df_clean = df.dropna(subset=[region_col, value_col])
        
        if df_clean.empty:
            print("❌ Aucune donnée valide pour la comparaison régionale")
            return
        
        # Créer le boxplot
        sns.boxplot(data=df_clean, x=region_col, y=value_col, 
                   palette='Set2')
        
        plt.title(title, fontsize=16, fontweight='bold', pad=20)
        plt.xlabel('Région', fontsize=12)
        plt.ylabel('Valeur', fontsize=12)
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        plt.show()
    
    def create_interactive_world_map(self, df: pd.DataFrame, value_col: str, 
                                   title: str = "Carte Mondiale Interactive") -> go.Figure:
        """
        Crée une carte mondiale interactive avec Plotly.
        
        Args:
            df (pd.DataFrame): Dataset avec codes pays et valeurs
            value_col (str): Nom de la colonne des valeurs
            title (str): Titre de la carte
            
        Returns:
            go.Figure: Figure Plotly interactive
        """
        fig = px.choropleth(
            df,
            locations='Country Code',
            color=value_col,
            hover_name='Country Name',
            color_continuous_scale='Viridis',
            title=title
        )
        
        fig.update_layout(
            title_font_size=16,
            title_x=0.5,
            geo=dict(showframe=False, showcoastlines=True)
        )
        
        return fig


def save_plot(filename: str, dpi: int = 300, bbox_inches: str = 'tight') -> None:
    """
    Sauvegarde le graphique actuel.
    
    Args:
        filename (str): Nom du fichier
        dpi (int): Résolution
        bbox_inches (str): Ajustement des bordures
    """
    plt.savefig(f'visualizations/{filename}', dpi=dpi, bbox_inches=bbox_inches)
    print(f"📊 Graphique sauvegardé: visualizations/{filename}")


if __name__ == "__main__":
    # Test du module
    print("🎨 Module de visualisation chargé avec succès!")
    
    # Créer des données de test
    test_data = pd.DataFrame({
        'Country': ['France', 'Germany', 'Spain', 'Italy'],
        'Education_Index': [85.2, 88.1, 82.3, 79.8],
        'GDP_per_capita': [42000, 46000, 38000, 35000]
    })
    
    visualizer = EducationVisualizer()
    print("✅ Visualiseur initialisé avec succès!")