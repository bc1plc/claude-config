# Primitives Cryptographiques Classiques (Non-PQC)

## Courbes Elliptiques (ECC)

### Choix Principal : Curve25519

**Usage** : Web, Mobile, Open Source, Applications Commerciales (90% des cas)

#### Variantes
| Algorithme | Usage | RFC |
|------------|-------|-----|
| X25519 | Échange de clés (ECDH) | RFC 7748 |
| Ed25519 | Signature numérique | RFC 8032 |

#### Avantages de Curve25519

1. **Immunité aux timing attacks**
   - Conception "constant-time" naturelle
   - Pas de branchements conditionnels dépendant des données

2. **Ed25519 déterministe**
   - Pas de dépendance au RNG lors de la signature
   - Élimine le risque catastrophique de réutilisation de nonce

3. **Performance**
   - Optimisée pour les implémentations logicielles
   - Clés compactes (32 octets)

4. **Confiance**
   - Conception publique et transparente (D.J. Bernstein)
   - Pas de constantes "magiques" inexpliquées

---

### Choix FIPS : NIST P-256

**Usage UNIQUEMENT si** : Conformité FIPS 140-3 requise

#### Contextes FIPS
- Secteur public / gouvernement
- Contrats militaires
- Banques régulées (certaines juridictions)
- Healthcare (HIPAA avec exigences FIPS)

#### Paramètres

| Niveau de Classification | Courbe | Usage |
|--------------------------|--------|-------|
| Jusqu'à SECRET | P-256 (secp256r1) | Standard |
| TOP SECRET | P-384 (secp384r1) | Haute assurance |

#### Précautions P-256

**ATTENTION** : P-256 nécessite une implémentation rigoureuse :

1. **Vérification des points** : Toujours vérifier que les points reçus sont sur la courbe
2. **Temps constant** : Implémenter des opérations sans branches data-dependent
3. **Validation des clés** : Rejeter les clés invalides (point à l'infini, hors courbe)

---

## Chiffrement Symétrique Authentifié (AEAD)

### Règle Fondamentale

> **"Pas de chiffrement sans intégrité"**

### Modes INTERDITS

| Mode | Problème | Risque |
|------|----------|--------|
| **ECB** | Motifs visibles dans les données chiffrées | Fuite d'information structurelle |
| **CBC sans HMAC** | Padding oracle attacks | Déchiffrement complet possible |
| **CTR sans MAC** | Aucune intégrité | Modification silencieuse des données |

---

### Option 1 : AES-256-GCM (Standard Industriel)

#### Caractéristiques
- Très rapide avec accélération matérielle (AES-NI)
- Authentification intégrée
- Standard NIST, FIPS-compliant

#### DANGER CRITIQUE : Gestion du Nonce

```
IV/Nonce : 96 bits (12 octets)
RÈGLE : Ne JAMAIS réutiliser un nonce avec la même clé
```

**Conséquence d'une réutilisation** :
- Destruction totale de l'authentification
- Récupération possible du keystream (XOR des deux ciphertexts)
- Compromission potentielle de la clé d'authentification

#### Stratégies de Nonce Sûres
1. **Compteur** : Incrémenter pour chaque message (attention aux redémarrages)
2. **Nonce dérivé** : KDF(key, message_id) si les IDs sont uniques
3. **NE PAS** : Générer aléatoirement (risque de collision après ~2^32 messages)

---

### Option 2 : XChaCha20-Poly1305 (Recommandé)

#### Caractéristiques
- Pas besoin d'AES-NI (excellent sur mobile, ARM)
- **Nonce de 192 bits** : Génération aléatoire sûre
- Préféré par Google, Cloudflare

#### Avantages sur AES-GCM

| Aspect | AES-GCM | XChaCha20-Poly1305 |
|--------|---------|---------------------|
| Taille nonce | 96 bits | **192 bits** |
| Nonce aléatoire | Risqué | **Sûr** |
| Hardware acceleration | Requis | Non requis |
| Complexité gestion état | Élevée | **Faible** |

#### Quand Utiliser
- Applications distribuées (plusieurs serveurs écrivant)
- Stockage (chaque fichier peut avoir un nonce aléatoire)
- Quand la gestion d'état est difficile

---

## Hachage de Mots de Passe

### Standard : Argon2id

**Vainqueur** de la Password Hashing Competition (PHC)
**Recommandé par** : OWASP, RFC 9106

#### Pourquoi Argon2id ?

| Algorithme | CPU | Mémoire | Résistance ASIC |
|------------|-----|---------|-----------------|
| PBKDF2 | Oui | Non | Faible |
| bcrypt | Oui | Faible (4KB) | Modérée |
| scrypt | Oui | Oui | Bonne |
| **Argon2id** | **Oui** | **Oui** | **Excellente** |

#### Mode "id" Hybride
- Combine résistance side-channel (mode "i")
- Avec résistance time-memory tradeoff (mode "d")

---

### Paramètres OWASP 2025/2026

```
Mode      : Argon2id
Mémoire   : 19 MiB minimum (64 MiB recommandé si possible)
Itérations: 2 minimum (3 recommandé)
Parallélisme: 1 (évite race conditions sur serveurs chargés)
Sel       : 16 octets minimum (généré cryptographiquement)
Hash      : 32 octets
```

#### Adaptation au Contexte

| Environnement | Mémoire | Itérations |
|---------------|---------|------------|
| Serveur web standard | 19 MiB | 2 |
| Serveur haute capacité | 64 MiB | 3 |
| Application mobile | 19 MiB | 2 |
| Dérivation clé (KDF) | 64 MiB+ | 4+ |

#### Questions à Poser
1. "Quelles sont les contraintes mémoire de vos serveurs d'authentification ?"
2. "Quel est le temps de réponse acceptable pour le login ?"
3. "Combien de tentatives de login par seconde attendez-vous ?"

---

### Algorithmes Tolérés (Legacy)

**bcrypt** : Acceptable si migration vers Argon2id impossible
- Minimum : cost factor 12+
- Limitation : 72 caractères max

**PBKDF2-HMAC-SHA256** : Uniquement pour conformité FIPS
- Minimum : 600,000 itérations (OWASP 2023+)
- Préférer Argon2id dès que FIPS non requis

---

## Tailles de Clés Minimales (2025+)

| Algorithme | Minimum | Recommandé |
|------------|---------|------------|
| AES | 128 bits | **256 bits** |
| RSA | 2048 bits | **3072+ bits** |
| ECDSA/ECDH | P-256 | P-256 ou Curve25519 |
| Ed25519 | 256 bits | 256 bits (fixe) |

---

## Références

- RFC 7748 : Elliptic Curves for Security (X25519)
- RFC 8032 : Edwards-Curve Digital Signature Algorithm (Ed25519)
- RFC 9106 : Argon2 Memory-Hard Function
- OWASP Password Storage Cheat Sheet (2025)
- NIST SP 800-57 : Key Management Guidelines
