#!/bin/bash

# 🚀 Script de Déploiement Automatique GitHub
# Auteur: Mohamed ALI JAMA
# Description: Automatise le déploiement du projet d'analyse des systèmes éducatifs

echo "🎯 === DÉPLOIEMENT GITHUB - PROJET ÉDUCATION ===" 
echo ""

# Couleurs pour l'affichage
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Fonction pour afficher les messages colorés
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Vérification des prérequis
print_status "Vérification des prérequis..."

# Vérifier si Git est installé
if ! command -v git &> /dev/null; then
    print_error "Git n'est pas installé. Veuillez l'installer d'abord."
    exit 1
fi

# Vérifier si on est dans le bon répertoire
if [ ! -f "README.md" ]; then
    print_error "Veuillez exécuter ce script depuis le répertoire racine du projet."
    exit 1
fi

print_success "Prérequis vérifiés ✅"

# Initialisation Git
print_status "Initialisation du repository Git..."

if [ ! -d ".git" ]; then
    git init
    print_success "Repository Git initialisé"
else
    print_warning "Repository Git déjà initialisé"
fi

# Configuration Git (optionnel)
read -p "🔧 Voulez-vous configurer votre nom et email Git ? (y/n): " configure_git
if [ "$configure_git" = "y" ] || [ "$configure_git" = "Y" ]; then
    read -p "📧 Entrez votre nom: " git_name
    read -p "📧 Entrez votre email: " git_email
    
    git config user.name "$git_name"
    git config user.email "$git_email"
    print_success "Configuration Git mise à jour"
fi

# Ajout des fichiers
print_status "Ajout des fichiers au repository..."

# Créer .gitignore s'il n'existe pas
if [ ! -f ".gitignore" ]; then
    print_warning ".gitignore manquant, création automatique..."
    cat > .gitignore << EOF
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Jupyter Notebook
.ipynb_checkpoints

# Environment
.env
.venv
env/
venv/
ENV/
env.bak/
venv.bak/

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
Thumbs.db

# Project specific
datasets_projet_2.zip
fichier_téléchargé.txt
temp/
*.tmp
EOF
fi

git add .
git status

# Commit initial
print_status "Création du commit initial..."
git commit -m "🎉 Initial commit: Education Systems Analysis Project

✨ Features:
- 📊 Comprehensive educational data analysis
- 🐍 Python modules for data processing and visualization  
- 📈 Interactive visualizations with Plotly and Seaborn
- 📚 Well-documented Jupyter notebooks
- 🏗️ Professional project structure
- 📋 Complete documentation and deployment guide

🛠️ Technologies:
- Python, Pandas, NumPy
- Matplotlib, Seaborn, Plotly
- Jupyter Notebooks
- Statistical Analysis
- Data Visualization"

print_success "Commit créé avec succès"

# Configuration du repository distant
print_status "Configuration du repository GitHub..."
echo ""
print_warning "⚠️  ÉTAPES MANUELLES REQUISES:"
echo "1. 🌐 Allez sur https://github.com"
echo "2. 🆕 Cliquez sur 'New repository'"
echo "3. 📝 Nom suggéré: 'education-systems-analysis'"
echo "4. 📄 Description: '🌍 Comprehensive analysis of global education systems using Python and Data Science techniques'"
echo "5. 🔓 Choisissez 'Public' pour le portfolio"
echo "6. ❌ NE PAS initialiser avec README"
echo "7. ✅ Cliquez 'Create repository'"
echo ""

read -p "📋 Avez-vous créé le repository sur GitHub ? (y/n): " repo_created
if [ "$repo_created" != "y" ] && [ "$repo_created" != "Y" ]; then
    print_warning "Veuillez créer le repository sur GitHub d'abord."
    exit 1
fi

# Demander l'URL du repository
read -p "🔗 Entrez l'URL de votre repository GitHub (ex: https://github.com/username/education-systems-analysis.git): " repo_url

if [ -z "$repo_url" ]; then
    print_error "URL du repository requise."
    exit 1
fi

# Ajouter l'origine remote
print_status "Ajout du repository distant..."
git remote add origin "$repo_url"
print_success "Repository distant configuré"

# Push vers GitHub
print_status "Envoi du code vers GitHub..."
git branch -M main
git push -u origin main

if [ $? -eq 0 ]; then
    print_success "🎉 Code envoyé avec succès vers GitHub!"
else
    print_error "Erreur lors de l'envoi. Vérifiez vos permissions GitHub."
    exit 1
fi

# Instructions post-déploiement
echo ""
echo "🎊 === DÉPLOIEMENT TERMINÉ AVEC SUCCÈS! ==="
echo ""
print_success "✅ Votre projet est maintenant sur GitHub!"
echo ""
print_status "🔧 ÉTAPES SUIVANTES RECOMMANDÉES:"
echo ""
echo "1. 🏷️  AJOUTER DES TOPICS:"
echo "   - Allez dans votre repository GitHub"
echo "   - Cliquez sur ⚙️ à côté de 'About'"
echo "   - Ajoutez: data-science, python, education, data-analysis, visualization"
echo ""
echo "2. 🌐 ACTIVER GITHUB PAGES (optionnel):"
echo "   - Settings → Pages → Source: Deploy from branch → main"
echo ""
echo "3. 📸 AJOUTER DES CAPTURES D'ÉCRAN:"
echo "   - Exécutez: jupyter notebook notebooks/portfolio_demo.ipynb"
echo "   - Sauvegardez les visualisations"
echo "   - Ajoutez-les au README"
echo ""
echo "4. 🔗 LIENS UTILES:"
echo "   - Repository: $repo_url"
echo "   - Notebook Viewer: https://nbviewer.org/github/$(echo $repo_url | sed 's/.*github.com\///g' | sed 's/\.git//g')/blob/main/notebooks/portfolio_demo.ipynb"
echo ""
print_success "🏆 Votre portfolio est prêt à impressionner les employeurs!"
echo ""
print_status "📖 Consultez DEPLOYMENT_GUIDE.md pour plus de détails."