# Import necessary libraries
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns

# Step 1: Load the data
data = pd.read_csv("data.csv")

# Step 2: Filter the data where FloodFlag = 5
filtered_data = data[data["FloodFlag (4:Non_Flood; 5:Flood)"] == 5]

# Step 3: Map Need Flag to labels and include None for cases where Need Flag is neither 6 nor 7
filtered_data["Label"] = filtered_data["Need Flag"].map({6: 1, 7: 0})

# If 'Need Flag' is neither 6 nor 7, label it as 'None' (2)
filtered_data["Label"].fillna(2, inplace=True)

# Step 4: Verify the distribution of classes (Needed, Available, and None)
class_counts = filtered_data["Label"].value_counts()
print(f"Number of 'Available' tweets (label 0): {class_counts.get(0, 0)}")
print(f"Number of 'Needed' tweets (label 1): {class_counts.get(1, 0)}")
print(f"Number of 'None' tweets (label 2): {class_counts.get(2, 0)}")

# Step 5: Prepare data for training
X = filtered_data["Tweet Text"]  # Tweet text data
y = filtered_data["Label"]  # Labels (Need, Available, None)

# Step 6: Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Step 7: Convert text data to numerical vectors using TF-IDF
vectorizer = TfidfVectorizer(max_features=5000, stop_words="english")
X_train_tfidf = vectorizer.fit_transform(X_train)
X_test_tfidf = vectorizer.transform(X_test)

# Step 8: Train a logistic regression model
classifier = LogisticRegression()
classifier.fit(X_train_tfidf, y_train)

# Step 9: Make predictions on the test set
y_pred = classifier.predict(X_test_tfidf)

# Step 10: Evaluate the model
# Accuracy Score
print("Accuracy:", accuracy_score(y_test, y_pred))

# Detailed Classification Report
print(classification_report(y_test, y_pred))

# Step 11: Confusion Matrix for detailed evaluation
conf_matrix = confusion_matrix(y_test, y_pred)

# Plot Confusion Matrix
plt.figure(figsize=(8, 6))
sns.heatmap(conf_matrix, annot=True, fmt="d", cmap="Blues", xticklabels=["Available", "Needed", "None"], yticklabels=["Available", "Needed", "None"])
plt.xlabel("Predicted Labels")
plt.ylabel("True Labels")
plt.title("Confusion Matrix")
plt.show()

# Step 12: Visualize accuracy for both test and train data
train_accuracy = accuracy_score(y_train, classifier.predict(X_train_tfidf))
test_accuracy = accuracy_score(y_test, y_pred)

# Plot accuracy comparison
plt.bar(["Train Accuracy", "Test Accuracy"], [train_accuracy, test_accuracy], color=["blue", "green"])
plt.ylim(0, 1)
plt.ylabel("Accuracy")
plt.title("Train vs Test Accuracy")
plt.show()

# Step 13: Predict manually for a new tweet
def predict_tweet(tweet):
    # Convert the tweet into the same vectorized format as the training data
    tweet_tfidf = vectorizer.transform([tweet])
    
    # Predict the label (0 = Available, 1 = Needed, 2 = None)
    label = classifier.predict(tweet_tfidf)[0]
    
    # Map the label to the corresponding text
    label_mapping = {0: "Available", 1: "Needed", 2: "None"}
    
    return label_mapping[label]

# Example: Test with a new tweet
new_tweet = "I urgently need food supplies in my area, please help!"
print("Sample tweet 1 : " + new_tweet)
print(f"The tweet is classified as: {predict_tweet(new_tweet)}")
print("\n")

print("-----------------------------------------------------------------------------")
print("\n")
print("\n")
new_tweet2 = "Food is available"
print("Sample tweet 2 :"+ new_tweet2)
print(f"The tweet is classified as: {predict_tweet(new_tweet2)}")

print("\n")
print("-----------------------------------------------------------------------------")
print("\n")
print("\n")

new_tweet3 = "I'm just sharing an update about the situation."
print("Sample tweet 3 :" + new_tweet3)
print(f"The tweet is classified as: {predict_tweet(new_tweet3)}")
