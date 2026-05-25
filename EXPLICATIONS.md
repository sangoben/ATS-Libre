# EXPLICATIONS — comment ça marche vraiment

Pour qui veut comprendre la mécanique avant de bricoler.

## Comment fonctionne un ATS

Quand tu envoies ton CV via un site emploi, il atterrit dans un logiciel (Workday, Taleo, iCIMS, SmartRecruiters, Lever, Greenhouse, BambooHR…). Ce logiciel fait **deux choses distinctes** :

### 1. Le parsing

Le logiciel extrait le texte du PDF/DOCX et essaie de le ranger automatiquement dans des champs structurés :

```
Nom: ...
Email: ...
Téléphone: ...
Expériences:
  - Poste: ...
    Entreprise: ...
    Dates: ...
Formation: ...
Compétences: ...
```

Pour faire ce rangement, l'ATS utilise :
- L'ordre du texte tel qu'il apparaît dans le fichier
- Des patterns connus (un email c'est `xxx@yyy.zz`)
- Des dictionnaires de noms de diplômes, d'entreprises, de villes
- Parfois du machine learning pour deviner les sections

**Là où ça casse** : si ton CV est sur deux colonnes, le parser lit "ligne 1 colonne gauche → ligne 1 colonne droite → ligne 2 colonne gauche → ligne 2 colonne droite…". Ton expérience récente se retrouve mélangée avec ton numéro de téléphone et ton master se retrouve dans la rubrique compétences. Si tes dates sont dans des icônes calendrier, elles ne sont jamais extraites. Si tes compétences sont représentées par des barres de progression, le logiciel ne voit rien.

### 2. La recherche

Une fois le CV "parsé", il dort dans la base. Quand le recruteur publie une annonce ou qu'il cherche dans son vivier, il tape des mots-clés : `Python développeur Lyon CDI 3 ans`. L'ATS renvoie les CVs où ces termes apparaissent (avec parfois un score de pertinence).

**Là où ça casse aussi** : si tes mots-clés ont été mal parsés (perdus dans des graphiques, des icônes, des images), le recruteur ne te trouve pas. Tu existes dans la base mais tu es invisible.

## Le mythe du "filtre IA qui détecte les CVs faits par IA"

On lit beaucoup que les ATS détecteraient les CVs générés par IA et les rejetteraient. **C'est très majoritairement faux.** Les ATS sont des outils de parsing et de stockage, pas des détecteurs de plagiat. Quelques outils RH ajoutent des modules de "détection IA", mais ils sont :
- Peu fiables (faux positifs nombreux)
- Pas activés par défaut
- Plus souvent utilisés sur les **lettres de motivation** que sur les CVs

Le vrai problème n'est pas "mon CV a été détecté comme IA", c'est "mon CV est mal parsé donc invisible".

## Pourquoi un design qui plaît à un humain casse les ATS

Quelques exemples typiques :

| Ce qui plaît à l'œil humain | Ce que le logiciel comprend |
|---|---|
| Deux colonnes (CV à la mode) | Texte mélangé, lecture en zigzag |
| Compétences en barres ou étoiles | Aucun mot-clé extrait |
| Icônes pour email/téléphone | Champs de contact perdus |
| Police décorative (Brush Script, etc.) | Caractères mal reconnus voire vides |
| Photo, logo, fond coloré | Texte parfois OCR-isé approximativement |
| Header/footer (nom, page X/Y) | Bruit qui parasite le parsing |
| Tableaux pour structurer les expériences | Cellules lues dans le désordre |
| Sections nommées "Mon univers", "What I love" | Sections non identifiées |

## Pourquoi la "page cachée" est une bonne approche

L'outil `blinder-mon-cv/` ajoute simplement une page supplémentaire au PDF, avec une version texte propre du CV. C'est plus honnête que les techniques à base de texte invisible (police blanche sur blanc, opacité 0, texte hors page) qui :

- Sont **détectées** par les ATS modernes via comparaison entre texte extrait et texte OCR-isé
- Peuvent valoir une mise en liste noire chez le recruteur si découvertes
- Sont visibles si quelqu'un sélectionne tout le texte (Ctrl+A)
- Vont à l'encontre de l'esprit (présenter honnêtement son travail)

La page ajoutée n'est pas un secret : si le recruteur scrolle jusqu'à elle, il verra le même contenu sous une forme plus brute. Aucune information n'est cachée, juste une couche supplémentaire pour la machine.

## Pourquoi la "structure native" est encore mieux

L'outil `creer-mon-cv/` va plus loin : au lieu de générer un PDF visuel et de le bidouiller, on génère **directement** un PDF qui :

- Déclare sa langue (`/Lang fr-FR` dans le catalogue)
- Se déclare comme balisé (`/MarkInfo /Marked true`)
- Utilise une structure linéaire propre, sans tableaux ni colonnes
- A des métadonnées correctes (titre, auteur, sujet)
- A des sections clairement nommées avec des titres en gras suivis de contenu

Le PDF reste lisible et joli pour un humain (sobre, mais lisible), et il est **trivialement parsable** par les ATS. Tu peux vérifier par toi-même : ouvre le PDF, fais Ctrl+A puis Ctrl+C, et colle dans un éditeur de texte. Si le résultat est dans le bon ordre, l'ATS le verra dans le bon ordre.

### Pour la conformité PDF/UA-1 stricte

PDF/UA-1 est une norme d'accessibilité qui impose un "structure tree" complet (rôles standards : Document, Sect, H1, P, L, LI, Figure, etc.) avec validation. Le script `creer_cv.py` utilise reportlab qui pose les bases (Lang, MarkInfo, métadonnées) mais ne génère pas un structure tree complet. Pour aller jusqu'à la conformité validée, deux pistes :

- **WeasyPrint** : `pip install weasyprint`, puis générer le PDF depuis du HTML sémantique avec `HTML(...).write_pdf(target, pdf_variant='pdf/ua-1')`. WeasyPrint génère un structure tree natif depuis les balises HTML.
- **Outils commerciaux** (Adobe, callas, axes4) : plus coûteux, plus complets.

Pour 95% des ATS, `creer-mon-cv/` telle qu'elle est suffit largement. La conformité PDF/UA stricte sert surtout aux lecteurs d'écran (accessibilité malvoyants), pas aux parsers ATS.

## Tester soi-même

Tu veux savoir comment ton CV actuel est lu ? Trois méthodes :

1. **Le test Ctrl+A** : ouvre ton CV, sélectionne tout, copie, colle dans un éditeur de texte. Si l'ordre est bizarre, les colonnes mélangées, les sections perdues → l'ATS verra la même chose.

2. **Le test `pdftotext`** : sur Linux/Mac, `pdftotext mon_cv.pdf -` te montre exactement ce que beaucoup d'ATS extraient.

3. **Sites de simulation gratuits** : Resume Worded, Jobscan (version gratuite limitée), CV-ATS-Checker (open source). Donnent un score et listent les problèmes.

## Limites honnêtes de l'approche

- **Ça ne te trouvera pas un emploi tout seul.** Ton contenu doit déjà être bon et l'offre doit correspondre. L'outil règle un problème technique, pas le marché de l'emploi.
- **Certains ATS très anciens** ignorent les pages au-delà de la première. Rare mais ça existe — dans ce cas, `creer-mon-cv/` (CV structuré dès le départ) est plus sûr.
- **Les filtres "hard"** (années d'expérience minimum, certifications requises, code postal) ne peuvent pas être contournés et il ne faut pas chercher à le faire.
- **Mentir reste mentir.** Si l'outil te suggère d'ajouter "SAP" parce que c'est dans l'offre et que tu n'as jamais vu SAP de ta vie, n'ajoute rien. La triche se voit en entretien.
