# Model backend code

# from flask import Flask, request, jsonify
# from flask_cors import CORS  # Import CORS
# import joblib
# import re

# # --- Load Keyword Dictionaries ---
# KEYWORD_DICTIONARIES = {
#     "food_items": ["water", "food", "rice", "bread", "milk", "biscuits", "supplies", "oil", "flour", "sugar", "salt", "dal", 
#         "wheat", "noodles", "fruits", "vegetables", "meals", "cereal", "tea", "coffee", "eggs", "butter", "paneer",
#         "pulses", "fish", "meat", "chicken", "mutton", "ghee", "cheese", "yogurt", "curd", "juices", "snacks", "potatoes", 
#         "onions", "tomatoes", "bananas", "apples", "mangoes", "oranges", "coconut water", "corn", "chapati", "roti", 
#         "paratha", "idli", "dosa", "sambar", "pulao", "biryani", "khichdi", "poha", "chowmein", "bread packets"],

#     "locations": ["Chennai", "Bangalore", "Mumbai", "Delhi", "Kolkata", "Hyderabad", "Ahmedabad", "Pune", "Jaipur", "Lucknow", 
#         "Patna", "Bhopal", "Surat", "Nagpur", "Thane", "Visakhapatnam", "Kanpur", "Agra", "Varanasi", "Coimbatore", 
#         "Madurai", "Indore", "Guwahati", "Raipur", "Chandigarh", "Mysore", "Ranchi", "Jodhpur", "Udaipur", "Nashik", 
#         "Gurgaon", "Noida", "Ghaziabad", "Faridabad", "Bhubaneswar", "Dehradun", "Amritsar", "Allahabad", "Meerut", 
#         "Vadodara", "Shimla", "Manali", "Mangalore", "Goa", "Jabalpur", "Tirupati", "Warangal", "Hubli", "Belgaum", 
#         "Kochi", "Thiruvananthapuram", "Aurangabad", "Jamshedpur"],

#     "medicines": ["paracetamol", "antibiotics", "ORS", "painkillers", "bandages", "sanitizer", "aspirin", "ibuprofen", "antiseptic", 
#         "cough syrup", "insulin", "ointment", "antihistamine", "glucose", "vitamins", "saline", "thermometer", "inhaler", 
#         "med kits", "syringe", "hydrocortisone", "antacids", "digene", "pain relief spray", "dettol", "betadine", 
#         "neosporin", "eye drops", "ear drops", "calamine lotion", "disinfectant", "pain balm", "emergency pills", "crepe bandage",
#         "surgical gloves", "face masks", "first aid kits", "hand wash", "antiviral", "anti-fungal", "clotrimazole", 
#         "loperamide", "ORS sachets", "doxycycline", "penicillin", "azithromycin", "amoxicillin"],

#     "diseases": ["fever", "dengue", "malaria", "cholera", "flu", "typhoid", "cold", "infection", "pneumonia", "diarrhea", 
#         "jaundice", "rash", "dehydration", "cough", "headache", "vomiting", "leptospirosis", "skin allergy", "injury", 
#         "fatigue", "heat stroke", "sunburn", "nausea", "arthritis", "tuberculosis", "breathing difficulty", "bronchitis", 
#         "asthma", "sepsis", "measles", "chickenpox", "mumps", "polio", "hepatitis", "heart disease", "diabetes", 
#         "depression", "anemia", "high blood pressure", "low blood pressure", "urinary infection", "paralysis", "gangrene"]
# }

# # --- Text Cleaning ---
# def clean_tweet(tweet):
#     if not isinstance(tweet, str):
#         return ""
#     tweet = re.sub(r'http\S+', '', tweet)
#     tweet = re.sub(r'[^a-zA-Z0-9\s]', '', tweet)
#     tweet = re.sub(r'\s+', ' ', tweet)
#     return tweet.strip()

