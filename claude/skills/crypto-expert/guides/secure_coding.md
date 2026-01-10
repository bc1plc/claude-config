# Guide d'Audit de Code et Implémentation Sécurisée

## Checklist d'Audit Critique

L'agent doit scanner le code pour ces vulnérabilités exactes.

---

## 1. Générateurs Aléatoires (RNG)

### VULNÉRABLE - Alerter Immédiatement

| Langage | Code Dangereux |
|---------|----------------|
| JavaScript | `Math.random()` |
| Python | `random.random()`, `random.randint()`, `random.choice()` |
| C/C++ | `rand()`, `srand()` |
| Java | `java.util.Random`, `ThreadLocalRandom` |
| PHP | `rand()`, `mt_rand()` |
| Go | `math/rand` |

### SÉCURISÉ - À Exiger

| Langage | Code Correct |
|---------|--------------|
| JavaScript (Browser) | `window.crypto.getRandomValues()` |
| JavaScript (Node.js) | `crypto.randomBytes()`, `crypto.randomUUID()` |
| Python | `secrets` module, `os.urandom()` |
| C/C++ | `/dev/urandom`, `getrandom()`, `BCryptGenRandom()` |
| Java | `java.security.SecureRandom` |
| PHP | `random_bytes()`, `random_int()` |
| Go | `crypto/rand` |
| Rust | `rand::rngs::OsRng`, `getrandom` crate |

### Exemple de Correction

```python
# VULNÉRABLE
import random
token = ''.join(random.choice('abcdef0123456789') for _ in range(32))

# SÉCURISÉ
import secrets
token = secrets.token_hex(16)  # 32 caractères hex
```

---

## 2. Attaques Temporelles (Timing Attacks)

### VULNÉRABLE - Comparaison de Secrets

```python
# DANGER : s'arrête à la première différence
if user_mac == calculated_mac:
    return True
```

```c
// DANGER : fuite du timing
if (memcmp(received_sig, expected_sig, 32) == 0) {
    return VALID;
}
```

**Risque** : Un attaquant peut deviner le secret octet par octet en mesurant le temps de réponse.

### SÉCURISÉ - Comparaison Constant-Time

| Langage | Fonction |
|---------|----------|
| Python | `hmac.compare_digest(a, b)` |
| Node.js | `crypto.timingSafeEqual(a, b)` |
| C (OpenSSL) | `CRYPTO_memcmp(a, b, len)` |
| C (libsodium) | `sodium_memcmp(a, b, len)` |
| Go | `subtle.ConstantTimeCompare(a, b)` |
| Rust | `constant_time_eq` crate |

### Pattern de Code Sécurisé

```python
import hmac

def verify_mac(received: bytes, expected: bytes) -> bool:
    """Vérifie un MAC sans fuiter d'information temporelle."""
    if len(received) != len(expected):
        return False  # Longueur différente = échec
    return hmac.compare_digest(received, expected)
```

---

## 3. Modes de Chiffrement Dangereux

### INTERDIT : Mode ECB

```python
# VULNÉRABLE - Ne JAMAIS utiliser
from Crypto.Cipher import AES
cipher = AES.new(key, AES.MODE_ECB)
```

**Problème** : Des blocs identiques produisent des chiffrés identiques, révélant la structure des données.

### INTERDIT : CBC sans Authentification

```python
# VULNÉRABLE - Padding Oracle Attack possible
cipher = AES.new(key, AES.MODE_CBC, iv)
ciphertext = cipher.encrypt(pad(data))
# PAS de MAC = données modifiables sans détection
```

### SÉCURISÉ : AEAD

```python
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

# Générer une clé
key = AESGCM.generate_key(bit_length=256)
aesgcm = AESGCM(key)

# Chiffrer avec authentification
nonce = os.urandom(12)  # 96 bits pour GCM
ciphertext = aesgcm.encrypt(nonce, plaintext, associated_data)
```

---

## 4. Gestion des Nonces

### Détection de Réutilisation

Chercher les patterns dangereux :

```python
# DANGER : nonce statique ou prévisible
nonce = b'\x00' * 12
nonce = b'fixed_nonce!'
nonce = hashlib.md5(message).digest()[:12]  # Même message = même nonce
```

### ECDSA et RFC 6979

**Contexte** : En ECDSA, si le nonce `k` est :
- Réutilisé : La clé privée est **mathématiquement exposée**
- Prévisible : La clé privée peut être calculée

**Solution** : RFC 6979 - Nonce déterministe

