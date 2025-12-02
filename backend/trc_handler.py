"""
Tuple Relational Calculus (TRC) Handler Module

This module handles conversion from SQL to Tuple Relational Calculus.
TRC provides a mathematical foundation for query validation and security checks.

Functions:
    convert_sql_to_trc(sql_query, kg_data): Convert SQL to TRC expression
    format_trc_explanation(trc_expression, sql_query, user_query): Format TRC for display

TRC Format (non-deterministic):
    { E.attr1, E.attr2 | employee(E) and condition }
    Example: { E.name, E.age | employee(E) and E.age > 30 }
"""

from typing import Dict, List
import re
import sqlparse
from sqlparse.sql import Statement, IdentifierList, Identifier, Where
from sqlparse.tokens import Keyword, DML


def convert_sql_to_trc(sql_query: str, kg_data: Dict) -> str:
    """
    Convert SQL query to Tuple Relational Calculus expression.
    
    The TRC output shows the attribute names that would be displayed by the SQL query,
    allowing users to confirm this is the result they actually want.
    
    Conversion Rules (Examples):
        SELECT * FROM employees WHERE age > 30
        → {t | Employee(t) ∧ t.age > 30}
        
        SELECT e.name, d.dept_name FROM employees e JOIN departments d ON e.dept_id = d.id
        → {t | ∃e ∃d (Employee(e) ∧ Department(d) ∧ e.dept_id = d.id ∧ t.name = e.name ∧ t.dept_name = d.dept_name)}
    
    Args:
        sql_query: Valid SQL query string
        kg_data: Knowledge Graph data for schema context (currently not used but kept for API compatibility)
        
    Returns:
        str: TRC expression in declarative format showing attributes that would be displayed
        
    Raises:
        ValueError: If SQL cannot be converted to TRC (e.g., contains dangerous operations)
    """
    # Handle None kg_data for compatibility
    if kg_data is None:
        kg_data = {}
    try:
        # Normalize SQL query: strip whitespace, remove trailing semicolon
        sql_query = sql_query.strip()
        if sql_query.endswith(';'):
            sql_query = sql_query[:-1].strip()
        
        # Security check: Ensure this is a SELECT-only query
        _validate_safe_query(sql_query)
        
        # Parse SQL query
        parsed = sqlparse.parse(sql_query)
        if not parsed or len(parsed) == 0:
            raise ValueError("Invalid SQL query: Could not parse")
        
        statement = parsed[0]
        
        # Extract components
        select_attrs = _extract_select_attributes(statement)
        from_tables = _extract_from_tables(statement)
        where_conditions = _extract_where_conditions(statement)
        joins = _extract_joins(statement)
        order_by = _extract_order_by(statement)
        
        # Build TRC expression
        trc = _build_trc_expression(select_attrs, from_tables, where_conditions, joins, order_by, statement)
        
        return trc
    
    except ValueError:
        raise
    except Exception as e:
        raise ValueError(f"Failed to convert SQL to TRC: {str(e)}")


def format_trc_explanation(trc_expression: str, sql_query: str, user_query: str) -> Dict[str, str]:
    """
    Format TRC explanation for user display.
    
    Returns:
        Dict: Structured explanation with keys:
            - query: Original user query
            - sql: Generated SQL
            - trc: TRC formula
            - description: English explanation
    """
    return {
        "query": user_query,
        "sql": sql_query,
        "trc": trc_expression,
        "description": "The TRC expression shows the attributes that would be displayed by this SQL query."
    }


# Helper functions for SQL parsing and TRC construction

def _validate_safe_query(sql_query: str) -> None:
    """
    Validate that the SQL query is safe (SELECT-only, no data modification).
    
    Raises:
        ValueError: If query contains dangerous operations
    """
    sql_upper = sql_query.upper()
    
    # Dangerous operations that should not be allowed
    dangerous_keywords = [
        'DROP', 'DELETE', 'UPDATE', 'INSERT', 'ALTER', 'CREATE', 'TRUNCATE',
        'EXEC', 'EXECUTE', 'CALL', 'GRANT', 'REVOKE', 'COMMIT', 'ROLLBACK'
    ]
    
    for keyword in dangerous_keywords:
        # Check if keyword appears as a standalone word (not part of another word)
        pattern = r'\b' + keyword + r'\b'
        if re.search(pattern, sql_upper):
            raise ValueError(f"Unsafe operation detected: {keyword}. Only SELECT queries are allowed.")