# # --- Extract Entities with Quantities ---
# def extract_entities(tweet):
#     # Patterns to match quantities like "of water 20ml", "food 2kg", or standalone items like "medicine"
#     patterns = [
#         r'(of\s+(\w+)\s+(\d+\w*))',  # Matches "of water 20ml", "of food 2kg"
#         r'(\b\w+\s+\d+\w*)',         # Matches "food 2kg", "water 20ml"
#         r'\b(' + '|'.join(KEYWORD_DICTIONARIES['food_items'] + KEYWORD_DICTIONARIES['medicines']) + r')\b'  # Matches standalone items like "medicine"
#     ]
    
#     entities = []
#     tweet_lower = tweet.lower()
    
#     # Check for each pattern
#     for pattern in patterns:
#         matches = re.finditer(pattern, tweet_lower)
#         for match in matches:
#             if 'of' in match.group(0):
#                 entities.append(match.group(0))
#             elif any(word in match.group(0) for word in KEYWORD_DICTIONARIES['food_items'] + KEYWORD_DICTIONARIES['medicines']):
#                 # Check if it's a quantity match or standalone item
#                 if re.search(r'\d+\w*', match.group(0)):
#                     entities.append(match.group(0))
#                 else:
#                     entities.append(match.group(0))

#     # Join entities into a single string
#     return ", ".join(set(entities)) if entities else "none"

# # --- NER Extraction with Keyword Matching ---
# def extract_ner_information_with_keywords(tweet):
#     tweet_words = set(tweet.lower().split())

#     food_items = [word for word in KEYWORD_DICTIONARIES['food_items'] if word in tweet_words]
#     locations = [word for word in KEYWORD_DICTIONARIES['locations'] if word.lower() in tweet_words]
#     medicines = [word for word in KEYWORD_DICTIONARIES['medicines'] if word in tweet_words]
#     diseases = [word for word in KEYWORD_DICTIONARIES['diseases'] if word in tweet_words]
    
#     # Extract entities with quantities
#     entities = extract_entities(tweet)

#     return {
#         'Food': list(set(food_items)),
#         'Location': list(set(locations)),
#         'Medicine': list(set(medicines)),
#         'Diseases': list(set(diseases)),
#         'entities': entities
#     }

# # --- Flask App ---
# app = Flask(__name__)
# CORS(app)  # Enable CORS for all routes

# # Load model and vectorizer
# classifier = joblib.load("model.pkl")
# tfidf_vectorizer = joblib.load("vectorizer.pkl")

# @app.route('/predict', methods=['POST'])
# def predict():
#     data = request.get_json()
    
#     tweets = data.get("tweets")
#     if not tweets or not isinstance(tweets, list):
#         return jsonify({"error": "Please provide a list of tweets using the 'tweets' key."}), 400

#     cleaned_tweets = [clean_tweet(tweet) for tweet in tweets]
#     X_tfidf = tfidf_vectorizer.transform(cleaned_tweets)
#     predictions = classifier.predict(X_tfidf)

#     results = []
#     for i, tweet in enumerate(tweets):
#         pred = predictions[i]
#         ner_info = extract_ner_information_with_keywords(tweet)

#         prediction_type = "NA"
#         if pred[3] == 1:  # Shelter Required
#             prediction_type = "need"
#         elif pred[3] == 0 and pred[0] == 1:
#             prediction_type = "available"

#         result = {
#             "tweet": tweet,
#             "predictions": {
#                 "type": prediction_type,
#                 "foodRequirement": int(pred[0]),
#                 "locationIdentified": int(pred[1]),
#                 "medicineRequirement": int(pred[2]),
#                 "shelterRequired": int(pred[3]),
#                 "nerInformation": {
#                     "foodItems": ner_info['Food'],
#                     "locations": ner_info['Location'],
#                     "medicines": ner_info['Medicine'],
#                     "diseases": ner_info['Diseases'],
#                     "entities": ner_info['entities']
#                 }
#             }
#         }
#         results.append(result)

