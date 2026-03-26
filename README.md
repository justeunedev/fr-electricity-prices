# ⚡ French Electricity TURPE TTC (CU4 Only)

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)
![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)
![GitHub Actions](https://img.shields.io/badge/GitHub_Actions-2088FF?style=for-the-badge&logo=github-actions&logoColor=white)
![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg?style=for-the-badge)
![Update Data](https://github.com/justeunedev/fr-electricity-prices/actions/workflows/update_tarifs.yml/badge.svg?style=for-the-badge)

---

Une application Python/Streamlit conçue pour suivre en temps réel les prix dynamiques de l'électricité en France, en intégrant automatiquement les prix Spot, le TURPE (uniquement CU4) et toutes les taxes (TTC).
Les données sont fournies par l'API publique du fournisseur d'électricité Sobry, afin d'être utiliser avec un de leur contrat.
L'API utilisée affiche le tarif particulier TTC et utilise le TURPE CU4 uniquement pour l'instant.

## Lien d'accès
Disponible publiquement :
- [**Hébergé sur Streamlit**](https://justeunedev-elecprices.streamlit.app), dépendant de Github Workflow et de la disponibilité de Streamlit, utilisant directement ce code source.

## 🛠️ Structure du Projet
- `app.py` : Interface utilisateur (Streamlit).
- `fetch_data.py` : Script backend pour récupérer les données de l'API et gérer la rétention des fichiers.
- `notifier.py` : Permet d'envoyer des notifications via NTFY.
- `.env` : Configuration des identifiants NTFY.
- `data/` : Dossier contenant les fichiers JSON quotidiens (historique glissant de 30 jours).
- `.github/workflows/update_tarifs.yml` : GitHub Action pour l'automatisation quotidienne de la récupération des prix.

## 🚀 Fonctionnalités
- **Zéro Maintenance** : GitHub Actions récupère automatiquement les prix du lendemain tous les jours via l'API publique de Sobry.
- **Nettoyage Intelligent** : `fetch_data.py` supprime automatiquement les fichiers JSON vieux de plus de 30 jours pour garder un environnement propre.
- **Accessibilité Cognitive** : Les couleurs sont calquées sur le Tarif Bleu officiel d'EDF (Heures Pleines / Heures Creuses) pour une prise de décision visuelle rapide, limitant la charge mentale.
- **Notifications** : Possibilité de recevoir des notifications directement via un serveur NTFY selon différents canaux.

## 🎨 Code Couleur (Référence Tarif Bleu EDF)
- **🟢 Vert Foncé (< 12.00 c€)** : Exceptionnel. Le meilleur moment pour lancer les gros appareils énergivores.
- **🍏 Vert Clair (12.00 - 15.79 c€)** : Très avantageux (Moins cher que les Heures Creuses Tarif Bleu d'EDF).
- **🟡 Jaune (15.79 - 18.22 c€)** : Zone neutre.
- **🟠 Orange (18.22 - 20.65 c€)** : Vigilance (On se rapproche du tarif Heures Pleines Tarif Bleu d'EDF).
- **🔴 Rouge (> 20.65 c€)** : À éviter (Plus cher que les Heures Pleines Tarif Bleu d'EDF).

## 🔔 Notifications Publiques
Vous pouvez accéder à des notifications fournies par le serveur NTFY d'Arniael en indiquant le serveur personnalisé [https://notif.arniael.eu](https://notif.arniael.eu) ainsi que le topic qui vous intéresse :
- **Notifications Générales de la journée** [jud-elecfr-general](https://notif.arniael.eu/jud-elecfr-general) : Des notifications thématisée. Une le matin à 7h30 pour le prix moyen de la journée (8h - 22h) et de la matinée (8h - 13h). Une à 12h30 pour la moyenne de l'après-midi (13h - 18), une à 13h11 pour vous indiquer que les tarifs du lendemain sont disponibles, accompagnés de la moyenne de la journée (8h - 22h) et de la nuit (00h - 06h / 22h - 00h) pour le lendemain. Une à 17h30 pour vous indiquer le prix moyen de la soirée (18h - 22) et enfin une dernière à 21h30 pour le prix moyen de la nuit (22h - 06h).
- **Notifications du prix tous les quarts d'heures** [jud-elecfr-15min](https://notif.arniael.eu/jud-elecfr-15min) : Une notification toutes les 15 minutes pour vous avertir du prix désormais en cours et de celui du quart d'heure qui suivra.
- **Notifications de la moyenne horaire** [jud-elecfr-hourly](https://notif.arniael.eu/jud-elecfr-hourly) : Une notification toutes les heures 15 minutes avant le début de la prochaine heure pour indiquer le prix moyen de l'heure qui arrive.
- **Notifications de la moyenne des trois prochaines heures** [jud-elecfr-3hours](https://notif.arniael.eu/jud-elecfr-3hours) : Une notification toutes les 3 heures, 15 minutes avant le début du prochain bloc de 3 heures, avec la moyenne des trois prochaines heures et le prix moyen de chacune des heures de ce bloc.

## ⚙️ Installation
1. Créer un dépôt GitHub et y pousser ces fichiers.
2. Autoriser l'écriture pour les Actions dans `Settings > Actions > General > Workflow permissions` (cocher **Read and write permissions**).
3. Déployer le dépôt gratuitement sur **Streamlit Community Cloud**.
4. En cas de self-hosting, possibilité de configurer le .env.example (renommer en .env ensuite) pour envoyer des notifications via un serveur NTFY.
5. Configurer une tâche cron pour enclencher notifier.py et fetch_data.py aux heures voulues.

---

## 👩‍💻 Crédits & Licence
Une app de **Juste Une Dev** - justeunedev(a)arniael.fr  
Distribué sous la **Licence MIT**.
Basée sur l'API publique de [Sobry](https://api.sobry.co/docs)
