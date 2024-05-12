import torch 
import torch.nn as nn 
from transformers import BertModel 
import os 

os.environ["CURL_CA_BUNDLE"]=""

class TransAutoEncoder(nn.Module):
    def __init__(self, transformer_model_name):
        super(TransAutoEncoder, self).__init__()
        self.encoder = BertModel.from_pretrained(transformer_model_name)
        self.decoder = nn.Linear(self.encoder.config.hidden_size, self.encoder.config.vocab_size)
    
    def forward(self, input_ids, attention_mask=None):
        encoded = self.encoder(input_ids, attention_mask)
        encoded_rep = encoded.last_hidden_state[:, 0, :]

        decoded = self.decoder(encoded_rep)
        return decoded

if __name__ == "__main__":
    model = TransAutoEncoder('bert-base-uncased')
    criterion = nn.MSELoss()
    optimiser = torch.optim.Adam(model.parameters(), lr=0.01)

    with open("dataGen/bnf/Dataset.txt") as file:
        data = file.readlines()
        data = list(map(lambda x : x.strip(), data))
        data = data[:100]
    
    for cmd in data:
        optimiser.zero_grad()
        pred = model(cmd)
        loss = criterion(cmd, pred) 
        loss.backward()
        optimiser.step()
    

    


