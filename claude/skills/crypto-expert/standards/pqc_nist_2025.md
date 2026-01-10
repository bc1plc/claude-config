# Standards Cryptographiques Post-Quantiques (NIST 2025/2026)

## Contexte

Le NIST a finalisé ses standards PQC en août 2024, marquant la plus grande mutation cryptographique depuis RSA. Ces algorithmes protègent contre les futures attaques quantiques.

---

## ML-KEM (FIPS 203) - Encapsulation de Clé

**Remplacement standard pour** : ECDH, RSA-KEM

### Algorithme
- **Nom** : Module-Lattice-Based Key-Encapsulation Mechanism
- **Ancien nom** : CRYSTALS-Kyber
- **Base mathématique** : Problème MLWE (Module Learning With Errors) sur réseaux euclidiens

### Paramètres Recommandés

| Paramètre | Niveau NIST | Équivalent | Usage |
|-----------|-------------|------------|-------|
| ML-KEM-512 | 1 | AES-128 | Non recommandé (marge trop juste) |
| **ML-KEM-768** | **3** | **AES-192** | **RECOMMANDÉ - Équilibre optimal** |
| ML-KEM-1024 | 5 | AES-256 | Haute sécurité, surcharge performance |

### Implémentation Hybride (OBLIGATOIRE)

**Règle** : Ne JAMAIS utiliser ML-KEM seul pendant la période de transition.

```
Secret_Final = KDF(X25519_Secret || ML-KEM_Secret)
```

- **Combiner avec** : X25519 (Curve25519)
- **Identifiant TLS** : `X25519Kyber768Draft00` (0x6399) ou standard final
- **Raison** : Si ML-KEM casse (comme SIKE en 2022), X25519 protège contre les ordinateurs classiques

### Distinction Importante
ML-KEM n'est **PAS** un échange Diffie-Hellman classique. C'est un mécanisme d'encapsulation (KEM) :
1. Alice génère une paire de clés
2. Bob encapsule un secret avec la clé publique d'Alice
3. Alice décapsule pour obtenir le même secret

---

## ML-DSA (FIPS 204) - Signature Numérique

**Remplacement standard pour** : ECDSA, RSA-PSS, Ed25519 (pour la PKI)

### Algorithme
- **Nom** : Module-Lattice-Based Digital Signature Algorithm
- **Ancien nom** : CRYSTALS-Dilithium

### Paramètres Recommandés

| Paramètre | Niveau NIST | Taille Signature | Taille Clé Pub |
|-----------|-------------|------------------|----------------|
| ML-DSA-44 | 2 | ~2.4 KB | ~1.3 KB |
| **ML-DSA-65** | **3** | **~3.3 KB** | **~2.0 KB** |
| ML-DSA-87 | 5 | ~4.6 KB | ~2.6 KB |

### Impact Performance

**ATTENTION** : Comparé à Ed25519 (64 octets signature, 32 octets clé) :
- Signatures ML-DSA : **~50x plus grandes**
- Implications :
  - Fragmentation IP/UDP (MTU ~1500 octets)
  - Latence handshake TLS augmentée
  - Bande passante accrue pour les certificats

### Recommandations Architecture
- Prévoir des buffers réseau plus grands
- Considérer la compression pour les certificats
- Évaluer l'impact sur les appareils IoT contraints

---

## SLH-DSA (FIPS 205) - Signature Hash-Based

**Usage** : Algorithme de **repli** (fallback) ultime

### Algorithme
- **Nom** : Stateless Hash-Based Digital Signature Algorithm
- **Base** : SPHINCS+
- **Sécurité** : Basé uniquement sur les fonctions de hachage (très conservateur)

### Cas d'Usage Spécifiques
1. **Signature de firmware** à très longue durée de vie (15+ ans)
2. **Archivage légal** où la certitude absolue prime
3. **Autorités de certification racine** (haute assurance)
4. **Backup** si les réseaux euclidiens sont cassés

### Caractéristiques

| Aspect | Valeur |
|--------|--------|
| Taille signature | **Plusieurs dizaines de KB** |
| Vitesse signature | Lente |
| Vitesse vérification | Modérée |
| Confiance mathématique | **Maximale** |

### Quand l'Utiliser
- Si une avancée mathématique casse ML-DSA (réseaux euclidiens)
- Pour des applications où la taille n'est pas critique
- Quand la durée de vie des signatures dépasse 10-15 ans

---

## Stratégie de Migration

### Phase 1 : Inventaire (2024-2025)
- Identifier tous les algorithmes cryptographiques en usage
- Cartographier les dépendances (TLS, PKI, signatures, stockage)

### Phase 2 : Hybride (2025-2027)
- Déployer X25519+ML-KEM-768 pour l'échange de clés
- Maintenir les signatures classiques + PQC en double
- Tester la compatibilité avec les partenaires

### Phase 3 : Migration Complète (2027+)
- Basculer vers PQC-only quand l'écosystème est mature
- Conserver la crypto-agilité pour futurs changements

---

## Bibliothèques Recommandées

| Langage | Bibliothèque | Support PQC |
|---------|--------------|-------------|
| C/C++ | liboqs, BoringSSL | ML-KEM, ML-DSA |
| Rust | pqcrypto, rustls | ML-KEM-768 hybride |
| Python | liboqs-python | Tous standards |
| Go | circl (Cloudflare) | ML-KEM, ML-DSA |
| Java | BouncyCastle | Support progressif |

---

## Références

- NIST FIPS 203 : https://csrc.nist.gov/pubs/fips/203/final
- NIST FIPS 204 : https://csrc.nist.gov/pubs/fips/204/final
- NIST FIPS 205 : https://csrc.nist.gov/pubs/fips/205/final
- ANSSI Recommandations PQC : Approche hybride obligatoire
- BSI TR-02102-1 : Guidelines cryptographiques allemandes
