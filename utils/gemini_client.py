import os
import json
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure the Gemini API
api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY environment variable is not set")

genai.configure(api_key=api_key)

def get_available_models():
    """List available models in the Gemini API."""
    try:
        models = genai.list_models()
        available_models = []
        for model in models:
            model_info = {
                "name": model.name,
                "display_name": model.display_name,
                "supports_functions": "generateContent" in [m.name for m in model.supported_methods]
            }
            available_models.append(model_info)
        return available_models
    except Exception as e:
        print(f"Error listing models: {e}")
        return []

def analyze_resume(resume_text):
    """
    Analyze resume using Gemini API.
    Returns structured data about the resume and suggestions for improvement.
    """
    # Get available models for debugging (optional)
    available_models = get_available_models()
    print(f"Available models: {json.dumps(available_models, indent=2)}")
    
    # Use gemini-2.0-flash model directly as specified
    try:
        print("Using model: gemini-2.0-flash")
        generation_model = genai.GenerativeModel("gemini-2.0-flash")
    except Exception as e:
        print(f"Error initializing gemini-2.0-flash model: {e}")
        raise Exception("Failed to initialize the gemini-2.0-flash model. Please check your API key and permissions.")

    # Continue with the existing prompt and response handling
    prompt = f"""
    You are a professional resume analyst. Please analyze the following resume and provide:
    
    1. Extract the personal information (name, email, phone, location, etc.)
    2. Extract skills mentioned in the resume
    3. Extract education history
    4. Extract work experience
    5. Provide 5-7 specific suggestions to improve this resume
    
    Format your response as a JSON object with the following structure:
    {{
        "personal_info": {{
            "name": "",
            "email": "",
            "phone": "",
            "location": ""
        }},
        "skills": ["skill1", "skill2", ...],
        "education": [
            {{"degree": "", "institution": "", "year": "", "details": ""}},
            ...
        ],
        "experience": [
            {{"position": "", "company": "", "duration": "", "details": ""}},
            ...
        ],
        "suggestions": ["suggestion1", "suggestion2", ...]
    }}
    
    RESUME TEXT:
    {resume_text}
    """
    
    try:
        response = generation_model.generate_content(prompt)
        
        # Extract JSON from response
        json_str = response.text
        # Clean up the string if there are markdown code blocks
        if "```json" in json_str:
            json_str = json_str.split("```json")[1].split("```")[0].strip()
        elif "```" in json_str:
            json_str = json_str.split("```")[1].split("```")[0].strip()
            
        # Parse JSON
        analysis = json.loads(json_str)
        return analysis
    except Exception as e:
        print(f"Error parsing Gemini API response: {e}")
        if 'response' in locals():
            print(f"Raw response: {response.text}")
        raise Exception(f"Failed to parse resume analysis: {str(e)}")
