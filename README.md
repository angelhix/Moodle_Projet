# AGL - Learning Management System (LMS)

## 📚 Vue d'ensemble

**AGL** est une plateforme d'apprentissage numérique complète et professionnelle conçue pour faciliter la gestion des cours, des devoirs et des interactions entre **enseignants** et **étudiants**. Basée sur **Django**, cette application web offre une solution robuste pour l'enseignement en ligne et la gestion académique.

---

## 🎯 Objectifs du projet

- Fournir une plateforme centralisée pour la gestion des cours
- Permettre aux enseignants de créer et gérer des cours et des devoirs
- Permettre aux étudiants de s'inscrire aux cours et de soumettre leurs devoirs
- Automatiser le processus de notation et d'évaluation
- Offrir une interface intuitive pour faciliter l'apprentissage en ligne

---

## ✨ Fonctionnalités principales

### 👥 Gestion des utilisateurs
- **Authentification duale** : Connexion séparée pour enseignants et étudiants
- **Inscription** : Création de compte pour les deux rôles
- **Profils personnalisés** : Espace dédié pour chaque utilisateur
- **Système de rôles** : Distinction claire entre enseignants et étudiants

### 📖 Gestion des cours
- **Création de cours** : Les enseignants peuvent créer et gérer leurs propres cours
- **Description détaillée** : Chaque cours inclut un titre et une description
- **Inscription des étudiants** : Les enseignants peuvent ajouter des étudiants à leurs cours
- **Vue d'ensemble** : Suivi de tous les étudiants inscrits

### 📝 Gestion des devoirs
- **Création de devoirs** : Les enseignants peuvent créer des devoirs pour chaque cours
- **Dates limites** : Définition de délais pour les soumissions
- **Descriptions détaillées** : Instructions claires pour chaque devoir
- **Suivi des soumissions** : Visualisation de toutes les soumissions par devoir

### 📤 Soumissions et notation
- **Upload de fichiers** : Les étudiants peuvent soumettre leurs travaux
- **Notation automatisée** : Les enseignants peuvent attribuer des notes
- **Historique des soumissions** : Suivi complet des dates et notes
- **Vue des notes** : Les étudiants peuvent consulter leurs notes et feedback

### 📊 Tableaux de bord
- **Tableau de bord étudiant** : Vue d'ensemble des cours, devoirs à venir et notes
- **Tableau de bord enseignant** : Gestion complète des cours, devoirs et soumissions
- **Notifications** : Affichage des devoirs à échéance dans les 7 prochains jours

### 🖨️ Impression de profil
- **Profil imprimable** : Les étudiants peuvent exporter leur profil complet
- **Résumé académique** : Génération d'un document avec tous les cours et notes

---

## 🏗️ Architecture et structure du projet

```
AGL/
├── manage.py                    # Script de gestion Django
├── AGLprojet/                   # Configuration principale du projet Django
│   ├── settings.py              # Paramètres Django (DB, apps, middleware)
│   ├── urls.py                  # Routing principal
│   ├── wsgi.py                  # Configuration WSGI
│   └── asgi.py                  # Configuration ASGI
├── appli/                       # Application principale
│   ├── models.py                # Modèles de données (User, Course, Assignment, Submission)
│   ├── views.py                 # Logique métier et vues
│   ├── urls.py                  # Routing de l'application
│   ├── forms.py                 # Formulaires Django
│   ├── admin.py                 # Configuration du panneau admin Django
│   ├── templates/appli/         # Fichiers HTML
│   └── migrations/              # Migrations de base de données
└── static/                      # Fichiers statiques (CSS, JS, images)
```

---

## 📦 Modèles de données

### **User** (Utilisateur personnalisé)
```python
- username : CharField (unique)
- email : EmailField
- password : Hashed password
- is_teacher : Boolean (enseignant ?)
- is_student : Boolean (étudiant ?)
```

### **Course** (Cours)
```python
- titre : CharField (max 255)
- description : TextField
- teacher : ForeignKey(User) - Enseignant créateur
- date_creation : DateTimeField (auto)
```

### **Enrollment** (Inscription)
```python
- student : ForeignKey(User)
- course : ForeignKey(Course)
- date_inscription : DateTimeField (auto)
```

### **Assignment** (Devoir)
```python
- course : ForeignKey(Course)
- titre : CharField (max 255)
- description : TextField
- date_creation : DateTimeField (auto)
- date_limite : DateTimeField
```

### **Submission** (Soumission)
```python
- assignment : ForeignKey(Assignment)
- student : ForeignKey(User)
- fichier : FileField (upload_to='submissions/')
- note : DecimalField (0-100)
- date_soumission : DateTimeField (auto)
```

---

## 🔄 Flux de fonctionnement

### Pour les **Enseignants** :
1. Inscription/Connexion
2. Création d'un cours
3. Ajout d'étudiants au cours
4. Création de devoirs avec date limite
5. Consultation des soumissions
6. Attribution des notes
7. Suivi des performances des étudiants

### Pour les **Étudiants** :
1. Inscription/Connexion
2. Consultation des cours disponibles
3. Inscription aux cours
4. Consultation des devoirs
5. Soumission des travaux
6. Consultation des notes et feedback
7. Génération d'un profil académique