def _extract_select_attributes(statement: Statement) -> List[Dict[str, str]]:
    """
    Extract attribute names from SELECT clause with their source table information.
    
    Returns:
        List of dicts with 'name' and 'source' keys
        Example: [{'name': 'name', 'source': 'e'}, {'name': 'age', 'source': None}]
        Or [{'name': '*', 'source': None}] for SELECT *
    """
    attributes = []
    
    # Find SELECT token and the identifier list
    for i, token in enumerate(statement.tokens):
        if isinstance(token, IdentifierList):
            # This is the SELECT list
            for identifier in token.get_identifiers():
                attr_str = str(identifier).strip()
                if attr_str.upper() == '*':
                    return [{'name': '*', 'source': None}]
                
                # Check for table.column format
                if '.' in attr_str:
                    dot_parts = attr_str.split('.')
                    if len(dot_parts) == 2:
                        source = dot_parts[0].strip().strip('"\'`')
                        attr_name = dot_parts[1].strip().strip('"\'`')
                        attributes.append({'name': attr_name, 'source': source})
                    else:
                        # Multiple dots - take last as attribute name
                        attr_name = dot_parts[-1].strip().strip('"\'`')
                        attributes.append({'name': attr_name, 'source': None})
                else:
                    # Simple attribute name
                    attr_name = attr_str.strip().strip('"\'`')
                    attributes.append({'name': attr_name, 'source': None})
            break
        elif isinstance(token, Identifier) and i > 0:
            # Single identifier after SELECT (not in a list)
            # Check if previous token was SELECT
            prev_idx = i - 1
            while prev_idx >= 0 and str(statement.tokens[prev_idx]).strip() == '':
                prev_idx -= 1
            if prev_idx >= 0:
                prev_token = statement.tokens[prev_idx]
                if prev_token.ttype is DML and prev_token.value.upper() == 'SELECT':
                    attr_str = str(token).strip()
                    if attr_str.upper() == '*':
                        return [{'name': '*', 'source': None}]
                    
                    if '.' in attr_str:
                        dot_parts = attr_str.split('.')
                        if len(dot_parts) == 2:
                            source = dot_parts[0].strip().strip('"\'`')
                            attr_name = dot_parts[1].strip().strip('"\'`')
                            attributes.append({'name': attr_name, 'source': source})
                        else:
                            attr_name = dot_parts[-1].strip().strip('"\'`')
                            attributes.append({'name': attr_name, 'source': None})
                    else:
                        attr_name = attr_str.strip().strip('"\'`')
                        attributes.append({'name': attr_name, 'source': None})
                    break
    
    return attributes if attributes else [{'name': '*', 'source': None}]


def _extract_from_tables(statement: Statement) -> List[Dict[str, str]]:
    """
    Extract table names from FROM clause.
    
    Returns:
        List of dicts with 'name' and optional 'alias' keys
        Example: [{'name': 'employees', 'alias': 'e'}, {'name': 'departments', 'alias': 'd'}]
    """
    tables = []
    
    for i, token in enumerate(statement.tokens):
        if token.ttype is Keyword and token.value.upper() == 'FROM':
            # Look for table identifier after FROM (skip whitespace)
            j = i + 1
            while j < len(statement.tokens) and str(statement.tokens[j]).strip() == '':
                j += 1
            
            if j < len(statement.tokens):
                next_token = statement.tokens[j]
                
                if isinstance(next_token, Identifier):
                    # Parse table name and alias
                    table_str = str(next_token).strip()
                    # Handle table alias (e.g., "employees e" or "employees AS e")
                    parts = re.split(r'\s+(?:AS\s+)?', table_str, flags=re.IGNORECASE)
                    table_name = parts[0].strip().strip('"\'`')
                    alias = parts[1].strip().strip('"\'`') if len(parts) > 1 and parts[1].strip() else None
                    
                    if table_name:
                        tables.append({'name': table_name, 'alias': alias})
            break
    
    return tables


