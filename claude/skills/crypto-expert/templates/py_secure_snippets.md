# Snippets Python Sécurisés

## 1. Génération de Tokens et Secrets

### Token URL-Safe

```python
import secrets

def generate_secure_token(length: int = 32) -> str:
    """Génère un token URL-safe cryptographiquement sûr.

    Args:
        length: Nombre d'octets d'entropie (32 = 256 bits)

    Returns:
        Token base64url-encoded
    """
    return secrets.token_urlsafe(length)

# Usage
api_token = generate_secure_token(32)  # ~43 caractères
session_id = generate_secure_token(16)  # ~22 caractères
```

### Token Hexadécimal

```python
import secrets

def generate_hex_token(length: int = 32) -> str:
    """Génère un token hexadécimal.

    Args:
        length: Nombre d'octets (32 = 64 caractères hex)
    """
    return secrets.token_hex(length)

# Usage
api_key = generate_hex_token(32)  # 64 caractères hex
```

### Mot de Passe Temporaire

```python
import secrets
import string

def generate_temp_password(length: int = 16) -> str:
    """Génère un mot de passe robuste avec tous types de caractères.

    Args:
        length: Longueur du mot de passe (minimum 12 recommandé)

    Returns:
        Mot de passe avec majuscules, minuscules, chiffres, symboles
    """
    alphabet = string.ascii_letters + string.digits + string.punctuation

    while True:
        password = ''.join(secrets.choice(alphabet) for _ in range(length))
        # Garantir au moins un de chaque type
        if (any(c.islower() for c in password)
            and any(c.isupper() for c in password)
            and any(c.isdigit() for c in password)
            and any(c in string.punctuation for c in password)):
            return password

# Usage
temp_pw = generate_temp_password(16)
```

---

## 2. Comparaison Constant-Time

### Vérification de MAC/Signature

```python
import hmac

def verify_signature(received_sig: bytes, expected_sig: bytes) -> bool:
    """Vérifie une signature sans fuiter d'information temporelle.

    CRITIQUE: Ne JAMAIS utiliser == pour comparer des secrets.

    Args:
        received_sig: Signature reçue de l'utilisateur
        expected_sig: Signature calculée côté serveur

    Returns:
        True si les signatures correspondent
    """
    # hmac.compare_digest parcourt TOUJOURS les deux buffers entièrement
    return hmac.compare_digest(received_sig, expected_sig)

# Usage
if verify_signature(user_provided_mac, computed_mac):
    process_request()
else:
    reject_request()
```

### Vérification de Token (Strings)

```python
import hmac

def verify_token(received: str, expected: str) -> bool:
    """Compare deux tokens de manière sécurisée.

    Fonctionne aussi avec des strings (pas seulement bytes).
    """
    # Encoder en bytes pour la comparaison
    return hmac.compare_digest(
        received.encode('utf-8'),
        expected.encode('utf-8')
    )
```

---

## 3. Hachage de Mots de Passe (Argon2)

### Avec Passlib

```python
# pip install passlib[argon2]
from passlib.hash import argon2

# Configuration OWASP 2025
secure_hasher = argon2.using(
    type='ID',       # Argon2id (hybride)
    memory_cost=19456,  # 19 MiB
    time_cost=2,     # 2 itérations
    parallelism=1,   # 1 thread
    salt_len=16,     # 16 octets de sel
    hash_len=32      # 32 octets de hash
)

def hash_password(password: str) -> str:
    """Hache un mot de passe avec Argon2id.

    Args:
        password: Mot de passe en clair

    Returns:
        Hash au format PHC string (stockable en DB)
    """
    return secure_hasher.hash(password)

def verify_password(password: str, hash_str: str) -> bool:
    """Vérifie un mot de passe contre son hash.

    Args:
        password: Mot de passe fourni par l'utilisateur
        hash_str: Hash stocké en base de données

    Returns:
        True si le mot de passe correspond
    """
    try:
        return secure_hasher.verify(password, hash_str)
    except Exception:
        return False  # Hash invalide ou corrompu

# Usage
hashed = hash_password("user_password_123")
# Stocke: $argon2id$v=19$m=19456,t=2,p=1$...

is_valid = verify_password("user_password_123", hashed)
```

