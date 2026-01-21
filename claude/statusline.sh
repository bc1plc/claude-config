#!/bin/bash
input=$(cat)

# Parse JSON
MODEL=$(echo "$input" | jq -r '.model.display_name // "Claude"')
SESSION_COST=$(echo "$input" | jq -r '.cost.total_cost_usd // 0')
SESSION_ID=$(echo "$input" | jq -r '.session.id // .sessionId // empty')
CTX_INPUT=$(echo "$input" | jq -r '.context_window.total_input_tokens // 0')
CTX_OUTPUT=$(echo "$input" | jq -r '.context_window.total_output_tokens // 0')
CTX_SIZE=$(echo "$input" | jq -r '.context_window.context_window_size // 200000')

# Contexte %
USAGE=$(echo "$input" | jq '.context_window.current_usage // null')
if [ "$USAGE" != "null" ]; then
    TOKENS=$(echo "$USAGE" | jq '(.input_tokens // 0) + (.cache_creation_input_tokens // 0) + (.cache_read_input_tokens // 0)')
    PERCENT=$((TOKENS * 100 / CTX_SIZE))
else
    PERCENT=0
fi

# Coût et tokens journaliers
TODAY=$(date +%Y-%m-%d)
DAILY_FILE="$HOME/.claude/daily_cost.json"

# Calcul tokens cumulés à partir du coût (estimation)
# Opus 4.5: $5/M input, $25/M output → moyenne pondérée ~$10/M
# On utilise le coût pour estimer les tokens réels consommés
read -r DAILY_TOTAL EST_INPUT_M EST_OUTPUT_M <<< $(python3 << PYTHON
import json
import os

today = "$TODAY"
session_cost = float("$SESSION_COST")
ctx_input = int("$CTX_INPUT" or 0)
ctx_output = int("$CTX_OUTPUT" or 0)
daily_file = "$DAILY_FILE"

# Prix Opus 4.5
PRICE_INPUT = 5    # $/M tokens
PRICE_OUTPUT = 25  # $/M tokens

def find_or_create_bucket(buckets, cost, threshold=5.0):
    """Trouve un bucket existant proche ou en crée un nouveau."""
    for bucket_id, bucket_cost in list(buckets.items()):
        # Si le coût est proche (dans les 5$) d'un bucket existant, c'est la même session
        if abs(bucket_cost - cost) < threshold or cost > bucket_cost * 0.9:
            return bucket_id
    # Nouveau bucket
    new_id = f"session_{len(buckets)}"
    return new_id

try:
    data = {}
    if os.path.exists(daily_file):
        with open(daily_file) as f:
            data = json.load(f)

    # Reset si nouveau jour
    if data.get("date") != today:
        data = {"date": today, "sessions": {}}

    sessions = data.get("sessions", {})

    # Trouver le bucket approprié pour ce coût
    bucket_id = find_or_create_bucket(sessions, session_cost)

    # Mettre à jour avec le max (le coût ne peut qu'augmenter dans une session)
    sessions[bucket_id] = max(sessions.get(bucket_id, 0), session_cost)
    data["sessions"] = sessions

    # Total = somme des max de chaque bucket
    total_cost = sum(sessions.values())

    # Estimation input/output
    if ctx_output > 0 and ctx_input > 0:
        ratio = ctx_input / ctx_output
        est_input = total_cost * 1_000_000 / (PRICE_INPUT + PRICE_OUTPUT / ratio)
        est_output = est_input / ratio
    else:
        est_input = total_cost * 1_000_000 * 0.8 / PRICE_INPUT
        est_output = total_cost * 1_000_000 * 0.2 / PRICE_OUTPUT

    with open(daily_file, "w") as f:
        json.dump(data, f)

    print(f"{total_cost:.2f} {est_input/1_000_000:.1f} {est_output/1_000_000:.1f}")
except Exception as e:
    print(f"{session_cost:.2f} 0.0 0.0")
PYTHON
)

SESSION_FMT=$(printf "%.2f" "$SESSION_COST")

# Couleurs ANSI
# Format: Model $Total/jour ($session) │ ~INM↓ ~OUTM↑ │ XX%
printf "\033[36m${MODEL}\033[0m \033[33m\$${DAILY_TOTAL}\033[0m\033[90m/jour\033[0m \033[90m(\$${SESSION_FMT})\033[0m │ \033[32m~${EST_INPUT_M}M↓\033[0m \033[31m~${EST_OUTPUT_M}M↑\033[0m │ \033[35m${PERCENT}%%\033[0m"
