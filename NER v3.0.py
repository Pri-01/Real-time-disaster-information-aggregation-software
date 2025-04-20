import google.generativeai as genai
import json
import os

# ------------------- Gemini API Setup -------------------
API_KEY = os.getenv("GEMINI_API_KEY", "Enter_your_key_here")
genai.configure(api_key=API_KEY)

# ------------------- Entity Extraction Function -------------------
def extract_ner_information_with_keywords(tweet):
    prompt = f"""
    Extract the following entity types from the given tweet and return them as a JSON object with keys 'Food', 'Location', 'Medicine', 'Diseases':
    - Food: Items like water, rice, bread
    - Location: Places like Chennai, Mumbai
    - Medicine: Drugs like paracetamol, antibiotics
    - Diseases: Conditions like dengue, malaria

    Tweet: {tweet.lower()}

    Example output:
    {{
        "Food": ["water", "rice"],
        "Location": ["Chennai"],
        "Medicine": ["paracetamol"],
        "Diseases": ["dengue"]
    }}

    Please provide the output in the same format.
    """

    try:
        model = genai.GenerativeModel('models/gemini-1.5-flash-001')
        response = model.generate_content(prompt)

        # Extract and parse the JSON block
        text = response.text.strip()
        json_start = text.find('{')
        json_end = text.rfind('}') + 1
        json_str = text[json_start:json_end]

        result = json.loads(json_str)
        return result

    except Exception as e:
        print("Failed to decode JSON response:", e)
        print("Raw response:", response.text)
        return None

# ------------------- Main Loop -------------------
def main():
    print("NER Extractor")
    print("Enter a tweet to extract entities. Type 'exit' to quit.\n")

    while True:
        tweet = input("> ")
        if tweet.lower() == "exit":
            print("Exiting...")
            break

        if not tweet.strip():
            print("Please enter a valid tweet.")
            continue

        result = extract_ner_information_with_keywords(tweet)
        if result:
            print("Extracted Entities:")
            print(json.dumps(result, indent=4))
        else:
            print("Could not extract entities.\n")

# ------------------- Run -------------------
if __name__ == "__main__":
    main()
