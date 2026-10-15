# Migpt

**An AI-powered conversational platform built for intelligent conversations, document-based question answering, and scalable AI applications.**

Migpt is a production-oriented AI application inspired by modern conversational AI platforms. It is being developed with a focus on clean architecture, security, maintainability, automated testing, and cloud deployment.

The goal is to build an application that supports AI-powered conversations, persistent chat history, and Retrieval-Augmented Generation (RAG), allowing users to interact with their documents and retrieve contextually relevant information.

## Project Goals

- Build a modern AI-powered conversational interface.
- Support user authentication and protected resources.
- Persist conversations and messages in a relational database.
- Implement streaming AI responses for a responsive chat experience.
- Enable document-based question answering using RAG.
- Use vector search to retrieve relevant document context.
- Implement background processing for resource-intensive tasks.
- Apply automated testing and production-oriented security practices.
- Containerize the application and prepare it for cloud deployment.

## Technology Stack

### Backend
- **FastAPI** — Asynchronous Python API framework.
- **SQLAlchemy** — Database ORM and SQL toolkit.
- **Alembic** — Database schema migrations.
- **PostgreSQL** — Relational database for users, conversations, messages, and application data.
- **ChromaDB** — Vector database for embeddings and semantic retrieval.
- **Celery** — Background task processing.
- **RabbitMQ** — Message broker for background tasks.
- **Redis** — Caching and other fast-access operations, where appropriate.
- **Pydantic** — Data validation and settings management.

### Frontend
- **React** — User interface.
- **TypeScript** — Type-safe application development.
- **Vite** — Development server and build tooling.
- **Tailwind CSS** — Utility-first styling.

### Testing
- **Pytest** — Backend testing.
- **Vitest** — Frontend unit and component testing.
- **React Testing Library** — Testing React components.
- **MSW** — Mocking API requests in frontend tests.

### DevOps and Infrastructure
- **Docker** — Application containerization.
- **Docker Compose** — Multi-service application configuration.
- **Docker Hub** — Container image registry.
- **AWS** — Cloud infrastructure and deployment.
- **Terraform** — Infrastructure as Code.
- **Git and GitHub** — Version control and collaboration.

The exact dependencies and versions will be documented in their respective application directories as development progresses.

## Planned Features

### AI Conversations
- Interactive chat interface.
- Conversation and message persistence.
- Context-aware responses using conversation history.
- Streaming AI responses.
- Conversation management.

### Authentication and Security
- User registration and login.
- Secure password hashing.
- Access-token and refresh-token authentication.
- Protected API endpoints.
- Input validation and appropriate authorization checks.

### Document-Based Question Answering
- Document upload and text extraction.
- Document chunking and embedding generation.
- Vector storage and semantic search with ChromaDB.
- Retrieval-Augmented Generation (RAG).
- Context-grounded answers based on retrieved document content.

### Background Processing
- Asynchronous processing of document ingestion and other suitable long-running tasks.
- Celery workers coordinated through RabbitMQ.
- Retry handling and operational error reporting where appropriate.

### Production Readiness
- Structured application configuration.
- Database migrations.
- Automated tests.
- Logging and error handling.
- API versioning.
- Health-check endpoints.
- Rate limiting and security controls.
- Containerization and cloud deployment preparation.

*Features are planned and will be marked as implemented as development progresses.*

## Architecture Overview

Migpt is designed around separate frontend and backend applications, with supporting infrastructure for persistence, AI retrieval, caching, and background processing.

```text
                    ┌─────────────────────┐
                    │   React Frontend    │
                    │  TypeScript + Vite  │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │    FastAPI Backend  │
                    │ Authentication      │
                    │ Chat and AI Logic   │
                    └──────────┬──────────┘
                               │
              ┌────────────────┼────────────────┐
              ▼                ▼                ▼
       ┌─────────────┐  ┌─────────────┐  ┌─────────────┐
       │ PostgreSQL  │  │  ChromaDB   │  │ LLM Provider│
       │ App Data    │  │ Vector Data │  │ AI Responses│
       └─────────────┘  └─────────────┘  └─────────────┘

                    Background Processing
                    ┌─────────────────────┐
                    │ Celery + RabbitMQ    │
                    │ Redis where needed   │
                    └─────────────────────┘
```

PostgreSQL will serve as the authoritative store for relational application data. ChromaDB will handle vector storage and semantic retrieval. PostgreSQL will not use the pgvector extension.

## Getting Started

### Prerequisites

Install or configure the following tools as needed:

- Python.
- Node.js and npm.
- PostgreSQL.
- Git.
- An LLM provider API key.
- `uv` for Python dependency management.

Docker Desktop is not required for initial local development. Dockerfiles and Docker Compose configuration will be prepared for containerized environments, with image builds performed using an available container runtime or remote build service.

### Clone the Repository

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd migpt
```

### Development Setup

The backend and frontend will have their own setup instructions:

- [Backend Setup](./backend/README.md)
- [Frontend Setup](./frontend/README.md)

These files will be added as the respective applications are implemented.

Environment-specific values should be configured through environment variables. Use `.env.example` to document the required configuration without exposing real credentials.

**Never commit API keys, database passwords, JWT secrets, or other sensitive credentials to GitHub.**

## API Documentation

During local backend development, FastAPI will provide interactive API documentation at:

- **Swagger UI:** `/docs`
- **ReDoc:** `/redoc`

API routes will use an explicit versioned prefix, such as `/api/v1/`.

## Testing

Testing will be incorporated throughout development rather than postponed until the end.

- Backend unit and integration tests with Pytest.
- Frontend component and unit tests with Vitest and React Testing Library.
- API mocking with MSW.
- Authentication, authorization, database, and error-handling tests.
- Additional integration tests for AI and document-processing workflows.

Test commands and configuration will be documented in the backend and frontend READMEs.

## Deployment

Migpt is being designed with containerized deployment and cloud infrastructure in mind.

The planned deployment workflow includes:

1. Build application container images.
2. Publish images to Docker Hub.
3. Provision the required cloud infrastructure using Terraform.
4. Configure application secrets and environment variables securely.
5. Deploy the application and supporting services.
6. Configure persistent storage, networking, HTTPS, logging, and health checks.
7. Validate the deployment with integration and smoke tests.

The final deployment architecture will be documented once the infrastructure has been implemented and tested.

## Project Structure

The repository is expected to follow this general structure as development progresses:

```text
migpt/
├── backend/
│   ├── README.md
│   ├── Dockerfile
│   └── ...
├── frontend/
│   ├── README.md
│   ├── Dockerfile
│   └── ...
├── docker-compose.yml
├── .env.example
├── .gitignore
└── README.md
```

The directory structure may evolve as the application grows.

## Development Philosophy

Migpt is being developed with an emphasis on:

- Clean, modular architecture.
- Separation of concerns.
- Secure authentication and data handling.
- Maintainable database schemas and migrations.
- Automated testing.
- Reproducible environments.
- Resource-conscious local development.
- Reliable background processing.
- Infrastructure as Code.
- Clear documentation.

## Project Status

**Status:** In development.

Migpt is currently in the initial environment setup and architecture stage. Features and infrastructure will be documented as they are implemented and verified.

## License

A license will be added when the project's distribution and licensing terms have been decided.
