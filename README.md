# CV Blindé

> Outil libre pour que ton CV arrive jusqu'aux yeux d'un humain.

## Le problème

Tu envoies ton CV. Pas de réponse. Tu en envoies dix de plus. Toujours rien. L'annonce est relancée trois mois plus tard. Tu te demandes si quelqu'un l'a seulement ouverte.

Réponse honnête : probablement non. Pas par méchanceté. Parce qu'entre toi et le recruteur, il y a un logiciel — un **ATS** (Applicant Tracking System) — qui lit ton CV avant qu'aucun humain ne le voie. Et ce logiciel n'est pas malin. Quand ton CV utilise :

- Des **colonnes** (typique des CV "design" sortis de Canva)
- Des **icônes** à la place des mots ("Email", "Téléphone")
- Des **tableaux**, des **graphiques de compétences** (les fameuses jauges)
- Des **polices fantaisistes** ou trop décoratives
- Des **headers/footers**, des images de fond, des couleurs sur du texte

…le logiciel n'arrive pas à extraire correctement les infos. Ton nom devient illisible, tes expériences se mélangent, tes compétences disparaissent. Tu n'es pas "rejeté" : tu deviens **invisible** quand le recruteur fait une recherche dans la base.

Et France Travail (ex-Pôle Emploi), qui pousse des modèles graphiques à ses inscrits, n'aide pas.

## Ce que fait cet outil

Cet outil ne triche pas. Il ne cache pas du faux texte dans tes pages. Il fait une chose simple : **il rend ton CV correctement lisible par les machines**, sans toucher à son apparence pour les humains.

Deux outils, deux cas d'usage, à choisir selon ta situation :

### 🛡️ `blinder-mon-cv/` — j'ai déjà un CV graphique, je veux qu'il passe les ATS

Une page web qui marche dans n'importe quel navigateur. À ouvrir directement, aucune installation.

1. Tu glisses ton CV graphique (PDF ou DOCX)
2. **Le diagnostic** : tu vois côte à côte ce que voit le recruteur (rendu visuel) et ce que l'ATS extrait (texte ordonné). Chaque fragment est numéroté ; en le survolant à droite, sa position s'éclaire à gauche. Les "sauts de lecture" suspects (typiques des CVs en colonnes lus en zigzag) sont signalés en rouge. Un verdict t'explique si ton CV est correctement lu ou non.
3. Tu colles l'offre d'emploi (optionnel) — l'outil détecte les mots-clés présents dans l'offre mais absents de ton CV
4. Tu télécharges un PDF qui contient **ton CV graphique en première page** + **une page "ATS-friendly"** ajoutée à la fin avec le texte propre, structuré, contenant les bons mots-clés

L'humain qui clique pour voir le PDF voit ton design. Le logiciel ATS parse les deux pages et range correctement toutes les infos dans sa base. Plus de candidature invisible.

C'est ce diagnostic visuel qui rend tangible le problème : la plupart des gens ne croient pas que leur CV puisse être mal lu jusqu'à ce qu'ils voient les sauts de lecture sur leur propre fichier.

**Pour l'utiliser** : ouvre `blinder-mon-cv/index.html` dans ton navigateur, c'est tout. Aucune installation. Tout reste dans ton navigateur, rien n'est envoyé sur un serveur — ton CV reste chez toi.

Pour le mettre en ligne : pousse le repo sur GitHub, active GitHub Pages sur le dossier `blinder-mon-cv/`, et c'est accessible publiquement gratuitement.

### 📄 `creer-mon-cv/` — je pars de zéro, je veux un CV chirurgicalement propre

Un script Python qui génère un CV à partir d'un simple fichier texte structuré (YAML).

C'est l'approche "ceinture et bretelles" : au lieu de partir d'un CV graphique et de coller une page propre derrière, on génère **directement un CV structuré sémantiquement**, où chaque section est explicitement marquée (titre, paragraphe, liste, etc.).

C'est techniquement plus solide (le PDF est balisé dès le départ avec une langue déclarée, des sections sémantiques, des métadonnées propres), mais ça veut dire renoncer à un design custom. Pour qui ? Plutôt les profils où le contenu compte plus que le look : tech, ingé, fonctions support, scientifique, juridique.

**Pour l'utiliser** :

```bash
cd creer-mon-cv/
pip install -r requirements.txt
python creer_cv.py exemple_cv.yaml -o mon_cv.pdf
```

Édite `exemple_cv.yaml` (c'est juste du texte structuré, ça se modifie dans n'importe quel éditeur) puis relance la commande.

## Lequel choisir ?

| Ta situation | L'outil pour toi |
|---|---|
| J'ai déjà un CV qui me plaît visuellement | `blinder-mon-cv/` |
| Je veux juste voir ce que l'ATS voit de mon CV actuel | `blinder-mon-cv/` (étape 02 du diagnostic suffit) |
| Je pars de zéro et le design m'importe peu | `creer-mon-cv/` |
| Je veux la version la plus robuste possible pour les ATS | `creer-mon-cv/` |
| Je suis à l'aise avec le terminal et un fichier texte | `creer-mon-cv/` |
| Je préfère cliquer dans un navigateur | `blinder-mon-cv/` |

Et rien n'empêche de faire les deux : générer un CV propre avec `creer-mon-cv`, puis passer le PDF résultat dans `blinder-mon-cv` pour vérifier le diagnostic.

## Quelques règles à connaître quoi qu'il arrive

Aucun outil ne remplace ces principes de base. Si tu les respectes, tu doubles déjà tes chances :

1. **Adapte ton CV à chaque offre.** Reprends les mots exacts utilisés dans l'annonce. Le logiciel cherche du littéral.
2. **Acronymes ET noms complets.** "Gestion de la relation client (CRM)" plutôt que juste "CRM" ou juste "GRC".
3. **Sections nommées simplement.** "Expérience professionnelle", "Formation", "Compétences". Pas "Mon parcours fou" ou "Ce qui me définit".
4. **Dates au format constant.** MM/AAAA – MM/AAAA partout.
5. **Une info par ligne.** Pas de tableaux. Pas de colonnes.

## L'esprit du projet

C'est libre, c'est ouvert, c'est forkable. Si tu trouves que c'est bancal, change-le. Si tu trouves que ça manque (un parseur pour LinkedIn, un dictionnaire ROME, une version pour autre chose qu'un CV…), ajoute-le.

L'idée n'est pas de "casser" les ATS. C'est de rétablir l'équilibre : tant que les recruteurs délèguent leur premier tri à des machines mal conçues, les candidats ont le droit de savoir comment ces machines lisent leurs CV — et de présenter leur travail dans un format que ces machines comprennent.

## Licence

MIT. Fais-en ce que tu veux. Si ça aide quelqu'un autour de toi, c'est gagné.

## Pour aller plus loin

- `EXPLICATIONS.md` : comment fonctionnent vraiment les ATS, en détail
- `blinder-mon-cv/` : la page web (HTML+JS, autonome)
- `creer-mon-cv/` : le script Python (avec exemple YAML)
