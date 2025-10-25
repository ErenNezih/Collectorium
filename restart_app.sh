#!/bin/bash
# Collectorium Django App Restart Script
# cPanel/Passenger restart mechanism

echo "=== COLLECTORIUM APP RESTART SCRIPT ==="
echo "Timestamp: $(date)"
echo "Working Directory: $(pwd)"

# Create tmp directory if it doesn't exist
mkdir -p /home/collecto/collectorium/tmp

# Touch restart.txt to trigger Passenger restart
touch /home/collecto/collectorium/tmp/restart.txt

echo "Passenger restart triggered"
echo "App should restart within 30 seconds"
echo "Check logs for any errors"

# Set proper permissions
chmod 755 /home/collecto/collectorium/tmp
chmod 644 /home/collecto/collectorium/tmp/restart.txt

echo "=== RESTART COMPLETE ==="
