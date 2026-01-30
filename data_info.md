# Resume Screening Datasets and Types

To train the **Deep Learning (RNN-LSTM)** model, you need a dataset that pairs resumes with target roles or scores.

## 1. Recommended Datasets
- **Kaggle Resume Dataset**: Contains thousands of resumes categorized by job role (e.g., Data Science, HR, Advocate).
- **Hiring Recommender Datasets**: Often contains (Job Description, Resume) pairs with a binary label (Match/No Match).

## 2. Dataset Types & Structure

### A. Classification Dataset (Categorization)
Used to train the LSTM to identify if a resume belongs to a specific department.
- **Input**: Resume Text
- **Label**: Job Category (0: IT, 1: HR, 2: Marketing, etc.)

### B. Similarity Dataset (Matching)
Used to train the model to output a "Match Score".
- **Input 1**: Resume Text (Embeddings)
- **Input 2**: Job Description Text (Embeddings)
- **Label**: Score (0.0 to 1.0)

## 3. NLP Pipeline (Current Implementation)
1. **Embedding (SBERT)**: We use `all-MiniLM-L6-v2` to convert text into a 384-dimensional vector. SBERT is state-of-the-art for capturing semantic meaning.
2. **Sequential Processing (RNN-LSTM)**:
   - For complex resumes, we can split text into sentences.
   - The LSTM processes these sentence embeddings as a sequence to understand the flow and context of the experience.
3. **Similarity Calculation**: In this app, we currently use **Cosine Similarity** between the SBERT embeddings, which is the most reliable "Deep Learning" approach for zero-shot matching.

## 4. Training Tips
- **Classes**: If you use classification, ensure you have at least 100-200 resumes per category.
- **Preprocessing**: Always remove stop words and special characters (implemented in `utils/nlp_processing.py`).
- **Sequence Length**: Keep sequence length consistent (e.g., top 20 lines of a resume).
