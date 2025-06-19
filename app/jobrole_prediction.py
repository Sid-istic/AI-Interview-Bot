# jobrole_prediction.py

import nltk
import re
import pickle
import fitz  # PyMuPDF
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

# Download NLTK data (can be skipped after first run)
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

# Initialize
stop_words = set(stopwords.words('english'))
lemmatizer = WordNetLemmatizer()

# Job label list
y_list = [
    'Accountant', 'Advocate', 'Agriculture', 'Apparel', 'Architecture',
    'Arts', 'Automobile', 'Aviation', 'Banking', 'Blockchain', 'BPO',
    'Building and Construction', 'Business Analyst', 'Civil Engineer',
    'Consultant', 'Data Science', 'Database', 'Designing', 'DevOps',
    'Digital Media', 'DotNet Developer', 'Education',
    'Electrical Engineering', 'ETL Developer', 'Finance',
    'Food and Beverages', 'Health and Fitness', 'Human Resources',
    'Information Technology', 'Java Developer', 'Management',
    'Mechanical Engineer', 'Network Security Engineer',
    'Operations Manager', 'PMO', 'Public Relations',
    'Python Developer', 'React Developer', 'Sales', 'SAP Developer',
    'SQL Developer', 'Testing', 'Web Designing'
]

# Path config
MODEL_PATH = r"app/model.pkl"
VEC_PATH = r"app/tfidf_vectorizer.pkl"

def preprocess_text(text):
    text = re.sub(r'[^a-zA-Z ]', ' ', text).lower()
    tokens = word_tokenize(text)
    tokens = [lemmatizer.lemmatize(word) for word in tokens if word not in stop_words]
    return ' '.join(tokens)

def load_model_and_vectorizer():
    with open(MODEL_PATH, 'rb') as f_model, open(VEC_PATH, 'rb') as f_vec:
        model = pickle.load(f_model)
        vectorizer = pickle.load(f_vec)
    return model, vectorizer

def extract_text_from_pdf(file_bytes):
    doc = fitz.open(stream=file_bytes, filetype="pdf")
    text = "\n".join([page.get_text() for page in doc])
    return text

def predict(file_bytes):
    try:
        text = extract_text_from_pdf(file_bytes)
        cleaned = preprocess_text(text)
        model, vectorizer = load_model_and_vectorizer()
        X_new = vectorizer.transform([cleaned])
        pred_index = model.predict(X_new)[0]
        return y_list[pred_index]
    except Exception as e:
        return f"Prediction failed: {e}"
