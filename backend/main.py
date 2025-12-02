"""
FastAPI Application Entry Point

This module sets up the FastAPI application with RESTful endpoints for:
- Schema upload and Knowledge Graph generation
- Natural language query processing and SQL generation

Endpoints:
    POST /api/submit-schema: Upload schema and generate KG
    POST /api/generate-sql: Process natural language query
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import re

# TODO: Import your modules once implemented
import llm_handler
from kg_store import save_kg, load_kg
from llm_handler import generate_sql
from validation_gauntlet import validate_query
from trc_handler import convert_sql_to_trc

app = FastAPI(title="Text2SQL API", version="1.0.0")

llm_handler.initialize_model()

# CORS middleware for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Frontend dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Pydantic models for request/response validation
class SchemaRequest(BaseModel):
    """Request model for schema upload"""
    schema_content: str  # SQL DDL format
    lower_bound_schema: Optional[str] = None
    upper_bound_schema: Optional[str] = None


class SchemaResponse(BaseModel):
    """Response model for schema upload"""
    database_id: str
    message: str


class QueryRequest(BaseModel):
    """Request model for SQL generation"""
    database_id: str
    user_query: str  # Natural language query


class QueryResponse(BaseModel):
    """Response model for SQL generation"""
    original_query: str
    sql_query: str
    trc_explanation: str
    validation_status: dict  # Results from three-stage validation
    errors: Optional[list] = None

def _extract_tables_from_schema(schema_ddl: str):
    """
    Very simple SQL parser to extract tables + columns.
    Works for CREATE TABLE ... (col ...).
    """
    tables = {}
    pattern = r"CREATE TABLE (\w+)\s*\((.*?)\);"
    matches = re.findall(pattern, schema_ddl, re.DOTALL | re.IGNORECASE)

    for table_name, cols_raw in matches:
        cols = []
        for line in cols_raw.split(","):
            col = line.strip().split()[0]
            if col:
                cols.append(col)
        tables[table_name] = cols

    return tables

@app.post("/api/submit-schema", response_model=SchemaResponse)
async def submit_schema(request: SchemaRequest):
    """
    Upload database schema and generate Knowledge Graph.
    
    TODO: Implement the following:
    1. Validate SQL DDL format
    2. Generate Knowledge Graph from schema
    3. Save KG to persistent store using kg_store.save_kg()
    4. Return unique database_id
    
    Args:
        request: SchemaRequest containing SQL DDL schema
        
    Returns:
        SchemaResponse with database_id and confirmation message
    """
    try:
        # TODO: Implement schema validation
        # TODO: Generate Knowledge Graph
        # TODO: Save to store and get database_id
        
        # Placeholder ID generation
        import uuid
        db_id = str(uuid.uuid4())
        
        # Placeholder KG data structure
        kg_data = {
            "schema_content": request.schema_content,
            "lower_bound_schema": request.lower_bound_schema,
            "upper_bound_schema": request.upper_bound_schema,
            "generated_kg": {} # TODO: Generate actual KG
        }
        
        # Save to store
        from kg_store import save_kg
        save_kg(db_id, kg_data)
        
        # Placeholder response
        return SchemaResponse(
            database_id=db_id,
            message="Schema uploaded successfully."
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/api/generate-sql", response_model=QueryResponse)
async def generate_sql_endpoint(request: QueryRequest):
    try:
        # Load schema+KG from database store
        kg_data = load_kg(request.database_id)
        

        # Extract tables + columns for prompt
        # (Assuming schema was saved under "generated_kg" or raw SQL)
        schema_dict = _extract_tables_from_schema(kg_data["schema_content"])
        print("Extracted schema:", schema_dict)
        print("User query:", request.user_query)
        # 3. Generate SQL using your FLAN-T5 LLM
        sql_query = generate_sql(
            user_query=request.user_query,
            tables=schema_dict
        )

        print("Generated SQL:", sql_query)

        return QueryResponse(
            original_query=request.user_query,
            sql_query=sql_query,
            trc_explanation="",
            validation_status={},
            errors=None
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/")
async def root():
    """Health check endpoint"""
    return {"message": "Text2SQL API is running"}


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