```python
# Le nonce est dérivé de : k = HMAC(private_key, H(message))
# Élimine la dépendance au RNG lors de la signature
```

Vérifier que la bibliothèque utilisée implémente RFC 6979 par défaut.

---

## 5. Gestion des Secrets en Mémoire

### Problèmes des Langages Managés

| Langage | Problème | Mitigation |
|---------|----------|------------|
| Python | Strings immuables, GC copie | Utiliser `bytearray`, effacer manuellement |
| Java | Strings dans le pool, GC | `char[]` au lieu de String, Arrays.fill() après usage |
| JavaScript | GC non déterministe | Typed arrays, null assignment |
| Go | GC, escape analysis | `memguard` package |

### Pattern de Nettoyage

```python
import ctypes

def secure_wipe(buffer: bytearray):
    """Efface un buffer de manière sécurisée."""
    length = len(buffer)
    ctypes.memset(ctypes.addressof((ctypes.c_char * length).from_buffer(buffer)), 0, length)

# Usage
password = bytearray(b"secret_password")
try:
    # Utiliser le mot de passe...
    hash_result = hash_password(password)
finally:
    secure_wipe(password)  # Toujours nettoyer
```

---

## 6. Validation des Entrées Cryptographiques

### Points à Vérifier

| Entrée | Validation |
|--------|------------|
| Clé publique ECC | Point sur la courbe, pas le point à l'infini |
| Signature | Format correct, longueur attendue |
| IV/Nonce | Longueur correcte (12 octets GCM, 24 octets XChaCha) |
| Tag d'authentification | Longueur complète (16 octets min pour GCM) |

### Exemple : Validation de Clé Publique

```python
from cryptography.hazmat.primitives.asymmetric import ec

def validate_public_key(key_bytes: bytes) -> bool:
    """Valide qu'une clé publique est sur la courbe."""
    try:
        # La bibliothèque vérifie automatiquement
        key = ec.EllipticCurvePublicKey.from_encoded_point(
            ec.SECP256R1(), key_bytes
        )
        return True
    except (ValueError, InvalidKey):
        return False  # Clé invalide ou attaque
```

---

## 7. Dépendances et Bibliothèques

### Bibliothèques Recommandées par Langage

| Langage | Recommandé | Éviter |
|---------|------------|--------|
| Python | `cryptography`, `PyNaCl` | `pycrypto` (abandonné) |
| JavaScript | `libsodium.js`, `Web Crypto API` | `crypto-js` (deprecated patterns) |
| Java | BouncyCastle, Tink | Implémentations custom |
| Go | `crypto/*`, `golang.org/x/crypto` | Packages tiers non audités |
| Rust | `ring`, `RustCrypto` | Implémentations non auditées |

### Vérifications de Dépendances

1. **Version à jour** : Pas de CVE connue
2. **Maintenance active** : Commits récents
3. **Audit de sécurité** : Préférer les libs auditées (NCC, Cure53)

---

## 8. Logging et Debug

### INTERDIT dans les Logs

- Clés (publiques ou privées)
- Mots de passe (même hachés)
- Tokens de session
- Données chiffrées avec contexte
- IVs/Nonces associés à des clés

### Pattern de Logging Sécurisé

```python
import logging

def log_crypto_operation(operation: str, key_id: str, success: bool):
    """Log une opération crypto sans exposer les secrets."""
    logging.info(f"crypto_op={operation} key_id={key_id[:8]}... success={success}")
    # Affiche seulement les 8 premiers caractères de l'ID
```

---

## Format de Rapport d'Audit

```markdown
## Rapport d'Audit Cryptographique

### [CRITIQUE] Utilisation de RNG non cryptographique
- **Fichier** : `auth/token.py:42`
- **Code** : `random.randint(0, 999999)`
- **Risque** : Tokens prévisibles, contournement d'authentification
- **Correction** : Remplacer par `secrets.randbelow(1000000)`

### [ÉLEVÉ] Comparaison non constant-time
- **Fichier** : `api/verify.py:128`
- **Code** : `if signature == expected:`
- **Risque** : Timing attack permettant de forger des signatures
- **Correction** : Utiliser `hmac.compare_digest()`

### [MODÉRÉ] Mode CBC sans authentification
- **Fichier** : `storage/encrypt.py:55`
- **Risque** : Padding oracle si erreurs de padding exposées
- **Correction** : Migrer vers AES-GCM ou ajouter HMAC-SHA256
```
