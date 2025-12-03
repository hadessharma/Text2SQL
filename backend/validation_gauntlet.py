"""
Three-Stage Validation Pipeline

This module implements a comprehensive validation gauntlet with three stages:
1. Syntactic Validation: Check SQL syntax using sqlparse
2. Semantic Validation: Validate against Knowledge Graph
3. Logical/Security Validation: TRC conversion and security checks

Functions:
    validate_query(sql_query, kg_data): Run all three validation stages
    is_syntactically_valid(sql_query): Stage 1 - Syntax check
    is_semantically_valid(sql_query, kg_data): Stage 2 - Semantic check
    is_logically_valid(sql_query, kg_data): Stage 3 - Logical/Security check
"""

from typing import Dict, Optional
import re

# TODO: Import sqlparse once installed
# import sqlparse


def validate_query(sql_query: str, kg_data: Dict, user_query: str = "") -> Dict:
    """
    Run three-stage validation pipeline on SQL query.
    
    TODO: Implement comprehensive validation with detailed error reporting
    
    Args:
        sql_query: SQL query string to validate
        kg_data: Knowledge Graph data for semantic validation
        user_query: Original natural language query for intent analysis
        
    Returns:
        Dict: Validation results with status and errors for each stage
        Format:
        {
            "syntactic": {"valid": bool, "errors": list},
            "semantic": {"valid": bool, "errors": list},
            "logical": {"valid": bool, "errors": list},
            "overall_valid": bool
        }
    """
    results = {
        "syntactic": {"valid": False, "errors": []},
        "semantic": {"valid": False, "errors": []},
        "logical": {"valid": False, "errors": []},
        "overall_valid": False
    }
    
    # Stage 1: Syntactic Validation
    results["syntactic"] = is_syntactically_valid(sql_query)
    
    # Only proceed to Stage 2 if Stage 1 passes
    if results["syntactic"]["valid"]:
        results["semantic"] = is_semantically_valid(sql_query, kg_data)
        
        # Only proceed to Stage 3 if Stage 2 passes
        if results["semantic"]["valid"]:
            results["logical"] = is_logically_valid(sql_query, kg_data, user_query)
    
    # Overall validation passes only if all stages pass
    results["overall_valid"] = (
        results["syntactic"]["valid"] and
        results["semantic"]["valid"] and
        results["logical"]["valid"]
    )
    
    return results


def is_syntactically_valid(sql_query: str) -> Dict:
    """
    Stage 1: Validate SQL syntax using sqlparse.
    
    TODO: Implement the following:
    1. Use sqlparse to parse SQL query
    2. Check for syntax errors
    3. Validate SQL keywords and structure
    4. Return validation result with error details
    
    Args:
        sql_query: SQL query string
        
    Returns:
        Dict: {"valid": bool, "errors": list}
    """
    try:
        # TODO: Use sqlparse to validate syntax
        # parsed = sqlparse.parse(sql_query)
        # if not parsed or len(parsed) == 0:
        #     return {"valid": False, "errors": ["Invalid SQL syntax"]}
        
        # Basic placeholder validation
        if not sql_query or not sql_query.strip():
            return {"valid": False, "errors": ["Empty SQL query"]}
        
        # Placeholder - TODO: Implement actual sqlparse validation
        return {"valid": True, "errors": []}
    
    except Exception as e:
        return {"valid": False, "errors": [f"Syntax error: {str(e)}"]}


def is_semantically_valid(sql_query: str, kg_data: Dict) -> Dict:
    """
    Stage 2: Validate SQL semantics against Knowledge Graph.
    
    TODO: Implement the following:
    1. Extract table names from SQL query
    2. Check if tables exist in KG
    3. Extract column names and validate against KG
    4. Validate relationships (JOINs, FOREIGN KEYs)
    5. Check data types compatibility
    6. Return validation result with error details
    
    Args:
        sql_query: SQL query string
        kg_data: Knowledge Graph data containing schema information
        
    Returns:
        Dict: {"valid": bool, "errors": list}
    """
    try:
        # TODO: Extract table names from SQL
        # tables = extract_tables_from_sql(sql_query)
        
        # TODO: Validate tables exist in KG
        # for table in tables:
        #     if table not in kg_data["tables"]:
        #         return {"valid": False, "errors": [f"Table {table} not found in schema"]}
        
        # TODO: Validate columns exist in respective tables
        # TODO: Validate relationships and JOINs
        
        # Placeholder
        return {"valid": True, "errors": []}
    
    except Exception as e:
        return {"valid": False, "errors": [f"Semantic error: {str(e)}"]}


def normalize_kg(kg_data: Dict) -> Dict:
    normalized = {}
    for table, table_info in kg_data.items():
        if not isinstance(table_info, dict):
            continue
        table_l = table.lower()
        normalized[table_l] = {
            "required": table_info.get("required", False),
            "columns": {col.lower(): req for col, req in table_info.get("columns", {}).items()}
        }
    return normalized


