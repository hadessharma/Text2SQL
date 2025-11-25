# Just to demonstrate the llm handler working and how it should be fed input and how output will look
# Feel free to delete if not needed anymore

import llm_handler

tables = {
    "employees": ["id", "name", "department", "salary"],
    "departments": ["id", "name", "location"]
}

queries = [
    "Find all employees",
    "Show employees in the marketing department",
    "List all departments",
    "Get all employees with salary over 50000",
    "Which departments are located in London?"
]

llm_handler.initialize_model()

for q in queries:
    print(f"User Query: {q}")
    sql = llm_handler.generate_sql(q, tables)  # pass tables dict, not schema string, might need to make function to translate
    print(f"Generated SQL:\n{sql}\n")

llm_handler.cleanup_model()
