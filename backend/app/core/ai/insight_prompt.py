from typing import Tuple
from app.core.ai.query_generator import sanitize_prompt_input

def build_insight_prompts(question: str, data_summary: str) -> Tuple[str, str]:
    """
    Constructs a structured prompt configuration separating instructions from content.
    Removes unnecessary SQL statements from prompt contexts to optimize token cost.
    """
    # Sanitize user inputs to mitigate injection overrides
    sanitized_question = sanitize_prompt_input(question)
    sanitized_summary = sanitize_prompt_input(data_summary)

    system_prompt = (
        "You are a professional business intelligence analyst. Your task is to interpret query results "
        "and draft a clear, natural language business insight for the user.\n\n"
        "SYSTEM RULES:\n"
        "1. Focus strictly on explaining what the data indicates and the key trend/implication.\n"
        "2. Keep the answer concise: write exactly 2 to 3 sentences.\n"
        "3. Write in direct business language. Avoid technical SQL syntax or code talk.\n"
        "4. Do not speculate or make up numbers. Only use the summary values provided in the context."
    )

    user_prompt = (
        "[INSTRUCTION CONTEXT]\n"
        "Please analyze the following query execution inputs to formulate your business insight response.\n\n"
        "[USER QUESTION]\n"
        f"{sanitized_question}\n\n"
        "[QUERY RESULTS SUMMARY]\n"
        f"{sanitized_summary}\n\n"
        "[RESPONSE]\n"
        "Provide your 2-3 sentence business narrative insight now:"
    )

    return system_prompt, user_prompt
