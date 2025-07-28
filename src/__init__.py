"""
Package pour l'analyse des systèmes éducatifs mondiaux.

Ce package contient tous les modules nécessaires pour analyser
les données éducatives de la Banque Mondiale.
"""

from .data_processing import EducationDataProcessor, load_and_process_data
from .visualization import EducationVisualizer, save_plot
from .analysis import EducationAnalyzer

__version__ = "1.0.0"
__author__ = "Mohamed ALIJAMA"
__email__ = "votre.email@example.com"

__all__ = [
    'EducationDataProcessor',
    'EducationVisualizer', 
    'EducationAnalyzer',
    'load_and_process_data',
    'save_plot'
]