#     return jsonify(results)

# if __name__ == '__main__':
#     app.run(debug=True, port=5000)  # Specify port for consistency

































# -----------------------------------------------------------------------------------------------------------------------------------------





# Entities + Gemini


from flask import Flask, request, jsonify
from flask_cors import CORS  # Import CORS
import re
import joblib
import google.generativeai as genai
import json
import logging

# ----------- SETUP LOGGING -----------
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# ----------- CONFIGURE GEMINI -----------
try:
    genai.configure(api_key="AIzaSyA4vZkUz2uzfiMRy1-JsKHg6a_ctEu5QOM")  # Replace with your actual Gemini API key
except Exception as e:
    logger.error(f"Failed to configure Gemini API: {e}")
    raise

# ----------- LOAD KEYWORDS FOR NER -----------
KEYWORD_DICTIONARIES = {
    "food_items": ["water", "food", "rice", "bread", "milk", "biscuits", "supplies", "oil", "flour", "sugar", "salt", 
                   "dal", "wheat", "noodles", "fruits", "vegetables", "meals", "cereal", "tea", "coffee", "eggs", 
                   "butter", "paneer", "pulses", "fish", "meat", "chicken", "mutton", "ghee", "cheese", "yogurt", 
                   "curd", "juices", "snacks", "potatoes", "onions", "tomatoes", "bananas", "apples", "mangoes", 
                   "oranges", "coconut water", "corn", "chapati", "roti", "paratha", "idli", "dosa", "sambar", 
                   "pulao", "biryani", "khichdi", "poha", "chowmein", "bread packets"],
    
    "locations": ["Chennai", "Bangalore", "Mumbai", "Delhi", "Kolkata", "Hyderabad", "Ahmedabad", "Pune", "Jaipur", 
                  "Lucknow", "Patna", "Bhopal", "Surat", "Nagpur", "Thane", "Visakhapatnam", "Kanpur", "Agra", 
                  "Varanasi", "Coimbatore", "Madurai", "Indore", "Guwahati", "Raipur", "Chandigarh", "Mysore", 
                  "Ranchi", "Jodhpur", "Udaipur", "Nashik", "Gurgaon", "Noida", "Ghaziabad", "Faridabad", 
                  "Bhubaneswar", "Dehradun", "Amritsar", "Allahabad", "Meerut", "Vadodara", "Shimla", "Manali", 
                  "Mangalore", "Goa", "Jabalpur", "Tirupati", "Warangal", "Hubli", "Belgaum", "Kochi", 
                  "Thiruvananthapuram", "Aurangabad", "Jamshedpur"],

    "medicines": ["paracetamol", "antibiotics", "ORS", "painkillers", "bandages", "sanitizer", "aspirin", "ibuprofen", 
                  "antiseptic", "cough syrup", "insulin", "ointment", "antihistamine", "glucose", "vitamins", 
                  "saline", "thermometer", "inhaler", "med kits", "syringe", "hydrocortisone", "antacids", "digene", 
                  "pain relief spray", "dettol", "betadine", "neosporin", "eye drops", "ear drops", "calamine lotion", 
                  "disinfectant", "pain balm", "emergency pills", "crepe bandage", "surgical gloves", "face masks", 
                  "first aid kits", "hand wash", "antiviral", "anti-fungal", "clotrimazole", "loperamide", 
                  "ORS sachets", "doxycycline", "penicillin", "azithromycin", "amoxicillin"],

    "diseases": ["fever", "dengue", "malaria", "cholera", "flu", "typhoid", "cold", "infection", "pneumonia", 
                 "diarrhea", "jaundice", "rash", "dehydration", "cough", "headache", "vomiting", "leptospirosis", 
                 "skin allergy", "injury", "fatigue", "heat stroke", "sunburn", "nausea", "arthritis", 
                 "tuberculosis", "breathing difficulty", "bronchitis", "asthma", "sepsis", "measles", "chickenpox", 
                 "mumps", "polio", "hepatitis", "heart disease", "diabetes", "depression", "anemia", 
                 "high blood pressure", "low blood pressure", "urinary infection", "paralysis", "gangrene"]
}

