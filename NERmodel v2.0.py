import google.generativeai as genai
import json
import os

# Configure the API key securely using an environment variable
API_KEY = os.getenv("GEMINI_API_KEY", "Enter_your_key_here")  # Replace fallback with your key if not using env
genai.configure(api_key=API_KEY)

# Your existing KEYWORD_DICTIONARIES
KEYWORD_DICTIONARIES = {
    "food_items": [
        "water", "food", "rice", "bread", "milk", "biscuits", "supplies", "oil", "flour", "sugar", "salt", "dal", 
        "wheat", "noodles", "fruits", "vegetables", "meals", "cereal", "tea", "coffee", "eggs", "butter", "paneer",
        "pulses", "fish", "meat", "chicken", "mutton", "ghee", "cheese", "yogurt", "curd", "juices", "snacks", "potatoes", 
        "onions", "tomatoes", "bananas", "apples", "mangoes", "oranges", "coconut water", "corn", "chapati", "roti", 
        "paratha", "idli", "dosa", "sambar", "pulao", "biryani", "khichdi", "poha", "chowmein", "bread packets",
        # Grains & Staples
        "quinoa", "barley", "oats", "ragi", "jowar", "bajra", "semolina (sooji)", "vermicelli", "couscous", "pasta", 
        "macaroni", "spaghetti", "basmati rice", "brown rice", "red rice", "puffed rice", "beaten rice (poha)", 
        # Dairy & Alternatives
        "condensed milk", "evaporated milk", "almond milk", "soy milk", "cottage cheese", "mozzarella", "cream", 
        "whipped cream", "buttermilk", "lassi", "kefir", 
        # Meat & Seafood
        "pork", "bacon", "sausages", "salami", "ham", "turkey", "duck", "lobster", "prawns", "shrimp", "crabs", 
        "squid", "oysters", "clams", "mussels", 
        #  Fruits (Additional)
        "grapes", "pears", "peaches", "plums", "kiwi", "pineapple", "watermelon", "muskmelon", "guava", "papaya", 
        "pomegranate", "strawberries", "blueberries", "raspberries", "blackberries", "cherries", "lychee", "dragon fruit", 
        # Vegetables (Additional)
        "carrots", "cauliflower", "cabbage", "brinjal", "ladyfinger", "beans", "peas", "capsicum", "bell peppers", 
        "zucchini", "pumpkin", "cucumber", "beetroot", "radish", "spinach", "fenugreek leaves", "coriander leaves", 
        "mint leaves", "spring onions", "garlic", "ginger", 
        # Ready-to-Eat & Packaged
        "granola bars", "energy bars", "protein bars", "popcorn", "chips", "nachos", "crackers", "cake", "pastries", 
        "croissants", "donuts", "muffins", "cookies", "chocolates", "candy", "gum", 
        # Indian Cuisine Specials
        "vada", "upma", "uthappam", "pongal", "bisi bele bath", "rasam", "kadhi", "dal tadka", "rajma", "chole", 
        "matar paneer", "palak paneer", "butter chicken", "tandoori chicken", "seekh kebab", "samosa", "kachori", 
        "pakora", "vada pav", "pav bhaji", "misal pav", "dhokla", "khandvi", "thepla", "undhiyu", 
        # Beverages
        "green tea", "herbal tea", "black tea", "hot chocolate", "milkshakes", "smoothies", "soda", "lemonade", 
        "iced tea", "energy drinks", "sports drinks", 
        # Cooking Essentials
        "vinegar", "soy sauce", "mustard sauce", "ketchup", "mayonnaise", "salsa", "hummus", "peanut butter", 
        "jam", "honey", "maple syrup", "chocolate syrup", "food coloring", "vanilla extract", 
        # Frozen Foods
        "ice cream", "frozen yogurt", "frozen vegetables", "frozen fruits", "frozen meals", "frozen parathas", 
        # Dry Fruits & Nuts
        "almonds", "cashews", "walnuts", "pistachios", "raisins", "dates", "figs", "prunes", "sunflower seeds", 
        "pumpkin seeds", "chia seeds", "flax seeds", 
        # Miscellaneous
        "pickles", "chutneys", "papad", "namkeen", "mixture", "sev", "bhujia", "sauerkraut", "kimchi", "olives", 
        "capers", "sprouts", "tofu", "tempeh", "soy chunks",
        # Long Shelf-Life Staples
        "canned beans", "canned vegetables", "canned fruits", "canned tuna", "canned chicken", "canned soup", 
        "canned tomatoes", "canned coconut milk", "instant noodles", "ramen packets", "dehydrated meals", 
        "freeze-dried fruits", "powdered milk", "protein powder", "meal replacement shakes", "peanut butter jars", 
        "nut butters", "trail mix", "beef jerky", "dry sausages", "hardtack biscuits", "pemmican", 
        # Dry Goods
        "lentils", "split peas", "chickpeas", "instant mashed potatoes", "dehydrated onion/garlic", "bouillon cubes", 
        "dry soup mixes", "instant coffee packets", "tea bags", "powdered juice mixes", "electrolyte powder", 
        # Preserved Items
        "honey (unprocessed)", "jams/preserves", "pickled vegetables", "salted nuts", "sun-dried tomatoes", 
        "dried mushrooms", "instant pancake mix", "crackers (sealed packs)", "rice cakes", "fortified cereal", 
        # Emergency Specific
        "MREs (Meals Ready-to-Eat)", "emergency ration bars", "water purification tablets", "high-energy biscuits", 
        "space food packets", "survival food buckets", 
        # Shelf-Stable Proteins
        "sardines in oil", "SPAM", "corned beef", "textured vegetable protein (TVP)", "soybean chunks", 
        "quinoa flakes", "chia seeds", "flaxseeds", 
        # Infant/Elderly Specific
        "baby formula", "instant oatmeal", "rice cereal", "ensure drinks", "pedialyte packets"
    ],
    "locations": [
        "Chennai", "Bangalore", "Mumbai", "Delhi", "Kolkata", "Hyderabad", "Ahmedabad", "Pune", "Jaipur", "Lucknow", 
        "Patna", "Bhopal", "Surat", "Nagpur", "Thane", "Visakhapatnam", "Kanpur", "Agra", "Varanasi", "Coimbatore", 
        "Madurai", "Indore", "Guwahati", "Raipur", "Chandigarh", "Mysore", "Ranchi", "Jodhpur", "Udaipur", "Nashik", 
        "Gurgaon", "Noida", "Ghaziabad", "Faridabad", "Bhubaneswar", "Dehradun", "Amritsar", "Allahabad", "Meerut", 
        "Vadodara", "Shimla", "Manali", "Mangalore", "Goa", "Jabalpur", "Tirupati", "Warangal", "Hubli", "Belgaum", 
        "Kochi", "Thiruvananthapuram", "Lucknow", "Varanasi", "Surat", "Aurangabad", "Jamshedpur",
        # Major Cities (Additional)
        "Gurugram", "Navi Mumbai", "Greater Noida", "Howrah", "Kalyan", "Vasai-Virar", "Pimpri-Chinchwad", "Guntur", "Rajkot", "Jalandhar",
        "Bareilly", "Moradabad", "Aligarh", "Gorakhpur", "Bhiwandi", "Saharanpur", "Guntur", "Bikaner", "Amravati", "Bhilai",
        "Bhavnagar", "Nanded", "Kolhapur", "Bathinda", "Rohtak", "Karnal", "Hisar", "Panipat", "Darbhanga", "Muzaffarpur",
        # State Capitals (Missing)
        "Dispur", "Gangtok", "Kohima", "Imphal", "Aizawl", "Agartala", "Shillong", "Itanagar", "Panaji", "Kavaratti",
        # Union Territories
        "Puducherry", "Karaikal", "Mahe", "Yanam", "Daman", "Diu", "Silvassa", "Port Blair",
        # Popular Tourist Destinations
        "Ooty", "Darjeeling", "Shillong", "Leh", "Ladakh", "Rishikesh", "Haridwar", "Ayodhya", "Mathura", "Dwarka",
        "Puri", "Konark", "Khajuraho", "Hampi", "Mahabalipuram", "Pondicherry", "Kodaikanal", "Munnar", "Kanyakumari",
        # Emerging Cities
        "Tiruchirappalli", "Salem", "Erode", "Tirunelveli", "Kottayam", "Palakkad", "Malappuram", "Kozhikode", "Thrissur", "Kollam",
        # Industrial/IT Hubs
        "Bhilwara", "Korba", "Bokaro", "Angul", "Jharsuguda", "Haldia", "Kakinada", "Anantapur", "Kurnool", "Nellore",
        # North-East Special
        "Dimapur", "Kohima", "Aizawl", "Agartala", "Shillong", "Tawang", "Bomdila", "Ziro", "Majuli", "Haflong",
        # Union Territory Districts
        "New Delhi", "Central Delhi", "East Delhi", "North Delhi", "South Delhi", "West Delhi", "North East Delhi", "North West Delhi", "Shahdara", "South East Delhi"
    ],
    "medicines": [
        "paracetamol", "antibiotics", "ORS", "painkillers", "bandages", "sanitizer", "aspirin", "ibuprofen", "antiseptic", 
        "cough syrup", "insulin", "ointment", "antihistamine", "glucose", "vitamins", "saline", "thermometer", "inhaler", 
        "med kits", "syringe", "hydrocortisone", "antacids", "digene", "pain relief spray", "dettol", "betadine", 
        "neosporin", "eye drops", "ear drops", "calamine lotion", "disinfectant", "pain balm", "emergency pills", "crepe bandage",
        "surgical gloves", "face masks", "first aid kits", "hand wash", "antiviral", "anti-fungal", "clotrimazole", 
        "loperamide", "ORS sachets", "doxycycline", "penicillin", "azithromycin", "amoxicillin",
        "naproxen", "diclofenac", "acetaminophen", "tramadol", "codeine", "morphine", "oxycodone",  
        "cephalexin", "ciprofloxacin", "levofloxacin", "metronidazole", "clindamycin", "vancomycin", "gentamicin",  
        "omeprazole", "ranitidine", "lansoprazole", "simethicone", "bisacodyl", "lactulose", "ondansetron",  
        "loratadine", "cetirizine", "fexofenadine", "montelukast", "salbutamol", "fluticasone", "budesonide",  
        "metformin", "glimepiride", "liraglutide", "levothyroxine", "prednisone", "hydrocortisone",  
        "atorvastatin", "simvastatin", "amlodipine", "losartan", "metoprolol", "warfarin", "clopidogrel",  
        "sertraline", "fluoxetine", "escitalopram", "venlafaxine", "diazepam", "alprazolam",  
        "miconazole", "terbinafine", "ketoconazole", "hydrocortisone cream", "benzoyl peroxide", "salicylic acid",  
        "ferrous sulfate (iron)", "folic acid", "vitamin D", "calcium carbonate", "dextromethorphan (cough suppressant)",  
        "guaifenesin (expectorant)", "activated charcoal", "epinephrine auto-injector", "permethrin (scabies)",  
        "gauze pads", "adhesive tape", "splints", "crutches", "nebulizer", "blood pressure monitor", "sterile needles"  
    ],
    "diseases": [
        # General
        "fever", "dengue", "malaria", "cholera", "flu", "typhoid", "cold", "infection", "pneumonia", "diarrhea", 
        "jaundice", "rash", "dehydration", "cough", "headache", "vomiting", "leptospirosis", "skin allergy", "injury", 
        "fatigue", "heat stroke", "sunburn", "nausea", "arthritis", "tuberculosis", "breathing difficulty", "bronchitis", 
        "asthma", "sepsis", "measles", "chickenpox", "mumps", "polio", "hepatitis", "heart disease", "diabetes", 
        "depression", "anemia", "high blood pressure", "low blood pressure", "urinary infection", "paralysis", "gangrene",
        # Infectious Diseases  
        "COVID-19", "influenza (flu)", "common cold", "tuberculosis", "HIV/AIDS", "hepatitis A", "hepatitis B", "hepatitis C",  
        "malaria", "dengue fever", "yellow fever", "Zika virus", "Ebola", "cholera", "typhoid fever", "measles", "mumps",  
        "rubella", "chickenpox", "shingles", "polio", "rabies", "tetanus", "whooping cough (pertussis)", "diphtheria",  
        "leprosy", "Lyme disease", "syphilis", "gonorrhea", "chlamydia", "herpes simplex", "human papillomavirus (HPV)",  
        "meningitis", "encephalitis", "pneumonia", "strep throat", "urinary tract infection (UTI)", "sepsis",  
        "gastroenteritis (stomach flu)", "norovirus", "rotavirus", "leptospirosis", "schistosomiasis", "filariasis",  
        # Chronic & Non-Communicable Diseases  
        "diabetes (type 1)", "diabetes (type 2)", "hypertension (high blood pressure)", "hypotension (low blood pressure)",  
        "coronary artery disease", "heart attack", "stroke", "heart failure", "arrhythmia", "atherosclerosis",  
        "asthma", "chronic obstructive pulmonary disease (COPD)", "bronchitis", "emphysema", "cystic fibrosis",  
        "Alzheimer disease", "Parkinson disease", "multiple sclerosis", "epilepsy", "migraine", "autism spectrum disorder",  
        "attention deficit hyperactivity disorder (ADHD)", "schizophrenia", "bipolar disorder", "major depressive disorder",  
        "anxiety disorder", "obsessive-compulsive disorder (OCD)", "post-traumatic stress disorder (PTSD)",  
        "osteoporosis", "arthritis (osteoarthritis)", "rheumatoid arthritis", "gout", "lupus", "fibromyalgia",  
        "chronic kidney disease", "kidney stones", "cirrhosis", "irritable bowel syndrome (IBS)", "Crohn disease",  
        "ulcerative colitis", "celiac disease", "peptic ulcer", "gallstones", "pancreatitis",  
        # Cancers  
        "lung cancer", "breast cancer", "prostate cancer", "colorectal cancer", "skin cancer (melanoma)", "leukemia",  
        "lymphoma (Hodgkin and non-Hodgkin)", "brain tumor", "liver cancer", "pancreatic cancer", "ovarian cancer",  
        "cervical cancer", "bladder cancer", "thyroid cancer",  
        # Rare & Genetic Disorders  
        "sickle cell anemia", "thalassemia", "hemophilia", "cystic fibrosis", "Huntington disease", "muscular dystrophy",  
        "Down syndrome", "Turner syndrome", "Klinefelter syndrome", "Tay-Sachs disease", "phenylketonuria (PKU)",  
        # Other Conditions  
        "anemia", "dehydration", "malnutrition", "obesity", "eating disorders (anorexia, bulimia)", "insomnia",  
        "sleep apnea", "vertigo", "tinnitus", "cataracts", "glaucoma", "macular degeneration", "conjunctivitis (pink eye)",  
        "deafness", "sinusitis", "tonsillitis", "appendicitis", "hemorrhoids", "endometriosis", "polycystic ovary syndrome (PCOS)",  
        "erectile dysfunction", "infertility", "menopause", "benign prostatic hyperplasia (BPH)",  
        # Injuries & Environmental Conditions  
        "concussion", "fracture", "sprain", "burn", "heat stroke", "hypothermia", "frostbite", "sunburn", "poisoning",  
        "allergic reaction", "anaphylaxis", "food poisoning", "radiation sickness" 
    ]
}

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
    tweet = "I have a fever and I need paracetamol, Norflox, ibuprofen, amoxicillin, azithromycin, atenolol, and metformin. I live in Chennai and I want some rice."
    extracted_info = extract_ner_information_with_keywords(tweet)
    print(json.dumps(extracted_info, indent=4))

    