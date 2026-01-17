#!/usr/bin/env python3
"""
Docker Security Audit Script
Analyse statique des Dockerfiles selon les benchmarks CIS
"""

import sys
import re
import json
from pathlib import Path


def audit_dockerfile(path: str) -> dict:
    """
    Analyse un Dockerfile et retourne un rapport de securite structure.
    """
    report = {"status": "success", "file": path, "issues": [], "recommendations": []}

    try:
        content = Path(path).read_text()
    except FileNotFoundError:
        return {"status": "error", "message": f"Fichier non trouve: {path}"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

    lines = content.split('\n')

    # Regle 1 : Detection de l'utilisateur Root (CIS 4.1)
    if not re.search(r'^\s*USER\s+(?!root)', content, re.MULTILINE):
        report["issues"].append({
            "severity": "CRITICAL",
            "code": "CIS-4.1",
            "message": "Aucun utilisateur non-root defini. Le conteneur s'executera en root.",
            "remediation": "Ajoutez: RUN addgroup -S appgroup && adduser -S appuser -G appgroup\nUSER appuser"
        })

    # Regle 2 : Detection de sudo
    if 'sudo' in content.lower():
        report["issues"].append({
            "severity": "HIGH",
            "code": "SEC-SUDO",
            "message": "Presence de 'sudo' detectee. Violation du principe de moindre privilege.",
            "remediation": "Supprimez sudo et configurez les permissions correctement"
        })

    # Regle 3 : Surface d'attaque ADD vs COPY (CIS 4.6)
    add_matches = re.findall(r'^\s*ADD\s+(.+)$', content, re.MULTILINE)
    for match in add_matches:
        # ADD est acceptable pour extraire des archives locales
        if not match.strip().endswith('.tar.gz') and not match.strip().endswith('.tar'):
            report["issues"].append({
                "severity": "MEDIUM",
                "code": "CIS-4.6",
                "message": f"Instruction ADD utilisee: {match.strip()}",
                "remediation": "Preferez COPY pour eviter les telechargements distants implicites"
            })

    # Regle 4 : Secrets potentiels (CIS 4.9)
    secret_patterns = [
        (r'(API_KEY|APIKEY)\s*=', "Cle API"),
        (r'(SECRET|SECRET_KEY)\s*=', "Secret"),
        (r'(PASSWORD|PASSWD|PWD)\s*=', "Mot de passe"),
        (r'(TOKEN|AUTH_TOKEN|ACCESS_TOKEN)\s*=', "Token"),
        (r'(PRIVATE_KEY|SSH_KEY)\s*=', "Cle privee"),
    ]

    for pattern, secret_type in secret_patterns:
        if re.search(pattern, content, re.IGNORECASE):
            report["issues"].append({
                "severity": "CRITICAL",
                "code": "CIS-4.9",
                "message": f"{secret_type} potentiellement code en dur detecte",
                "remediation": "Utilisez des secrets Docker, des variables d'environnement au runtime, ou un gestionnaire de secrets"
            })

    # Regle 5 : Tag :latest (Best Practice)
    if re.search(r'^\s*FROM\s+\S+:latest', content, re.MULTILINE) or re.search(r'^\s*FROM\s+[^\s:]+\s*$', content, re.MULTILINE):
        report["issues"].append({
            "severity": "HIGH",
            "code": "BP-TAG",
            "message": "Image de base sans tag specifique ou avec :latest detectee",
            "remediation": "Specifiez une version precise (ex: alpine:3.19, python:3.12-slim)"
        })

    # Regle 6 : HEALTHCHECK (CIS 4.5)
    if not re.search(r'^\s*HEALTHCHECK\s+', content, re.MULTILINE):
        report["issues"].append({
            "severity": "MEDIUM",
            "code": "CIS-4.5",
            "message": "Aucune instruction HEALTHCHECK definie",
            "remediation": "Ajoutez: HEALTHCHECK --interval=30s --timeout=3s CMD curl -f http://localhost/ || exit 1"
        })

    # Regle 7 : Execution en tant que root explicite
    if re.search(r'^\s*USER\s+root\s*$', content, re.MULTILINE):
        report["issues"].append({
            "severity": "CRITICAL",
            "code": "SEC-ROOT",
            "message": "Execution explicite en tant que root detectee",
            "remediation": "Basculez vers un utilisateur non-root apres les operations necessitant root"
        })

    # Regle 8 : Packages de developpement non supprimes
    if re.search(r'(gcc|make|g\+\+|build-essential)', content) and 'multi-stage' not in content.lower():
        if not re.search(r'&&\s*(rm|apk\s+del|apt-get\s+remove)', content):
            report["recommendations"].append({
                "code": "BP-BUILD",
                "message": "Outils de build detectes sans nettoyage apparent",
                "suggestion": "Utilisez un build multi-stage ou supprimez les outils de build apres compilation"
            })

    # Regle 9 : Cache non nettoye
    if re.search(r'(apt-get\s+install|apk\s+add)', content):
        if not re.search(r'(rm\s+-rf\s+/var/cache|apt-get\s+clean|--no-cache)', content):
            report["recommendations"].append({
                "code": "BP-CACHE",
                "message": "Cache de packages potentiellement non nettoye",
                "suggestion": "Ajoutez --no-cache (apk) ou && apt-get clean && rm -rf /var/lib/apt/lists/*"
            })

    # Resume
    critical_count = sum(1 for i in report["issues"] if i["severity"] == "CRITICAL")
    high_count = sum(1 for i in report["issues"] if i["severity"] == "HIGH")
    medium_count = sum(1 for i in report["issues"] if i["severity"] == "MEDIUM")

    report["summary"] = {
        "total_issues": len(report["issues"]),
        "critical": critical_count,
        "high": high_count,
        "medium": medium_count,
        "recommendations": len(report["recommendations"]),
        "passed": len(report["issues"]) == 0
    }

    return report


def audit_compose(path: str) -> dict:
    """
    Analyse un fichier docker-compose.yml pour les problemes de securite.
    """
    report = {"status": "success", "file": path, "issues": [], "recommendations": []}

    try:
        content = Path(path).read_text()
    except Exception as e:
        return {"status": "error", "message": str(e)}

    # Regle 1 : privileged: true
    if re.search(r'privileged:\s*true', content, re.IGNORECASE):
        report["issues"].append({
            "severity": "CRITICAL",
            "code": "CIS-5.4",
            "message": "Mode privilegie active sur un ou plusieurs services",
            "remediation": "Supprimez privileged: true et utilisez cap_add pour les capabilities specifiques"
        })

    # Regle 2 : no-new-privileges absent
    if not re.search(r'no-new-privileges', content):
        report["issues"].append({
            "severity": "HIGH",
            "code": "CIS-5.25",
            "message": "Option no-new-privileges non definie",
            "remediation": "Ajoutez security_opt: [no-new-privileges:true] a chaque service"
        })

    # Regle 3 : Ports exposes sur 0.0.0.0
    exposed_ports = re.findall(r'ports:\s*\n(\s+-\s*["\']?\d+:\d+["\']?\s*\n?)+', content)
    if exposed_ports:
        report["recommendations"].append({
            "code": "BP-PORTS",
            "message": "Ports exposes detectes",
            "suggestion": "Limitez l'exposition aux interfaces necessaires (ex: 127.0.0.1:8080:8080)"
        })

    # Regle 4 : Volumes sensibles
    sensitive_mounts = ['/var/run/docker.sock', '/etc/shadow', '/etc/passwd']
    for mount in sensitive_mounts:
        if mount in content:
            report["issues"].append({
                "severity": "CRITICAL",
                "code": "SEC-MOUNT",
                "message": f"Montage sensible detecte: {mount}",
                "remediation": f"Evitez de monter {mount} sauf absolue necessite"
            })

    # Resume
    critical_count = sum(1 for i in report["issues"] if i["severity"] == "CRITICAL")
    high_count = sum(1 for i in report["issues"] if i["severity"] == "HIGH")

    report["summary"] = {
        "total_issues": len(report["issues"]),
        "critical": critical_count,
        "high": high_count,
        "passed": len(report["issues"]) == 0
    }

    return report


def main():
    if len(sys.argv) < 2:
        print(json.dumps({"status": "error", "message": "Usage: audit_dockerfile.py <chemin_fichier>"}, indent=2))
        sys.exit(1)

    filepath = sys.argv[1]

    if 'compose' in filepath.lower() or filepath.endswith('.yml') or filepath.endswith('.yaml'):
        result = audit_compose(filepath)
    else:
        result = audit_dockerfile(filepath)

    print(json.dumps(result, indent=2, ensure_ascii=False))

    # Code de sortie base sur la severite
    if result.get("status") == "error":
        sys.exit(2)
    elif result.get("summary", {}).get("critical", 0) > 0:
        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == "__main__":
    main()
