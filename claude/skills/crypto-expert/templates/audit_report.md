# Template de Rapport d'Audit Cryptographique

## En-tête

```markdown
# Rapport d'Audit Cryptographique

**Projet** : [Nom du projet]
**Date** : [YYYY-MM-DD]
**Auditeur** : Claude Code - Expert Crypto
**Version du code** : [commit hash ou version]
**Scope** : [Fichiers/modules audités]

---
```

## Résumé Exécutif

```markdown
## Résumé Exécutif

### Score Global de Sécurité : [X/10]

| Catégorie | Vulnérabilités |
|-----------|----------------|
| Critiques | X |
| Élevées | X |
| Modérées | X |
| Informatives | X |

### Principales Conclusions
1. [Point clé 1]
2. [Point clé 2]
3. [Point clé 3]

### Actions Immédiates Requises
- [ ] [Action 1]
- [ ] [Action 2]
```

---

## Section Vulnérabilités

### Template Vulnérabilité Critique

```markdown
## [CRITIQUE] Titre de la Vulnérabilité

**ID** : CRYPTO-001
**Sévérité** : CRITIQUE
**CVSS** : 9.8 (si applicable)
**CWE** : CWE-XXX

### Localisation
- **Fichier** : `path/to/file.py`
- **Ligne(s)** : 42-45
- **Fonction** : `generate_token()`

### Description
[Description claire du problème]

### Code Vulnérable
```python
# VULNÉRABLE
import random
token = ''.join(random.choice('abc123') for _ in range(32))
```

### Impact
- Compromission potentielle de [X]
- Attaquant peut [action possible]

### Preuve de Concept
```
[Étapes pour démontrer la vulnérabilité]
```

### Correction Recommandée
```python
# SÉCURISÉ
import secrets
token = secrets.token_urlsafe(32)
```

### Références
- [OWASP/NIST/RFC pertinent]
```

### Template Vulnérabilité Élevée

```markdown
## [ÉLEVÉ] Titre de la Vulnérabilité

**ID** : CRYPTO-002
**Sévérité** : ÉLEVÉ

### Localisation
- **Fichier** : `path/to/file.py`
- **Ligne(s)** : 128

### Description
[Description]

### Code Problématique
```python
# À CORRIGER
if user_signature == expected_signature:  # Timing attack possible
```

### Risque
[Explication du risque]

### Correction
```python
# CORRIGÉ
import hmac
if hmac.compare_digest(user_signature, expected_signature):
```
```

### Template Vulnérabilité Modérée

```markdown
## [MODÉRÉ] Titre du Problème

**ID** : CRYPTO-003
**Sévérité** : MODÉRÉ

### Localisation
- **Fichier** : `path/to/file.py`

### Description
[Description]

### Recommandation
[Action à prendre]
```

### Template Information

```markdown
## [INFO] Observation

**ID** : CRYPTO-004
**Sévérité** : INFORMATIF

### Observation
[Observation qui n'est pas une vulnérabilité mais mérite attention]

### Suggestion
[Amélioration suggérée]
```

---

## Section Analyse par Domaine

### Générateurs Aléatoires (RNG)

```markdown
## Analyse RNG

### Résultat : ✓ Conforme / ⚠ Attention Requise / ✗ Non Conforme

### Usages Détectés

| Fichier | Ligne | Code | Statut |
|---------|-------|------|--------|
| auth.py | 23 | `secrets.token_urlsafe()` | ✓ Sûr |
| utils.py | 45 | `random.randint()` | ✗ Dangereux |

### Conclusion
[Résumé]
```

### Gestion des Clés

```markdown
## Analyse Gestion des Clés

### Résultat : ✓ / ⚠ / ✗

### Points Vérifiés

| Aspect | Statut | Détail |
|--------|--------|--------|
| Stockage des clés | ✓/✗ | [Détail] |
| Rotation | ✓/✗ | [Détail] |
| Séparation DEK/KEK | ✓/✗ | [Détail] |
| Nettoyage mémoire | ✓/✗ | [Détail] |
```

