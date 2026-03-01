# Holiday Trip Planner

AI-powered holiday trip planning application using multi-agent system with FastAPI backend.

## Features

- Multi-agent AI system for trip planning and research
- Real-time destination research using Tavily and Serper APIs
- Google Maps integration for location services
- Budget-aware trip planning
- FastAPI web interface
- Docker containerized deployment
- AWS ECR integration

## Prerequisites

- Python 3.11+
- Docker
- AWS CLI (for ECR deployment)
- API Keys:
  - Groq API Key
  - Serper API Key
  - Google Maps API Key
  - Tavily API Key

## Installation

### Local Development

```bash
# Clone repository
git clone <repository-url>
cd TravelBot

# Install package
pip install -e .

# Create .env file with required API keys
cp .env.example .env
# Edit .env with your API keys
```

### Environment Variables

Create a `.env` file:

```env
GROQ_API_KEY=your_groq_api_key
SERPER_API_KEY=your_serper_api_key
MAP_API_KEY=your_google_maps_api_key
TAVILY_API_KEY=your_tavily_api_key

LANGSMITH_TRACING=true
LANGSMITH_ENDPOINT=https://api.smith.langchain.com
LANGSMITH_API_KEY=your_langsmith_api_key
LANGSMITH_PROJECT=HolidayTripAgent

AWS_REPOSITORY_URI=your_ecr_uri
AWS_REPOSITORY_NAME=holidaytripagent
AWS_DEFAULT_REGION=us-east-1
AWS_ACCESS_KEY=your_aws_access_key
AWS_SECRET_KEY=your_aws_secret_key
```

## Usage

### Run Locally

```bash
python app.py
```

Access the application at `http://localhost:8080`

### Docker Deployment

```bash
# Build image
docker build -t holidaytripagent:latest .

# Run container
docker run -p 8080:8080 --env-file .env holidaytripagent:latest
```

### AWS ECR Deployment

```bash
# Authenticate Docker to ECR
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 266735847797.dkr.ecr.us-east-1.amazonaws.com

# Build and tag image
docker build -t 266735847797.dkr.ecr.us-east-1.amazonaws.com/holidaytripagent:latest .

# Push to ECR
docker push 266735847797.dkr.ecr.us-east-1.amazonaws.com/holidaytripagent:latest

# Run from ECR
docker run -p 8080:8080 --env-file .env 266735847797.dkr.ecr.us-east-1.amazonaws.com/holidaytripagent:latest
```

## Project Structure

```
TravelBot/
├── HolidayAgent/
│   ├── agents/          # AI agents (planner, researcher)
│   ├── core/            # Core utilities (logger, exceptions)
│   ├── prompts/         # Agent prompts
│   ├── tools/           # External API tools
│   └── utils/           # Helper utilities
├── app.py               # FastAPI application
├── dockerfile           # Docker configuration
├── pyproject.toml       # Project dependencies
└── README.md
```

## API Endpoints

- `GET /` - Web interface
- `POST /plan-trip` - Plan trip endpoint
  ```json
  {
    "destination": "Goa",
    "days": 3,
    "source": "Chennai",
    "people": 2,
    "budget": 50000,
    "extra_info": "Beach activities"
  }
  ```

## Troubleshooting

### ModuleNotFoundError in Docker

Ensure `pyproject.toml` has `[build-system]` section:
```toml
[build-system]
requires = ["setuptools>=61.0"]
build-backend = "setuptools.build_meta"
```

### Container Exits Immediately

Check logs:
```bash
docker logs <container-id>
```

Verify environment variables are set correctly.

## License

MIT
