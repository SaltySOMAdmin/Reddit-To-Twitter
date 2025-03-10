#!/bin/bash

# Variables
LOG_FILE="/home/ubuntu/Reddit-To-Twitter/twitter_log.txt"
# Load configuration file. Can replace with WEBHOOK_URL="https://yourWebhook.yaddayadda"
source "/home/ubuntu/Reddit-To-Twitter/webhook.txt"  # Replace with the actual path to your config.txt file

# Check if the log file exists
if [ ! -f "$LOG_FILE" ]; then
    echo "Log file does not exist: $LOG_FILE"
    exit 1
fi

# Upload the log file to the Discord webhook
response=$(curl -s -o /dev/null -w "%{http_code}" \
    -F "file=@$LOG_FILE" \
    "$WEBHOOK_URL")

# Check if the upload was successful
if [ "$response" -eq 200 ]; then
    echo "Log file successfully uploaded."
    # Delete the log file
    rm "$LOG_FILE"
    if [ $? -eq 0 ]; then
        echo "Log file deleted successfully."
    else
        echo "Failed to delete log file."
    fi
else
    echo "Failed to upload log file. HTTP status: $response"
fi
