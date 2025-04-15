# Disaster Tweet Analysis

This repository contains a comprehensive Python-based project designed to analyze disaster-related tweets for extracting critical information such as food requirements, geographic locations, medical needs, and prevalent diseases. The project leverages natural language processing (NLP) techniques and machine learning to classify tweets, identify key entities, and provide actionable insights for disaster response and management. The codebase is structured to be modular, extensible, and reusable, making it suitable for researchers, data scientists, and disaster response teams.

## Project Structure
![Screenshot 2025-04-15 204719](https://github.com/user-attachments/assets/f926b25b-928f-451d-869c-6818ad681156)


The repository is organized as follows:

- **`Draft1/`**:
  - A directory for draft or experimental files that may contain early versions or prototypes of the code. This is optional and can be ignored if not in use.

- **`data/`**: (To be added by the respective developer - create a data folder and keep the file `Tweet_Disaster.xlsx` inside it as shown in the project structure)
  - Contains the dataset used for training and testing the model.
  - **`Tweet_Disaster.xlsx`**: The primary Excel file containing tweet data with columns such as `Tweet Text`, `HashTags`, `Keywords (Needed things(food,water))`, `Keywords (Locations)`, `Keywords (Medicines)`, `Keywords (Diseases)`, and target flags (e.g., `Flag`, `IndFlag`, `FloodFlag`, `Need Flag`). This file is excluded from version control due to potential sensitivity and size.

- **`src/`**:
  - The source code directory housing the main scripts.
  - **`train_model.py`**: The core script responsible for loading the dataset, preprocessing text, training a machine learning model (MultiOutputClassifier with LogisticRegression), evaluating its performance, and testing it on sample tweets. (Paste the path for your `Tweet_Disaster.xlsx` file in the required line (153) (obviously removing the - ${}) as shown in this image -

     ![Screenshot 2025-04-16 004109](https://github.com/user-attachments/assets/b8296d3a-a392-47c8-b7aa-3160eea51c58) )

  - **`visualize.py`**: A script dedicated to generating and displaying visualizations (e.g., bar plots comparing true vs. predicted counts for each target category).
  - **`.gitignore`**: A configuration file specifying files and directories to exclude from Git version control, such as sensitive data, virtual environments, and temporary files.

- **`README.md`**:
  - This file, providing an overview of the project, installation instructions, usage guidelines, and additional notes.

- **`requirements.txt`**:
  - A text file listing all Python dependencies required to run the project, generated using `pip freeze > requirements.txt`.

## Project Overview

The `train_model.py` script serves as the main entry point, integrating several key functionalities:

### **Key Features**
1. **Data Loading and Preprocessing**:
   - Loads the `Tweet_Disaster.xlsx` file into a pandas DataFrame.
   - Cleans tweet text by removing URLs, special characters, and extra whitespace, and combines relevant columns (e.g., `Tweet Text`, `HashTags`, `Keywords`) into a single `combined_text` column for model input.

2. **Keyword-Based Named Entity Recognition (NER)**:
   - Uses predefined dictionaries (`KEYWORD_DICTIONARIES`) containing lists of food items, locations, medicines, and diseases to extract entities from tweets.
   - Example dictionaries include:
     - **Food Items**: "water", "rice", "bread", etc.
     - **Locations**: "Chennai", "Mumbai", "Bangalore", etc.
     - **Medicines**: "paracetamol", "antibiotics", "ORS", etc.
     - **Diseases**: "dengue", "malaria", "fever", etc.

3. **Machine Learning Model**:
   - Employs a `MultiOutputClassifier` with `LogisticRegression` as the base estimator to predict multiple binary targets:
     - `Flag (0:Non_Eng; 1:Eng)`: Indicates if the tweet is in English.
     - `IndFlag (2:Non_Ind; 3:Ind/Ban/Sri)`: Indicates if the tweet is from India, Bangladesh, or Sri Lanka.
     - `FloodFlag (4:Non_Flood; 5:Flood)`: Indicates if the tweet is flood-related.
     - `Need Flag (6:Supply required; 7:supply material available)`: Indicates supply needs or availability.
   - Converts text data into TF-IDF features using `TfidfVectorizer` with a maximum of 5000 features.

4. **Model Training and Evaluation**:
   - Splits the dataset into 80% training and 20% testing sets.
   - Trains the model and prints a `classification_report` for each target column to assess precision, recall, and F1-score.
   - Visualizes results using `matplotlib` to compare true vs. predicted counts.

5. **Testing and Entity Extraction**:
   - Tests the model on a set of sample tweets (e.g., "Urgent requirement for water and food in Chennai").
   - Extracts entities using the custom NER function and displays predictions alongside extracted information.

6. **Visualization**:
   - Generates bar plots for each target category, showing the distribution of true and predicted values.

### **Use Case**
This project can be deployed by disaster response teams to monitor social media (e.g., Twitter/X) in real-time, automatically identify urgent needs (e.g., "Chennai needs water and paracetamol"), and prioritize aid delivery based on the extracted data.

## Prerequisites

- **Python**: Version 3.7 or higher.
- **Required Libraries**: Listed in `requirements.txt`, including:
  - `pandas` for data manipulation.
  - `numpy` for numerical operations.
  - `scikit-learn` for machine learning and text vectorization.
  - `transformers` (HuggingFace) for potential future NER enhancements (currently unused).
  - `matplotlib` for visualization.
  - `re` for text preprocessing.

## Installation guide - 

- Clone the repo using - "git clone `<repo-url>`"
- Change directory to the file using - "cd `<repo-name>`"
- Create a virtual environment using the following scripts - 
  - Install virtualenv if not already installed
    - "pip install virtualenv"

  - Create and activate virtual environment
    - "virtualenv venv"

    - Windows:
      - "venv\Scripts\activate"

    - macOS/Linux:
      - "source venv/bin/activate"

- Install Dependencies - 
  - "pip install -r requirements.txt"
- Go to the train_model file and run it or use - 
  - "python src/train_model.py"
