.. _indic:

===========================
Indictateurs et graphiques
===========================

Les types de représentations
=============================

Afin de rendre compte au mieux des données, nous utilisons trois types de représentations:

* **Compteurs**: ceux-ci codés en JS représentent les 3 scores ESG sur la page d'accueil
* **Graphiques**: que ce soit des graphiques lignes ou bar ils servent à représenter l'évolution temporel d'un indicateur 
* **Echelles de couleurs**: lorsque qu'un indicateur est calculé à partir d'un modèle, il est représenté sous la forme d'une échelle de couleurs comme on peut le retrouver dans la page Social avec le rayonement de l'exploitation.
* **Cartes**: ce support est utilisé pour représentées des données spatiales avec une dimension temporelle


Exemple d'indicateurs
===========================

Carte des feu de forêts
------------------------

Sur la base des données `du Climate Data Store <https://cds.climate.copernicus.eu/cdsapp#!/dataset/sis-tourism-fire-danger-indicators?tab=overview>`__, base de l'UE, nous avons pu exporter ces données, les traiter et les netoyer pour notre usage. Nous avons décidé de choisir les données du modèle du GIEC RCP 4.5 car représente le scenario le plus probable.
Ces données ont ensuite été présentées sur une carte disponible dans Environnement.


Graph des canicules
------------------------

Toujours sur la base des données `du Climate Data Store <https://cds.climate.copernicus.eu/cdsapp#!/dataset/sis-heat-and-cold-spells?tab=overview>`__, nous avons selectioner ces données représentant le nombre de jour de canicule. Il nous a semblé plus judicieux de ne représenter les jours de canciules que à l'emplacement du viticultuteur.