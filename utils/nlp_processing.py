import re
from sentence_transformers import SentenceTransformer
import torch

# Initialize SBERT model
model = SentenceTransformer('all-MiniLM-L6-v2')

def preprocess_text(text):
    if not text:
        return ""
    text = text.lower()
    # Remove special characters and numbers
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    # Remove extra whitespaces
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def get_embeddings(text):
    clean_text = preprocess_text(text)
    if not clean_text:
        return torch.zeros(384)
    embeddings = model.encode(clean_text, convert_to_tensor=True)
    return embeddings
