# 🔐 Guide d'Authentification GitHub

## 🚨 Problème : Device Activation Required

GitHub demande une activation d'appareil pour des raisons de sécurité. Voici comment résoudre ce problème.

## 🔑 Solution 1 : Token Personnel (Recommandée)

### Étape 1 : Créer un Token Personnel
1. **Allez sur GitHub.com** et connectez-vous
2. **Cliquez sur votre avatar** (coin supérieur droit)
3. **Settings** → **Developer settings** → **Personal access tokens** → **Tokens (classic)**
4. **Cliquez "Generate new token"** → **Generate new token (classic)**
5. **Remplissez les informations** :
   - **Note** : "Education Analysis Project"
   - **Expiration** : 90 days (ou plus)
   - **Permissions** à cocher :
     - ✅ `repo` (Full control of private repositories)
     - ✅ `workflow` (Update GitHub Action workflows)
     - ✅ `write:packages` (Upload packages)
     - ✅ `delete:packages` (Delete packages)

6. **Cliquez "Generate token"**
7. **COPIEZ LE TOKEN** immédiatement (il ne sera plus affiché)

### Étape 2 : Utiliser le Token
```bash
# Supprimer l'ancien remote
git remote remove origin

# Ajouter le nouveau remote avec token
git remote add origin https://VOTRE-TOKEN@github.com/malijama/Analyse-des-syst-mes-ducatifs-mondiaux.git

# Pousser le code
git push -u origin main
```

## 📱 Solution 2 : Activation d'Appareil

### Si vous voyez un code d'activation :
1. **Allez sur** : https://github.com/login/device
2. **Entrez le code** affiché dans votre terminal
3. **Cliquez "Continue"**
4. **Autorisez l'accès** à votre repository

## 🌐 Solution 3 : GitHub CLI

### Installation de GitHub CLI (optionnel)
```bash
# Sur macOS avec Homebrew
brew install gh

# Authentification
gh auth login
```

## 🔧 Commandes de Dépannage

### Vérifier la configuration Git
```bash
git config --list
git remote -v
git status
```

### Réinitialiser l'authentification
```bash
# Supprimer les credentials stockés
git config --global --unset credential.helper
git config --global credential.helper osxkeychain

# Ou forcer une nouvelle authentification
git config --global credential.helper ""
```

### Test de connexion
```bash
# Tester la connexion SSH (si configurée)
ssh -T git@github.com

# Tester avec HTTPS
git ls-remote origin
```

## 🆘 En Cas de Problème

### Erreur "Authentication failed"
1. Vérifiez que votre token est correct
2. Assurez-vous que le token a les bonnes permissions
3. Vérifiez que le repository existe sur GitHub

### Erreur "Repository not found"
1. Vérifiez l'URL du repository
2. Assurez-vous que le repository est public ou que vous avez accès
3. Vérifiez l'orthographe du nom d'utilisateur

### Erreur "Permission denied"
1. Utilisez un token personnel au lieu du mot de passe
2. Vérifiez les permissions du token
3. Assurez-vous d'être propriétaire du repository

## 📝 Format de l'URL avec Token

```bash
# Format général
https://TOKEN@github.com/USERNAME/REPOSITORY.git

# Votre cas spécifique
https://VOTRE-TOKEN@github.com/malijama/Analyse-des-syst-mes-ducatifs-mondiaux.git
```

## ✅ Vérification du Succès

Une fois le push réussi, vous devriez voir :
```
Enumerating objects: X, done.
Counting objects: 100% (X/X), done.
Delta compression using up to X threads
Compressing objects: 100% (X/X), done.
Writing objects: 100% (X/X), X.XX KiB | X.XX MiB/s, done.
Total X (delta X), reused X (delta X), pack-reused 0
To https://github.com/malijama/Analyse-des-syst-mes-ducatifs-mondiaux.git
 * [new branch]      main -> main
Branch 'main' set up to track remote branch 'main' from 'origin'.
```

## 🎯 Prochaines Étapes

Après un push réussi :
1. ✅ Vérifiez que votre code est visible sur GitHub
2. ✅ Ajoutez des topics à votre repository
3. ✅ Activez GitHub Pages (optionnel)
4. ✅ Ajoutez des captures d'écran au README
5. ✅ Partagez le lien sur LinkedIn

---

💡 **Conseil** : Gardez votre token en sécurité et ne le partagez jamais publiquement !