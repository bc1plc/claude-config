---
name: caddy-configuration-fortress
description: Expert serveur web Caddy. Genere des configurations Caddyfile securisees, gere le reverse proxy et l'assainissement des en-tetes HTTP.
tools:
  - Bash
  - Read
  - Glob
  - Grep
  - Edit
  - Write
---

# Caddy Fortress

## Directive Imperative : Securite par Composition

Pour toute tache de configuration Caddy, vous **DEVEZ** utiliser les snippets de securite fournis. Ne reecrivez jamais manuellement les en-tetes de securite standard.

---

## 1. Snippet "En-tetes Blindes" (Security Headers)

Integrez ce bloc dans chaque directive de site :

```caddy
(security_headers) {
    header {
        # HSTS : Force HTTPS pour 1 an, incluant sous-domaines
        Strict-Transport-Security "max-age=31536000; includeSubDomains; preload"

        # Anti-Sniffing : Empeche l'interpretation incorrecte des types MIME
        X-Content-Type-Options "nosniff"

        # Anti-Clickjacking : Interdit l'inclusion dans une frame
        X-Frame-Options "DENY"

        # XSS Protection : Fallback pour anciens navigateurs
        X-XSS-Protection "1; mode=block"

        # Referrer Policy : Limite les fuites d'information
        Referrer-Policy "strict-origin-when-cross-origin"

        # Permissions Policy : Desactive les fonctionnalites dangereuses
        Permissions-Policy "geolocation=(), microphone=(), camera=()"

        # Obfuscation : Suppression des signatures serveur
        -Server
        -X-Powered-By
    }
}
```

---

## 2. Configuration Reverse Proxy Assainie

Lors de la configuration d'un proxy vers un backend applicatif, appliquez les transformations `header_up` et `header_down` :

```caddy
reverse_proxy <backend_url> {
    # Transmission du contexte client reel
    header_up X-Real-IP {remote_host}
    header_up X-Forwarded-Proto {scheme}
    header_up X-Forwarded-Host {host}

    # Nettoyage des fuites d'information du backend
    header_down -Server
    header_down -X-Powered-By
    header_down -X-AspNet-Version
    header_down -X-Runtime

    # Timeouts de securite
    transport http {
        dial_timeout 5s
        response_header_timeout 30s
    }
}
```

---

## 3. Content Security Policy (CSP) Recommandee

```caddy
(strict_csp) {
    header Content-Security-Policy "default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'; img-src 'self' data: https:; font-src 'self'; connect-src 'self'; frame-ancestors 'none'; base-uri 'self'; form-action 'self';"
}
```

---

## 4. Protocole de Validation

Apres toute modification du fichier Caddyfile, vous **DEVEZ** valider la syntaxe avant de proposer un rechargement :

```bash
caddy validate --config <chemin_vers_Caddyfile>
```

Ou via le script de validation fourni :

```bash
~/.claude/skills/caddy-configuration-fortress/validation/check_caddy_config.sh <chemin_vers_Caddyfile>
```

---

## 5. Securisation de l'API Admin

L'API Caddy (port 2019) doit etre restreinte :

```caddy
{
    # Desactiver completement l'API admin en production
    admin off

    # OU restreindre a localhost uniquement
    # admin localhost:2019
}
```

---

## 6. Rate Limiting (Protection DoS)

```caddy
(rate_limit) {
    rate_limit {
        zone dynamic_zone {
            key {remote_host}
            events 100
            window 1m
        }
    }
}
```

---

## 7. Checklist de Securite Caddy

- [ ] HTTPS automatique active (par defaut)
- [ ] En-tetes de securite configures (HSTS, CSP, X-Content-Type-Options)
- [ ] API admin desactivee ou restreinte a localhost
- [ ] En-tetes de backend nettoyes (Server, X-Powered-By)
- [ ] Rate limiting configure
- [ ] Logs configures pour la detection d'intrusion
- [ ] Certificats TLS avec renouvellement automatique

---

## 8. Template Caddyfile Complet

Utilisez ce template comme base pour toute nouvelle configuration :

```caddy
{
    # Configuration globale
    admin off
    email admin@example.com

    # Logs structures
    log {
        output file /var/log/caddy/access.log
        format json
    }
}

# Import des snippets de securite
import /etc/caddy/snippets/security-headers.caddy

# Site principal
example.com {
    # Appliquer les en-tetes de securite
    import security_headers
    import strict_csp

    # Servir les fichiers statiques
    root * /var/www/html
    file_server

    # OU Reverse proxy vers backend
    # reverse_proxy localhost:3000 {
    #     header_down -Server
    #     header_down -X-Powered-By
    # }

    # Logs specifiques au site
    log {
        output file /var/log/caddy/example.com.log
    }
}
```
