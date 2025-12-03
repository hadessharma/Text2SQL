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
from typing import Optional, Dict
import re

# TODO: Import your modules once implemented
import llm_handler
from kg_store import save_kg, load_kg
from llm_handler import generate_sql
from validation_gauntlet import validate_query
from trc_handler import convert_sql_to_trc, format_trc_explanation

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
    trc_explanation: Dict
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
    
    1. Validate SQL DDL format (Basic check)
    2. Parse lower/upper bound schemas
    3. Save KG to persistent store using kg_store.save_kg()
    4. Return unique database_id
    
    Args:
        request: SchemaRequest containing SQL DDL schema and bound schemas
        
    Returns:
        SchemaResponse with database_id and confirmation message
    """
    try:
        # Placeholder ID generation
        import uuid
        import json
        db_id = str(uuid.uuid4())
        
        # Parse JSON strings if provided
        lower_bound = None
        if request.lower_bound_schema:
            try:
                lower_bound = json.loads(request.lower_bound_schema)
            except json.JSONDecodeError:
                raise HTTPException(status_code=400, detail="Invalid JSON in lower_bound_schema")

        upper_bound = None
        if request.upper_bound_schema:
            try:
                upper_bound = json.loads(request.upper_bound_schema)
            except json.JSONDecodeError:
                raise HTTPException(status_code=400, detail="Invalid JSON in upper_bound_schema")

        # Construct KG data structure
        # In a real implementation, we would parse the SQL DDL to populate this further
        kg_data = {
            "schema_content": request.schema_content,
            "lower_bound_schema": lower_bound,
            "upper_bound_schema": upper_bound,
            "generated_kg": {
                # TODO: This would be the result of parsing the DDL and merging with bounds
                "tables": upper_bound.get("tables", {}) if upper_bound else {}
            }
        }
        
        # Save to store
        from kg_store import save_kg
        if save_kg(db_id, kg_data):
            return SchemaResponse(
                database_id=db_id,
                message="Schema uploaded and KG saved successfully."
            )
        else:
            raise HTTPException(status_code=500, detail="Failed to save Knowledge Graph")

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/api/databases")
async def list_databases():
    """List all available database IDs."""
    from kg_store import list_all_databases
    return {"databases": list_all_databases()}


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

        # 4. Generate TRC explanation
        trc_query = convert_sql_to_trc(sql_query, kg_data)
        trc_explanation = format_trc_explanation(trc_query, sql_query, request.user_query)

        # 5. Validate query
        # Use structured tables data for validation
        tables_data_for_val = kg_data.get("generated_kg", {}).get("tables", {})
        validation_result = validate_query(sql_query, tables_data_for_val, request.user_query)

        # Redact SQL if validation failed
        if not validation_result["overall_valid"]:
            sql_query = ""

        return QueryResponse(
            original_query=request.user_query,
            sql_query=sql_query,
            trc_explanation=trc_explanation,
            validation_status=validation_result,
            errors=validation_result.get("errors")
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

