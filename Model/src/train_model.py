import os
import pandas as pd
import numpy as np
import re
from transformers import pipeline  # Use HuggingFace Transformers NER pipeline
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.multioutput import MultiOutputClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
import matplotlib.pyplot as plt
import json  # For storing and using keyword dictionaries
import joblib

# --- 1. Keyword Dictionaries (manually extracted from Excel sheet) ---
KEYWORD_DICTIONARIES = {
    "food_items": [
        "water", "food", "rice", "bread", "milk", "biscuits", "supplies", "oil", "flour", "sugar", "salt", "dal", 
        "wheat", "noodles", "fruits", "vegetables", "meals", "cereal", "tea", "coffee", "eggs", "butter", "paneer",
        "pulses", "fish", "meat", "chicken", "mutton", "ghee", "cheese", "yogurt", "curd", "juices", "snacks", "potatoes", 
        "onions", "tomatoes", "bananas", "apples", "mangoes", "oranges", "coconut water", "corn", "chapati", "roti", 
        "paratha", "idli", "dosa", "sambar", "pulao", "biryani", "khichdi", "poha", "chowmein", "bread packets"
    ],
    "locations": [
        "Chennai", "Bangalore", "Mumbai", "Delhi", "Kolkata", "Hyderabad", "Ahmedabad", "Pune", "Jaipur", "Lucknow", 
        "Patna", "Bhopal", "Surat", "Nagpur", "Thane", "Visakhapatnam", "Kanpur", "Agra", "Varanasi", "Coimbatore", 
        "Madurai", "Indore", "Guwahati", "Raipur", "Chandigarh", "Mysore", "Ranchi", "Jodhpur", "Udaipur", "Nashik", 
        "Gurgaon", "Noida", "Ghaziabad", "Faridabad", "Bhubaneswar", "Dehradun", "Amritsar", "Allahabad", "Meerut", 
        "Vadodara", "Shimla", "Manali", "Mangalore", "Goa", "Jabalpur", "Tirupati", "Warangal", "Hubli", "Belgaum", 
        "Kochi", "Thiruvananthapuram", "Lucknow", "Varanasi", "Surat", "Aurangabad", "Jamshedpur"
    ],
    "medicines": [
        "paracetamol", "antibiotics", "ORS", "painkillers", "bandages", "sanitizer", "aspirin", "ibuprofen", "antiseptic", 
        "cough syrup", "insulin", "ointment", "antihistamine", "glucose", "vitamins", "saline", "thermometer", "inhaler", 
        "med kits", "syringe", "hydrocortisone", "antacids", "digene", "pain relief spray", "dettol", "betadine", 
        "neosporin", "eye drops", "ear drops", "calamine lotion", "disinfectant", "pain balm", "emergency pills", "crepe bandage",
        "surgical gloves", "face masks", "first aid kits", "hand wash", "antiviral", "anti-fungal", "clotrimazole", 
        "loperamide", "ORS sachets", "doxycycline", "penicillin", "azithromycin", "amoxicillin"
    ],
    "diseases": [
        "fever", "dengue", "malaria", "cholera", "flu", "typhoid", "cold", "infection", "pneumonia", "diarrhea", 
        "jaundice", "rash", "dehydration", "cough", "headache", "vomiting", "leptospirosis", "skin allergy", "injury", 
        "fatigue", "heat stroke", "sunburn", "nausea", "arthritis", "tuberculosis", "breathing difficulty", "bronchitis", 
        "asthma", "sepsis", "measles", "chickenpox", "mumps", "polio", "hepatitis", "heart disease", "diabetes", 
        "depression", "anemia", "high blood pressure", "low blood pressure", "urinary infection", "paralysis", "gangrene"
    ]
}


# --- 2. Load Data ---
def load_data(file_path):
    try:
        df = pd.read_excel(file_path)
    except Exception as e:
        print(f"Error loading file: {e}")
        return None
    return df

# --- 3. Data Preprocessing ---
def clean_tweet(tweet):
    if not isinstance(tweet, str):
        return ""
    tweet = re.sub(r'http\S+', '', tweet)  # Remove URLs
    tweet = re.sub(r'[^a-zA-Z0-9\s]', '', tweet)  # Remove special characters
    tweet = re.sub(r'\s+', ' ', tweet)  # Remove extra whitespace
    return tweet.strip()

def preprocess_data(df):
    text_columns = ['Tweet Text', 'HashTags', 'Keywords (Needed things(food,water))', 'Keywords (Locations)', 'Keywords (Medicines)', 'Keywords (Diseases)']
    
    for col in text_columns:
        df[col] = df[col].fillna('').astype(str)
        df[col] = df[col].apply(clean_tweet)
    
    df['combined_text'] = df['Tweet Text'] + ' ' + df['HashTags'] + ' ' + df['Keywords (Needed things(food,water))'] + ' ' + \
                          df['Keywords (Locations)'] + ' ' + df['Keywords (Medicines)'] + ' ' + df['Keywords (Diseases)']
    return df

