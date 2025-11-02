# Text2SQL Project

A comprehensive system that converts natural language queries into SQL using Knowledge Graphs and Tuple Relational Calculus. This project consists of a modern React frontend and a Python/FastAPI backend.

## 🚀 Quick Start

### Prerequisites

**Frontend:**
- **Node.js** (version 18 or higher)
- **npm** (comes with Node.js)

**Backend:**
- **Python** (version 3.9 or higher)
- **pip** (Python package manager)

### Installation & Setup

#### Frontend Setup

1. **Navigate to the frontend directory:**
   ```bash
   cd frontend
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Start the development server:**
   ```bash
   npm run dev
   ```

4. **Open your browser:**
   Navigate to `http://localhost:5173` to view the application.

#### Backend Setup

1. **Navigate to the backend directory:**
   ```bash
   cd backend
   ```

2. **Create virtual environment (recommended):**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables:**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration if needed
   ```

5. **Start the backend server:**
   ```bash
   python main.py
   # Or use uvicorn directly:
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

6. **Access API documentation:**
   - Swagger UI: `http://localhost:8000/docs`
   - ReDoc: `http://localhost:8000/redoc`

## 🛠️ Available Scripts

| Command | Description |
|---------|-------------|
| `npm run dev` | Start development server with hot reload |
| `npm run build` | Build production-ready application |
| `npm run preview` | Preview production build locally |
| `npm run lint` | Run ESLint for code quality checks |

## 🎨 Features

### Modern UI Components
- **Schema Upload**: Drag-and-drop SQL file upload with validation
- **Query Input**: Natural language query interface with examples
- **Results Display**: Tabbed view showing SQL, TRC explanation, and execution info
- **Responsive Design**: Works seamlessly on desktop, tablet, and mobile

### Key Functionality
- **File Upload**: Support for .sql and .txt files
- **Interactive Examples**: Clickable example queries for better UX
- **Real-time Validation**: Instant feedback on user input
- **Copy to Clipboard**: One-click SQL copying functionality
- **Loading States**: Visual feedback during API operations

## 🏗️ Project Structure

```
Text2SQL/
├── frontend/                    # React frontend application
│   ├── src/
│   │   ├── components/          # React components
│   │   │   ├── SchemaUpload.jsx # Schema upload interface
│   │   │   ├── QueryInput.jsx   # Natural language input
│   │   │   └── OutputDisplay.jsx # Results display
│   │   ├── services/            # API services
│   │   │   └── api.js          # Backend API integration
│   │   ├── App.jsx             # Main application component
│   │   ├── main.jsx            # Application entry point
│   │   └── index.css           # Global styles
│   ├── public/                 # Static assets
│   ├── package.json            # Dependencies and scripts
│   └── vite.config.js         # Vite configuration
│
├── backend/                     # Python/FastAPI backend
│   ├── main.py                 # FastAPI application entry point
│   ├── kg_store.py             # Knowledge Graph storage module
│   ├── llm_handler.py          # FLAN-T5 SQL generation
│   ├── validation_gauntlet.py  # Three-stage validation pipeline
│   ├── trc_handler.py          # SQL ↔ TRC conversion
│   ├── requirements.txt        # Python dependencies
│   ├── .env.example            # Environment variables template
│   └── README.md               # Backend-specific documentation
│
├── README.md                    # This file (project overview)
└── TODO.md                      # Project architecture and implementation plan
```

### Backend Module Overview

#### `main.py`
- FastAPI application setup and configuration
- API endpoints:
  - `POST /api/submit-schema`: Upload schema and generate Knowledge Graph
  - `POST /api/generate-sql`: Process natural language query and generate SQL
- Request/response models using Pydantic
- CORS middleware for frontend integration

#### `kg_store.py`
- Knowledge Graph persistence layer
- Functions for saving/loading KGs with unique database IDs
- Storage management (JSON/pickle files in local directory)
- Database ID generation and management

#### `llm_handler.py`
- FLAN-T5 model integration via transformers library
- SQL generation from natural language queries
- Model initialization and caching for performance
- Schema-aware prompt formatting

