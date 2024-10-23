from sentence_transformers import SentenceTransformer, util
import torch
import os

# Initialize the embedding model
embedding_model = SentenceTransformer('all-MiniLM-L6-v2')

MALICIOUS_FILE = "malicious.txt"

# Load bad prompts from the file
if not os.path.exists(MALICIOUS_FILE):
    # Create the file if it doesn't exist
    with open(MALICIOUS_FILE, 'w') as file:
        pass

with open(MALICIOUS_FILE, "r") as file:
    bad_prompts = [line.strip() for line in file.readlines()]

# Compute embeddings for bad prompts
if bad_prompts:
    bad_prompt_embeddings = embedding_model.encode(bad_prompts, convert_to_tensor=True)
else:
    bad_prompt_embeddings = None

def check_user_input(user_input):
    # Compute the embedding of the user input
    user_input_embedding = embedding_model.encode(user_input, convert_to_tensor=True)

    if bad_prompt_embeddings is not None and len(bad_prompt_embeddings) > 0:
        # Compute cosine similarity with bad prompts
        similarities = util.cos_sim(user_input_embedding, bad_prompt_embeddings)
        print(similarities)
        max_similarity = torch.max(similarities).item()

        # If similarity exceeds threshold, reject the input
        if max_similarity >= 0.7:
            return None

    return user_input

def check_response_input(user_input, response):
    secret_flag = "CAPSTONE"

    if secret_flag in response:
        # If the response contains the secret flag, add the user's input to the malicious prompts
        with open(MALICIOUS_FILE, "a") as file:
            file.write(f"{user_input}\n")
        return True

    return False
