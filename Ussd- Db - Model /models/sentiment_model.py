import torch
from transformers import DistilBertTokenizer, DistilBertForSequenceClassification
from config import MODEL_PATH

# Load model and tokenizer
tokenizer = DistilBertTokenizer.from_pretrained(MODEL_PATH)
model = DistilBertForSequenceClassification.from_pretrained(MODEL_PATH)

def predict_sentiment(text):
    # Tokenize input text
    inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True)
    
    # Forward pass through the model
    with torch.no_grad():
        outputs = model(**inputs)
    
    # Get logits and probabilities
    logits = outputs.logits
    probabilities = torch.softmax(logits, dim=1)
    
    # Get predicted label
    predicted_label = torch.argmax(probabilities, dim=1).item()
    
    return predicted_label