def _extract_where_conditions(statement: Statement) -> List[str]:
    """
    Extract WHERE clause conditions.
    
    Returns:
        List of condition strings
    """
    conditions = []
    
    for token in statement.tokens:
        if isinstance(token, Where):
            # Extract the condition part (everything after WHERE keyword)
            where_str = str(token).strip()
            # Remove "WHERE" keyword
            where_str = re.sub(r'^\s*WHERE\s+', '', where_str, flags=re.IGNORECASE)
            if where_str:
                conditions.append(where_str.strip())
            break
    
    return conditions


def _extract_joins(statement: Statement) -> List[Dict[str, str]]:
    """
    Extract JOIN information from the statement.
    
    Returns:
        List of join dicts with 'type', 'table', 'alias', 'condition' keys
    """
    joins = []
    tokens = statement.tokens
    
    i = 0
    while i < len(tokens):
        token = tokens[i]
        token_str = str(token).upper().strip()
        
        if token_str in ('JOIN', 'INNER JOIN', 'LEFT JOIN', 'RIGHT JOIN', 'FULL JOIN', 'LEFT OUTER JOIN', 'RIGHT OUTER JOIN', 'FULL OUTER JOIN'):
            join_type = token_str.replace('OUTER', '').strip()
            join_info = {'type': join_type, 'table': None, 'alias': None, 'condition': None}
            
            # Get table name (next non-whitespace token)
            j = i + 1
            while j < len(tokens) and str(tokens[j]).strip() == '':
                j += 1
            if j < len(tokens):
                table_token = tokens[j]
                if isinstance(table_token, Identifier):
                    table_str = str(table_token).strip()
                    # Handle table alias (e.g., "departments d" or "departments AS d")
                    parts = re.split(r'\s+(?:AS\s+)?', table_str, flags=re.IGNORECASE)
                    join_info['table'] = parts[0].strip().strip('"\'`')
                    join_info['alias'] = parts[1].strip().strip('"\'`') if len(parts) > 1 and parts[1].strip() else None
                else:
                    # Fallback: parse as string
                    table_str = str(table_token).strip()
                    parts = re.split(r'\s+(?:AS\s+)?', table_str, flags=re.IGNORECASE)
                    join_info['table'] = parts[0].strip().strip('"\'`')
                    join_info['alias'] = parts[1].strip().strip('"\'`') if len(parts) > 1 and parts[1].strip() else None
                j += 1
            
            # Look for ON condition
            while j < len(tokens) and str(tokens[j]).strip() == '':
                j += 1
            if j < len(tokens) and str(tokens[j]).upper().strip() == 'ON':
                # Collect ON condition
                on_condition = []
                j += 1
                # Skip whitespace after ON
                while j < len(tokens) and str(tokens[j]).strip() == '':
                    j += 1
                while j < len(tokens):
                    on_token = tokens[j]
                    token_str = str(on_token).upper().strip()
                    # Stop at next major clause
                    if on_token.ttype is Keyword and token_str in ('WHERE', 'GROUP', 'ORDER', 'HAVING', 'LIMIT', 'JOIN', 'INNER', 'LEFT', 'RIGHT', 'FULL', 'ON'):
                        break
                    # Don't add empty whitespace tokens
                    if str(on_token).strip():
                        on_condition.append(str(on_token))
                    j += 1
                condition_str = ' '.join(on_condition).strip()
                if condition_str:
                    join_info['condition'] = condition_str
                i = j - 1
            else:
                i = j
            
            joins.append(join_info)
        else:
            i += 1
    
    return joins


def _extract_order_by(statement: Statement) -> List[Dict[str, str]]:
    """
    Extract ORDER BY information.
    
    Returns:
        List of dicts with 'column' and 'direction' keys
    """
    order_by = []
    
    # Find ORDER BY clause
    idx = -1
    for i, token in enumerate(statement.tokens):
        if token.ttype is Keyword and token.value.upper() == 'ORDER BY':
            idx = i
            break
            
    if idx != -1:
        # Process tokens after ORDER BY
        j = idx + 1
        while j < len(statement.tokens):
            token = statement.tokens[j]
            if isinstance(token, IdentifierList):
                for identifier in token.get_identifiers():
                    _process_order_identifier(identifier, order_by)
            elif isinstance(token, Identifier):
                _process_order_identifier(token, order_by)
            elif token.ttype is Keyword and token.value.upper() in ('ASC', 'DESC'):
                # Handle standalone direction keywords if not caught in identifier
                if order_by:
                    order_by[-1]['direction'] = token.value.upper()
            j += 1
            
    return order_by


