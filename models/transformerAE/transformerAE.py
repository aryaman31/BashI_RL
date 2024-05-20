import torch 
import torch.nn as nn 
from torch.autograd import Variable
from transformers import AutoModel, AutoTokenizer
from tqdm import tqdm
import random
from sklearn.model_selection import train_test_split

# import os 

# os.environ["CURL_CA_BUNDLE"]=""

class TransAutoEncoder(nn.Module):
    def __init__(self, transformer_model_name):
        super(TransAutoEncoder, self).__init__()
        self.tokenizer = AutoTokenizer.from_pretrained(transformer_model_name)
        self.encoder = AutoModel.from_pretrained(transformer_model_name)
        self.decoder = nn.Linear(self.encoder.config.hidden_size, self.encoder.config.vocab_size)
    
    def forward(self, tokenize_input, attention_mask=None):
        encoded = self.encoder(tokenize_input, attention_mask)
        encoded_rep = encoded.last_hidden_state

        decoded = self.decoder(encoded_rep)
        _, predicted_ids = torch.max(decoded, dim=-1)
        return predicted_ids

    def decode(self, tensor_probs):
        pred_tokens = [self.tokenizer.convert_ids_to_tokens(token_id.item()) for token_id in tensor_probs[0]]
        return self.tokenizer.convert_tokens_to_string(pred_tokens)
    
    def tokenize(self, str):
        input_ids = self.tokenizer.encode(str, add_special_tokens=True)
        return torch.tensor(input_ids).unsqueeze(0)

if __name__ == "__main__":
    model = TransAutoEncoder('microsoft/codebert-base')
    criterion = nn.MSELoss()
    optimiser = torch.optim.Adam(model.parameters(), lr=0.01)

    with open("dataGen/bnf/Dataset.txt", "r") as file:
        data = file.readlines()
        data = list(map(lambda x : x.strip(), data))
        # data = data[:100000]
    
    train_data, test_data = train_test_split(data, test_size=0.01, train_size=0.99)

    file = open("testOutput.txt", "w")

    no_epochs = 1
    for i in range(no_epochs):
        total_loss = 0
        for cmd in tqdm(train_data):
            tokenized_cmd = model.tokenize(cmd)
            pred = model(tokenized_cmd)
            optimiser.zero_grad()
            loss = criterion(tokenized_cmd.to(torch.float32), pred.to(torch.float32))
            loss = Variable(loss, requires_grad=True)
            total_loss += loss.item()
            loss.backward()
            optimiser.step()
            
        file.write(f'Epoch [{i+1} / {no_epochs}], Loss: {total_loss}\n')
        torch.save(model, "models/model_weights/TransAutoEncoder.model")
    
    # Test
    for cmd in (test_data):
        pred_t = model(model.tokenize(cmd))
        pred = model.decode(pred_t)
        file.write("Input    :" + cmd + "\n")
        file.write("Predicted:" + pred + "\n")
    
    file.close()


    