# ----------- CLEAN TWEET FUNCTION -----------
def clean_tweet(tweet):
    if not isinstance(tweet, str):
        return ""
    tweet = re.sub(r'http\S+', '', tweet)
    tweet = re.sub(r'[^a-zA-Z0-9\s]', '', tweet)
    tweet = re.sub(r'\s+', ' ', tweet)
    return tweet.strip()

# ----------- EXTRACT ENTITIES WITH QUANTITIES -----------
def extract_entities(tweet):
    # Patterns to match quantities like "of water 20ml", "food 2kg", or standalone items like "medicine"
    patterns = [
        r'(of\s+(\w+)\s+(\d+\w*))',  # Matches "of water 20ml", "of food 2kg"
        r'(\b\w+\s+\d+\w*)',         # Matches "food 2kg", "water 20ml"
        r'\b(' + '|'.join(KEYWORD_DICTIONARIES['food_items'] + KEYWORD_DICTIONARIES['medicines']) + r')\b'  # Matches standalone items like "medicine"
    ]
    
    entities = []
    tweet_lower = tweet.lower()
    
    # Check for each pattern
    for pattern in patterns:
        matches = re.finditer(pattern, tweet_lower)
        for match in matches:
            if 'of' in match.group(0):
                entities.append(match.group(0))
            elif any(word in match.group(0) for word in KEYWORD_DICTIONARIES['food_items'] + KEYWORD_DICTIONARIES['medicines']):
                # Check if it's a quantity match or standalone item
                if re.search(r'\d+\w*', match.group(0)):
                    entities.append(match.group(0))
                else:
                    entities.append(match.group(0))

    # Join entities into a single string
    return ", ".join(set(entities)) if entities else "none"

# ----------- NER BASED ON KEYWORDS -----------
def extract_ner_information_with_keywords(tweet):
    tweet_words = set(tweet.lower().split())
    food_items = [word for word in KEYWORD_DICTIONARIES['food_items'] if word in tweet_words]
    locations = [word for word in KEYWORD_DICTIONARIES['locations'] if word.lower() in tweet_words]
    medicines = [word for word in KEYWORD_DICTIONARIES['medicines'] if word in tweet_words]
    diseases = [word for word in KEYWORD_DICTIONARIES['diseases'] if word in tweet_words]
    
    # Extract entities with quantities
    entities = extract_entities(tweet)
    
    return {
        'foodItems': list(set(food_items)),
        'locations': list(set(locations)),
        'medicines': list(set(medicines)),
        'diseases': list(set(diseases)),
        'entities': entities
    }

