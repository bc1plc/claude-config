# Référence SEO 2026 — Blog Glys

## Statistiques SEO 2026 (contexte)

### Taux de clic (CTR) organique moyen
| Position | CTR Desktop | CTR Mobile |
|----------|-------------|------------|
| #1 | 39.8% | 33.2% |
| #2 | 18.7% | 15.8% |
| #3 | 10.2% | 9.4% |
| #4-10 | 2-7% | 1.5-5% |

### Impact des AI Overviews (AIO)
- **~30% des requêtes** affichent un AI Overview en 2026
- CTR position #1 **baisse de 15-25%** quand un AIO est affiché
- **Requêtes de niche B2B** : moins d'AIO car contenu spécialisé insuffisant
- **Stratégie** : cibler les requêtes longue traîne spécialisées où l'IA manque de données

### Zero-click searches
- **~65% des recherches** n'aboutissent à aucun clic (featured snippets, AIO, knowledge panels)
- **Contre-mesure** : créer du contenu qu'on ne peut PAS résumer (tableaux, outils, données contextuelles)

---

## Checklist SEO on-page (20 points)

### Structure & Contenu
- [ ] **H1 unique** contenant le mot-clé principal (< 60 caractères)
- [ ] **Meta title** = H1 ou variante (< 60 caractères)
- [ ] **Meta description** 150-160 caractères avec mot-clé principal et CTA implicite
- [ ] **URL/slug** court, avec le mot-clé, en minuscules, tirets (pas d'accents)
- [ ] **H2 sémantiques** couvrant les sous-thèmes (5-8 par article)
- [ ] **Introduction** de 150-200 mots avec le mot-clé dans les 100 premiers mots
- [ ] **Longueur** : 1500-3000 mots
- [ ] **Mot-clé principal** apparaît 3-5 fois naturellement
- [ ] **Mots-clés secondaires** répartis dans les H2 et le corps

### Médias & Visuels
- [ ] **Au moins 1 image** avec alt text descriptif contenant un mot-clé
- [ ] **Au moins 1 tableau** (données chiffrées, comparatifs)
- [ ] **Images optimisées** : format WebP, < 100KB, dimensions adaptées

### Liens
- [ ] **Liens internes** : 2-3 liens vers d'autres articles du blog
- [ ] **Liens externes** : 2-3 liens vers des sources officielles (legifrance, IFCE, etc.)
- [ ] **Pas de liens cassés** ni de redirections inutiles

### Technique
- [ ] **Schema.org Article** avec author, datePublished, dateModified
- [ ] **Open Graph** : title, description, image (1200x630)
- [ ] **Canonical URL** définie
- [ ] **Temps de lecture** estimé et affiché

### UX & Engagement
- [ ] **FAQ structurée** (3-5 questions) en fin d'article
- [ ] **CTA unique** vers Glys (naturel, non intrusif)

---

## Checklist pré-publication

1. [ ] Relire l'article à voix haute (fluidité)
2. [ ] Vérifier toutes les sources citées (liens fonctionnels)
3. [ ] Vérifier les dates et montants (exactitude)
4. [ ] Passer la checklist SEO on-page (20 points ci-dessus)
5. [ ] Vérifier le frontmatter (title, description, category, tags, date)
6. [ ] Générer/vérifier le slug (court, mot-clé, pas d'accent)
7. [ ] S'assurer que `draft: false` si prêt à publier
8. [ ] Vérifier le rendu sur `/blog/[slug]` en local

---

## Structure Markdown d'un article type

```markdown
---
title: "Titre optimisé < 60 caractères"
description: "Meta description 150-160 caractères avec mot-clé et CTA implicite"
date: 2026-02-15
updatedDate: 2026-02-15
author: "Équipe Glys"
category: "reglementation"
tags: ["mot-clé-1", "mot-clé-2", "mot-clé-3"]
image: "/blog/article-hero.webp"
imageAlt: "Description accessible de l'image hero"
draft: false
---

Introduction captivante de 150-200 mots. Le mot-clé principal apparaît
dans les 100 premiers mots. On pose le problème et on promet la solution.

## H2 sémantique couvrant le premier sous-thème

Contenu approfondi avec exemples concrets du monde équestre.

### H3 si nécessaire pour détailler un point

| Colonne 1 | Colonne 2 | Colonne 3 |
|-----------|-----------|-----------|
| Donnée | Donnée | Donnée |

## H2 sémantique couvrant le deuxième sous-thème

Contenu avec liens vers des sources officielles.

> Citation ou point clé mis en évidence

## En pratique : comment faire

Étapes concrètes et actionnables.

1. **Étape 1** : Description
2. **Étape 2** : Description
3. **Étape 3** : Description

## Questions fréquentes

### Question 1 ?

Réponse concise et complète.

### Question 2 ?

Réponse concise et complète.

### Question 3 ?

Réponse concise et complète.

## Ce qu'il faut retenir

Résumé en 3-5 points clés. CTA naturel vers Glys si pertinent :
"Des logiciels spécialisés comme [Glys](https://glys.io) permettent
d'automatiser [action liée au sujet de l'article]."
```

---

## Mots-clés cibles — Domaine équestre

### Haute priorité (réglementation + comptabilité)
| Mot-clé | Volume estimé | Difficulté | Intent |
|---------|---------------|------------|--------|
| factur-x écurie | Faible | Très faible | Informationnel |
| facturation électronique centre équestre | Faible | Très faible | Informationnel |
| tva centre équestre | Moyen | Faible | Informationnel |
| tva pension cheval | Moyen | Faible | Informationnel |
| registre équidés | Moyen | Faible | Informationnel |
| export fec comptabilité | Moyen | Moyen | Informationnel |
| contrôle ddpp écurie | Faible | Très faible | Informationnel |

### Priorité moyenne (gestion pratique)
| Mot-clé | Volume estimé | Difficulté | Intent |
|---------|---------------|------------|--------|
| logiciel gestion écurie | Moyen | Moyen | Transactionnel |
| gestion centre équestre | Moyen | Moyen | Mixte |
| import sire cheval | Faible | Très faible | Informationnel |
| copropriété cheval | Faible | Faible | Informationnel |
| facturation écurie pension | Faible | Très faible | Mixte |
| suivi soins cheval écurie | Faible | Très faible | Informationnel |

### Priorité basse (thought leadership)
| Mot-clé | Volume estimé | Difficulté | Intent |
|---------|---------------|------------|--------|
| logiciel équestre | Faible | Moyen | Transactionnel |
| digitalisation écurie | Très faible | Très faible | Informationnel |
| sécurité données écurie | Très faible | Très faible | Informationnel |
| application mobile écurie | Faible | Faible | Transactionnel |
| rgpd centre équestre | Très faible | Très faible | Informationnel |

---

## Catégories du blog

| Catégorie | Slug | Description |
|-----------|------|-------------|
| Réglementation | `reglementation` | Obligations légales, mises en conformité, contrôles |
| Gestion | `gestion` | Organisation quotidienne, processus métier, bonnes pratiques |
| Comptabilité | `comptabilite` | TVA, facturation, FEC, comptabilité équestre |
| Digital | `digital` | Transformation numérique, outils, sécurité des données |
| Guides | `guides` | Tutoriels pas à pas, how-to pratiques |

---

## Plan éditorial — 12 premiers articles

### Priorité 1 : Réglementation (articles 1-4)

1. **Factur-X obligatoire : ce que ça change pour les écuries en 2026**
   - Catégorie : `reglementation`
   - Mots-clés : factur-x écurie, facturation électronique centre équestre
   - Angle : nouveau calendrier, impact concret, comment se préparer

2. **TVA équestre : taux à 10% ou 20% ? Le guide complet**
   - Catégorie : `comptabilite`
   - Mots-clés : tva équestre, tva centre équestre, tva pension cheval
   - Angle : quand appliquer 10% vs 20%, cas particuliers, exemples chiffrés

3. **Registre des équidés : comment être conforme en cas de contrôle**
   - Catégorie : `reglementation`
   - Mots-clés : registre équidés, contrôle élevage cheval
   - Angle : ce que la DDPP vérifie, documents à préparer, sanctions

4. **Export FEC : le guide pour les professionnels du cheval**
   - Catégorie : `comptabilite`
   - Mots-clés : export fec écurie, comptabilité équestre, fichier écritures comptables
   - Angle : qu'est-ce que le FEC, format attendu, comment le générer

### Priorité 2 : Gestion pratique (articles 5-8)

5. **Import SIRE : récupérer automatiquement les données de vos chevaux**
   - Catégorie : `guides`
   - Mots-clés : import sire, fichier sire cheval, données ifce
   - Angle : tutoriel pas à pas, format du fichier, erreurs courantes

6. **Gérer les copropriétés de chevaux : le guide pratique**
   - Catégorie : `gestion`
   - Mots-clés : copropriété cheval, parts cheval, gestion propriétaires
   - Angle : aspects juridiques, répartition des frais, modèles de convention

7. **5 erreurs de facturation que font 90% des écuries**
   - Catégorie : `comptabilite`
   - Mots-clés : facturation écurie, erreurs facturation pension
   - Angle : erreurs concrètes avec conséquences chiffrées, comment les éviter

8. **Organiser le suivi des soins dans une écurie de 50+ chevaux**
   - Catégorie : `gestion`
   - Mots-clés : suivi soins cheval, gestion sanitaire écurie
   - Angle : planification, traçabilité, obligations vaccinales

### Priorité 3 : Thought leadership (articles 9-12)

9. **Logiciel de gestion équestre : comment choisir en 2026**
   - Catégorie : `digital`
   - Mots-clés : logiciel gestion écurie, logiciel équestre
   - Angle : critères de choix, comparatif fonctionnel, pièges à éviter

10. **Sécurité des données : pourquoi votre écurie mérite un chiffrement**
    - Catégorie : `digital`
    - Mots-clés : sécurité données écurie, rgpd équestre, chiffrement
    - Angle : risques concrets, obligations RGPD, solutions techniques simplifiées

11. **Du papier au numérique : migrer la gestion de votre centre équestre**
    - Catégorie : `digital`
    - Mots-clés : digitalisation écurie, gestion numérique cheval
    - Angle : plan de migration en 5 étapes, pièges, retour d'expérience

12. **Application mobile pour écurie : gérer ses chevaux depuis le terrain**
    - Catégorie : `digital`
    - Mots-clés : application mobile écurie, app gestion cheval
    - Angle : cas d'usage terrain, synchronisation, offline-first
