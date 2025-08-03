# Feature Voting System

A full-stack web application for collecting and voting on feature requests. Users can submit feature requests, vote on them, and track their status.

## Project Structure

```
feature-voting-system/
├── backend/               # Flask backend
│   ├── app/              # Application code
│   ├── scripts/          # Utility scripts
│   ├── tests/            # Test suite
│   └── requirements.txt  # Python dependencies
└── frontend/             # React frontend
    ├── src/              # Source code
    └── package.json      # Node.js dependencies
```

## Features

- User authentication (register/login)
- Create and manage feature requests
- Vote/like system for features
- Feature categorization (Bug, Feature, Enhancement)
- Status tracking (Open/Closed)
- Responsive design with modern UI
- REST API with Swagger documentation

## Prerequisites

- Python 3.10 or higher
- Node.js 18 or higher
- pnpm (for frontend package management)

## Backend Setup

1. Navigate to the backend directory:

   ```bash
   cd backend
   ```

2. Create and activate a virtual environment:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: .\venv\Scripts\activate
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Set up environment variables:

   ```bash
   cp .env.example .env
   ```

   Edit `.env` with your configurations.

5. Initialize the database:

   ```bash
   ./scripts/migrate.sh
   ```

6. Start the development server:
   ```bash
   ./scripts/start.sh
   ```
   The API will be available at `http://localhost:3000`

## Frontend Setup

1. Navigate to the frontend directory:

   ```bash
   cd frontend
   ```

2. Install dependencies:

   ```bash
   pnpm install
   ```

3. Start the development server:
   ```bash
   pnpm dev
   ```
   The application will be available at `http://localhost:5173`

## Available Scripts

### Backend

- `./scripts/start.sh`: Starts the Flask development server
- `./scripts/seed.sh`: Seeds the database
- `./scripts/migrate.sh`: Runs database migrations
- `./scripts/test.sh`: Runs the test suite

### Frontend

- `pnpm dev`: Starts the Vite development server
- `pnpm build`: Builds the production version
- `pnpm lint`: Runs ESLint
- `pnpm preview`: Previews the production build locally

## API Documentation

Once the backend is running, you can access the Swagger documentation at:

```
http://localhost:3000/api/docs
```

## Technologies Used

### Backend

- Flask: Web framework
- SQLAlchemy: ORM
- Pydantic: Data validation
- Flask-JWT-Extended: Authentication
- pytest: Testing

### Frontend

- React
- TypeScript
- Vite
- TailwindCSS
- React Query
- React Router
- React Hook Form
- Radix UI

## Development

### Backend Development

The backend follows a modular structure:

- `app/modules/`: Contains feature-specific modules
- `app/shared/`: Shared utilities and base classes
- Each module has its own:
  - Models
  - Routes
  - Schemas
  - Services
  - Repositories

### Frontend Development

The frontend follows a modern React architecture:

- `src/components/`: Reusable UI components
- `src/pages/`: Route-level components
- `src/hooks/`: Custom React hooks
- `src/stores/`: State management
- `src/lib/`: Utilities and API client

## Testing

### Backend Tests

```bash
cd backend
./scripts/test.sh
```

## License

MIT License