# ----------- GEMINI API CALL FUNCTION -----------
def ask_gemini(tweets):
    prompt = f"""
You are an AI that classifies disaster-related tweets. For each tweet, return a JSON object with:
- tweet: original tweet text
- predictions:
  - type: "need", "available", or "NA"
  - foodRequirement: 1 or 0
  - locationIdentified: 1 or 0
  - medicineRequirement: 1 or 0
  - shelterRequired: 1 or 0
  - nerInformation:
    - foodItems: list of food words
    - locations: list of cities/places
    - medicines: list of medicines
    - diseases: list of diseases
    - entities: string describing items with quantities (e.g., "of water 20ml, of food 2kg, medicine") for both "need" and "available" types

Input tweets: {json.dumps(tweets)}
Return a JSON array of objects, one per tweet. Output only valid JSON, without markdown or extra text.
"""
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(prompt)
        logger.info("Gemini Raw Response: %s", response.text)

        # Strip markdown or code block markers
        cleaned_response = response.text.strip()
        if cleaned_response.startswith("```json"):
            cleaned_response = cleaned_response[7:-3].strip()

        # Validate and parse JSON
        try:
            result = json.loads(cleaned_response)
            if not isinstance(result, list):
                logger.error("Gemini response is not a JSON array")
                return {"error": "Invalid Gemini response format", "details": "Response is not a JSON array"}
            return result
        except json.JSONDecodeError as e:
            logger.error("JSON parsing error: %s", str(e))
            logger.error("Faulty response: %s", cleaned_response)
            # Fallback to keyword-based NER
            return [
                {
                    "tweet": tweet,
                    "predictions": {
                        "type": "NA",
                        "foodRequirement": 1 if extract_ner_information_with_keywords(tweet)['foodItems'] else 0,
                        "locationIdentified": 1 if extract_ner_information_with_keywords(tweet)['locations'] else 0,
                        "medicineRequirement": 1 if extract_ner_information_with_keywords(tweet)['medicines'] else 0,
                        "shelterRequired": 0,
                        "nerInformation": extract_ner_information_with_keywords(tweet)
                    }
                } for tweet in tweets
            ]
    except Exception as e:
        logger.error("Gemini API error: %s", str(e))
        # Fallback to keyword-based NER
        return [
            {
                "tweet": tweet,
                "predictions": {
                    "type": "NA",
                    "foodRequirement": 1 if extract_ner_information_with_keywords(tweet)['foodItems'] else 0,
                    "locationIdentified": 1 if extract_ner_information_with_keywords(tweet)['locations'] else 0,
                    "medicineRequirement": 1 if extract_ner_information_with_keywords(tweet)['medicines'] else 0,
                    "shelterRequired": 0,
                    "nerInformation": extract_ner_information_with_keywords(tweet)
                }
            } for tweet in tweets
        ]

