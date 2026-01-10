# Standards de Conformité Cryptographique

## FIPS 140-3

### Niveaux de Sécurité

| Niveau | Exigences | Cas d'Usage |
|--------|-----------|-------------|
| **Level 1** | Algorithme approuvé, tests de base | Logiciel général |
| **Level 2** | Evidence de tamper, authentification rôles | Cloud KMS standard |
| **Level 3** | Résistance physique, zeroization | HSM, banques, gouvernement |
| **Level 4** | Protection environnementale complète | Militaire, haute sécurité |

### Algorithmes Approuvés FIPS

#### Chiffrement Symétrique
- **AES** : 128, 192, 256 bits (modes approuvés : GCM, CCM, CBC+CMAC)
- **Triple-DES** : Déprécié, éviter pour nouveaux systèmes

#### Hachage
- **SHA-2** : SHA-256, SHA-384, SHA-512
- **SHA-3** : SHA3-256, SHA3-384, SHA3-512
- **SHAKE** : SHAKE128, SHAKE256 (XOF)

#### Signature
- **RSA** : 2048+ bits avec PSS padding
- **ECDSA** : P-256, P-384, P-521
- **EdDSA** : Ed25519, Ed448 (FIPS 186-5)

#### Échange de Clés
- **ECDH** : P-256, P-384, P-521
- **DH** : 2048+ bits (éviter si possible)

#### Post-Quantique (FIPS 203/204/205)
- **ML-KEM** : ML-KEM-512, ML-KEM-768, ML-KEM-1024
- **ML-DSA** : ML-DSA-44, ML-DSA-65, ML-DSA-87
- **SLH-DSA** : Toutes variantes

### Algorithmes NON-FIPS (À Éviter en Contexte Régulé)

| Algorithme | Statut |
|------------|--------|
| ChaCha20-Poly1305 | Non approuvé FIPS |
| Curve25519 / Ed25519 | Non approuvé FIPS (jusqu'à récemment) |
| Argon2 | Non approuvé FIPS |
| MD5, SHA-1 | Dépréciés |

---

## PCI-DSS 4.0 (Paiements)

### Exigences Cryptographiques Clés

#### Requirement 3.5 : Protection des Clés

| Exigence | Détail |
|----------|--------|
| 3.5.1 | Accès aux clés restreint au minimum nécessaire |
| 3.5.2 | Clés stockées sous forme chiffrée |
| 3.5.3 | Séparation des composants de clés |

#### Requirement 4 : Transmission Chiffrée

- TLS 1.2+ obligatoire pour les données cardholder
- Certificats de confiance publique
- Pas de protocoles obsolètes (SSL, TLS 1.0/1.1)

#### Tailles de Clés Minimales (PCI)

| Type | Minimum |
|------|---------|
| AES | 128 bits |
| RSA | 2048 bits |
| ECC | P-256 |
| 3DES | Déprécié (2023+) |

---

## GDPR (Protection des Données)

### Article 32 : Sécurité du Traitement

Le GDPR ne prescrit pas d'algorithmes spécifiques mais exige :

1. **Pseudonymisation** : Séparer les identifiants des données
2. **Chiffrement** : État de l'art approprié au risque
3. **Intégrité** : Capacité de restauration
4. **Tests réguliers** : Évaluation de l'efficacité

### Recommandations Techniques GDPR

| Donnée | Recommandation |
|--------|----------------|
| Données au repos | AES-256-GCM ou ChaCha20-Poly1305 |
| Données en transit | TLS 1.3 |
| Clés | HSM ou KMS avec audit |
| Mots de passe | Argon2id (ou bcrypt minimum) |

### Transferts Internationaux

- **Clauses Contractuelles Types** : Chiffrement end-to-end recommandé
- **Schrems II** : Mesures techniques supplémentaires pour UE→US

---

## HIPAA (Santé - US)

### Technical Safeguards

| Exigence | Standard |
|----------|----------|
| Encryption | Addressable (fortement recommandé) |
| Transmission Security | TLS 1.2+ |
| Access Controls | Authentification forte |
| Audit Controls | Logging complet |

### Algorithmes Recommandés HIPAA

- **Chiffrement** : AES-128+ (FIPS compliant)
- **Hachage** : SHA-256+
- **Transport** : TLS 1.2+, IPsec

---

## SOC 2 Type II

### Critères de Sécurité Pertinents

| Critère | Focus Crypto |
|---------|--------------|
| CC6.1 | Logical access controls, encryption |
| CC6.6 | Transmission security (TLS) |
| CC6.7 | Encryption of data at rest |

### Preuves Attendues

1. **Politique de chiffrement** documentée
2. **Rotation des clés** avec audit trail
3. **Tests de pénétration** incluant crypto
4. **Gestion des certificats** (expiration, révocation)

---

## ANSSI (France)

### Recommandations Cryptographiques (RGS)

#### Niveau Renforcé (Recommandé)

| Type | Algorithme |
|------|------------|
| Symétrique | AES-256 |
| Asymétrique | RSA-3072, ECDSA P-256 |
| Hachage | SHA-256, SHA-3 |
| MAC | HMAC-SHA-256 |

#### Post-Quantique

L'ANSSI recommande explicitement l'**approche hybride** :
- Combiner algorithme classique + PQC
- Ne pas migrer vers PQC seul avant maturité complète

---

## BSI (Allemagne) TR-02102

### Recommandations 2024+

#### Tailles de Clés

| Type | Minimum | Recommandé |
|------|---------|------------|
| RSA | 3000 bits | 4096 bits |
| DSA | 3000 bits | Éviter (préférer ECDSA) |
| ECDSA | P-256 | P-384 |
| AES | 128 bits | 256 bits |

#### Protocoles

- TLS 1.3 préféré
- TLS 1.2 acceptable avec cipher suites modernes
- Interdire TLS 1.1 et antérieur

---

## Checklist de Conformité Multi-Standard

### Évaluation Rapide

| Critère | FIPS | PCI-DSS | GDPR | HIPAA |
|---------|------|---------|------|-------|
| AES-256-GCM | ✓ | ✓ | ✓ | ✓ |
| ChaCha20-Poly1305 | ✗ | ✓ | ✓ | ✗ |
| RSA-2048 | ✓ | ✓ | ✓ | ✓ |
| P-256 ECDSA | ✓ | ✓ | ✓ | ✓ |
| Ed25519 | ✓* | ✓ | ✓ | ✓* |
| Argon2id | ✗ | ✓ | ✓ | ✗ |
| PBKDF2-SHA256 | ✓ | ✓ | ✓ | ✓ |
| TLS 1.3 | ✓ | ✓ | ✓ | ✓ |

*Ed25519 approuvé dans FIPS 186-5 (2023)

### Questions d'Évaluation

1. "Quels régimes de conformité s'appliquent à votre organisation ?"
2. "Traitez-vous des données de paiement (PCI) ?"
3. "Avez-vous des clients dans l'UE (GDPR) ?"
4. "Travaillez-vous avec le gouvernement US (FIPS) ?"
5. "Gérez-vous des données de santé (HIPAA) ?"

---

## Références

- NIST SP 800-131A Rev. 2 : Transitioning the Use of Cryptographic Algorithms
- PCI DSS v4.0 : https://www.pcisecuritystandards.org/
- GDPR Article 32 : https://gdpr-info.eu/art-32-gdpr/
- ANSSI RGS : https://www.ssi.gouv.fr/
- BSI TR-02102 : https://www.bsi.bund.de/