---

## 🚀 Installation et configuration

### Prérequis
- Python 3.9+
- PostgreSQL
- Django 6.0.1
- pip (gestionnaire de paquets)

### Étapes d'installation

1. **Cloner le repository**
   ```bash
   git clone https://github.com/angelhix/AGL.git
   cd AGL
   ```

2. **Créer un environnement virtuel**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Sur Windows: venv\Scripts\activate
   ```

3. **Installer les dépendances**
   ```bash
   pip install django==6.0.1 psycopg2-binary
   ```

4. **Configurer la base de données**
   - Éditer `AGLprojet/settings.py`
   - Remplacer les identifiants PostgreSQL
   ```python
   DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.postgresql',
           'NAME': 'agl_db',
           'USER': 'votre_utilisateur',
           'PASSWORD': 'votre_mot_de_passe',
           'HOST': 'localhost',
           'PORT': '5432',
       }
   }
   ```

5. **Exécuter les migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Créer un superutilisateur**
   ```bash
   python manage.py createsuperuser
   ```

7. **Lancer le serveur de développement**
   ```bash
   python manage.py runserver
   ```
   
   L'application sera accessible à `http://127.0.0.1:8000/`

---

## 🌐 Routes principales

| Route | Description |
|-------|-------------|
| `/` | Page d'accueil |
| `/login/etudiant/` | Connexion étudiant |
| `/login/professeur/` | Connexion enseignant |
| `/logout/` | Déconnexion |
| `/student/dashboard/` | Tableau de bord étudiant |
| `/teacher/dashboard/` | Tableau de bord enseignant |
| `/student/cours/` | Liste des cours (étudiant) |
| `/teacher/courses/` | Gestion des cours (enseignant) |
| `/teacher/assignments/` | Gestion des devoirs (enseignant) |
| `/teacher/submissions/` | Gestion des soumissions (enseignant) |

---

## 🛠️ Technologie utilisée

| Technologie | Version | Utilisation |
|-------------|---------|-------------|
| **Django** | 6.0.1 | Framework web principal |
| **Python** | 3.9+ | Langage de programmation |
| **PostgreSQL** | 12+ | Base de données |
| **HTML/CSS** | Latest | Frontend (templates Django) |
| **JavaScript** | ES6 | Interactions frontend |

---

## 📋 Composition du code

- **HTML** : 65.9% (Templates et interface utilisateur)
- **Python** : 34.1% (Logique métier et backend)

---

## 🔐 Sécurité

- ✅ Authentification utilisateur obligatoire
- ✅ Séparation des rôles (enseignant/étudiant)
- ✅ Validation des permissions
- ✅ Protection CSRF intégrée dans Django
- ✅ Gestion sécurisée des mots de passe (hachage)

---

## 📱 Interface utilisateur

L'application dispose d'une interface complète avec :
- **Pages de connexion/inscription** séparées pour enseignants et étudiants
- **Tableaux de bord** personnalisés selon le rôle
- **Formulaires** pour la création de cours et devoirs
- **Listes** pour la visualisation des étudiants et soumissions
- **Profils** étudiants imprimables

---

## 🔧 Pannel d'administration

Accédez à `/admin/` pour gérer :
- ✅ Les utilisateurs (créer, modifier, supprimer)
- ✅ Les cours (modifier, surveiller)
- ✅ Les devoirs (gérer les détails)
- ✅ Les soumissions (consulter les notes)
- ✅ Les inscriptions (gérer les étudiants par cours)

---

## 📈 Améliorations futures

- 📌 Système de messagerie entre enseignants et étudiants
- 📌 Notifications par email
- 📌 Système de quizz et tests en ligne
- 📌 Téléchargement de ressources d'apprentissage
- 📌 Statistiques et graphiques de performance
- 📌 Système de commentaires et feedback
- 📌 Export des résultats en PDF
- 📌 Interface mobile responsive
- 📌 Intégration avec OAuth2 (Google, Microsoft)

---

## 🤝 Contribution

Les contributions sont bienvenues ! Veuillez :
1. Fork le projet
2. Créer une branche pour votre fonctionnalité
3. Commiter vos changements
4. Pousser vers la branche
5. Ouvrir une Pull Request

---

## 📄 Licence

Ce projet est open source et disponible sous la licence MIT.

---

## 👤 Auteur

**Créé par** : [angelhix](https://github.com/angelhix)

---

## 📞 Support et assistance

Pour des questions ou des problèmes, veuillez :
- Ouvrir une issue sur GitHub
- Consulter la documentation Django : https://docs.djangoproject.com/
- Vérifier les configurations dans `AGLprojet/settings.py`

---

## 🎓 Ressources utiles

- [Documentation Django](https://docs.djangoproject.com/)
- [Guide Django Models](https://docs.djangoproject.com/en/stable/topics/db/models/)
- [Django Admin Documentation](https://docs.djangoproject.com/en/stable/ref/contrib/admin/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)

---

**Dernière mise à jour** : Janvier 2026  
**Statut du projet** : En développement actif ✅
