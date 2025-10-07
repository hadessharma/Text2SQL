# Text2SQL Project

A comprehensive system that converts natural language queries into SQL using a multi-stage validation pipeline with Knowledge Graphs and Tuple Relational Calculus.

## 🏗️ Architecture Overview

The system follows a clean separation of concerns with the following components:

```
Frontend (React) <--> API (Python/FastAPI) <--> Core Logic (FLAN-T5, KG, TRC) & KG Store <--> Database (SQLite)
```

### High-Level Components

- **Frontend**: React-based single-page application
- **Backend API**: Python/FastAPI with RESTful endpoints
- **Core Logic Engine**: FLAN-T5, Knowledge Graph, TRC processing
- **Knowledge Graph Store**: Persistent storage for generated KGs
- **Database**: SQLite for relational data

## 🔄 Workflow

### Phase 1: Schema Upload (Owner)
1. Owner uploads database schema (SQL DDL format)
2. Backend generates Knowledge Graph from schema
3. KG is saved to persistent store with unique database_id
4. Owner receives confirmation with database_id

### Phase 2: Query Processing (User)
1. User selects database_id and enters natural language query
2. Frontend sends request to `/api/generate-sql`
3. Backend loads schema and KG from store
4. FLAN-T5 generates initial SQL query
5. Three-stage validation pipeline processes the query
6. Results (SQL + TRC explanation) are returned to frontend

## 🛠️ Backend Implementation

### Core Modules

#### 1. `main.py` (API Layer)
- **Purpose**: FastAPI application entry point
- **Endpoints**:
  - `POST /api/submit-schema`: Upload schema and generate KG
  - `POST /api/generate-sql`: Process natural language query
- **Features**: Pydantic models for validation, automatic API docs

#### 2. `kg_store.py` (Knowledge Graph Storage)
- **Functions**:
  - `save_kg(db_id, kg_data)`: Persist KG to storage
  - `load_kg(db_id)`: Retrieve KG by database ID
- **Storage**: Local directory with JSON/pickle files or dedicated database
- **Features**: Unique ID generation, version tracking

#### 3. `llm_handler.py` (Query Generation)
- **Function**: `generate_sql(schema, user_query)`
- **Integration**: FLAN-T5 model via transformers library
- **Features**: Schema serialization, natural language processing

#### 4. `validation_gauntlet.py` (Three-Stage Validation)
- **Stage 1 - Syntactic**: `is_syntactically_valid(sql_query)` using sqlparse
- **Stage 2 - Semantic**: `is_semantically_valid(sql_query, kg_data)` using KG
- **Stage 3 - Logical/Security**: `convert_sql_to_trc(sql_query)` for TRC conversion
- **Features**: Comprehensive error reporting, security checks

#### 5. `trc_handler.py` (TRC Conversion)
- **Purpose**: Bidirectional SQL ↔ Tuple Relational Calculus conversion
- **Features**: Core algorithm implementation, security validation

### Schema Format

**Primary Format**: SQL DDL (Data Definition Language)

**Example**:
```sql
CREATE TABLE employees (
    emp_id INTEGER PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    age INTEGER,
    department_id INTEGER,
    salary DECIMAL(10,2),
    hire_date DATE,
    FOREIGN KEY (department_id) REFERENCES departments(dept_id)
);

CREATE TABLE departments (
    dept_id INTEGER PRIMARY KEY,
    dept_name VARCHAR(100) NOT NULL,
    manager_id INTEGER,
    budget DECIMAL(15,2)
);
```

**Features**:
- Universal standard format
- Rich metadata (constraints, relationships)
- Easy parsing and validation
- Familiar to database owners

## 🎨 Frontend Implementation

### React Components

#### 1. `SchemaUpload`
- **Purpose**: File upload interface for database schemas
- **Features**: DDL validation, progress indicators, error feedback

#### 2. `QueryInput`
- **Purpose**: Natural language query input area
- **Features**: Auto-completion, query history, validation

#### 3. `OutputDisplay`
- **Purpose**: Results display with SQL, TRC explanation, and errors
- **Features**: Syntax highlighting, copy-to-clipboard, export options

#### 4. `App.js`
- **Purpose**: Main application component
- **Features**: State management, API orchestration, routing

## 🔍 TRC Output Format

**Format**: Raw Tuple Relational Calculus expressions

**Example**:
```
Query Translation:
"Find all employees older than 30"

SQL Generated:
SELECT * FROM employees WHERE age > 30

TRC Output:
{t | t ∈ employees ∧ t.age > 30}
```

## 📋 Implementation Checklist

### Backend Development
- [ ] Set up FastAPI project structure
- [ ] Implement `main.py` with API endpoints
- [ ] Create `kg_store.py` for KG persistence
- [ ] Develop `llm_handler.py` with FLAN-T5 integration
- [ ] Build `validation_gauntlet.py` with three-stage validation
- [ ] Implement `trc_handler.py` for TRC conversion
- [ ] Add comprehensive error handling and logging
- [ ] Create unit tests for all modules

### Frontend Development
- [ ] Set up React project with necessary dependencies
- [ ] Implement `SchemaUpload` component
- [ ] Create `QueryInput` component
- [ ] Build `OutputDisplay` component
- [ ] Develop `App.js` with state management
- [ ] Add responsive design and styling
- [ ] Implement error handling and user feedback
- [ ] Create integration tests

### Integration & Testing
- [ ] End-to-end testing of complete workflow
- [ ] Performance testing with large schemas
- [ ] Security testing for SQL injection prevention
- [ ] User acceptance testing
- [ ] Documentation and deployment guides

## 🔐 Security Considerations

- **SQL Injection Prevention**: Input validation and sanitization
- **Access Control**: Future authentication system for owners
- **Data Privacy**: Secure storage of schemas and KGs
- **Query Validation**: Comprehensive security checks in TRC stage

## 🚀 Future Enhancements

- **Authentication System**: Owner registration and access control
- **Advanced KG Features**: Relationship inference, constraint propagation
- **Performance Optimization**: Caching, query optimization
- **Multi-Database Support**: PostgreSQL, MySQL, etc.
- **Analytics Dashboard**: Usage statistics and performance metrics

## 📚 Dependencies

### Backend
- FastAPI
- transformers (FLAN-T5)
- sqlparse
- pydantic
- uvicorn

### Frontend
- React
- Axios
- Material-UI (or similar)
- React Router

## 🎯 Success Metrics

- **Accuracy**: >90% correct SQL generation for valid queries
- **Performance**: <2s response time for typical queries
- **Usability**: Intuitive interface requiring minimal training
- **Reliability**: Robust error handling and validation

---

*This README serves as the complete reference for the Text2SQL project implementation. All development should follow this architecture and these specifications.*