def _process_order_identifier(identifier: Identifier, order_by: List[Dict]):
    """Helper to process an identifier in ORDER BY clause."""
    # Check for direction in the identifier itself
    s = str(identifier).strip()
    parts = re.split(r'\s+', s)
    
    direction = 'ASC' # Default
    column = parts[0]
    
    if len(parts) > 1:
        if parts[-1].upper() in ('ASC', 'DESC'):
            direction = parts[-1].upper()
            column = ' '.join(parts[:-1])
            
    order_by.append({'column': column, 'direction': direction})


def _build_trc_expression(select_attrs: List[Dict], from_tables: List[Dict], 
                          where_conditions: List[str], joins: List[Dict], 
                          order_by: List[Dict],
                          statement: Statement) -> str:
    """
    Build TRC expression from parsed SQL components.
    
    The TRC expression shows the attributes that would be displayed by the SQL query.
    
    Args:
        select_attrs: List of attribute dicts with 'name' and 'source' keys
        from_tables: List of table dicts with 'name' and 'alias'
        where_conditions: List of WHERE conditions
        joins: List of JOIN information
        statement: Parsed SQL statement for additional context
        
    Returns:
        str: TRC expression showing attributes that would be displayed
    """
    if not from_tables:
        raise ValueError("No tables found in FROM clause")
    
    # Main tuple variable (use uppercase letter for main table, following academic convention)
    main_table = from_tables[0]
    main_alias_orig = main_table.get('alias') or main_table['name']
    
    # Convert to uppercase single letter tuple variable
    if len(main_alias_orig) == 1:
        main_alias = main_alias_orig.upper()
    else:
        # Use first letter of alias or table name, capitalized (e.g., 'employees' -> 'E', 'emp' -> 'E')
        main_alias = main_alias_orig[0].upper()
    
    # Build relation predicates and tuple variable assignments
    predicates = []
    quantifiers = []
    
    # Create alias mapping: original alias -> table_name
    alias_to_table = {}
    for table in from_tables:
        alias = table.get('alias') or table['name']
        alias_to_table[alias] = table['name']
    
    for join in joins:
        join_alias = join.get('alias') or join['table']
        alias_to_table[join_alias] = join['table']
    
    # Map original aliases to uppercase tuple variables for consistency
    alias_to_tuple_var = {}
    alias_to_tuple_var[main_alias_orig] = main_alias
    
    # Handle main table - use lowercase table name for relation predicate
    table_name = _format_table_name_for_trc(main_table['name'])
    predicates.append(f"{table_name}({main_alias})")
    
    # Handle joins with existential quantifiers
    for join in joins:
        join_table = join['table']
        join_alias_orig = join.get('alias') or join_table
        
        # Convert join alias to uppercase single letter tuple variable
        if len(join_alias_orig) == 1:
            join_tuple_var = join_alias_orig.upper()
        else:
            # Use first letter of alias or table name, capitalized
            join_tuple_var = join_alias_orig[0].upper() if join_alias_orig else join_table[0].upper()
        
        alias_to_tuple_var[join_alias_orig] = join_tuple_var
        
        table_name = _format_table_name_for_trc(join_table)
        predicates.append(f"{table_name}({join_tuple_var})")
        quantifiers.append(f"(exists {join_tuple_var})")
        
        # Add join condition - convert aliases to tuple variables
        if join.get('condition'):
            condition = _convert_condition_to_trc(join['condition'], list(alias_to_table.keys()), alias_to_tuple_var)
            predicates.append(condition)
    
    # Handle WHERE conditions - convert aliases to tuple variables
    for condition in where_conditions:
        trc_condition = _convert_condition_to_trc(condition, list(alias_to_table.keys()), alias_to_tuple_var)
        predicates.append(trc_condition)
    
    # Build attribute list for SELECT clause (non-deterministic format)
    # Attributes are listed explicitly in the TRC expression
    displayed_attrs = []
    
    # Check if we have valid select attributes (not empty and not just whitespace)
    if not select_attrs or (len(select_attrs) == 1 and select_attrs[0].get('name') == '*'):
        # SELECT * - use tuple variable directly (all attributes)
        # Format: { E | employee(E) and ... }
        attr_list = main_alias
    else:
        # Build explicit attribute list with source variables
        # Format: { E.attr1, E.attr2 | employee(E) and ... }
        attr_parts = []
        for attr_info in select_attrs:
            attr_name = attr_info.get('name', '').strip()
            if not attr_name or attr_name == '*':
                continue
                
            source_alias = attr_info.get('source')
            
            # Determine source table tuple variable
            if source_alias:
                # Use the mapped tuple variable if available
                source_var = alias_to_tuple_var.get(source_alias)
                if not source_var:
                    # Convert to uppercase single letter
                    if len(source_alias) == 1:
                        source_var = source_alias.upper()
                    else:
                        source_var = source_alias[0].upper()
                    alias_to_tuple_var[source_alias] = source_var
            else:
                # Use main tuple variable
                source_var = main_alias
            
            # Format as source_var.attr_name (e.g., "E.eID", "E.name")
            attr_parts.append(f"{source_var}.{attr_name}")
            displayed_attrs.append(attr_name)
        
        attr_list = ', '.join(attr_parts)
    
    # Combine predicates with 'and' (non-deterministic format uses 'and' not '∧')
    predicate_str = ' and '.join(predicates)
    
    # Build final TRC expression in non-deterministic format
    # Format: { attr_list | condition }
    if quantifiers:
        # Wrap quantifiers and predicates
        quantifier_str = ' '.join(quantifiers) + ' '
        trc = f"{{ {attr_list} | {quantifier_str}({predicate_str}) }}"
    else:
        trc = f"{{ {attr_list} | {predicate_str} }}"
        
    # Append sorting information (educational annotation)
    if order_by:
        sort_parts = []
        for item in order_by:
            col = item['column']
            # Try to map alias to tuple variable
            if '.' in col:
                parts = col.split('.')
                alias = parts[0]
                attr = parts[1]
                if alias in alias_to_tuple_var:
                    col = f"{alias_to_tuple_var[alias]}.{attr}"
            else:
                # Assume main table
                col = f"{main_alias}.{col}"
                
            sort_parts.append(f"{col} {item['direction']}")
            
        trc += f" sorted by {', '.join(sort_parts)}"
    
    return trc


