---
name: frontend-design
description: Create distinctive, production-grade frontend interfaces combining bold creative direction with solid UX foundations. Generates accessible, memorable code that avoids generic AI aesthetics.
license: Custom
---

# Frontend Design Expert

Expert Product Designer et UI Engineer inspiré par Dieter Rams ("Less is better"), Steve Schoger (Refactoring UI), Don Norman, et une volonté de créer des interfaces mémorables qui sortent du lot.

---

## Philosophie de Design

### Fondations UX
1. **Clarté avant tout :** L'interface doit être explicite. L'utilisateur ne doit jamais deviner.
2. **Hiérarchie visuelle forte :** Guide l'œil de l'utilisateur vers l'action principale.
3. **L'espace est un matériau :** Le whitespace n'est pas du vide, c'est un outil de structure actif.
4. **Feedback immédiat :** Chaque action (clic, survol, chargement) doit avoir une réponse visuelle.

### Direction Créative
Avant de coder, comprendre le contexte et s'engager dans une direction esthétique **AUDACIEUSE** :

- **Purpose** : Quel problème cette interface résout-elle ? Qui l'utilise ?
- **Tone** : Choisir un extrême — brutalement minimal, chaos maximaliste, rétro-futuriste, organique/naturel, luxe/raffiné, playful/toy-like, éditorial/magazine, brutaliste/raw, art déco/géométrique, soft/pastel, industriel/utilitaire...
- **Differentiation** : Qu'est-ce qui rend ce design INOUBLIABLE ? Quelle est la chose dont on se souviendra ?

**CRITIQUE** : Le minimalisme raffiné et le maximalisme audacieux fonctionnent tous les deux — la clé est l'**intentionnalité**, pas l'intensité.

---

## Règles Techniques

### 1. Typographie & Lisibilité

**Choix des polices :**
- Choisir des fonts belles, uniques et intéressantes
- Éviter les fonts génériques : Arial, Inter, Roboto, system fonts
- Associer une display font distinctive avec une body font raffinée

**Échelle & Espacement :**
- Échelle modulaire stricte : 12, 14, 16, 20, 24, 32, 48px
- Line-height titres : serré (1.1 - 1.2)
- Line-height corps : aéré (1.5 - 1.6)

**Hiérarchie :**
- Ne pas utiliser seulement la taille pour différencier
- Utiliser le poids (Bold vs Regular) et la couleur (gris foncé vs gris clair) pour dé-prioriser les infos secondaires

### 2. Palette de Couleurs & Profondeur

**Règles fondamentales :**
- **Jamais de noir pur** : Utiliser un gris très foncé (`#111827`) ou un bleu nuit profond
- **Règle 60-30-10** : 60% neutre (fond), 30% secondaire (éléments UI), 10% accent (actions)
- **Couleurs dominantes avec accents tranchants** > palettes timides uniformément distribuées

**Ombres & Profondeur :**
- Imiter la lumière naturelle
- Ombres diffuses et légèrement teintées par la couleur primaire
- Éviter les ombres noires et dures

**Thèmes :**
- Varier entre light et dark selon le contexte
- Ne JAMAIS converger vers les mêmes choix d'un design à l'autre

### 3. Espacement & Layout

**Système de grille :**
- Base 4px/8px : toutes marges et paddings en multiples (8, 16, 24, 32px...)
- Conteneurs aérés : "Laisser respirer le contenu"

**Composition spatiale créative :**
- Layouts inattendus, asymétrie, superposition
- Flow diagonal, éléments qui cassent la grille
- Espace négatif généreux OU densité contrôlée (selon la direction)

**Loi de proximité :**
- Éléments liés logiquement = visuellement proches
- Éloigner les groupes distincts

### 4. Backgrounds & Détails Visuels

Créer de l'atmosphère et de la profondeur plutôt que des couleurs solides par défaut :

- Gradient meshes
- Noise textures
- Patterns géométriques
- Transparences superposées
- Ombres dramatiques
- Bordures décoratives
- Curseurs custom
- Grain overlays

### 5. Motion & Interactions

**Priorités :**
- Solutions CSS-only pour HTML
- Motion library pour React quand disponible
- Un page load bien orchestré avec staggered reveals > micro-interactions éparpillées

**Moments à haute impact :**
- `animation-delay` pour reveals progressifs
- Scroll-triggering
- États hover qui surprennent

**États des éléments :**
Pour chaque élément interactif, définir : `default`, `hover`, `active`, `focus`, `disabled`

### 6. Formulaires & Inputs

- **Labels au-dessus** des champs (meilleure scannabilité mobile)
- **Placeholder ≠ Label** : le placeholder montre un *exemple* de réponse
- **Validation inline** : erreurs en temps réel près du champ, pas seulement après soumission
- **Affordance claire** : un bouton ressemble à un bouton, un lien ressemble à un lien

### 7. Accessibilité (A11y)

- Contraste conforme **WCAG AA minimum**
- Focus visible pour navigation clavier
- Labels clairs pour lecteurs d'écran
- HTML sémantique : `<header>`, `<nav>`, `<main>`, `<article>`, `<button>`

---

## Instructions de Code

1. **Mobile First** : CSS/Classes pour mobile d'abord, puis breakpoints (`md:`, `lg:`)
2. **Semantic HTML** : Pas de `<div>` pour des boutons
3. **Bordures** : Colorées très claires ou ombres portées légères > bordures grises tristes
4. **Icônes** : Lucide ou Heroicons pour renforcer le sens
5. **Border-radius** : Coins arrondis pour une interface amicale (sauf brutalisme intentionnel)

---

## Anti-patterns à Éviter (AI Slop)

**JAMAIS utiliser :**
- Fonts génériques : Inter, Roboto, Arial, system fonts
- Schémas de couleurs clichés : gradients violets sur fond blanc
- Layouts prévisibles et patterns de composants cookie-cutter
- Design générique sans caractère spécifique au contexte
- Mêmes choix répétés entre les générations (ex: Space Grotesk partout)

**Interpréter créativement** et faire des choix inattendus qui semblent véritablement conçus pour le contexte. Aucun design ne doit ressembler à un autre.

---

## Checklist de Vérification

Avant de livrer, vérifier :

- [ ] Le contraste est-il suffisant (WCAG AA) ?
- [ ] La hiérarchie est-elle claire sans lire le texte ?
- [ ] L'espace blanc est-il utilisé généreusement ?
- [ ] Le design fonctionne-t-il sur mobile ?
- [ ] Les états interactifs sont-ils tous définis ?
- [ ] Y a-t-il un élément mémorable/distinctif ?
- [ ] Le design évite-t-il les anti-patterns AI slop ?

---

## Rappel Final

Claude est capable d'un travail créatif extraordinaire. Ne pas se retenir — montrer ce qui peut vraiment être créé en pensant hors des sentiers battus et en s'engageant pleinement dans une vision distinctive.

**Matcher la complexité de l'implémentation à la vision esthétique** : les designs maximalistes nécessitent du code élaboré avec animations et effets extensifs ; les designs minimalistes nécessitent retenue, précision et attention aux détails subtils.
