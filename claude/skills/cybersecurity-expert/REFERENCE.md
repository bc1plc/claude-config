# Reference Technique Cybersecurite

## PARTIE I : GOUVERNANCE & METHODOLOGIE

### Cycle de Vie du Developpement Logiciel Securise (SSDLC)

| Phase du SDLC | Activites de Securite Cles | Livrables Attendus |
|---------------|---------------------------|-------------------|
| **Exigences** | Analyse d'impact metier (BIA), identification des "abuse cases" | User stories de securite, criteres d'acceptation |
| **Planification** | Evaluation de l'appetit pour le risque, budgetisation securite | Plan de test de securite, matrice de couverture |
| **Conception** | Modelisation des menaces (STRIDE/PASTA), definition des protocoles | Diagrammes de flux (DFD), architecture de securite |
| **Developpement** | Standards de codage securise, revues de code, plugins IDE | Code signe, alertes SAST/SCA traitees |
| **Verification** | Tests automatises CI/CD, DAST, tests de penetration | Rapports de vulnerabilite, validation Quality Gates |
| **Deploiement** | Scan de conteneurs, verification IaC, secrets management | Attestation de conformite, SBOM |
| **Maintenance** | Surveillance continue, gestion des patchs, audits periodiques | Rapport de posture, journal de remediation |

### Principes Directeurs

1. **Security by Design** : Chaque decision architecturale est pesee a l'aune de son exposition au risque
2. **Zero Trust** : Ne jamais supposer la confiance implicite, meme pour les perimetres internes
3. **Defense en profondeur** : Plusieurs couches de controles independants
4. **Fail Secure** : Le systeme echoue de maniere securisee en cas d'erreur
5. **Least Privilege** : Chaque composant possede uniquement les permissions minimales necessaires

---

## Modelisation Strategique des Menaces

### Methodologie STRIDE (Approche Tactique)

| Categorie | Description | Propriete Violee | Question d'Audit |
|-----------|-------------|-----------------|------------------|
| **S**poofing | Usurper l'identite d'un utilisateur ou systeme | Authentification | "Peut-on se faire passer pour un autre ?" |
| **T**ampering | Modifier illegalement des donnees | Integrite | "Les donnees peuvent-elles etre alterees en transit/stockage ?" |
| **R**epudiation | Nier avoir effectue une action | Non-repudiation | "Les actions sont-elles tracables et prouvables ?" |
| **I**nformation Disclosure | Exposer des donnees sensibles | Confidentialite | "Des donnees sont-elles accessibles a des non-autorises ?" |
| **D**enial of Service | Empecher l'acces legitime | Disponibilite | "Le service peut-il etre sature ou bloque ?" |
| **E**levation of Privilege | Obtenir des droits superieurs | Autorisation | "Un utilisateur peut-il escalader ses privileges ?" |

### Methodologie PASTA (7 etapes)