def _format_table_name_for_trc(table_name: str) -> str:
    """
    Convert table name to lowercase form for TRC predicate (non-deterministic format).
    Example: 'employees' -> 'employee', 'departments' -> 'department'
    """
    # Remove quotes if present
    table_name = table_name.strip('"\'`')
    # Convert to lowercase for non-deterministic TRC format
    return table_name.lower()


def _convert_condition_to_trc(condition: str, table_aliases: List[str], alias_to_tuple_var: Dict[str, str] = None) -> str:
    """
    Convert SQL condition to TRC format.
    
    Args:
        condition: SQL condition string
        table_aliases: List of table aliases used in the query
        alias_to_tuple_var: Mapping from original aliases to tuple variables
        
    Returns:
        str: TRC-formatted condition
    """
    # Clean up the condition
    condition = condition.strip()
    trc_condition = condition
    
    # Handle table.column references - convert aliases to tuple variables
    if alias_to_tuple_var:
        # Replace aliases with tuple variables in the condition
        # Sort by length (longest first) to avoid partial matches
        sorted_aliases = sorted(alias_to_tuple_var.keys(), key=len, reverse=True)
        for alias in sorted_aliases:
            tuple_var = alias_to_tuple_var[alias]
            if alias != tuple_var:
                # Replace alias.column with tuple_var.column
                pattern = rf'\b{re.escape(alias)}\.(\w+)'
                trc_condition = re.sub(pattern, rf'{tuple_var}.\1', trc_condition)
                # Also replace standalone alias references (for comparisons)
                pattern = rf'\b{re.escape(alias)}\b'
                trc_condition = re.sub(pattern, tuple_var, trc_condition)
    else:
        # Fallback: just ensure proper formatting
        for alias in table_aliases:
            pattern = rf'\b{re.escape(alias)}\.(\w+)'
            trc_condition = re.sub(pattern, rf'{alias}.\1', trc_condition)
    
    return trc_condition
