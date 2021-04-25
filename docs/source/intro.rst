===========================
Introduction
===========================



Se connecter
===========================

Pour voir le dasboard, rendez-vous sur `app.grid-tech.fr <http://app.grid-tech.fr>`__ .

Pour les besoins de la démonstration dans le cadre du concours FIFG, un compte test a été créé:

* **Nom d'utilisateur**: test
* **Mot de passe**: test

.. tip::
   Avec notre infrastructure actuelle, le chargement des pages peut praître long mais nous y travaillons.

.. attention::
   Le dashboard est pour le moment optimiser pour les écrans d'ordinateurs

Pour plus de détail sur le déploiement :ref:`instal`


Les données
============


Les données d'entrée
---------------------

Le GRID fonctionne à partir de 2 types de données d'entrées:

* Les données externes provenant de Météo France, Copernicus, etc
* Les données liées à l'exploitation:
	* Données internes rentrées par l'agriculteur par un questionaire
	* Données financières rentrées par le banquier


Données pour le PoC
---------------------

Pour le PoC, afin de démontrer la capacité dynamique du dashboard, à chaque login, une partue des des données sont tirées au hasard, en particulier celles:

* Les scores RSE présentés sur la première page
* Les données financières (cf page indicateur et le module `agri_data` pour plus de détail)

Toutes les données sont `ici <https://github.com/Green-Investement-Dashboard/data/tree/main/data_eg>`__

Pour plus de détail sur les données et leur exploitation :ref:`indic`