# --- 4. Model Training ---
def train_model(X, y):
    tfidf_vectorizer = TfidfVectorizer(max_features=5000)
    X_tfidf = tfidf_vectorizer.fit_transform(X)
    
    X_train, X_test, y_train, y_test = train_test_split(X_tfidf, y, test_size=0.2, random_state=42)
    
    classifier = MultiOutputClassifier(LogisticRegression(max_iter=1000))
    classifier.fit(X_train, y_train)
    
    y_pred = classifier.predict(X_test)
    for i, col in enumerate(y.columns):
        print(f"Classification Report for {col}:")
        print(classification_report(y_test.iloc[:, i], y_pred[:, i]))
    
    visualize_results(y_test, y_pred, y.columns)
    
    return classifier, tfidf_vectorizer, X_test, y_test, y_pred

# --- 5. Custom NER Function with Keyword Matching ---
def extract_ner_information_with_keywords(tweet):
    tweet_words = set(tweet.lower().split())
    
    food_items = [word for word in KEYWORD_DICTIONARIES['food_items'] if word in tweet_words]
    locations = [word for word in KEYWORD_DICTIONARIES['locations'] if word in tweet_words]
    medicines = [word for word in KEYWORD_DICTIONARIES['medicines'] if word in tweet_words]
    diseases = [word for word in KEYWORD_DICTIONARIES['diseases'] if word in tweet_words]
    
    return {
        'Food': list(set(food_items)),
        'Location': list(set(locations)),
        'Medicine': list(set(medicines)),
        'Diseases': list(set(diseases))
    }

# --- 6. Test Custom Tweets with NER ---
def test_random_tweets_with_ner(classifier, tfidf_vectorizer, tweets):
    cleaned_tweets = [clean_tweet(tweet) for tweet in tweets]
    X_tfidf = tfidf_vectorizer.transform(cleaned_tweets)
    predictions = classifier.predict(X_tfidf)
    
    for i, tweet in enumerate(tweets):
        print("\nInput Tweet:", tweet)
        print("Predicted Categories:")
        print(f"Food Requirement: {predictions[i][0]}")
        print(f"Location Identified: {predictions[i][1]}")
        print(f"Medicine Requirement: {predictions[i][2]}")
        print(f"Shelter Required: {predictions[i][3]}")
        
        ner_info = extract_ner_information_with_keywords(tweet)
        print("\nExtracted NER Information:")
        print(f"Food Items: {ner_info['Food']}")
        print(f"Locations: {ner_info['Location']}")
        print(f"Medicines: {ner_info['Medicine']}")
        print(f"Diseases: {ner_info['Diseases']}")

# --- 7. Visualization of Results ---
def visualize_results(y_test, y_pred, target_columns):
    for i, col in enumerate(target_columns):
        true_values = y_test.iloc[:, i].value_counts()
        predicted_values = pd.Series(y_pred[:, i]).value_counts()
        
        plt.figure(figsize=(10, 5))
        true_values.plot(kind='bar', color='skyblue', label='True Values', width=0.3, position=1)
        predicted_values.plot(kind='bar', color='salmon', label='Predicted Values', width=0.3, position=0)
        
        plt.title(f'True vs Predicted Counts for {col}')
        plt.xlabel('Class Labels')
        plt.ylabel('Counts')
        plt.legend()
        plt.show()

# --- 8. Main Function ---
def main():
    #Give the path for your data.xlsx file here - 
    file_path = r'C:\Users\RITIK RAJ PRASAD\OneDrive\Desktop\Grp-42_Disaster_Info_Aggregator\Data\Tweet_Disaster.xlsx'
    df = load_data(file_path)
    if df is None:
        print("Failed to load data. Exiting...")
        return
    
    df = preprocess_data(df)
    
    target_columns = ['Flag (0:Non_Eng; 1:Eng)', 'IndFlag (2:Non_Ind; 3:Ind/Ban/Sri)', 'FloodFlag (4:Non_Flood; 5:Flood)', 
                      'Need Flag (6:Supply required, 7:suppy material available)']
    
    for col in target_columns:
        df[col] = df[col].fillna(0).astype(int)
    
    X = df['combined_text']
    y = df[target_columns]
    
    classifier, tfidf_vectorizer, X_test, y_test, y_pred = train_model(X, y)
    joblib.dump(classifier, 'model.pkl')
    joblib.dump(tfidf_vectorizer, 'vectorizer.pkl')
    
    test_tweets = [
        "Urgent requirement for water and food in Chennai",
        "People are stuck at location Bangalore and need shelter urgently",
        "Send paracetamol and antibiotics to Mumbai urgently",
        "Outbreak of dengue in Hyderabad due to flood situation"
    ]
    test_random_tweets_with_ner(classifier, tfidf_vectorizer, test_tweets)

if __name__ == "__main__":
    main()
