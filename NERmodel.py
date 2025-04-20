import google.generativeai as genai
import json
import os

# Configure the API key securely using an environment variable
API_KEY = os.getenv("GEMINI_API_KEY", "Enter_your_key_here")  # Replace fallback with your key if not using env
genai.configure(api_key=API_KEY)

def extract_ner_information_with_keywords(tweet):
    # Define a prompt to extract entities
    prompt = f"""
    Extract the following entity types from the given tweet and return them as a JSON object with keys 'Food', 'Location', 'Medicine', 'Diseases':
    - Food: Items like water, rice, bread
    - Location: Places like Chennai, Mumbai
    - Medicine: Drugs like paracetamol, antibiotics
    - Diseases: Conditions like dengue, malaria

    Tweet: {tweet.lower()}
    Example output:
    ```json
    {{
        "Food": ["water", "rice"],
        "Location": ["Chennai"],
        "Medicine": ["paracetamol"],
        "Diseases": ["dengue"]
    }}
    ```

    Please provide the output in the same format.
    """

    # Initialize model
    model = genai.GenerativeModel('models/gemini-1.5-flash-001')  # limit of 15 RPM and 1,500 RPD
    response = model.generate_content(prompt)
    
    # Try parsing the JSON from the response
    try:
        # Extract JSON block
        text = response.text
        json_start = text.find('{')
        json_end = text.rfind('}') + 1
        json_str = text[json_start:json_end]
        result = json.loads(json_str)
        return result
    except Exception as e:
        print("Failed to decode JSON response:", e)
        print("Raw response:", response.text)
        return None

    
if __name__ == "__main__":
    # tweet = "I have a fever and I need paracetamol, Norflox, ibuprofen, amoxicillin, azithromycin, atenolol, and metformin. I live in Chennai and I want some rice."
    tweet = "I have severe diarrhea and need ORS, loperamide, norfloxacin, and zinc tablets. I also require bottled water and bananas. My location is Bangalore."
    extracted_info = extract_ner_information_with_keywords(tweet)
    print(json.dumps(extracted_info, indent=4))
