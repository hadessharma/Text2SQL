"""
LLM Handler Module

SQL generation using FLAN-T5 Text-to-SQL model via HuggingFace transformers.

Function:
    generate_sql(tables, user_query): Generate SQL from natural language.
"""

import os
import logging
from typing import Dict, List

try:
    from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
    import torch
    TRANSFORMERS_AVAILABLE = True
except ImportError:
    TRANSFORMERS_AVAILABLE = False
    logging.warning("transformers library not available. Falling back to rule-based SQL.")

# Global model cache
_model = None
_tokenizer = None


# Main SQL Generation

def generate_sql(user_query: str, tables: Dict[str, List[str]]) -> str:
    """
    Generate SQL query from natural language using FLAN-T5.
    
    Args:
        user_query: Natural language query string.
        tables: Dictionary of table_name -> list of columns
    
    Returns:
        str: SQL query string
    """
    try:
        if not TRANSFORMERS_AVAILABLE:
            return _fallback_sql_generation(tables, user_query)

        initialize_model()

        input_ids = _prepare_input(user_query, tables)
        input_ids = input_ids.to(_model.device)

        outputs = _model.generate(
            input_ids,
            num_beams=10,
            max_length=512
        )

        sql = _tokenizer.decode(outputs[0], skip_special_tokens=True)
        sql = _clean_sql(sql)
        return sql

    except Exception as e:
        logging.error(f"Error during SQL generation: {e}")
        return _fallback_sql_generation(tables, user_query)


# Model Initialization

def initialize_model():
    """
    Load FLAN-T5 model and tokenizer once.
    """
    global _model, _tokenizer

    if not TRANSFORMERS_AVAILABLE:
        return

    if _model is not None and _tokenizer is not None:
        return  # already loaded

    model_name = os.getenv("MODEL_NAME", "juierror/flan-t5-text2sql-with-schema-v2")
    cache_dir = os.getenv("MODEL_CACHE_DIR", "./model_cache")

    logging.info(f"Loading FLAN-T5 model: {model_name}")

    _tokenizer = AutoTokenizer.from_pretrained(model_name, cache_dir=cache_dir)
    _model = AutoModelForSeq2SeqLM.from_pretrained(model_name, cache_dir=cache_dir)
    _model.eval()
    if torch.cuda.is_available():
        _model.to("cuda")

    logging.info("FLAN-T5 loaded successfully")


# Input preparation

def _get_prompt(tables: str, question: str) -> str:
    return f"convert question and table into SQL query. tables: {tables}. question: {question}"


def _prepare_input(question: str, tables: Dict[str, List[str]]):
    """
    Convert table dict into prompt string and tokenize.
    """
    table_strs = [f"{name}({','.join(cols)})" for name, cols in tables.items()]
    tables_prompt = ", ".join(table_strs)
    prompt = _get_prompt(tables_prompt, question)
    input_ids = _tokenizer(prompt, max_length=512, truncation=True, return_tensors="pt").input_ids
    return input_ids


# Output cleaning

def _clean_sql(sql: str) -> str:
    sql = sql.strip()
    if not sql.endswith(";"):
        sql += ";"
    return sql


# Fallback

def _fallback_sql_generation(tables: Dict[str, List[str]], user_query: str) -> str:
    """
    Simple rule-based SQL if model unavailable.
    """
    if not tables:
        return "SELECT * FROM table;"
    
    first_table = list(tables.keys())[0]

    if "department" in user_query.lower():
        return "SELECT * FROM departments;"
    if "employee" in user_query.lower():
        return "SELECT * FROM employees;"
    
    return f"SELECT * FROM {first_table};"


# Cleanup

def cleanup_model():
    """
    Release model and tokenizer.
    """
    global _model, _tokenizer
    _model = None
    _tokenizer = None