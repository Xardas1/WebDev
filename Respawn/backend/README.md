# Respawn Backend

FastAPI backend for the Respawn addiction recovery RPG tracker.

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the server:
```bash
python run.py
```

Or with uvicorn directly:
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## API Endpoints

- `GET /` - Health check
- `GET /users` - Users endpoint (placeholder)
- `GET /quests` - Quests endpoint (placeholder)
- `GET /bosses` - Bosses endpoint (placeholder)

## Database

- SQLite database (`respawn.db`) will be created automatically
- Tables are created on startup if they don't exist
- Models: User, Quest, Boss

## Future Implementation

This is the foundation setup. Future steps will include:
- User authentication and authorization
- Quest management and completion logic
- Boss battle mechanics
- XP and leveling system
- Streak tracking
- Progress analytics
