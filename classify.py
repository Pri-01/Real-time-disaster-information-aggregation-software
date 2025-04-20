import google.generativeai as genai
import json
import os

# Set your API key here or from environment variable
API_KEY = os.getenv("GEMINI_API_KEY", "Enter_your_key_here")
genai.configure(api_key=API_KEY)

# ------------------- Classification Function -------------------
def classify_tweet_resource(tweet):
    prompt = f"""
    You are an AI that classifies tweets during disaster relief efforts.

    Analyze the following tweet and classify it into one of the following categories:
    - "resource need": if it expresses a request or need (e.g., "need water").
    - "resource available": if it offers help/resources (e.g., "providing shelter").
    - "neither": if it is irrelevant or unclear.

    Return your answer **only** as a plain JSON object, without any explanation or markdown.

    Tweet: "{tweet}"

    Your response should look like this:
    {{
        "classification": "resource need",
        "confidence": 0.92
    }}
    """

    try:
        model = genai.GenerativeModel("models/gemini-1.5-flash-001")
        response = model.generate_content(prompt)

        # Optional debug output
        # print("Raw Gemini Response:", repr(response.text))

        # Extract JSON part from response
        text = response.text.strip()
        json_start = text.find("{")
        json_end = text.rfind("}") + 1
        json_str = text[json_start:json_end]

        result = json.loads(json_str)
        return result

    except (json.JSONDecodeError, AttributeError, Exception) as e:
        print(f"\n Gemini API error: {e}\n")
        return {
            "classification": "neither",
            "confidence": 0.0
        }

# ------------------- Main Loop -------------------
def main():
    print("🔍 Tweet Resource Classifier")
    print("Type a tweet to classify it. Type 'exit' to quit.\n")

    while True:
        tweet = input("> ")
        if tweet.lower() == "exit":
            print("Exiting... Stay safe!")
            break

        if not tweet.strip():
            print("Please enter a valid tweet.")
            continue

        result = classify_tweet_resource(tweet)
        print(f"Classification: {result['classification']} (Confidence: {result['confidence']:.2f})\n")

# ------------------- Run -------------------
if __name__ == "__main__":
    main()
