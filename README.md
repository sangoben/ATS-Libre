# CV Blindé

> Trois outils libres pour que ton CV arrive jusqu'aux yeux d'un humain.

## Le problème

Tu envoies ton CV. Pas de réponse. Tu en envoies dix de plus. Toujours rien. L'annonce est relancée trois mois plus tard. Tu te demandes si quelqu'un l'a seulement ouverte.

Réponse honnête : probablement non. Pas par méchanceté. Parce qu'entre toi et le recruteur, il y a un logiciel — un **ATS** (Applicant Tracking System) — qui lit ton CV avant qu'aucun humain ne le voie. Et ce logiciel n'est pas malin. Quand ton CV utilise :

- Des **colonnes** (typique des CV "design" sortis de Canva)
- Des **icônes** à la place des mots ("Email", "Téléphone")
- Des **tableaux**, des **graphiques de compétences** (les fameuses jauges)
- Des **polices fantaisistes** ou trop décoratives
- Des **headers/footers**, des images de fond, des couleurs sur du texte

…le logiciel n'arrive pas à extraire correctement les infos. Tu n'es pas rejeté : tu deviens **invisible** dans les recherches du recruteur.

Mais le format n'est qu'une partie du problème. Même un CV parfaitement formaté peut être faible sur le **contenu** : pas assez de chiffres, des verbes faibles, des clichés ("dynamique", "rigoureux"), des sections mal nommées. Les checkers commerciaux notent ces critères durement.

## Ce que fait ce projet

Trois outils complémentaires, libres, qui tournent **entièrement dans ton navigateur** (rien n'est envoyé sur un serveur) :

### 🛡️ `blinder-mon-cv/` — j'ai un CV graphique, je veux qu'il passe les ATS

Diagnostic visuel (vue humaine vs vue machine) + ajout d'une page texte ATS-friendly à ton PDF existant. Tu gardes ton design, tu rends ton CV parseable.

→ [Lancer l'outil](blinder-mon-cv/)

### 🎯 `tester-mon-cv/` — je veux savoir ce que vaut mon contenu

Score local sur 100, calculé sur 6 critères (chiffres, verbes d'action, clichés, sections, longueur, variété). Indices progressifs en 3 niveaux pour chaque problème détecté. Comparaison permanente avec ta version d'origine. Idéal pour iterer.

→ [Lancer le test](tester-mon-cv/)

### 📄 `creer-mon-cv/` — je pars de zéro, je veux un CV chirurgicalement propre

Script Python qui génère un CV nativement structuré (PDF balisé, métadonnées propres, structure linéaire) depuis un fichier YAML lisible. Pour qui veut la solution la plus solide possible côté machine, sans se prendre la tête sur le design.

→ [Voir le code](creer-mon-cv/)

## Lequel choisir ?

| Ta situation | L'outil pour toi |
|---|---|
| J'ai déjà un CV qui me plaît visuellement | `blinder-mon-cv/` |
| Mon CV a un score faible sur Enhancv/Resume Worded | `tester-mon-cv/` |
| Je veux savoir ce que l'ATS voit de mon CV actuel | `blinder-mon-cv/` (diagnostic) |
| Je veux savoir ce que vaut mon contenu écrit | `tester-mon-cv/` |
| Je pars de zéro et le design m'importe peu | `creer-mon-cv/` |
| Je veux la version la plus robuste possible | `creer-mon-cv/` + `tester-mon-cv/` |

Les trois outils sont complémentaires. Un workflow type : `tester` pour améliorer le contenu, puis `blinder` ou `creer` pour finaliser le format.

## Quelques règles à connaître quoi qu'il arrive

Aucun outil ne remplace ces principes de base. Si tu les respectes, tu doubles déjà tes chances :

1. **Adapte ton CV à chaque offre.** Reprends les mots exacts utilisés dans l'annonce. Le logiciel cherche du littéral.
2. **Quantifie tes expériences.** Combien de personnes ? Quel budget ? Sur quelle durée ? Quel résultat ? Un chiffre vaut dix adjectifs.
3. **Verbes d'action forts.** "Pilote", "déploie", "optimise" — pas "responsable de" ou "j'ai aidé à".
4. **Sections nommées simplement.** "Expérience professionnelle", "Formation", "Compétences". Pas "Mon parcours fou".
5. **Pas de clichés.** "Dynamique" et "rigoureux" ne distinguent personne. Montre par les faits.

## L'esprit du projet

C'est libre, c'est ouvert, c'est forkable. Si tu trouves que c'est bancal, change-le. Si tu trouves que ça manque (un parseur pour LinkedIn, un dictionnaire ROME, des détections supplémentaires…), ajoute-le.

L'idée n'est pas de "casser" les ATS ni de tricher : c'est de rétablir l'équilibre. Tant que les recruteurs délèguent leur premier tri à des machines mal conçues, les candidats ont le droit de savoir comment ces machines lisent leurs CV — et de présenter leur travail dans un format que ces machines comprennent.

## Licence

MIT. Fais-en ce que tu veux. Si ça aide quelqu'un autour de toi, c'est gagné.

## Pour aller plus loin

- `EXPLICATIONS.md` : comment fonctionnent vraiment les ATS, en détail
- `blinder-mon-cv/` : la page web de blindage
- `tester-mon-cv/` : le test interactif avec indices progressifs
- `creer-mon-cv/` : le script Python de génération