def is_logically_valid(sql_query: str, kg_data: Dict, user_query: str = "") -> Dict:
    """
    Takes in a JSON of the following format for KG
    ...
    Returns:
    Dict: {"valid": bool, "errors": list}
    Checks for CREATE and DROP queries.
    Also checks for insert.
    """
    errors = []
    
    # ----------- CHECK USER INTENT -----------
    # Check if the user is asking for destructive actions
    if user_query:
        user_query_lower = user_query.lower()
        destructive_keywords = ["delete", "remove", "drop", "insert", "update", "truncate", "alter"]
        for keyword in destructive_keywords:
            # Simple check: word boundary to avoid partial matches like "update_date"
            if re.search(r'\b' + re.escape(keyword) + r'\b', user_query_lower):
                return {"valid": False, "errors": [f"Destructive action '{keyword}' is not allowed."]}

    kg_data = normalize_kg(kg_data)
    # Normalize spacing
    sql_clean = sql_query.strip().lower()

    # ----------- CHECK DELETE -----------
    # Use search instead of match to find it anywhere (though usually it's at start)
    # Also check for just "delete" keyword if it's not followed by "from" immediately in some weird cases
    if "delete" in sql_clean:
         return {"valid": False, "errors": ["DELETE queries are not allowed."]}

    # ----------- CHECK SELECT -----------
    m = re.match(r"select\s+", sql_clean)
    if m:
        # SELECT is always allowed (read-only)
        return {"valid": True, "errors": []}

    # ----------- CHECK CREATE TABLE -----------
    m = re.match(r"create\s+table\s+(\w+)", sql_clean)
    if m:
        table = m.group(1)
        if table not in kg_data:
            errors.append(f"CREATE TABLE '{table}' is not allowed (not defined).")
        elif kg_data[table]["required"]:
            errors.append(f"CREATE TABLE '{table}' not allowed (table is required).")
        return {"valid": len(errors) == 0, "errors": errors}

    # ----------- CHECK DROP TABLE -----------
    m = re.match(r"drop\s+table\s+(\w+)", sql_clean)
    if m:
        table = m.group(1)
        if table not in kg_data:
            errors.append(f"DROP TABLE '{table}' is not allowed (not defined).")
        elif kg_data[table]["required"]:
            errors.append(f"DROP TABLE '{table}' not allowed (table is required).")
        return {"valid": len(errors) == 0, "errors": errors}

    # ----------- CHECK ALTER TABLE ADD COLUMN -----------
    m = re.match(r"alter\s+table\s+(\w+)\s+add\s+column\s+(\w+)", sql_clean)
    if m:
        table, column = m.groups()
        if table not in kg_data:
            errors.append(f"ALTER TABLE on '{table}' is not allowed (table not defined).")
        else:
            if column not in kg_data[table]["columns"]:
                errors.append(f"Column '{column}' not allowed for table '{table}'.")
            elif not kg_data[table]["columns"][column]:
                errors.append(f"Column '{column}' cannot be added (not required = FALSE).")
        return {"valid": len(errors) == 0, "errors": errors}

    # ----------- CHECK ALTER TABLE DROP COLUMN -----------
    m = re.match(r"alter\s+table\s+(\w+)\s+drop\s+column\s+(\w+)", sql_clean)
    if m:
        table, column = m.groups()
        if table not in kg_data:
            errors.append(f"ALTER TABLE on '{table}' is not allowed (table not defined).")
        else:
            if column not in kg_data[table]["columns"]: # Fixed typo tabkg_datales -> kg_data
                errors.append(f"Column '{column}' does not exist in metadata.")
            elif kg_data[table]["columns"][column]:
                errors.append(f"Column '{column}' is required and cannot be dropped.")
        return {"valid": len(errors) == 0, "errors": errors}

    # ----------- CHECK INSERT INTO -----------
    m = re.match(r"insert\s+into\s+(\w+)\s*\((.*?)\)\s*values", sql_clean)
    if m:
        table, cols_raw = m.groups()
        cols = [c.strip() for c in cols_raw.split(",")]

        if table not in kg_data:
            errors.append(f"INSERT into '{table}' is not allowed (table not defined).")
        else:
            # all required columns must be listed
            for col, required in kg_data[table]["columns"].items():
                if required and col not in cols:
                    errors.append(f"Required column '{col}' missing from INSERT into '{table}'.")

        return {"valid": len(errors) == 0, "errors": errors}

    return {"valid": False, "errors": ["SQL query type not recognized or unsupported."]}

def extract_tables_from_sql(sql_query: str) -> list:
    """
    Helper function to extract table names from SQL query.
    
    TODO: Implement robust table name extraction
    - Handle FROM clauses
    - Handle JOIN clauses
    - Handle subqueries
    - Handle aliases
    
    Args:
        sql_query: SQL query string
        
    Returns:
        list: List of table names found in query
    """
    # TODO: Implement using sqlparse or regex
    # This is a placeholder
    return []

