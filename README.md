# Gestion des Tâches Collaboratives - ESMT

Application web de gestion des tâches collaboratives pour les enseignants et étudiants de l'ESMT.

## Technologies utilisées
- Python / Django
- SQLite
- Bootstrap 5

## Installation

### 1. Cloner le projet
git clone https://github.com/sadikhnd7/gestion-taches-esmt
cd gestion_taches

### 2. Installer les dépendances
pip install django

### 3. Appliquer les migrations
python manage.py migrate

### 4. Créer un compte admin
python manage.py createsuperuser

### 5. Lancer le serveur
python manage.py runserver

### 6. Accéder à l'application
- Application : http://127.0.0.1:8000
- Admin : http://127.0.0.1:8000/admin

## Modèles de données

### Profile
| Champ | Type | Description |
|-------|------|-------------|
| user | OneToOneField | Lié à l'utilisateur Django |
| role | CharField | etudiant ou professeur |
| avatar | ImageField | Photo de profil |

### Project
| Champ | Type | Description |
|-------|------|-------------|
| name | CharField | Nom du projet |
| description | TextField | Description |
| created_by | ForeignKey | Créateur du projet |
| members | ManyToManyField | Membres du projet |

### Task
| Champ | Type | Description |
|-------|------|-------------|
| title | CharField | Titre de la tâche |
| description | TextField | Description |
| deadline | DateTimeField | Date limite |
| status | CharField | todo/in_progress/done |
| project | ForeignKey | Projet associé |
| assigned_to | ForeignKey | Utilisateur assigné |
| created_by | ForeignKey | Créateur de la tâche |
| completed_at | DateTimeField | Date de complétion |

## Routes disponibles
| URL | Méthode | Description |
|-----|---------|-------------|
| /register/ | GET/POST | Inscription |
| /login/ | GET/POST | Connexion |
| /logout/ | GET | Déconnexion |
| / | GET | Tableau de bord |
| /profile/ | GET/POST | Mon profil |
| /stats/ | GET | Statistiques et primes |
| /projects/create/ | GET/POST | Créer un projet |
| /projects/<pk>/edit/ | GET/POST | Modifier un projet |
| /projects/<pk>/delete/ | GET | Supprimer un projet |
| /projects/<pk>/add_member/ | GET/POST | Ajouter un membre |
| /tasks/create/ | GET/POST | Créer une tâche |
| /tasks/<pk>/edit/ | GET/POST | Modifier une tâche |
| /tasks/<pk>/delete/ | GET | Supprimer une tâche |

## Règles métier
- Un étudiant ne peut pas assigner un professeur à une tâche
- Seul le créateur d'un projet peut ajouter/supprimer des tâches
- Les utilisateurs assignés peuvent uniquement modifier leurs tâches
- Prime de 30 000 FCFA pour 90% des tâches dans les délais
- Prime de 100 000 FCFA pour 100% des tâches dans les délais