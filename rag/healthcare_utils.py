from typing import List, Dict, Any
from claude_llm import Claude  # Import the Claude class we updated earlier

def categorize_query(query: str, claude_instance: Claude) -> str:
    """
    Use Claude 3.5 Sonnet to categorize the healthcare query.
    """
    prompt = f"""
    Categorize the following healthcare query into one of these categories:
    - diagnosis
    - treatment
    - research
    - patient_education
    - general

    If the query doesn't fit into any of these categories, classify it as 'general'.

    Query: {query}

    Respond with only the category name.
    """
    
    response = claude_instance.complete(prompt)
    category = response.strip().lower()
    
    # Validate the category
    valid_categories = ["diagnosis", "treatment", "research", "patient_education", "general"]
    return category if category in valid_categories else "general"

def format_healthcare_response(response: str, category: str, claude_instance: Claude) -> str:
    """
    Use Claude 3.5 Sonnet to format the healthcare response based on the query category.
    """
    prompt = f"""
    Format the following healthcare response for the category '{category}'. 
    Add a suitable prefix and ensure the response is clear, concise, and appropriate for the category.

    Original response: {response}

    Formatted response:
    """
    
    formatted_response = claude_instance.complete(prompt)
    return formatted_response.strip()

def extract_key_points(response: str, claude_instance: Claude) -> List[str]:
    """
    Use Claude 3.5 Sonnet to extract key points from the healthcare response.
    """
    prompt = f"""
    Extract the key points from the following healthcare response. 
    Present them as a bullet-point list.

    Response: {response}

    Key points:
    """
    
    key_points = claude_instance.complete(prompt)
    return [point.strip() for point in key_points.split('\n') if point.strip()]

def generate_follow_up_questions(response: str, category: str, claude_instance: Claude) -> List[str]:
    """
    Use Claude 3.5 Sonnet to generate relevant follow-up questions based on the response and category.
    """
    prompt = f"""
    Based on the following healthcare response in the category '{category}', 
    generate 3 relevant follow-up questions that a patient or healthcare provider might ask.

    Response: {response}

    Follow-up questions:
    1.
    2.
    3.
    """
    
    questions = claude_instance.complete(prompt)
    return [q.strip() for q in questions.split('\n') if q.strip() and q[0].isdigit()]

def process_healthcare_query(query: str, claude_instance: Claude) -> Dict[str, Any]:
    """
    Process a healthcare query using Claude 3.5 Sonnet's capabilities.
    """
    category = categorize_query(query, claude_instance)
    response = claude_instance.complete(query)
    formatted_response = format_healthcare_response(response, category, claude_instance)
    key_points = extract_key_points(response, claude_instance)
    follow_up_questions = generate_follow_up_questions(response, category, claude_instance)
    
    return {
        "category": category,
        "original_query": query,
        "response": formatted_response,
        "key_points": key_points,
        "follow_up_questions": follow_up_questions
    }