# ----------- FLASK SETUP -----------
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        tweets = data.get("tweets")
        if not tweets or not isinstance(tweets, list):
            return jsonify({"error": "Please provide a list of tweets using the 'tweets' key."}), 400

        # Gemini Integration
        gemini_response = ask_gemini(tweets)
        return jsonify(gemini_response)
    except Exception as e:
        logger.error("Prediction error: %s", str(e))
        return jsonify({"error": "Internal server error", "details": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)







# ----------------------------------------------------------------------------------------------------------------------------------------




# Gemini + Entities + Twitter API


# from flask import Flask, request, jsonify
# from flask_cors import CORS
# import re
# import joblib
# import google.generativeai as genai
# import json
# import logging
# import requests

# # ----------- SETUP LOGGING -----------
# logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
# logger = logging.getLogger(__name__)

# # ----------- CONFIGURE GEMINI -----------
# try:
#     genai.configure(api_key="AIzaSyA4vZkUz2uzfiMRy1-JsKHg6a_ctEu5QOM")  # Replace with your actual Gemini API key
# except Exception as e:
#     logger.error(f"Failed to configure Gemini API: {e}")
#     raise

# # ----------- LOAD KEYWORDS FOR NER -----------
# KEYWORD_DICTIONARIES = {
#     "food_items": ["water", "food", "rice", "bread", "milk", "biscuits", "supplies", "oil", "flour", "sugar", "salt", 
#                    "dal", "wheat", "noodles", "fruits", "vegetables", "meals", "cereal", "tea", "coffee", "eggs", 
#                    "butter", "paneer", "pulses", "fish", "meat", "chicken", "mutton", "ghee", "cheese", "yogurt", 
#                    "curd", "juices", "snacks", "potatoes", "onions", "tomatoes", "bananas", "apples", "mangoes", 
#                    "oranges", "coconut water", "corn", "chapati", "roti", "paratha", "idli", "dosa", "sambar", 
#                    "pulao", "biryani", "khichdi", "poha", "chowmein", "bread packets"],
    
#     "locations": ["Chennai", "Bangalore", "Mumbai", "Delhi", "Kolkata", "Hyderabad", "Ahmedabad", "Pune", "Jaipur", 
#                   "Lucknow", "Patna", "Bhopal", "Surat", "Nagpur", "Thane", "Visakhapatnam", "Kanpur", "Agra", 
#                   "Varanasi", "Coimbatore", "Madurai", "Indore", "Guwahati", "Raipur", "Chandigarh", "Mysore", 
#                   "Ranchi", "Jodhpur", "Udaipur", "Nashik", "Gurgaon", "Noida", "Ghaziabad", "Faridabad", 
#                   "Bhubaneswar", "Dehradun", "Amritsar", "Allahabad", "Meerut", "Vadodara", "Shimla", "Manali", 
#                   "Mangalore", "Goa", "Jabalpur", "Tirupati", "Warangal", "Hubli", "Belgaum", "Kochi", 
#                   "Thiruvananthapuram", "Aurangabad", "Jamshedpur"],

#     "medicines": ["paracetamol", "antibiotics", "ORS", "painkillers", "bandages", "sanitizer", "aspirin", "ibuprofen", 
#                   "antiseptic", "cough syrup", "insulin", "ointment", "antihistamine", "glucose", "vitamins", 
#                   "saline", "thermometer", "inhaler", "med kits", "syringe", "hydrocortisone", "antacids", "digene", 
#                   "pain relief spray", "dettol", "betadine", "neosporin", "eye drops", "ear drops", "calamine lotion", 
#                   "disinfectant", "pain balm", "emergency pills", "crepe bandage", "surgical gloves", "face masks", 
#                   "first aid kits", "hand wash", "antiviral", "anti-fungal", "clotrimazole", "loperamide", 
#                   "ORS sachets", "doxycycline", "penicillin", "azithromycin", "amoxicillin"],

#     "diseases": ["fever", "dengue", "malaria", "cholera", "flu", "typhoid", "cold", "infection", "pneumonia", 
#                  "diarrhea", "jaundice", "rash", "dehydration", "cough", "headache", "vomiting", "leptospirosis", 
#                  "skin allergy", "injury", "fatigue", "heat stroke", "sunburn", "nausea", "arthritis", 
#                  "tuberculosis", "breathing difficulty", "bronchitis", "asthma", "sepsis", "measles", "chickenpox", 
#                  "mumps", "polio", "hepatitis", "heart disease", "diabetes", "depression", "anemia", 
#                  "high blood pressure", "low blood pressure", "urinary infection", "paralysis", "gangrene"]
# }

# # ----------- CLEAN TWEET FUNCTION -----------
# def clean_tweet(tweet):
#     if not isinstance(tweet, str):
#         return ""
#     tweet = re.sub(r'http\S+', '', tweet)
#     tweet = re.sub(r'[^a-zA-Z0-9\s]', '', tweet)
#     tweet = re.sub(r'\s+', ' ', tweet)
#     return tweet.strip()

# # ----------- EXTRACT ENTITIES WITH QUANTITIES -----------
# def extract_entities(tweet):
#     # Patterns to match quantities like "of water 20ml", "food 2kg", or standalone items like "medicine"
#     patterns = [
#         r'(of\s+(\w+)\s+(\d+\w*))',  # Matches "of water 20ml", "of food 2kg"
#         r'(\b\w+\s+\d+\w*)',         # Matches "food 2kg", "water 20ml"
#         r'\b(' + '|'.join(KEYWORD_DICTIONARIES['food_items'] + KEYWORD_DICTIONARIES['medicines']) + r')\b'  # Matches standalone items like "medicine"
#     ]
    
#     entities = []
#     tweet_lower = tweet.lower()
    
#     # Check for each pattern
#     for pattern in patterns:
#         matches = re.finditer(pattern, tweet_lower)
#         for match in matches:
#             if 'of' in match.group(0):
#                 entities.append(match.group(0))
#             elif any(word in match.group(0) for word in KEYWORD_DICTIONARIES['food_items'] + KEYWORD_DICTIONARIES['medicines']):
#                 # Check if it's a quantity match or standalone item
#                 if re.search(r'\d+\w*', match.group(0)):
#                     entities.append(match.group(0))
#                 else:
#                     entities.append(match.group(0))

#     # Join entities into a single string
#     return ", ".join(set(entities)) if entities else "none"

# # ----------- NER BASED ON KEYWORDS -----------
# def extract_ner_information_with_keywords(tweet):
#     tweet_words = set(tweet.lower().split())
#     food_items = [word for word in KEYWORD_DICTIONARIES['food_items'] if word in tweet_words]
#     locations = [word for word in KEYWORD_DICTIONARIES['locations'] if word.lower() in tweet_words]
#     medicines = [word for word in KEYWORD_DICTIONARIES['medicines'] if word in tweet_words]
#     diseases = [word for word in KEYWORD_DICTIONARIES['diseases'] if word in tweet_words]
    
#     # Extract entities with quantities
#     entities = extract_entities(tweet)
    
#     return {
#         'foodItems': list(set(food_items)),
#         'locations': list(set(locations)),
#         'medicines': list(set(medicines)),
#         'diseases': list(set(diseases)),
#         'entities': entities
#     }

# # ----------- GEMINI API CALL FUNCTION -----------
# def ask_gemini(tweets):
#     prompt = f"""
# You are an AI that classifies disaster-related tweets. For each tweet, return a JSON object with:
# - tweet: original tweet text
# - predictions:
#   - type: "need", "available", or "NA"
#   - foodRequirement: 1 or 0
#   - locationIdentified: 1 or 0
#   - medicineRequirement: 1 or 0
#   - shelterRequired: 1 or 0
#   - nerInformation:
#     - foodItems: list of food words
#     - locations: list of cities/places
#     - medicines: list of medicines
#     - diseases: list of diseases
#     - entities: string describing items with quantities (e.g., "of water 20ml, of food 2kg, medicine") for both "need" and "available" types

# Input tweets: {json.dumps(tweets)}
# Return a JSON array of objects, one per tweet. Output only valid JSON, without markdown or extra text.
# """
#     try:
#         model = genai.GenerativeModel("gemini-1.5-flash")
#         response = model.generate_content(prompt)
#         logger.info("Gemini Raw Response: %s", response.text)

#         # Strip markdown or code block markers
#         cleaned_response = response.text.strip()
#         if cleaned_response.startswith("```json"):
#             cleaned_response = cleaned_response[7:-3].strip()

#         # Validate and parse JSON
#         try:
#             result = json.loads(cleaned_response)
#             if not isinstance(result, list):
#                 logger.error("Gemini response is not a JSON array")
#                 return {"error": "Invalid Gemini response format", "details": "Response is not a JSON array"}
#             return result
#         except json.JSONDecodeError as e:
#             logger.error("JSON parsing error: %s", str(e))
#             logger.error("Faulty response: %s", cleaned_response)
#             # Fallback to keyword-based NER
#             return [
#                 {
#                     "tweet": tweet,
#                     "predictions": {
#                         "type": "NA",
#                         "foodRequirement": 1 if extract_ner_information_with_keywords(tweet)['foodItems'] else 0,
#                         "locationIdentified": 1 if extract_ner_information_with_keywords(tweet)['locations'] else 0,
#                         "medicineRequirement": 1 if extract_ner_information_with_keywords(tweet)['medicines'] else 0,
#                         "shelterRequired": 0,
#                         "nerInformation": extract_ner_information_with_keywords(tweet)
#                     }
#                 } for tweet in tweets
#             ]
#     except Exception as e:
#         logger.error("Gemini API error: %s", str(e))
#         # Fallback to keyword-based NER
#         return [
#             {
#                 "tweet": tweet,
#                 "predictions": {
#                     "type": "NA",
#                     "foodRequirement": 1 if extract_ner_information_with_keywords(tweet)['foodItems'] else 0,
#                     "locationIdentified": 1 if extract_ner_information_with_keywords(tweet)['locations'] else 0,
#                     "medicineRequirement": 1 if extract_ner_information_with_keywords(tweet)['medicines'] else 0,
#                     "shelterRequired": 0,
#                     "nerInformation": extract_ner_information_with_keywords(tweet)
#                 }
#             } for tweet in tweets
#         ]

# # ----------- TWITTER API FUNCTIONS -----------
# # Replace with your actual Twitter Bearer Token
# TWITTER_BEARER_TOKEN = "AAAAAAAAAAAAAAAAAAAAAKoN2gEAAAAAymyh%2FzBhXLnuut%2BfOx%2F6ASAkI4I%3DljinB06kBGsb2rNg927fep8JVARIeQpiYQxQf9Cd2ob3tTaKVb"

# def get_ndrf_user_id():
#     url = "https://api.twitter.com/2/users/by/username/ndrfhq"
#     headers = {
#         "Authorization": f"Bearer {TWITTER_BEARER_TOKEN}"
#     }
#     try:
#         response = requests.get(url, headers=headers)
#         response.raise_for_status()  # Raise an exception for bad status codes
#         data = response.json()
#         if "data" not in data:
#             raise Exception("NDRF user not found")
#         return data["data"]["id"]
#     except requests.exceptions.RequestException as e:
#         logger.error(f"Failed to fetch NDRF user ID: {e}")
#         raise

# def fetch_ndrf_tweets():
#     user_id = get_ndrf_user_id()
#     url = f"https://api.twitter.com/2/users/{user_id}/tweets?tweet.fields=created_at&max_results=10"
#     headers = {
#         "Authorization": f"Bearer {TWITTER_BEARER_TOKEN}"
#     }
#     try:
#         response = requests.get(url, headers=headers)
#         response.raise_for_status()
#         data = response.json()
#         if "data" not in data:
#             raise Exception("No tweets found for NDRF")
#         return [tweet["text"] for tweet in data["data"]]
#     except requests.exceptions.RequestException as e:
#         logger.error(f"Failed to fetch NDRF tweets: {e}")
#         raise

# # ----------- FLASK SETUP -----------
# app = Flask(__name__)
# CORS(app)  # Enable CORS for frontend requests

# @app.route('/predict', methods=['POST'])
# def predict():
#     try:
#         data = request.get_json()
#         tweets = data.get("tweets")
#         if not tweets or not isinstance(tweets, list):
#             return jsonify({"error": "Please provide a list of tweets using the 'tweets' key."}), 400

#         # Gemini Integration
#         gemini_response = ask_gemini(tweets)
#         return jsonify(gemini_response)
#     except Exception as e:
#         logger.error("Prediction error: %s", str(e))
#         return jsonify({"error": "Internal server error", "details": str(e)}), 500

# @app.route('/fetch-ndrf-tweets', methods=['GET'])
# def fetch_and_analyze_tweets():
#     try:
#         # Fetch tweets from NDRF
#         tweets = fetch_ndrf_tweets()
#         logger.info(f"Fetched tweets: {tweets}")

#         # Send tweets to the /predict endpoint
#         predict_response = app.test_client().post(
#             '/predict',
#             json={"tweets": tweets},
#             content_type='application/json'
#         )
#         if predict_response.status_code != 200:
#             raise Exception(f"Failed to analyze tweets: {predict_response.get_json().get('error', 'Unknown error')}")
        
#         return jsonify(predict_response.get_json())
#     except Exception as e:
#         logger.error(f"Error in fetch_and_analyze_tweets: {e}")
#         return jsonify({"error": str(e)}), 500

# if __name__ == '__main__':
#     app.run(debug=True, port=5000)