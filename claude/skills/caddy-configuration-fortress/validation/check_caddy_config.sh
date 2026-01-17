#!/bin/bash
# =================================================================
# Caddy Configuration Validator
# Valide la syntaxe et les bonnes pratiques de securite
# =================================================================

set -e

CONFIG_FILE="${1:-Caddyfile}"

# Couleurs pour l'output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo "=========================================="
echo "Caddy Security Configuration Validator"
echo "=========================================="
echo ""

# Verifier que le fichier existe
if [ ! -f "$CONFIG_FILE" ]; then
    echo -e "${RED}ERREUR: Fichier non trouve: $CONFIG_FILE${NC}"
    exit 1
fi

echo "Fichier: $CONFIG_FILE"
echo ""

# =================================================================
# VALIDATION SYNTAXIQUE
# =================================================================
echo "--- Validation Syntaxique ---"

if command -v caddy &> /dev/null; then
    if caddy validate --config "$CONFIG_FILE" 2>/dev/null; then
        echo -e "${GREEN}[OK] Syntaxe valide${NC}"
    else
        echo -e "${RED}[ERREUR] Syntaxe invalide${NC}"
        caddy validate --config "$CONFIG_FILE"
        exit 1
    fi
else
    echo -e "${YELLOW}[WARN] Caddy non installe - validation syntaxique ignoree${NC}"
fi

echo ""

# =================================================================
# VERIFICATION DES BONNES PRATIQUES DE SECURITE
# =================================================================
echo "--- Verification Securite ---"

ISSUES=0
WARNINGS=0

# Check 1: HSTS
if grep -q "Strict-Transport-Security" "$CONFIG_FILE"; then
    echo -e "${GREEN}[OK] HSTS configure${NC}"
else
    echo -e "${RED}[SECURITE] HSTS non configure${NC}"
    ISSUES=$((ISSUES + 1))
fi

# Check 2: X-Content-Type-Options
if grep -q "X-Content-Type-Options" "$CONFIG_FILE"; then
    echo -e "${GREEN}[OK] X-Content-Type-Options configure${NC}"
else
    echo -e "${YELLOW}[WARN] X-Content-Type-Options non configure${NC}"
    WARNINGS=$((WARNINGS + 1))
fi

# Check 3: X-Frame-Options
if grep -q "X-Frame-Options" "$CONFIG_FILE"; then
    echo -e "${GREEN}[OK] X-Frame-Options configure${NC}"
else
    echo -e "${YELLOW}[WARN] X-Frame-Options non configure${NC}"
    WARNINGS=$((WARNINGS + 1))
fi

# Check 4: API Admin
if grep -q "admin off" "$CONFIG_FILE"; then
    echo -e "${GREEN}[OK] API Admin desactivee${NC}"
elif grep -q "admin localhost" "$CONFIG_FILE"; then
    echo -e "${GREEN}[OK] API Admin restreinte a localhost${NC}"
else
    echo -e "${YELLOW}[WARN] API Admin potentiellement exposee${NC}"
    WARNINGS=$((WARNINGS + 1))
fi

# Check 5: TLS desactive
if grep -qi "tls off\|auto_https off" "$CONFIG_FILE"; then
    echo -e "${RED}[CRITIQUE] TLS/HTTPS desactive detecte!${NC}"
    ISSUES=$((ISSUES + 1))
else
    echo -e "${GREEN}[OK] TLS/HTTPS actif (par defaut)${NC}"
fi

# Check 6: Server header
if grep -q "\-Server" "$CONFIG_FILE"; then
    echo -e "${GREEN}[OK] Header Server supprime${NC}"
else
    echo -e "${YELLOW}[WARN] Header Server non supprime${NC}"
    WARNINGS=$((WARNINGS + 1))
fi

# Check 7: X-Powered-By
if grep -q "\-X-Powered-By" "$CONFIG_FILE"; then
    echo -e "${GREEN}[OK] Header X-Powered-By supprime${NC}"
else
    echo -e "${YELLOW}[WARN] Header X-Powered-By non supprime${NC}"
    WARNINGS=$((WARNINGS + 1))
fi

# Check 8: CSP
if grep -q "Content-Security-Policy" "$CONFIG_FILE"; then
    echo -e "${GREEN}[OK] Content-Security-Policy configure${NC}"
else
    echo -e "${YELLOW}[WARN] Content-Security-Policy non configure${NC}"
    WARNINGS=$((WARNINGS + 1))
fi

echo ""
echo "=========================================="
echo "RESUME"
echo "=========================================="
echo "Problemes critiques: $ISSUES"
echo "Avertissements: $WARNINGS"

if [ $ISSUES -gt 0 ]; then
    echo -e "${RED}RESULTAT: ECHEC - Corrections requises${NC}"
    exit 1
elif [ $WARNINGS -gt 0 ]; then
    echo -e "${YELLOW}RESULTAT: ATTENTION - Ameliorations recommandees${NC}"
    exit 0
else
    echo -e "${GREEN}RESULTAT: SUCCES - Configuration securisee${NC}"
    exit 0
fi
