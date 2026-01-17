#!/usr/bin/env python3
"""
Suggest minimal Linux capabilities for Docker containers
Based on application type and requirements
"""

import sys
import json

# Mapping des types d'applications vers leurs capabilities minimales
APP_CAPABILITIES = {
    "web-server": {
        "description": "Serveur web (nginx, apache, caddy)",
        "caps": ["NET_BIND_SERVICE"],
        "notes": "Necessaire uniquement si ecoute sur port < 1024"
    },
    "database": {
        "description": "Base de donnees (postgres, mysql, mongodb)",
        "caps": ["CHOWN", "SETUID", "SETGID"],
        "notes": "Pour la gestion des fichiers de donnees"
    },
    "network-tool": {
        "description": "Outil reseau (ping, traceroute)",
        "caps": ["NET_RAW"],
        "notes": "Pour les paquets ICMP"
    },
    "scheduler": {
        "description": "Planificateur (cron, systemd)",
        "caps": ["SETUID", "SETGID", "SYS_NICE"],
        "notes": "Pour changer d'utilisateur et ajuster les priorites"
    },
    "minimal": {
        "description": "Application standard sans besoins speciaux",
        "caps": [],
        "notes": "Utilisez --cap-drop ALL pour une securite maximale"
    },
    "file-processor": {
        "description": "Traitement de fichiers avec changement de proprietaire",
        "caps": ["CHOWN", "FOWNER"],
        "notes": "Pour modifier les attributs de fichiers"
    }
}

def suggest_capabilities(app_type: str) -> dict:
    """Suggere les capabilities minimales pour un type d'application."""

    if app_type not in APP_CAPABILITIES:
        return {
            "status": "error",
            "message": f"Type inconnu: {app_type}",
            "available_types": list(APP_CAPABILITIES.keys())
        }

    config = APP_CAPABILITIES[app_type]

    # Generer la commande Docker
    caps = config["caps"]
    if caps:
        cap_add = " ".join([f"--cap-add {c}" for c in caps])
        docker_cmd = f"docker run --cap-drop ALL {cap_add} <image>"
    else:
        docker_cmd = "docker run --cap-drop ALL <image>"

    # Generer le snippet docker-compose
    if caps:
        compose_snippet = f"""services:
  app:
    image: <image>
    cap_drop:
      - ALL
    cap_add:
{chr(10).join([f'      - {c}' for c in caps])}
    security_opt:
      - no-new-privileges:true"""
    else:
        compose_snippet = """services:
  app:
    image: <image>
    cap_drop:
      - ALL
    security_opt:
      - no-new-privileges:true"""

    return {
        "status": "success",
        "app_type": app_type,
        "description": config["description"],
        "capabilities": caps,
        "notes": config["notes"],
        "docker_command": docker_cmd,
        "compose_snippet": compose_snippet
    }


def list_all_capabilities():
    """Liste toutes les configurations disponibles."""
    result = {"status": "success", "configurations": []}

    for app_type, config in APP_CAPABILITIES.items():
        result["configurations"].append({
            "type": app_type,
            "description": config["description"],
            "capabilities": config["caps"]
        })

    return result


def main():
    if len(sys.argv) < 2:
        print(json.dumps(list_all_capabilities(), indent=2, ensure_ascii=False))
        sys.exit(0)

    app_type = sys.argv[1].lower()

    if app_type == "--list" or app_type == "-l":
        result = list_all_capabilities()
    else:
        result = suggest_capabilities(app_type)

    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