#### `validation_gauntlet.py`
- Three-stage validation pipeline:
  1. **Syntactic Validation**: SQL syntax checking using sqlparse
  2. **Semantic Validation**: Schema validation against Knowledge Graph
  3. **Logical/Security Validation**: TRC conversion and security checks
- Comprehensive error reporting for each validation stage

#### `trc_handler.py`
- Bidirectional SQL ↔ Tuple Relational Calculus conversion
- TRC expression formatting for user display
- Security validation through logical structure analysis
- Mathematical foundation for query validation

### Frontend Component Overview

#### `SchemaUpload.jsx`
- Drag-and-drop SQL file upload interface
- DDL validation and progress indicators
- Error feedback for invalid schemas

#### `QueryInput.jsx`
- Natural language query input area
- Interactive example queries
- Auto-completion and validation

#### `OutputDisplay.jsx`
- Tabbed results display showing:
  - Generated SQL query
  - TRC explanation
  - Validation results
  - Execution information
- Syntax highlighting and copy-to-clipboard functionality

## 🎯 User Workflow

### Phase 1: Schema Upload (Owner)
1. Owner uploads database schema in SQL DDL format via frontend
2. Backend generates Knowledge Graph from schema
3. KG is saved to persistent store with unique `database_id`
4. Owner receives confirmation with `database_id`

### Phase 2: Query Processing (User)
1. User selects `database_id` and enters natural language query
2. Frontend sends request to `/api/generate-sql`
3. Backend loads schema and KG from store
4. FLAN-T5 generates initial SQL query
5. Three-stage validation pipeline processes the query:
   - Syntactic validation (syntax check)
   - Semantic validation (schema/KG validation)
   - Logical/security validation (TRC conversion)
6. Results (SQL + TRC explanation) are returned to frontend
7. User views generated SQL, TRC explanation, and validation details

## 🔧 Configuration

### Frontend Environment Variables

Create a `.env` file in the `frontend/` directory:

```env
# API Configuration
VITE_API_BASE_URL=http://localhost:8000/api
```

### Backend Environment Variables

Create a `.env` file in the `backend/` directory (copy from `.env.example`):

```env
# API Configuration
API_HOST=0.0.0.0
API_PORT=8000

# Frontend URL for CORS
FRONTEND_URL=http://localhost:5173

# Model Configuration
MODEL_NAME=google/flan-t5-base
MODEL_CACHE_DIR=./model_cache

# Storage Configuration
KG_STORAGE_DIR=./kg_storage

# Logging
LOG_LEVEL=INFO
```

### API Integration

The frontend communicates with the backend through the following REST endpoints:

#### `POST /api/submit-schema`
- **Purpose**: Upload database schema and generate Knowledge Graph
- **Request Body**: 
  ```json
  {
    "schema_content": "CREATE TABLE employees (...);"
  }
  ```
- **Response**: 
  ```json
  {
    "database_id": "unique-id-here",
    "message": "Schema uploaded successfully"
  }
  ```

#### `POST /api/generate-sql`
- **Purpose**: Process natural language query and generate validated SQL
- **Request Body**: 
  ```json
  {
    "database_id": "unique-id-here",
    "user_query": "Find all employees older than 30"
  }
  ```
- **Response**: 
  ```json
  {
    "sql_query": "SELECT * FROM employees WHERE age > 30;",
    "trc_explanation": "{t | Employee(t) ∧ t.age > 30}",
    "validation_status": {
      "syntactic": {"valid": true, "errors": []},
      "semantic": {"valid": true, "errors": []},
      "logical": {"valid": true, "errors": []}
    },
    "errors": null
  }
  ```

## 🏛️ Architecture

```
Frontend (React) 
    ↕ HTTP/REST
Backend API (FastAPI)
    ↕
Core Logic (FLAN-T5, KG, TRC)
    ↕
Storage Layer (KG Store, SQLite)
```

The system follows a clean separation of concerns:
- **Frontend**: User interface and interaction
- **API Layer**: Request handling and routing
- **Core Logic**: Business logic (ML, validation, conversion)
- **Storage**: Persistent data management
