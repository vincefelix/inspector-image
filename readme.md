# Image Inspector Tool

## Description  
L'Image Inspector est un outil de ligne de commande conçu pour analyser les images numériques. Il permet d'extraire les métadonnées et de détecter des données cachées, telles que des clés PGP, à des fins d'analyse en cybersécurité et d'investigation numérique.

---

## Fonctionnalités  
- **Extraction des métadonnées** : Informations telles que géolocalisation, appareil, date, etc.  
- **Détection de stéganographie** : Extraction de données cachées, notamment les clés PGP.

---

## Installation  

---
## Prérequis  
- **Python 3.x**  
- Modules nécessaires :  
  ```bash
  pip install pillow piexif stegano
- Cloner le projet
    ```bash
    Copier
    Modifier
    git clone https://learn.zone01dakar.sn/git/vindour/inspector-image.git
    cd inspector-image```

---
## Utilisation
- Commande d'Aide
    ```bash
    python main.py -help
    Affiche une description des options disponibles.
    ```

- Extraction des métadonnées
    ```bash
    python main.py -m <chemin_image> -o <fichier_sortie>
    Exemple :
    python main.py -m image.jpeg -o metadata.txt
    ```

- Détection de données cachées
    ```bash
    python main.py -s <chemin_image> -o <fichier_sortie>
    Exemple :
    python main.py -s image.jpeg -o hidden_data.txt
    ```

## Avertissement Éthique
L'analyse d'images pour détecter des données cachées ou extraire des métadonnées doit toujours respecter les considérations éthiques et légales. L'utilisation abusive de cet outil est strictement interdite.

    - Exemples de Résultats
        -----BEGIN PGP PUBLIC KEY BLOCK-----
        Version: 01

        mQENBGIwpy4BC...
        =N8hc
        -----END PGP PUBLIC KEY BLOCK-----
    - Test
        Pour tester l'outil avec des images fournies :
        python main.py -s image-example1.jpeg image-example2.jpeg
    

## Contribution
Les contributions sont les bienvenues ! Merci de proposer des améliorations ou de signaler des problèmes via des issues.

## Licence
Zone01Dakar License [https://www.zone01dakar.sn]

