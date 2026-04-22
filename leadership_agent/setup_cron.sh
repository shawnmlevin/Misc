#!/usr/bin/env bash
# Prints the crontab line to add for daily 7am delivery.
# Run: bash setup_cron.sh
# Then: crontab -e  and paste the line shown below.

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PYTHON="$(which python3)"
LOG="$SCRIPT_DIR/agent.log"

echo ""
echo "Add this line to your crontab (run 'crontab -e' to edit):"
echo ""
echo "0 7 * * * $PYTHON $SCRIPT_DIR/agent.py >> $LOG 2>&1"
echo ""
echo "This will send your daily brief at 7:00am every day."
echo "Logs will be written to: $LOG"
