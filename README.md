# Twitch Bot

A Kubernetes-based Twitch chat bot that can be deployed for multiple channels.

## Features

- Multi-channel support with separate deployments per channel
- MongoDB integration for data persistence
- Health monitoring endpoints
- Kubernetes-native deployment
- Configurable through environment variables

## Prerequisites

- Python 3.11+
- MongoDB
- Kubernetes cluster (tested with MicroK8s)
- Twitch Developer Account

## Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/twitch-bot.git
cd twitch-bot
```

2. Create necessary Kubernetes secrets:
```bash
# Create MongoDB credentials
kubectl create secret generic mongodb-credentials \
  --from-literal=username=your_mongodb_user \
  --from-literal=password=your_mongodb_password \
  --from-literal=app_password=your_app_password

# Create Twitch credentials
kubectl create secret generic twitch-bot-secret \
  --from-literal=token=oauth:your_twitch_token \
  --from-literal=client_id=your_client_id
```

3. Deploy MongoDB:
```bash
kubectl apply -f k8s/mongodb-pvc.yaml
kubectl apply -f k8s/mongodb-deployment.yaml
kubectl apply -f k8s/mongodb-service.yaml
```

4. Deploy the bot:
```bash
# Deploy for a specific channel
kubectl apply -f k8s/twitch-bot-deployment.yaml
```

## Configuration

Copy `.env.example` to `.env` and update the values:

```bash
cp .env.example .env
# Edit .env with your configuration
```

## Development

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
.\venv\Scripts\activate  # Windows
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run locally:
```bash
python src/bot.py --channel your_channel_name
```

## Kubernetes Deployment

The application is designed to run in Kubernetes with the following components:

- MongoDB StatefulSet for data persistence
- Separate deployments for each Twitch channel
- Health checks for monitoring
- ConfigMaps for channel-specific configuration
- Secrets for sensitive data

## Directory Structure

```
.
├── backend/
│   ├── src/
│   │   ├── bot.py
│   │   ├── config.py
│   │   └── health.py
│   └── requirements.txt
├── k8s/
│   ├── mongodb-deployment.yaml
│   ├── mongodb-service.yaml
│   ├── mongodb-pvc.yaml
│   └── twitch-bot-deployment.yaml
└── README.md
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

MIT License - see LICENSE file for details 