# Infrastructure de Gestion de Clés (KMS)

## Hiérarchie de Décision

Le choix de l'infrastructure de gestion de clés dépend du contexte de conformité et de l'architecture.

---

## Niveau 1 : Cloud KMS (Standard)

### AWS KMS / Google Cloud KMS / Azure Key Vault

**Usage** : Majorité des applications cloud-natives

#### Caractéristiques

| Aspect | AWS KMS | GCP Cloud KMS | Azure Key Vault |
|--------|---------|---------------|-----------------|
| Type HSM | FIPS 140-2 Level 2 (ou 3) | FIPS 140-2 Level 3 | FIPS 140-2 Level 2 |
| Intégration IAM | Native | Native | Native (Azure AD) |
| Rotation auto | Oui (annuelle) | Oui | Oui |
| Prix | Par clé + opération | Par clé + opération | Par clé + opération |

#### Avantages
- **Clés ne quittent jamais le HSM** : Déchiffrement uniquement dans le service
- **Audit intégré** : CloudTrail, Cloud Audit Logs
- **Scaling automatique** : Milliers d'opérations/seconde
- **Conformité** : SOC2, PCI-DSS, HIPAA

#### Architecture Typique

```
[Application] → API → [Cloud KMS] → [HSM Hardware]
                              ↓
                        [Audit Logs]
```

#### Quand Choisir Cloud KMS
- Applications 100% cloud
- Équipe DevOps standard (pas de cryptographes)
- Conformité SOC2, PCI-DSS, HIPAA standard
- Budget modéré

#### Exemple AWS KMS (Python)

```python
import boto3

kms = boto3.client('kms')

# Chiffrer
response = kms.encrypt(
    KeyId='arn:aws:kms:region:account:key/key-id',
    Plaintext=b'sensitive-data'
)
ciphertext = response['CiphertextBlob']

# Déchiffrer
response = kms.decrypt(CiphertextBlob=ciphertext)
plaintext = response['Plaintext']
```

---

## Niveau 2 : HashiCorp Vault (Multi-Cloud / Hybride)

### Abstraction Unifiée

**Usage** : Environnements multi-cloud, hybrides, ou avec secrets dynamiques

#### Caractéristiques

| Aspect | Détail |
|--------|--------|
| Déploiement | Self-hosted ou HCP Vault |
| Backend secrets | AWS, GCP, Azure, databases, PKI, SSH |
| Secrets dynamiques | Oui (génération à la volée) |
| Lease/TTL | Secrets temporaires auto-révoqués |
| Audit | Complet, exportable |

#### Avantages Clés

1. **Secrets Dynamiques**
   - Générer des credentials DB pour 10 minutes
   - Credentials uniques par pod/container
   - Réduction de la surface d'attaque

2. **Encryption as a Service (Transit)**
   - Chiffrer/déchiffrer sans exposer les clés
   - Rotation transparente
   - Versioning des clés

3. **PKI Intégrée**
   - Génération de certificats à la volée
   - Courte durée de vie (heures/jours)
   - Révocation automatique

#### Architecture

```
[App 1] ─┐
[App 2] ─┼→ [Vault API] → [Backend: AWS KMS / HSM / Auto-unseal]
[App 3] ─┘      ↓
           [Audit Log]
           [Policy Engine]
```

#### Exemple : Secret Dynamique PostgreSQL

```hcl
# Configuration Vault
path "database/creds/readonly" {
  capabilities = ["read"]
}

# L'application demande des credentials
vault read database/creds/readonly
# Retourne: username=v-app-readonly-abc123, password=xyz789
# TTL: 1 heure, puis automatiquement révoqué
```

#### Quand Choisir Vault
- Multi-cloud (AWS + GCP + on-premise)
- Besoin de secrets dynamiques (databases, cloud APIs)
- PKI interne à grande échelle
- Équipe DevOps mature

---

## Niveau 3 : HSM Physique (Haute Assurance)

### Thales Luna / Entrust nShield / AWS CloudHSM

**Usage** : Banques, Autorités de Certification, Gouvernement

#### Niveaux de Certification

