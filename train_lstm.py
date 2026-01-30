import torch
import torch.nn as nn
import torch.optim as optim
from models.lstm_model import ResumeLSTM
import numpy as np

# This is a demonstration script for training the RNN-LSTM model
def train_demo():
    # 1. Hyperparameters
    input_size = 384  # SBERT embedding size
    hidden_size = 128
    num_layers = 2
    learning_rate = 0.001
    num_epochs = 10

    # 2. Initialize Model, Loss, and Optimizer
    model = ResumeLSTM(input_size, hidden_size, num_layers)
    criterion = nn.BCELoss() # Binary Cross Entropy for match/no-match
    optimizer = optim.Adam(model.parameters(), lr=learning_rate)

    # 3. Dummy Data (Representing processed SBERT embeddings)
    # Shape: (batch_size, sequence_length, input_size)
    # We'll simulate 10 resumes, each with 1 combined embedding
    dummy_inputs = torch.randn(10, 1, input_size) 
    dummy_labels = torch.randint(0, 2, (10, 1)).float()

    print("Starting Demo Training...")
    for epoch in range(num_epochs):
        # Forward pass
        outputs = model(dummy_inputs)
        loss = criterion(outputs, dummy_labels)
        
        # Backward and optimize
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        
        if (epoch+1) % 2 == 0:
            print(f'Epoch [{epoch+1}/{num_epochs}], Loss: {loss.item():.4f}')

    # 4. Save the trained model
    torch.save(model.state_dict(), 'models/resume_lstm.pth')
    print("Model saved to models/resume_lstm.pth")

if __name__ == "__main__":
    train_demo()
