import torch
import os
from utils.nlp_processing import get_embeddings
from torch.nn.functional import cosine_similarity
from models.lstm_model import ResumeLSTM

# Initialize and load the LSTM model if it exists
MODEL_PATH = 'models/resume_lstm.pth'
input_size = 384
hidden_size = 128
num_layers = 2
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

model = ResumeLSTM(input_size, hidden_size, num_layers).to(device)
if os.path.exists(MODEL_PATH):
    model.load_state_dict(torch.load(MODEL_PATH, map_location=device, weights_only=True))
    model.eval()

def screen_resume(resume_text, jd_text):
    """
    Takes resume and JD text, generates SBERT embeddings, 
    and predicts match score using the RNN-LSTM model.
    """
    if not jd_text or not resume_text:
        return 0, "Missing resume or job description text."

    # 1. Get SBERT Embeddings (Deep NLP)
    resume_emb = get_embeddings(resume_text).to(device)
    jd_emb = get_embeddings(jd_text).to(device)
    
    # 2. Calculate Cosine Similarity for Semantic Baseline
    similarity = cosine_similarity(resume_emb.unsqueeze(0), jd_emb.unsqueeze(0))
    base_score = similarity.item()
    
    # 3. Use RNN-LSTM for Refined Prediction (Deep Learning)
    # The LSTM expects (batch, seq, feature)
    # We combine/process the interaction between resume and JD
    # In this logic, we pass the difference/relation or simply the resume context
    with torch.no_grad():
        lstm_input = resume_emb.unsqueeze(0).unsqueeze(0) # (1, 1, 384)
        lstm_prediction = model(lstm_input).item()
    
    # Combined score (Hybrid approach: 70% Semantic Similarity + 30% DL Pattern)
    final_score = int((base_score * 0.7 + lstm_prediction * 0.3) * 100)
    
    # Ensure score is within 0-100 range and normalize
    final_score = max(5, min(98, final_score))
    
    feedback = "Good match in technical skills. Consider adding more project-specific details."
    if final_score > 85:
        feedback = "Excellent fit! Your profile matches the core technical requirements and seniority level."
    elif final_score < 60:
        feedback = "The profile lacks some core technologies required. Focus on the specific stack mentioned."
        
    return final_score, feedback