### Modes de Chiffrement

```markdown
## Analyse Chiffrement

### Résultat : ✓ / ⚠ / ✗

### Algorithmes Utilisés

| Algorithme | Fichier | Évaluation |
|------------|---------|------------|
| AES-256-GCM | crypto.py | ✓ Recommandé |
| AES-CBC | legacy.py | ⚠ Vérifier auth |
| DES | old_module.py | ✗ Obsolète |
```

### Comparaisons de Secrets

```markdown
## Analyse Timing Attacks

### Points de Comparaison Détectés

| Fichier | Ligne | Méthode | Statut |
|---------|-------|---------|--------|
| auth.py | 89 | `hmac.compare_digest()` | ✓ Sûr |
| api.py | 156 | `==` | ✗ Vulnérable |
```

---

## Section Conformité

```markdown
## Évaluation de Conformité

### Standards Applicables
- [ ] FIPS 140-3
- [ ] PCI-DSS 4.0
- [ ] GDPR
- [ ] HIPAA
- [ ] SOC 2

### Matrice de Conformité

| Exigence | Statut | Commentaire |
|----------|--------|-------------|
| Chiffrement au repos | ✓/✗ | [Détail] |
| Chiffrement en transit | ✓/✗ | [Détail] |
| Gestion des clés | ✓/✗ | [Détail] |
| Audit trail | ✓/✗ | [Détail] |
```

---

## Section Recommandations

```markdown
## Plan de Remédiation

### Priorité Immédiate (0-7 jours)
1. [ ] Corriger CRYPTO-001 (RNG non sécurisé)
2. [ ] Corriger CRYPTO-002 (Timing attack)

### Priorité Haute (1-2 semaines)
1. [ ] Migrer de AES-CBC vers AES-GCM
2. [ ] Implémenter rotation des clés

### Priorité Moyenne (1 mois)
1. [ ] Ajouter logging cryptographique
2. [ ] Documenter la politique de gestion des clés

### Améliorations Long Terme
1. [ ] Évaluer migration post-quantique
2. [ ] Implémenter HSM pour clés critiques
```

---

## Annexes

```markdown
## Annexe A : Outils Utilisés

| Outil | Version | Usage |
|-------|---------|-------|
| Claude Code | - | Analyse statique |
| grep/ripgrep | - | Recherche de patterns |
| [Autres outils] | - | - |

## Annexe B : Fichiers Analysés

[Liste complète des fichiers dans le scope]

## Annexe C : Références

- OWASP Cryptographic Failures
- NIST SP 800-57 (Key Management)
- RFC pertinentes
```

---

## Exemple Complet

```markdown
# Rapport d'Audit Cryptographique

**Projet** : MonApplication
**Date** : 2026-01-10
**Auditeur** : Claude Code - Expert Crypto
**Version** : commit abc123
**Scope** : src/auth/*, src/crypto/*

---

## Résumé Exécutif

### Score Global : 6/10

| Catégorie | Vulnérabilités |
|-----------|----------------|
| Critiques | 1 |
| Élevées | 2 |
| Modérées | 3 |
| Informatives | 2 |

### Actions Immédiates
- [ ] Remplacer `random.randint()` par `secrets` dans auth/token.py
- [ ] Utiliser `hmac.compare_digest()` dans api/verify.py

---

## [CRITIQUE] Utilisation de RNG Non Cryptographique

**ID** : CRYPTO-001
**CWE** : CWE-338

### Localisation
- **Fichier** : `src/auth/token.py:42`
- **Fonction** : `generate_reset_token()`

### Code Vulnérable
```python
import random
def generate_reset_token():
    return str(random.randint(100000, 999999))
```

### Impact
Tokens de réinitialisation de mot de passe prévisibles. Un attaquant peut :
- Prédire les tokens générés
- Réinitialiser n'importe quel compte utilisateur

### Correction
```python
import secrets
def generate_reset_token():
    return secrets.token_urlsafe(32)
```

### Référence
- OWASP: Cryptographic Failures (A02:2021)
```