1. Definition des Objectifs (impact metier, conformite RGPD/PCI DSS)
2. Definition de la Portee Technique (infrastructure, frameworks, dependances)
3. Decomposition de l'Application (DFD, utilisateurs, frontieres de confiance)
4. Analyse des Menaces (profils d'attaquants, motivations, vecteurs)
5. Analyse des Vulnerabilites (correlation SAST/pentest avec actifs critiques)
6. Modelisation d'Attaques (arbres d'attaque, simulation de scenarios)
7. Analyse des Risques et Remediation (calcul d'impact financier)

### Quantification avec DREAD (echelle 1-10)

| Critere | Question |
|---------|----------|
| **D**amage | Quel est le potentiel de dommage ? |
| **R**eproducibility | Est-ce facilement reproductible ? |
| **E**xploitability | Quelle expertise requise pour exploiter ? |
| **A**ffected Users | Combien d'utilisateurs impactes ? |
| **D**iscoverability | Est-ce facile a decouvrir ? |

**Score DREAD** = (D + R + E + A + D) / 5

---

## Analyse de Code : SAST, SCA et Reachability

### Comparatif SAST vs SCA

| Critere | SAST (Static Analysis) | SCA (Composition Analysis) |
|---------|------------------------|---------------------------|
| **Cible** | Code source proprietaire | Bibliotheques et composants tiers |
| **Types de failles** | Erreurs de logique, injections, secrets hardcodes | CVE connues, licences obsoletes |
| **Acces requis** | Code source complet | Manifestes (package.json, requirements.txt) |
| **Remediation** | Modification manuelle du code | Mise a jour/remplacement de librairie |
| **Livrables** | Alertes par ligne de code | SBOM, inventaire de licences |

### Analyse de Reachability

Verifie si le code proprietaire appelle reellement la fonction vulnerable d'une bibliotheque tierce :
1. CVE detectee dans lib X ?
2. Code appelle fonction vulnerable ?
3. Chemin d'attaque depuis entree utilisateur ?

Si OUI aux 3 : RISQUE REEL (P0/P1)
Si NON a une etape : Risque mitigue (documenter pour audit)

---

## Hygiene des Secrets

### Architecture de Protection (Defense en Profondeur)

**COUCHE 1 : Prevention locale (Developpeur)**
- Pre-commit Hook (Git Secrets, Spectral)
- Scan patterns avant commit local

**COUCHE 2 : Prevention serveur (SCM)**
- Pre-receive Hook (GitLab/GitHub)
- Bloque push si secret detecte

**COUCHE 3 : Detection continue (CI/CD)**
- Gitleaks, TruffleHog dans pipeline
- Scan historique et differentiel

**COUCHE 4 : Stockage securise (Production)**
- HashiCorp Vault / AWS Secrets Manager
- Rotation automatique, audit logs

### Regles de Gestion des Secrets

| Environnement | Methode Autorisee | Methode Interdite |
|---------------|-------------------|-------------------|
| Dev local | Variables d'environnement (.env gitignored) | Hardcoding dans le code |
| CI/CD | Secrets natifs (GitHub Secrets, GitLab CI Variables) | Variables en clair dans YAML |
| Production | Vault avec rotation automatique | Fichiers de config non chiffres |
| Conteneurs | Secrets Kubernetes, Docker Secrets | Variables ENV dans Dockerfile |

### Politique de Rotation

- api_keys: 90 jours
- database_credentials: 60 jours
- service_accounts: 180 jours
- encryption_keys: 365 jours (avec re-chiffrement)

---

## Pipeline DevSecOps

### Architecture

```
COMMIT → BUILD → TEST → DEPLOY
   │        │       │       │
   ▼        ▼       ▼       ▼
Secrets   SAST    DAST   Container
 Scan    + SCA  + Pentest   Scan
   │        │       │       │
   └────────┴───────┴───────┘
              │
        QUALITY GATES
   • 0 vulnerabilite Critique
   • 0 secret detecte
   • Couverture SAST > 80%
   • Politiques IaC validees
```

### Strategies d'Optimisation

| Strategie | Description | Benefice |
|-----------|-------------|----------|
| Scan incremental | Analyser uniquement fichiers modifies | Velocite preservee |
| Cache des dependances | Reutiliser resultats SCA si lock file inchange | Reduction temps build |
| Tests paralleles | SAST, SCA, secrets scan en parallele | Feedback rapide |
| DAST nocturne | Tests dynamiques hors heures de pointe | Profondeur sans friction |

---

## Metriques Cles

### MTTR (Mean Time to Remediate)

| Severite | SLA Recommande | SLA Critique |
|----------|---------------|--------------|
| Critique | 24-72 heures | 4-24 heures |
| Haute | 7 jours | 48-72 heures |
| Moyenne | 30 jours | 14 jours |
| Basse | 90 jours | 30 jours |

### TDR (Technical Debt Ratio)
TDR = (Effort remediation dette) / (Effort dev nouvelles features) x 100
Seuil d'alerte : TDR > 15%

### ALE (Annual Loss Expectancy)
ALE = SLE (Single Loss Expectancy) x ARO (Annual Rate of Occurrence)

---

## PARTIE II : VULNERABILITES PAR CWE

### Priorite P0 - Critique (RCE/Injection)

| CWE | Nom | Langages concernes |
|-----|-----|-------------------|
| CWE-94 | Code Injection | JS, Python, PHP, Ruby |
| CWE-78 | OS Command Injection | Tous |
| CWE-502 | Deserialization of Untrusted Data | Python, PHP, Java |
| CWE-89 | SQL Injection | Tous |
| CWE-347 | Improper Verification of Cryptographic Signature | JWT |

### Priorite P1 - Haute

| CWE | Nom | Langages concernes |
|-----|-----|-------------------|
| CWE-79 | Cross-site Scripting (XSS) | JS, React, PHP |
| CWE-798 | Hardcoded Credentials | Tous |
| CWE-312 | Cleartext Storage of Sensitive Info | Mobile (RN, iOS, Android) |
| CWE-601 | Open Redirect | Tous |
| CWE-639 | IDOR (Authorization Bypass) | Tous |

### Priorite P2 - Moyenne

| CWE | Nom | Langages concernes |
|-----|-----|-------------------|
| CWE-1021 | Missing Security Headers | Web |
| CWE-942 | CORS Misconfiguration | Web |
| CWE-209 | Information Exposure Through Error | Tous |
| CWE-352 | CSRF | Web |

---

## Directives par Stack

### JavaScript / TypeScript
- Prototype Pollution : filtrer __proto__, constructor, prototype
- Supply Chain : auditer contre typosquatting, verifier postinstall
- Eviter le type `any` en TypeScript

### React & React Native
- XSS : sanitizer HTML avec DOMPurify
- URLs : valider protocol (bloquer javascript:)
- Mobile : SecureStore ou Keychain (pas AsyncStorage pour secrets)
- Deep Links : whitelist screens + validation params

### AdonisJS
- ORM : Query Builder ou bindings parametres
- Shield : CSRF enabled, CSP strict, HSTS
- Validation : VineJS avec enums pour roles

### Python
- CWE-502 : json ou yaml.safe_load (pas de deserialisation non securisee)
- CWE-78 : subprocess avec liste d'args, shell=False
- Path Traversal : pathlib avec is_relative_to()

### Rust
- Auditer tous les blocs `unsafe`
- Eviter unwrap() en production
- Arithmetique : checked_* ou saturating_*

### Go
- exec.Command sans shell intermediaire
- SQL avec parametres bindes ($1, $2)
- html/template (pas text/template) pour XSS

### PHP
- PDO prepared statements
- json_decode au lieu de unserialize
- Comparaison stricte === et password_verify
- Upload : finfo pour MIME reel + renommage aleatoire

---

## OWASP Top 10 2021 Checklist

### A01 - Broken Access Control
- [ ] IDOR : Tester modification ID dans URL/body
- [ ] Privilege Escalation : Acces fonctions admin sans droits
- [ ] CORS : Access-Control-Allow-Origin pas "*"
- [ ] JWT : Verification signature, pas de alg:none

### A02 - Cryptographic Failures
- [ ] TLS 1.2 minimum, 1.3 recommande
- [ ] Mots de passe : Bcrypt (cost >= 10) ou Argon2id
- [ ] Chiffrement au repos pour PII (AES-256-GCM)

### A03 - Injection
- [ ] SQL : Requetes parametrees partout
- [ ] NoSQL : Validation de type sur MongoDB
- [ ] Command : Pas de shell=True, pas d'interpolation
- [ ] XSS : Encodage contextuel des sorties

### A04 - Insecure Design
- [ ] Rate limiting sur login, reset password, APIs sensibles
- [ ] Business logic : Regles metier non contournables

### A05 - Security Misconfiguration
- [ ] Debug mode desactive en production
- [ ] Headers de securite presents
- [ ] Pas de .git, .env, node_modules exposes

### A06 - Vulnerable Components
- [ ] npm/pip/cargo audit clean
- [ ] Pas de CVE critiques non patchees

### A07 - Authentication Failures
- [ ] Protection brute force (lockout, captcha)
- [ ] Tokens session : longs, aleatoires, expiration
- [ ] MFA disponible pour comptes sensibles

### A08 - Software and Data Integrity
- [ ] CI/CD securise
- [ ] Pas de deserialisation de donnees non fiables
- [ ] Signatures verifiees sur les mises a jour

### A09 - Logging & Monitoring
- [ ] Evenements de securite logges
- [ ] Pas de donnees sensibles dans les logs
- [ ] Alerting sur comportements suspects

### A10 - SSRF
- [ ] URLs utilisateur : whitelist de domaines
- [ ] Pas de suivi redirections automatique
- [ ] Bloquer acces metadonnees cloud (169.254.169.254)

---

## Format de Rapport

Pour chaque vulnerabilite detectee :

| Attribut | Valeur |
|----------|--------|
| **Severite** | Critique / Haute / Moyenne / Basse |
| **CVSS 3.1** | Score + Vector |
| **CWE** | CWE-XXX - Nom |
| **OWASP** | A0X:2021 - Categorie |
| **Stack** | Technologies concernees |
| **Fichier** | chemin:lignes |
| **Reachability** | Confirme / Probable / A verifier |

Inclure : Description, Code vulnerable, PoC, Impact metier, Remediation, References

---

## Limitations

- **Pas de DAST** : Analyse statique uniquement
- **Contexte requis** : Certaines vulns dependent du deploiement
- **Faux positifs possibles** : Signaler le niveau de confiance
- **Non exhaustif** : Un audit ne detecte pas 100% des vulns
- **Snapshot temporel** : Etat du code a un instant T
