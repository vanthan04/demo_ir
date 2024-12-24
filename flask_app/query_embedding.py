from transformers import AutoTokenizer, AutoModel
import torch
import torch.nn.functional as F


# Mean Pooling - Take attention mask into account for correct averaging
def mean_pooling(model_output, attention_mask):
    token_embeddings = model_output[0]  # First element of model_output contains all token embeddings
    input_mask_expanded = attention_mask.unsqueeze(-1).expand(token_embeddings.size()).float()
    return torch.sum(token_embeddings * input_mask_expanded, 1) / torch.clamp(input_mask_expanded.sum(1), min=1e-9)


# Load model and tokenizer from HuggingFace Hub
tokenizer = AutoTokenizer.from_pretrained('sentence-transformers/all-MiniLM-L6-v2')
model = AutoModel.from_pretrained('sentence-transformers/all-MiniLM-L6-v2')

# Di chuyển model sang GPU (nếu có)
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model = model.to(device)


# Hàm để tính embedding cho một chuỗi
def get_embedding(text):
    # Tokenize sentences
    encoded_input = tokenizer(text, padding=True, truncation=True, return_tensors='pt')

    # Di chuyển encoded_input sang GPU (nếu có)
    encoded_input = {key: value.to(device) for key, value in encoded_input.items()}

    # Compute token embeddings
    with torch.no_grad():
        model_output = model(**encoded_input)

    # Perform pooling
    sentence_embedding = mean_pooling(model_output, encoded_input['attention_mask'])

    # Normalize embedding
    sentence_embedding = F.normalize(sentence_embedding, p=2, dim=1)

    return sentence_embedding.cpu().numpy()  # Di chuyển về CPU để lưu vào DataFrame