### Avec argon2-cffi (Alternative)

```python
# pip install argon2-cffi
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

# Configuration sécurisée
ph = PasswordHasher(
    time_cost=2,
    memory_cost=19456,  # 19 MiB
    parallelism=1,
    hash_len=32,
    salt_len=16
)

def hash_password(password: str) -> str:
    return ph.hash(password)

def verify_password(password: str, hash_str: str) -> bool:
    try:
        ph.verify(hash_str, password)
        return True
    except VerifyMismatchError:
        return False
```

---

## 4. Chiffrement Symétrique (AEAD)

### AES-256-GCM

```python
import os
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

def generate_key() -> bytes:
    """Génère une clé AES-256 (32 octets)."""
    return AESGCM.generate_key(bit_length=256)

def encrypt_aes_gcm(
    key: bytes,
    plaintext: bytes,
    associated_data: bytes = b""
) -> tuple[bytes, bytes]:
    """Chiffre avec AES-256-GCM.

    Args:
        key: Clé de 32 octets
        plaintext: Données à chiffrer
        associated_data: Données authentifiées mais non chiffrées

    Returns:
        (nonce, ciphertext) - Le nonce DOIT être stocké avec le ciphertext

    ATTENTION: Ne JAMAIS réutiliser un nonce avec la même clé!
    """
    nonce = os.urandom(12)  # 96 bits pour GCM
    aesgcm = AESGCM(key)
    ciphertext = aesgcm.encrypt(nonce, plaintext, associated_data)
    return nonce, ciphertext

def decrypt_aes_gcm(
    key: bytes,
    nonce: bytes,
    ciphertext: bytes,
    associated_data: bytes = b""
) -> bytes:
    """Déchiffre avec AES-256-GCM.

    Raises:
        InvalidTag: Si l'authentification échoue (données modifiées)
    """
    aesgcm = AESGCM(key)
    return aesgcm.decrypt(nonce, ciphertext, associated_data)

# Usage
key = generate_key()
nonce, encrypted = encrypt_aes_gcm(key, b"secret data", b"metadata")
decrypted = decrypt_aes_gcm(key, nonce, encrypted, b"metadata")
```

### ChaCha20-Poly1305 (Recommandé)

```python
import os
from cryptography.hazmat.primitives.ciphers.aead import ChaCha20Poly1305

def encrypt_chacha(
    key: bytes,
    plaintext: bytes,
    associated_data: bytes = b""
) -> tuple[bytes, bytes]:
    """Chiffre avec XChaCha20-Poly1305.

    Avantage: Nonce de 24 octets permet la génération aléatoire sûre.
    """
    # Note: cryptography utilise ChaCha20-Poly1305 (nonce 12 bytes)
    # Pour XChaCha (nonce 24 bytes), utiliser PyNaCl
    nonce = os.urandom(12)
    chacha = ChaCha20Poly1305(key)
    ciphertext = chacha.encrypt(nonce, plaintext, associated_data)
    return nonce, ciphertext

# Avec PyNaCl pour XChaCha20 (nonce 24 bytes)
# pip install pynacl
from nacl.secret import SecretBox
from nacl.utils import random

def encrypt_xchacha(key: bytes, plaintext: bytes) -> bytes:
    """Chiffre avec XChaCha20-Poly1305 (nonce inclus dans le résultat)."""
    box = SecretBox(key)
    # Le nonce est automatiquement généré et préfixé
    return box.encrypt(plaintext)

def decrypt_xchacha(key: bytes, ciphertext: bytes) -> bytes:
    """Déchiffre (le nonce est extrait automatiquement)."""
    box = SecretBox(key)
    return box.decrypt(ciphertext)
```

---

## 5. Dérivation de Clés (KDF)

### HKDF pour Dériver des Sous-Clés

