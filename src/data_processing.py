"""
Module de traitement des données pour l'analyse des systèmes éducatifs.

Ce module contient les fonctions nécessaires pour charger, nettoyer et 
préparer les données éducatives pour l'analyse.
"""

import pandas as pd
import numpy as np
import os
from typing import Dict, List, Tuple, Optional


class EducationDataProcessor:
    """Classe pour le traitement des données éducatives."""
    
    def __init__(self, data_path: str = "data/raw"):
        """
        Initialise le processeur de données.
        
        Args:
            data_path (str): Chemin vers les données brutes
        """
        self.data_path = data_path
        self.datasets = {}
        
    def load_datasets(self) -> Dict[str, pd.DataFrame]:
        """
        Charge tous les datasets éducatifs.
        
        Returns:
            Dict[str, pd.DataFrame]: Dictionnaire contenant tous les datasets
        """
        files = {
            'country_series': 'EdStatsCountry-Series.csv',
            'country': 'EdStatsCountry.csv',
            'indicator': 'EdStatsData.csv',
            'description': 'EdStatsFootNote.csv',
            'topic': 'EdStatsSeries.csv'
        }
        
        for name, filename in files.items():
            filepath = os.path.join(self.data_path, filename)
            if os.path.exists(filepath):
                self.datasets[name] = pd.read_csv(filepath)
                print(f"✅ {filename} chargé avec succès ({self.datasets[name].shape})")
            else:
                print(f"❌ Fichier non trouvé: {filepath}")
                
        return self.datasets
    
    def clean_data(self, df: pd.DataFrame, dataset_name: str) -> pd.DataFrame:
        """
        Nettoie un dataset spécifique.
        
        Args:
            df (pd.DataFrame): Dataset à nettoyer
            dataset_name (str): Nom du dataset
            
        Returns:
            pd.DataFrame: Dataset nettoyé
        """
        df_clean = df.copy()
        
        # Supprimer les colonnes vides
        df_clean = df_clean.dropna(axis=1, how='all')
        
        # Supprimer les colonnes 'Unnamed'
        unnamed_cols = [col for col in df_clean.columns if 'Unnamed' in str(col)]
        df_clean = df_clean.drop(columns=unnamed_cols)
        
        print(f"🧹 {dataset_name} nettoyé: {df.shape} → {df_clean.shape}")
        
        return df_clean
    
    def get_missing_data_summary(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Génère un résumé des données manquantes.
        
        Args:
            df (pd.DataFrame): Dataset à analyser
            
        Returns:
            pd.DataFrame: Résumé des données manquantes
        """
        missing_data = pd.DataFrame({
            'Column': df.columns,
            'Missing_Count': df.isnull().sum(),
            'Missing_Percentage': (df.isnull().sum() / len(df)) * 100
        })
        
        return missing_data.sort_values('Missing_Percentage', ascending=False)
    
    def filter_by_years(self, df: pd.DataFrame, start_year: int, end_year: int) -> pd.DataFrame:
        """
        Filtre les données par période.
        
        Args:
            df (pd.DataFrame): Dataset à filtrer
            start_year (int): Année de début
            end_year (int): Année de fin
            
        Returns:
            pd.DataFrame: Dataset filtré
        """
        year_columns = [col for col in df.columns if str(col).isdigit() and 
                       start_year <= int(col) <= end_year]
        
        base_columns = [col for col in df.columns if not str(col).isdigit()]
        
        return df[base_columns + year_columns]
    
    def get_top_countries_by_indicator(self, df: pd.DataFrame, indicator_code: str, 
                                     year: int, top_n: int = 10) -> pd.DataFrame:
        """
        Obtient le top N des pays pour un indicateur donné.
        
        Args:
            df (pd.DataFrame): Dataset des indicateurs
            indicator_code (str): Code de l'indicateur
            year (int): Année de référence
            top_n (int): Nombre de pays à retourner
            
        Returns:
            pd.DataFrame: Top N des pays
        """
        filtered_df = df[df['Indicator Code'] == indicator_code]
        
        if str(year) in filtered_df.columns:
            result = filtered_df[['Country Name', str(year)]].copy()
            result = result.dropna()
            result = result.sort_values(str(year), ascending=False).head(top_n)
            return result
        else:
            print(f"❌ Année {year} non disponible dans les données")
            return pd.DataFrame()


def load_and_process_data(data_path: str = "data/raw") -> Dict[str, pd.DataFrame]:
    """
    Fonction utilitaire pour charger et traiter rapidement les données.
    
    Args:
        data_path (str): Chemin vers les données brutes
        
    Returns:
        Dict[str, pd.DataFrame]: Datasets traités
    """
    processor = EducationDataProcessor(data_path)
    datasets = processor.load_datasets()
    
    # Nettoyer chaque dataset
    cleaned_datasets = {}
    for name, df in datasets.items():
        cleaned_datasets[name] = processor.clean_data(df, name)
    
    return cleaned_datasets


if __name__ == "__main__":
    # Test du module
    processor = EducationDataProcessor()
    datasets = processor.load_datasets()
    
    if datasets:
        print("\n📊 Résumé des datasets:")
        for name, df in datasets.items():
            print(f"  {name}: {df.shape}")