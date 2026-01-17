# Sync Config to GitHub

Synchronise la configuration Claude locale vers le repo GitHub.

## Instructions

Exécute le script de synchronisation :

```bash
~/.claude/scripts/sync-to-github.sh "$ARGUMENTS"
```

Si `$ARGUMENTS` est vide, utilise un message de commit par défaut.

Après l'exécution :
1. Affiche le résultat à l'utilisateur
2. Si des erreurs surviennent, aide à les résoudre
3. Confirme que la sync est terminée avec le lien GitHub

## Exemple d'utilisation

- `/sync-config` → sync avec message par défaut
- `/sync-config "feat: add new security skill"` → sync avec message personnalisé