| Niveau FIPS 140-2 | Protection |
|-------------------|------------|
| Level 2 | Evidence de tamper, rôles basiques |
| **Level 3** | **Résistance physique au tamper, zeroization** |
| Level 4 | Protection environnementale complète |

#### Caractéristiques HSM Level 3

| Aspect | Détail |
|--------|--------|
| Protection physique | Boîtier anti-intrusion, auto-destruction |
| Clés | **Jamais exportables en clair** |
| Génération | RNG hardware certifié |
| Authentification | Multi-factor, quorum (M-of-N) |
| Audit | Tamper-evident logs |

#### Cas d'Usage Obligatoires

1. **Autorités de Certification (CA)**
   - Clés racines PKI
   - Exigences WebTrust, ETSI

2. **Banques & Paiements**
   - Clés de signature PCI-PIN
   - Dérivation de clés EMV

3. **Gouvernement & Défense**
   - Données classifiées
   - Infrastructure critique

4. **Blockchain Institutionnelle**
   - Custody de crypto-actifs
   - Clés de signature on-chain

#### Architecture HSM On-Premise

```
[Application] → [HSM Client] → [Network] → [HSM Appliance]
                                                 ↓
                                           [Tamper-Evident Logs]
                                           [Backup HSM (DR)]
```

#### AWS CloudHSM (HSM-as-a-Service)

```python
# Exemple avec PKCS#11
from pkcs11 import lib, Mechanism

# Connexion au HSM
library = lib('/opt/cloudhsm/lib/libcloudhsm_pkcs11.so')
token = library.get_token(token_label='hsm-token')
session = token.open(user_pin='crypto_user:password')

# Générer une clé dans le HSM (ne quitte jamais le HSM)
key = session.generate_key(
    KeyType.AES, 256,
    store=True, label='app-encryption-key'
)

# Chiffrer (le plaintext va au HSM, le ciphertext revient)
ciphertext = key.encrypt(plaintext, mechanism=Mechanism.AES_GCM)
```

---

## Tableau de Décision

| Critère | Cloud KMS | Vault | HSM Physique |
|---------|-----------|-------|--------------|
| Coût | $ | $$ | $$$$ |
| Complexité ops | Faible | Moyenne | Élevée |
| Multi-cloud | Non (vendor lock) | Oui | Variable |
| Secrets dynamiques | Non | **Oui** | Non |
| FIPS 140-2 Level 3 | Parfois | Via backend | **Toujours** |
| Contrôle physique | Non | Non (sauf self-host) | **Oui** |
| Régulation stricte | Suffisant | Suffisant | **Obligatoire** |

---

## Bonnes Pratiques Transversales

### 1. Séparation des Clés

```
[Key Encryption Key (KEK)] → chiffre → [Data Encryption Key (DEK)]
        ↓                                      ↓
    Stocké dans KMS/HSM                  Stocké avec les données
```

- KEK : Longue durée de vie, très protégée
- DEK : Courte durée de vie, une par ressource

### 2. Rotation des Clés

| Type | Fréquence Recommandée |
|------|----------------------|
| DEK (données) | À chaque écriture ou mensuelle |
| KEK (master) | Annuelle |
| Clés d'API | 90 jours max |
| Certificats TLS | 90 jours (Let's Encrypt) à 1 an |

### 3. Backup et DR

- **HSM** : Backup chiffré vers HSM secondaire
- **Vault** : Snapshot régulier + unseal keys distribuées
- **Cloud KMS** : Multi-région automatique

### 4. Principe du Moindre Privilège

```hcl
# Exemple Vault Policy
path "secret/data/app-a/*" {
  capabilities = ["read"]  # Pas de write
}

path "secret/data/app-b/*" {
  capabilities = []  # Aucun accès
}
```

---

## Références

- AWS KMS Best Practices : https://docs.aws.amazon.com/kms/latest/developerguide/best-practices.html
- HashiCorp Vault Architecture : https://developer.hashicorp.com/vault/docs/internals/architecture
- NIST SP 800-57 : Recommendation for Key Management
- PCI DSS Key Management : Section 3.5-3.6
