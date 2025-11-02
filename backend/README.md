# Text2SQL Backend

Python/FastAPI backend for the Text2SQL system.

## 🚀 Quick Start

### Prerequisites

- **Python** (version 3.9 or higher)
- **pip** (Python package manager)

### Installation

1. **Create virtual environment (recommended):**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables:**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

4. **Run the server:**
   ```bash
   python main.py
   # Or use uvicorn directly:
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

5. **Access API documentation:**
   - Swagger UI: `http://localhost:8000/docs`
   - ReDoc: `http://localhost:8000/redoc`

## 📁 Project Structure

```
backend/
├── main.py                    # FastAPI application entry point
├── kg_store.py                # Knowledge Graph storage module
├── llm_handler.py             # FLAN-T5 SQL generation
├── validation_gauntlet.py     # Three-stage validation pipeline
├── trc_handler.py             # SQL ↔ TRC conversion
├── requirements.txt           # Python dependencies
├── .env.example               # Environment variables template
└── README.md                  # This file
```

## 🔧 Module Overview

### `main.py`
- FastAPI application setup
- API endpoints (`/api/submit-schema`, `/api/generate-sql`)
- Request/response models
- CORS configuration

### `kg_store.py`
- Knowledge Graph persistence
- Database ID generation
- Storage management (JSON/pickle files)

### `llm_handler.py`
- FLAN-T5 model integration
- SQL generation from natural language
- Model initialization and caching

### `validation_gauntlet.py`
- Three-stage validation pipeline:
  1. Syntactic validation (sqlparse)
  2. Semantic validation (KG-based)
  3. Logical/security validation (TRC)

### `trc_handler.py`
- SQL to Tuple Relational Calculus conversion
- TRC expression formatting
- Security validation via TRC

## 📝 TODO

See comments in each module for implementation details. Key tasks:
- [ ] Implement Knowledge Graph generation from schema
- [ ] Integrate FLAN-T5 model for SQL generation
- [ ] Complete three-stage validation pipeline
- [ ] Implement TRC conversion algorithm
- [ ] Add comprehensive error handling and logging
- [ ] Write unit tests

## 🧪 Testing

```bash
# Run tests (once implemented)
pytest

# Run with coverage
pytest --cov=.
```

## 🔐 Security Notes

- Input validation via Pydantic models
- SQL injection prevention in validation stages
- CORS configured for frontend integration
- TODO: Add authentication for production use

