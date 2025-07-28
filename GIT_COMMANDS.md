# 🚀 Commandes Git pour Déploiement Manuel

## Étapes de Déploiement Manuel vers GitHub

### 1. Initialiser Git (si pas déjà fait)
```bash
git init
```

### 2. Configurer Git (première fois seulement)
```bash
git config user.name "Votre Nom"
git config user.email "votre.email@example.com"
```

### 3. Ajouter tous les fichiers
```bash
git add .
```

### 4. Créer le commit initial
```bash
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
```

### 5. Ajouter le repository distant
```bash
# Remplacez VOTRE-USERNAME par votre nom d'utilisateur GitHub
git remote add origin https://github.com/VOTRE-USERNAME/education-systems-analysis.git
```

### 6. Pousser vers GitHub
```bash
git branch -M main
git push -u origin main
```

## 🔧 Commandes Utiles

### Vérifier le statut
```bash
git status
```

### Voir l'historique des commits
```bash
git log --oneline
```

### Vérifier les remotes configurés
```bash
git remote -v
```

### Ajouter des modifications futures
```bash
git add .
git commit -m "✨ Description de vos modifications"
git push
```

## 🆘 Résolution de Problèmes

### Si vous avez une erreur d'authentification
```bash
# Utiliser un token personnel au lieu du mot de passe
# Allez dans GitHub Settings > Developer settings > Personal access tokens
```

### Si le repository existe déjà
```bash
git remote set-url origin https://github.com/VOTRE-USERNAME/education-systems-analysis.git
```

### Si vous voulez forcer le push
```bash
git push -f origin main
```

## 📝 Notes Importantes

- ✅ Assurez-vous d'avoir créé le repository sur GitHub d'abord
- ✅ Utilisez l'URL HTTPS pour plus de simplicité
- ✅ Le repository doit être PUBLIC pour votre portfolio
- ✅ N'initialisez PAS avec README sur GitHub (on a déjà le nôtre)