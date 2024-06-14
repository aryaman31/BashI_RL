from torch.utils.data import DataLoader
import torch.nn as nn
import torch.optim as optim
import torch
from tqdm import tqdm
import shlex
from sklearn.model_selection import train_test_split

from models.gruAE.encoder import Encoder
from models.gruAE.decoder import Decoder

# max length of bash command in chars
max_length = 200
device = torch.device("cuda") if torch.cuda.is_available() else torch.device("cpu")

def train(input_tensor, encoder, decoder, encoder_optimizer, decoder_optimizer, criterion,device, backprop=True):
    encoder_hidden = encoder.initHidden()

    if backprop:
        encoder_optimizer.zero_grad()
        decoder_optimizer.zero_grad()

    input_length = input_tensor.size(0)

    encoder_outputs = torch.zeros(max_length, encoder.hidden_size, device=device)

    loss = 0

    for ei in range(input_length):
        encoder_output, encoder_hidden = encoder(input_tensor[ei], encoder_hidden)
        encoder_outputs[ei] = encoder_output[0, 0]

    decoder_input = torch.tensor([[cmd_to_idx["SOL"]]], device=device)

    decoder_hidden = encoder_hidden

    # use_teacher_forcing = True if random.random() < teacher_forcing_ratio else False
    pred_output = []

    for di in range(input_length):
        decoder_output, decoder_hidden, decoder_attention = decoder(
            decoder_input, decoder_hidden, encoder_outputs)
        topv, topi = decoder_output.topk(1)
        decoder_input = topi.squeeze().detach()  # detach from history as input

        loss += criterion(decoder_output, input_tensor[di].to(torch.float32))
        pred_output.append(topi.cpu().detach().numpy()[0][0])
        if decoder_input.item() == cmd_to_idx["EOL"]:
            break
    
    if not backprop:
        print("".join([idx_to_cmd[current] for current in pred_output]))
        print("".join([idx_to_cmd[current] for current in input_tensor.cpu().detach().numpy().flatten()]))
        print()

    if backprop:
        loss.backward()

        encoder_optimizer.step()
        decoder_optimizer.step()

    return loss.item()

def cmd_to_tensor(cmd):
    # cmd = "SOL " + cmd + " EOL"
    # tokens = cmd.split()
    tokens = list(cmd)
    # tokens.insert(0, "SOL")
    # tokens.append("EOL")
    # tokens = list(cmd)
    tensor = torch.tensor([torch.tensor(cmd_to_idx[t]) for t in tokens], device=device)
    return tensor

with open("dataGen/combined_rand_logs.txt") as file:
    data = file.readlines()
    data = list(map(lambda x : x.strip(), data))
    data = data[:100]

    # token_set = set(" ".join(data).split())
    token_set = set(list("".join(data)))
    token_set.add("SOL")
    token_set.add("EOL")
    cmd_to_idx = {token:i for i, token in enumerate(token_set)}
    idx_to_cmd = {i:token for token, i in cmd_to_idx.items()}



data_tensor = [cmd_to_tensor(s) for s in data]
# data_tensor = nn.utils.rnn.pad_sequence(data_tensor, batch_first=True, padding_value=0)
train_data, test_data = train_test_split(data_tensor, test_size=0.2, train_size=0.8)

trainLoader = DataLoader(data_tensor, batch_size=32, shuffle=True)

input_size = len(token_set)
hidden_size = 800
encoder = Encoder(input_size, hidden_size, max_length)
decoder = Decoder(hidden_size, input_size, max_length)

criterion = nn.MSELoss()
encoder_optimiser = optim.Adam(list(encoder.parameters()), lr=0.01)
decoder_optimiser = optim.Adam(list(decoder.parameters()), lr=0.01)

# Training Loop
num_epochs = 1
for epoch in range(num_epochs):
    running_loss = 0.0
    for cmd in tqdm(train_data):
        loss = train(cmd, encoder, decoder, encoder_optimiser, decoder_optimiser, criterion, device)
        running_loss += loss 

    print(f'Epoch [{epoch + 1}/{num_epochs}], Loss: {running_loss:.4f}')

# Testing Loop
totalMSE = 0
for cmd in test_data:
    totalMSE += train(cmd, encoder, decoder, None, None, criterion, device, backprop=False)
print(f'TotalMSE: {totalMSE:.4f}')

torch.save(encoder, "models/model_weights/encoder.model")
torch.save(decoder, "models/model_weights/decoder.model")

print("DONE")

