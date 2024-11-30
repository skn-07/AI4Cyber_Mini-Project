import sys
import pickle
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import string

import warnings
warnings.filterwarnings('ignore')

# Load the trained model and vectorizer
with open('C:\\AI4Cyber\\FinalSubmission\\Model\\rf_classifier.pkl', 'rb') as model_file:
    rf_classifier = pickle.load(model_file)

with open('C:\\AI4Cyber\\FinalSubmission\\Model\\tfidf_vectorizer.pkl', 'rb') as vectorizer_file:
    vectorizer = pickle.load(vectorizer_file)

# Initialize stopwords and punctuation
stop_words = set(stopwords.words('english'))
punctuation = set(string.punctuation)

# Preprocess the input script
def preprocess_script(script):
    # Tokenize the script
    tokens = word_tokenize(script)
    # Convert to lowercase
    tokens = [token.lower() for token in tokens]
    # Remove punctuation
    tokens = [token for token in tokens if token not in punctuation]
    # Remove stopwords
    tokens = [token for token in tokens if token not in stop_words]
    # Join tokens back to string
    processed_script = ' '.join(tokens)
    return processed_script

# Function to classify a command and return probabilities
def classify_command(command):
    # Preprocess the command
    processed_command = preprocess_script(command)
    
    # Transform the command using the loaded vectorizer
    command_vector = vectorizer.transform([processed_command])
    
    # Predict using the loaded classifier
    prediction = rf_classifier.predict(command_vector)
    prediction_proba = rf_classifier.predict_proba(command_vector)

    # Return the prediction (1 for malicious, 0 for benign) and probabilities
    return prediction[0], prediction_proba[0]

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python scriptAnalyzer.py \"<PowerShell command>\"")
        sys.exit(1)

    # Get the PowerShell command from the command line arguments
    powershell_command = sys.argv[1]

    # Classify the command
    result, probabilities = classify_command(powershell_command)

    # Print the results
    print(result)  # Prediction: 1 for malicious, 0 for benign
    print(probabilities[1])  # Probability of malicious
    print(probabilities[0])  # Probability of benign