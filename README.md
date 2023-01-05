# Data Storytelling Covid19 - Énergies

L’objectif de ce data storytelling est de mettre en avant la consommation et la production énergétique (gaz et électricité) française durant la période covid-19 de 2019 à 2022.  

## Installation Linux/MacOs ou Windows
1. À la racine du projet, lancer la commande `make install_requirements` ou `pip3 install -r requirements.txt`

## Lancer l'application Linux/MacOs ou Windows
2. À la racine du projet, lancer la commande `make run` ou `streamlit run index.py`

## Description de l'application

* index.py : Construction de la page WEB contenant les graphiques
* contents/ : Package servant à l'élaboration des graphiques
* contents/process.py : Algorithmes de récupération des données, de mise en forme des données et de création des graphiques
* contents/sides.py : Fonctions de manipulation des dataframes et de données
* contents/utils.py : Variables globales
* data/ : Dossier contenant les données brutes utilisées pour le datastorytelling
* docs/ : Recherches et documentation relative aux données et aux graphiques
