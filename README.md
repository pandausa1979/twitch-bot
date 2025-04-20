# Twitch Chat Bot and Dashboard

A full-stack application for monitoring and analyzing Twitch chat messages, built with Python, Next.js, and MongoDB.

## Project Structure

```
twitch-bot/
├── backend/           # Python backend service
│   ├── src/          # Backend source code
│   │   ├── bot.py    # Twitch chat bot implementation
│   │   ├── auth.py   # Authentication utilities
│   │   └── __main__.py
│   └── requirements.txt
├── frontend/         # Next.js frontend application
│   ├── src/          # Frontend source code
│   ├── public/       # Static assets
│   └── certificates/ # SSL certificates
└── k8s/              # Kubernetes deployment configurations
    └── mongodb/      # MongoDB deployment files
```

## Features

- Real-time Twitch chat monitoring
- Message storage and analysis
- Modern web dashboard
- Kubernetes deployment support

## Setup

### Backend

1. Create a Python virtual environment:
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Create a `.env` file with your Twitch credentials:
   ```
   TWITCH_BOT_USERNAME=your_bot_username
   TWITCH_OAUTH_TOKEN=oauth:your_oauth_token
   TWITCH_CHANNEL=channel_to_join
   ```

### Frontend

1. Install dependencies:
   ```bash
   cd frontend
   npm install
   ```

2. Generate SSL certificates (for local development):
   ```bash
   ./mkcert-v1.4.4-linux-amd64 localhost
   mv localhost.pem localhost-key.pem certificates/
   ```

3. Start the development server:
   ```bash
   npm run dev
   ```

### MongoDB

The application uses MongoDB for data storage. You can either:
- Use a local MongoDB instance
- Use the provided Kubernetes configuration in the `k8s/mongodb` directory

## Development

- Backend: Python 3.8+
- Frontend: Next.js with TypeScript
- Database: MongoDB
- Deployment: Kubernetes

## License

MIT 