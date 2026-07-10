"""
SchemaSay Utilities — Input Validation Helpers

Provides clean validation logic checks for user natural language prompts.
"""

def validate_prompt(prompt: str) -> tuple[bool, str]:
    """
    Validates a natural language search query.
    Returns:
      - (True, "") if valid.
      - (False, "error message") if validation fails.
    """
    if not prompt or not prompt.strip():
        return False, "Prompt query cannot be empty or contain only whitespace characters."
    
    cleaned = prompt.strip()
    if len(cleaned) < 5:
        return False, "Query prompt is too short. Please enter a descriptive request (at least 5 characters)."
        
    return True, ""
