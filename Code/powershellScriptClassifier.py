import streamlit as st
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import string

# Load the saved model and vectorizer
with open('C:\AI4Cyber\FinalSubmission\Model\\rf_classifier.pkl', 'rb') as model_file:
    rf_classifier = pickle.load(model_file)

with open('C:\AI4Cyber\FinalSubmission\Model\\tfidf_vectorizer.pkl', 'rb') as vectorizer_file:
    vectorizer = pickle.load(vectorizer_file)

# Initialize NLTK stopwords and punctuation
stop_words = set(stopwords.words('english'))
punctuation = set(string.punctuation)

# Preprocessing function
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

# Streamlit app
st.title("PowerShell Script Classification")
st.write("Upload a PowerShell script (.ps1 file) to check if it is malicious or benign.")

# File uploader
uploaded_file = st.file_uploader("Choose a .ps1 file", type=['ps1'])

if uploaded_file is not None:
    # Read the file
    script_content = uploaded_file.read().decode('utf-8')

    # Display the script content
    st.subheader("Uploaded Script Content:")
    st.text_area("Script Content", script_content, height=200)

    # Preprocess the script
    processed_script = preprocess_script(script_content)

    # Transform using TF-IDF vectorizer
    script_vector = vectorizer.transform([processed_script])

    # Make prediction
    prediction = rf_classifier.predict(script_vector)[0]
    prediction_proba = rf_classifier.predict_proba(script_vector)

    # Display the result
    st.subheader("Classification Result:")
    if prediction == 1:
        st.error("The script is classified as **Malicious**.")
    else:
        st.success("The script is classified as **Benign**.")

    # Show prediction probabilities
    st.write("Prediction Probabilities:")
    st.write(f"Benign: {prediction_proba[0][0]:.4f}")
    st.write(f"Malicious: {prediction_proba[0][1]:.4f}")