```python
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives import hashes

def derive_key(
    master_key: bytes,
    salt: bytes,
    info: bytes,
    length: int = 32
) -> bytes:
    """Dérive une sous-clé depuis une clé maître.

    Args:
        master_key: Clé maître (doit avoir haute entropie)
        salt: Sel (peut être public, doit être unique par contexte)
        info: Contexte d'utilisation (ex: b"encryption" ou b"authentication")
        length: Longueur de la clé dérivée

    Returns:
        Clé dérivée
    """
    hkdf = HKDF(
        algorithm=hashes.SHA256(),
        length=length,
        salt=salt,
        info=info
    )
    return hkdf.derive(master_key)

# Usage: Dériver clé de chiffrement et clé d'authentification
master = os.urandom(32)
salt = os.urandom(16)

encryption_key = derive_key(master, salt, b"encryption", 32)
auth_key = derive_key(master, salt, b"authentication", 32)
```

---

## 6. Signature Numérique (Ed25519)

```python
from cryptography.hazmat.primitives.asymmetric.ed25519 import (
    Ed25519PrivateKey, Ed25519PublicKey
)

def generate_signing_keypair() -> tuple[bytes, bytes]:
    """Génère une paire de clés Ed25519.

    Returns:
        (private_key_bytes, public_key_bytes)
    """
    private_key = Ed25519PrivateKey.generate()
    public_key = private_key.public_key()

    return (
        private_key.private_bytes_raw(),
        public_key.public_bytes_raw()
    )

def sign_message(private_key_bytes: bytes, message: bytes) -> bytes:
    """Signe un message avec Ed25519.

    Note: Ed25519 est déterministe (pas besoin de RNG).
    """
    private_key = Ed25519PrivateKey.from_private_bytes(private_key_bytes)
    return private_key.sign(message)

def verify_signature(
    public_key_bytes: bytes,
    message: bytes,
    signature: bytes
) -> bool:
    """Vérifie une signature Ed25519."""
    try:
        public_key = Ed25519PublicKey.from_public_bytes(public_key_bytes)
        public_key.verify(signature, message)
        return True
    except Exception:
        return False

# Usage
priv, pub = generate_signing_keypair()
sig = sign_message(priv, b"important document")
is_valid = verify_signature(pub, b"important document", sig)
```

---

## 7. Nettoyage Sécurisé de Mémoire

```python
import ctypes

def secure_wipe(buffer: bytearray) -> None:
    """Efface un buffer de manière sécurisée.

    ATTENTION: Ne fonctionne que pour bytearray, pas pour str ou bytes
    (qui sont immuables en Python).

    Args:
        buffer: bytearray contenant des données sensibles
    """
    length = len(buffer)
    ctypes.memset(
        ctypes.addressof((ctypes.c_char * length).from_buffer(buffer)),
        0,
        length
    )

# Usage
password = bytearray(b"secret_password")
try:
    # Utiliser le mot de passe...
    hashed = hash_password(password.decode())
finally:
    secure_wipe(password)  # Toujours nettoyer
```

---

## 8. HMAC pour Authentification de Messages

```python
import hmac
import hashlib

def create_hmac(key: bytes, message: bytes) -> bytes:
    """Crée un HMAC-SHA256 pour un message.

    Args:
        key: Clé secrète (au moins 32 octets recommandé)
        message: Message à authentifier

    Returns:
        Tag HMAC de 32 octets
    """
    return hmac.new(key, message, hashlib.sha256).digest()

def verify_hmac(key: bytes, message: bytes, tag: bytes) -> bool:
    """Vérifie un HMAC de manière sécurisée (constant-time)."""
    expected = create_hmac(key, message)
    return hmac.compare_digest(tag, expected)

# Usage
key = os.urandom(32)
message = b"transaction: send $100 to Alice"
tag = create_hmac(key, message)

# Vérification
if verify_hmac(key, message, tag):
    process_transaction()
```

---

## Notes d'Utilisation

1. **Dépendances requises** :
   ```bash
   pip install cryptography passlib[argon2] pynacl
   ```

2. **Ne jamais** :
   - Logger des secrets
   - Stocker des clés en dur dans le code
   - Réutiliser des nonces
   - Utiliser `random` pour la crypto

3. **Toujours** :
   - Utiliser `secrets` ou `os.urandom()` pour l'aléatoire
   - Comparer les secrets avec `hmac.compare_digest()`
   - Nettoyer les buffers sensibles après usage
