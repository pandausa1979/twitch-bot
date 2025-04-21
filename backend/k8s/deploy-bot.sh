#!/bin/bash

# Check if channel name is provided
if [ -z "$1" ]; then
    echo "Usage: $0 <channel_name>"
    echo "Example: $0 caedrel"
    exit 1
fi

CHANNEL=$1

# Remove '#' if present in channel name
CHANNEL=${CHANNEL/#\#/}

# Convert template to actual deployment
sed "s/\${CHANNEL}/$CHANNEL/g" twitch-bot-deployment.yaml > twitch-bot-$CHANNEL.yaml

# Apply the deployment
microk8s kubectl apply -f twitch-bot-$CHANNEL.yaml

echo "Deployed bot for channel: $CHANNEL"
echo "To check status: microk8s kubectl get pods -l channel=$CHANNEL"
echo "To view logs: microk8s kubectl logs -f -l channel=$CHANNEL" 