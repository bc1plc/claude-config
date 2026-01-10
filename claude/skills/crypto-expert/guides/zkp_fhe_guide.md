# Technologies de Confidentialité (Privacy Tech)

## Zero-Knowledge Proofs (ZKP)

### Introduction

Les ZKP permettent de prouver la connaissance d'une information sans la révéler. En 2025/2026, ils sont devenus une infrastructure critique pour :
- Blockchain (Layer 2, privacy coins)
- Identité numérique (prouver l'âge sans révéler la date de naissance)
- Vote électronique
- Conformité réglementaire préservant la vie privée

---

## Matrice de Choix des Frameworks ZKP

### 1. Circom + SnarkJS (Débutant / Prototypage)

**Usage** : Débutants, projets web, prototypage rapide

#### Caractéristiques
| Aspect | Détail |
|--------|--------|
| Langage | DSL Circom + JavaScript |
| Système | R1CS (Rank-1 Constraint System) |
| Preuve | Groth16 (ou PLONK) |
| Setup | **Trusted Setup spécifique par circuit** |
| Écosystème | Très large, nombreux exemples |

#### Avantages
- Courbe d'apprentissage douce pour développeurs JS
- Documentation abondante
- Intégration facile dans les dApps web

#### Inconvénients
- **Trusted Setup** : Chaque circuit nécessite sa propre cérémonie
- Performance du prouveur limitée pour grands circuits
- Le DSL Circom peut être verbeux

#### Exemple Simple
```circom
template Multiplier() {
    signal input a;
    signal input b;
    signal output c;

    c <== a * b;  // Contrainte : prouver que c = a * b
}
```

---

### 2. Halo2 (Industriel / Scalable)

**Usage** : Production, Ethereum L2, applications d'entreprise

#### Caractéristiques
| Aspect | Détail |
|--------|--------|
| Langage | Rust |
| Système | Plonkish (arithmétisation flexible) |
| Setup | **Universal Setup** (pas de trusted setup par circuit) |
| Origine | Zcash Foundation, Protocol Labs |

#### Avantages
- Pas de trusted setup spécifique par circuit
- Très performant et optimisé
- Arithmétisation flexible (lookups, custom gates)
- Récursion native (prouver des preuves)

#### Inconvénients
- Courbe d'apprentissage plus raide
- Documentation moins accessible que Circom
- Requiert maîtrise de Rust

#### Quand Choisir Halo2
- Circuits complexes (>100k contraintes)
- Besoin de récursion (agrégation de preuves)
- Production à grande échelle
- Équipe expérimentée Rust

---

### 3. SP1 / RISC Zero (zkVM)

**Usage** : Développeurs non-crypto, applications générales

#### Révolution 2025 : Les zkVM

Au lieu d'écrire des circuits cryptographiques :
1. Écrivez du code **Rust normal** (ou C++)
2. Compilez vers **RISC-V**
3. La zkVM génère une preuve de l'exécution correcte

#### Caractéristiques
| Aspect | SP1 (Succinct) | RISC Zero |
|--------|----------------|-----------|
| Langage source | Rust | Rust, C, C++ |
| Cible | RISC-V | RISC-V |
| Performance | Optimisé cloud | Optimisé GPU |
| Maturité | Production 2025 | Production 2024 |

#### Avantages Majeurs
- **Pas de circuits à écrire** : Code Rust standard
- Réutilisation de bibliothèques existantes
- Debug avec outils standard
- Temps de développement drastiquement réduit

#### Inconvénients
- Temps de génération de preuve plus long
- Overhead par rapport aux circuits optimisés
- Contraintes mémoire de la VM

#### Exemple SP1
```rust
// Ce code Rust normal peut être prouvé
fn main() {
    let a: u32 = 5;
    let b: u32 = 7;
    let c = a * b;

    // La zkVM prouve que c == 35
    sp1_zkvm::io::commit(&c);
}
```

---

### Tableau Comparatif Synthétique

| Critère | Circom | Halo2 | SP1/RISC Zero |
|---------|--------|-------|---------------|
| Difficulté | Facile | Difficile | Facile |
| Performance prover | Moyenne | Haute | Basse-Moyenne |
| Trusted Setup | Par circuit | Universal | Universal |
| Langage | DSL + JS | Rust | Rust/C/C++ |
| Circuits custom | Manuel | Manuel | Automatique |
| **Recommandé pour** | Prototypes | Production | Nouvelles apps |

---

## Fully Homomorphic Encryption (FHE)

### Concept

Le FHE permet d'effectuer des calculs **sur des données chiffrées** sans jamais les déchiffrer.

```
encrypt(a) + encrypt(b) = encrypt(a + b)
encrypt(a) * encrypt(b) = encrypt(a * b)
```

### Cas d'Usage

1. **Santé** : Analyse de données médicales chiffrées
2. **Finance** : Scoring de crédit sans voir les données
3. **ML** : Inférence sur données privées
4. **Cloud** : Traitement de données sensibles

---

## Bibliothèques FHE Recommandées

### 1. OpenFHE (C++) - Production

**Le standard de facto académique et industriel**

#### Caractéristiques
| Aspect | Détail |
|--------|--------|
| Langage | C++ (bindings Python disponibles) |
| Schémas | BGV, BFV, CKKS, TFHE |
| Maturité | Très mature, successeur de PALISADE |
| Performance | Optimisée, support hardware |

#### Schémas Disponibles
- **BFV/BGV** : Entiers exacts
- **CKKS** : Nombres réels (approximatifs)
- **TFHE** : Portes logiques, bootstrapping rapide

#### Installation
```bash
# Build from source
git clone https://github.com/openfheorg/openfhe-development.git
cd openfhe-development && mkdir build && cd build
cmake .. && make -j$(nproc)
```

---

### 2. TenSEAL (Python) - Data Science

**Wrapper Python pour opérations vectorielles**

#### Caractéristiques
| Aspect | Détail |
|--------|--------|
| Langage | Python |
| Backend | Microsoft SEAL |
| Focus | ML et opérations tensorielles |
| Facilité | Très accessible |

#### Exemple
```python
import tenseal as ts

# Créer un contexte CKKS
context = ts.context(
    ts.SCHEME_TYPE.CKKS,
    poly_modulus_degree=8192,
    coeff_mod_bit_sizes=[60, 40, 40, 60]
)
context.generate_galois_keys()
context.global_scale = 2**40

# Chiffrer un vecteur
v = [1.0, 2.0, 3.0, 4.0]
enc_v = ts.ckks_vector(context, v)

# Calcul sur chiffré
enc_result = enc_v * enc_v  # v^2 sans déchiffrer
result = enc_result.decrypt()  # [1.0, 4.0, 9.0, 16.0]
```

---

### 3. Concrete-ML (ML sur FHE)

**Machine Learning compatible FHE par Zama**

#### Usage
- Conversion de modèles scikit-learn vers FHE
- Inférence privée

```python
from concrete.ml.sklearn import LogisticRegression

# Entraîner normalement
model = LogisticRegression()
model.fit(X_train, y_train)

# Compiler pour FHE
model.compile(X_train)

# Inférence sur données chiffrées
predictions = model.predict(X_encrypted)
```

---

## Concepts Clés FHE

### 1. Noise Budget (Budget de Bruit)

**Chaque opération ajoute du "bruit" aux chiffrés**

```
[Message] + [Petit bruit] = [Chiffré valide]
[Chiffré] * [Chiffré] = [Chiffré + Plus de bruit]
```

- Si le bruit dépasse un seuil : **déchiffrement impossible**
- Les multiplications consomment plus de budget que les additions

### 2. Multiplicative Depth

**Nombre de multiplications successives possibles**

| Depth | Applications Typiques |
|-------|----------------------|
| 1-2 | Calculs simples, statistiques |
| 5-10 | Modèles ML basiques |
| 10+ | Réseaux de neurones (requiert bootstrapping) |

### 3. Bootstrapping

**Technique pour "nettoyer" le bruit et continuer les calculs**

```
[Chiffré bruyant] → Bootstrapping → [Chiffré propre]
```

- Opération très coûteuse (secondes à minutes)
- Permet des calculs arbitrairement longs
- À éviter si la profondeur du circuit est connue et faible

---

## Comparaison ZKP vs FHE

| Aspect | ZKP | FHE |
|--------|-----|-----|
| But | Prouver sans révéler | Calculer sur chiffré |
| Qui calcule | Le prouveur (sait les données) | Le serveur (ne sait rien) |
| Performance | Prover lent, verifier rapide | Calculs 10-1000x plus lents |
| Maturité production | Bonne (2024+) | Émergente (2025+) |
| Use case type | Vérification d'identité | Outsourced computation |

---

## Références

### ZKP
- Circom Docs : https://docs.circom.io/
- Halo2 Book : https://zcash.github.io/halo2/
- SP1 Docs : https://docs.succinct.xyz/

### FHE
- OpenFHE : https://openfhe.org/
- TenSEAL : https://github.com/OpenMined/TenSEAL
- Zama Concrete : https://docs.zama.ai/concrete
