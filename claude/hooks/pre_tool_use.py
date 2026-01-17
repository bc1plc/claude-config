#!/usr/bin/env python3
"""
Hook de Gouvernance - Pre Tool Use
Analyse et valide les commandes avant leur execution
Agit comme un "Policy Enforcement Point" pour la securite
"""

import sys
import json
import re


def validate_bash_command(command: str) -> list:
    """
    Analyse heuristique des commandes shell pour detecter les violations de politique.
    Retourne une liste de violations detectees.
    """
    violations = []

    # =================================================================
    # REGLES DOCKER
    # =================================================================

    # Regle 1 : Interdiction formelle du mode privilegie Docker
    if "--privileged" in command:
        violations.append(
            "DANGER: Le flag '--privileged' est strictement interdit. "
            "Utilisez '--cap-add' pour des permissions granulaires specifiques."
        )

    # Regle 2 : Interdiction d'ajouter toutes les capabilities
    if re.search(r'cap-add\s*(=|:)?\s*ALL', command, re.IGNORECASE):
        violations.append(
            "EXCES DE POUVOIR: L'ajout de toutes les capabilities (ALL) est interdit. "
            "Specifiez uniquement les capabilities necessaires."
        )

    # Regle 3 : Detection de montage du socket Docker
    if re.search(r'-v\s+["\']?/var/run/docker\.sock', command):
        violations.append(
            "RISQUE ELEVE: Le montage du socket Docker est dangereux. "
            "Cela donne un acces root effectif a l'hote."
        )

    # Regle 4 : Detection du mode host network
    if "--network=host" in command or "--network host" in command:
        violations.append(
            "ATTENTION: Le mode '--network=host' expose tous les ports de l'hote. "
            "Preferez un reseau bridge avec des ports specifiques."
        )

    # Regle 5 : Detection de --pid=host
    if "--pid=host" in command or "--pid host" in command:
        violations.append(
            "RISQUE: '--pid=host' permet de voir tous les processus de l'hote. "
            "Cela peut faciliter les attaques par injection de processus."
        )

    # =================================================================
    # REGLES CADDY
    # =================================================================

    # Regle 6 : Desactivation de TLS
    if re.search(r'tls\s+off', command, re.IGNORECASE):
        violations.append(
            "NON-CONFORMITE: La desactivation de TLS dans Caddy est interdite. "
            "HTTPS doit rester actif pour la securite des communications."
        )

    # Regle 7 : Desactivation de HTTPS automatique
    if re.search(r'auto_https\s+off', command, re.IGNORECASE):
        violations.append(
            "NON-CONFORMITE: La desactivation de auto_https est interdite. "
            "Caddy doit gerer automatiquement les certificats TLS."
        )

    # =================================================================
    # REGLES FICHIERS SYSTEME
    # =================================================================

    # Regle 8 : Protection des fichiers de configuration critiques
    dangerous_patterns = [
        (r'rm\s+(-rf?\s+)?/etc/caddy', "fichiers de configuration Caddy"),
        (r'rm\s+(-rf?\s+)?/etc/docker', "fichiers de configuration Docker"),
        (r'>\s*/etc/passwd', "fichier passwd"),
        (r'>\s*/etc/shadow', "fichier shadow"),
        (r'chmod\s+777', "permissions 777 (trop permissives)"),
    ]

    for pattern, description in dangerous_patterns:
        if re.search(pattern, command, re.IGNORECASE):
            violations.append(
                f"PROTECTION: Operation dangereuse sur {description} detectee. "
                "Cette action est bloquee par la politique de securite."
            )

    # Regle 9 : Detection de curl/wget avec execution directe
    if re.search(r'(curl|wget)\s+.*\|\s*(bash|sh|sudo)', command):
        violations.append(
            "RISQUE: Execution directe de script distant detectee. "
            "Telechargez d'abord, verifiez, puis executez."
        )

    return violations


def validate_edit_command(file_path: str, new_content: str) -> list:
    """
    Valide les modifications de fichiers sensibles.
    """
    violations = []

    # Fichiers proteges
    protected_files = [
        '/etc/passwd',
        '/etc/shadow',
        '/etc/sudoers',
        '/root/.ssh/authorized_keys',
    ]

    for protected in protected_files:
        if file_path.startswith(protected):
            violations.append(
                f"PROTECTION: Modification du fichier systeme {protected} interdite."
            )

    return violations


def main():
    """
    Point d'entree du hook.
    Lit l'intention de l'agent depuis STDIN et decide d'autoriser ou rejeter.
    """
    try:
        input_data = json.load(sys.stdin)
    except json.JSONDecodeError:
        # En cas d'erreur technique, fail-closed (securite)
        print(json.dumps({
            "decision": "reject",
            "reason": "Erreur de lecture du hook: JSON invalide"
        }))
        sys.exit(0)

    tool_name = input_data.get("tool", "")
    tool_input = input_data.get("input", {})

    violations = []

    # Validation selon le type d'outil
    if tool_name == "Bash":
        command = tool_input.get("command", "")
        violations = validate_bash_command(command)

    elif tool_name in ["Edit", "Write"]:
        file_path = tool_input.get("file_path", "")
        new_content = tool_input.get("new_string", "") or tool_input.get("content", "")
        violations = validate_edit_command(file_path, new_content)

    # Decision
    if violations:
        print(json.dumps({
            "decision": "reject",
            "reason": "\n".join(violations)
        }))
    else:
        print(json.dumps({"decision": "allow"}))


if __name__ == "__main__":
    main()
